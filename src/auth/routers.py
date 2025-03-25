from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi import Depends

import jwt
from auth.dependencies import passes_service, send_mail_service, user_service

from auth.schemas import ResponceCreate, UserCreate, UserLogin, UserRead
from auth.service import SendMailService, UserPassService, UserService


from authx import AuthX, AuthXConfig

user_router = APIRouter(tags=["Users"])


conf_auth = AuthXConfig()
conf_auth.JWT_SECRET_KEY = "ami_SECRET_KEY"
conf_auth.JWT_ACCESS_COOKIE_NAME = "ami_access_token"
conf_auth.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=conf_auth)


@user_router.get("", response_model=list[UserRead])
async def get_all_users(
    user_service: Annotated[UserService, Depends(user_service)],
):
    users = await user_service.get_all()
    if users == [] or not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@user_router.post("/registration", response_model=ResponceCreate)
async def add_one_user(
    user_data: UserCreate,
    user_service: Annotated[UserService, Depends(user_service)],
    user_pass_service: Annotated[UserPassService, Depends(passes_service)],
    send_mail_service: Annotated[SendMailService, Depends(send_mail_service)],
):
    try: 
        new_user = await user_service.add_one(user_data)
        print(f"Добавлен новый пользователь с ID: {new_user.id}")
        
        new_pass = await user_pass_service.add_pass(new_user.id)
        print(f"Добавлен пароль для пользователя с id: {new_user.id}")

        send_mail_service.send_ya_mail_password(user_data.email, new_pass)
        print(f"Отправлено письмо для пользователя с id: {new_user.id}")

        return ResponceCreate(user_id=new_user.id)
    
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")
        raise HTTPException(status_code=400, detail=f"User already exists")



@user_router.post("/login")
async def log_user(credentials: UserLogin, response: Response,
                   user_service: Annotated[UserService, Depends(user_service)],
                   user_pass_service: Annotated[UserPassService, Depends(passes_service)],
                   ):
    user_id = await user_service.get_id_by_email(credentials.email)
    if not user_id:
            raise HTTPException(status_code=401, detail="Incorrect login or password")
    
    user_hash = await user_pass_service.get_hash_by_id(user_id)
    if not user_hash:
            raise HTTPException(status_code=401, detail="Incorrect login or password")
    
    # verif_user_id = await user_service.verify_user(credentials, user_hash)

    if user_service.verify_user(crdnt=credentials, hash_pass=user_hash) == False:
        print(f"hash: {user_hash}; pass: {credentials.password}")
        raise HTTPException(status_code=401, detail="Incorrect login or password 3")
    
    token = security.create_access_token(uid=f'{user_id}')
    response.set_cookie(conf_auth.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token}
    


# dependencies=[Depends(security.access_token_required)]  - делает обязательным наличие токена в куках, но выкидывает 500 except
@user_router.get("/protected")
async def protected(request: Request, user_service: Annotated[UserService, Depends(user_service)]):
    token = request.cookies.get(conf_auth.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=403, detail="Not permission access")
    
    payload = jwt.decode(token, conf_auth.JWT_SECRET_KEY, algorithms=[conf_auth.JWT_ALGORITHM])
    current_user = await user_service.get_current_user(payload)

    if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
    
    return UserRead(**current_user.dict())