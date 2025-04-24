from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi import Depends

import jwt
from auth.dependencies import passes_service, send_mail_service, user_service

from auth.schemas import ResponceCreate, UserCreate, UserLogin, UserRead
from auth.service import SendMailService, UserPassService, UserService


from authx import AuthX, AuthXConfig
from utils.temp_access import generate_verification_code, verify_code
from utils.pass_worker import convert_pass_to_hash
from config import settings

user_router = APIRouter(tags=["Users"])


conf_auth = AuthXConfig()
conf_auth.JWT_SECRET_KEY = settings.secrets.JWT_SECRET_KEY
conf_auth.JWT_ACCESS_COOKIE_NAME = "ami_access_token"
conf_auth.JWT_TOKEN_LOCATION = ["cookies"]
conf_auth.JWT_COOKIE_MAX_AGE = 3600

security = AuthX(config=conf_auth)

# Секретный ключ для временного токена
TEMP_JWT_SECRET_KEY = settings.secrets.TEMP_JWT_SECRET_KEY
TEMP_JWT_COOKIE_NAME = "temp_access_token"


@user_router.get("", response_model=list[UserRead])
async def get_all_users(
    user_service: Annotated[UserService, Depends(user_service)],
):
    users = await user_service.get_all()
    # if users == [] or not users:
    #     raise HTTPException(status_code=404, detail="Users not found")
    return users


@user_router.post("/registration", response_model=ResponceCreate)
async def add_one_user(
    user_service: Annotated[UserService, Depends(user_service)],
    user_pass_service: Annotated[UserPassService, Depends(passes_service)],
    send_mail_service: Annotated[SendMailService, Depends(send_mail_service)],
    user_data: UserCreate = Depends()
):
    try: 
        new_user = await user_service.add_one(user_data)
        print(f"Добавлен новый пользователь с ID: {new_user.id}")
        
        #new_pass = await user_pass_service.add_pass(new_user.id)
        new_pass = user_pass_service.generate_pass_for_user()

        response_pass = await user_pass_service.add_pass(new_user.id, new_pass.get("hash_pass"))
        print(f"Добавлен пароль для пользователя с id: {new_user.id} от {response_pass}")

        text = f"Данное письмо высылается автоматически при регистрации, на него не нужно отвечать. \nПри регистрации в АППО для вас был сгенерирован \
                пароль для входа через ваш email. Никому его не показывайте! \nВаш пароль: {new_pass.get('rand_pass')} \nСмените его на свой сразу после входа в своем профиле"
        
        send_mail_service.send_ya_mail_password(user_data.email, text)
        print(f"Отправлено письмо для пользователя с id: {new_user.id}")

        return ResponceCreate(user_id=new_user.id)
    
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")
        raise HTTPException(status_code=400, detail=f"User already exists")



@user_router.post("/login")
async def log_user(response: Response,
                   user_service: Annotated[UserService, Depends(user_service)],
                   user_pass_service: Annotated[UserPassService, Depends(passes_service)],
                   credentials: UserLogin = Depends()
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
        raise HTTPException(status_code=401, detail="Incorrect login or password")
    
    token = security.create_access_token(uid=f'{user_id}')
    response.set_cookie(conf_auth.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token}




def generate_temp_token(user_id: int):
    """Генерация временного токена для смены пароля."""
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(minutes=5)  # Время действия токена
    }
    token = jwt.encode(payload, TEMP_JWT_SECRET_KEY, algorithm=conf_auth.JWT_ALGORITHM)
    return token



@user_router.get("/edit_pass/send_verif_code")
async def send_verif_code(request: Request, user_service: Annotated[UserService, Depends(user_service)], send_mail_service: Annotated[SendMailService, Depends(send_mail_service)],):
    payload = get_current_token_payload(request)
    user_id = int(payload.get("sub", "0"))
    if user_id == 0:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        user = await user_service.get_by_id(user_id)
        temp_code = generate_verification_code(user_id)
        
        text = f"Данное письмо высылается автоматически, на него не нужно отвечать. \nДля подтверждения личности при изменении пароля в АППО для вас был сгенерирован \
            временный код верификации. Используйте его для подтверждения личности и никому не показывайте! \nВаш код: {temp_code} \nВнимание! Код действителен всего 5 минут."

        send_mail_service.send_ya_mail_password(user.email, text)
        print(f"Отправлено письмо для пользователя с id: {user.id}")
        return {"message" : "Письмо отправлено", "status" : 200}
    except Exception as e:
        print(f"Ошибка отправки кода верификации: {e}")
        raise e
        


@user_router.post("/edit_pass/confirm/{code_access}")
async def confirmation(request: Request, input_code: str, response: Response):
    """Функция создания временного токена для смены пароля."""
    # Пользователь вводит код, при совпадении отдается токен
    payload = get_current_token_payload(request)
    user_id = int(payload.get("sub", "0"))

    if user_id == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_code(user_id, input_code):
        raise HTTPException(status_code=401, detail="Incorrect code")
        
    temp_token = generate_temp_token(user_id)
    print("Токен для смены пароля создан")
    response.set_cookie(TEMP_JWT_COOKIE_NAME, temp_token, httponly=True)

    return {"temp_access_token": temp_token}


@user_router.post("/edit_pass/{new_pass}")
async def edit_pass(request: Request, new_pass: str, response: Response, user_pass_service: Annotated[UserPassService, Depends(passes_service)],):
    """Функция обновления пароля с использованием временного токена."""
    # При наличии токена дается возможность поменять пароль

    temp_token = request.cookies.get(TEMP_JWT_COOKIE_NAME)

    if not temp_token:
        raise HTTPException(status_code=403, detail="Not permission temp_access")

    try:
        payload = jwt.decode(temp_token, TEMP_JWT_SECRET_KEY, algorithms=[conf_auth.JWT_ALGORITHM])
        user_id = payload['user_id']
        # Здесь вы можете обновить пароль пользователя
        hash_pass = convert_pass_to_hash(new_pass)
        response_pass = await user_pass_service.add_pass(user_id, hash_pass)
        print(f"Добавлен новый пароль для пользователя {user_id}")
        response.delete_cookie(TEMP_JWT_COOKIE_NAME)
        
        return {"message" : f"Пароль успешно обновлен. Дата обновления: {response_pass}", "status" : 200}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Срок действия временного токена истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Недействительный временный токен")

    

# dependencies=[Depends(security.access_token_required)]  - делает обязательным наличие токена в куках, но выкидывает 500 except
@user_router.get("/protected")
async def protected(request: Request, user_service: Annotated[UserService, Depends(user_service)]):

    payload = get_current_token_payload(request)
    user_id = int(payload.get("sub", "0"))
    if user_id == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user = await user_service.get_by_id(user_id)
    return UserRead(**current_user.dict())



def get_current_token_payload(request: Request):
    try:
        token = request.cookies.get(conf_auth.JWT_ACCESS_COOKIE_NAME)
        if not token:
            raise HTTPException(status_code=403, detail="Not permission access")

        payload = jwt.decode(token, conf_auth.JWT_SECRET_KEY, algorithms=[conf_auth.JWT_ALGORITHM])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Срок действия токена истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Недействительный токен")