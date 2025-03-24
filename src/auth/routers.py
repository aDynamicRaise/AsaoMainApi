from fastapi import APIRouter, HTTPException, Request, Response
from fastapi import Depends

import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_helper import db_helper

from auth.schemas import UserCreate, UserLogin, UserRead
from auth.service import add_one, get_all, get_current_user, get_id_by_email


from authx import AuthX, AuthXConfig

router = APIRouter(tags=["Users"])


conf_auth = AuthXConfig()
conf_auth.JWT_SECRET_KEY = "ami_SECRET_KEY"
conf_auth.JWT_ACCESS_COOKIE_NAME = "ami_access_token"
conf_auth.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=conf_auth)


@router.get("", response_model=list[UserRead])
async def get_all_users(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_all(session=session)



@router.post("/registration", response_model=UserCreate)
async def add_one_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    new_user = await add_one(session=session, **user_data.dict())
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user




@router.post("/login")
async def log_user(
    credentials: UserLogin,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_getter), 
):
    user_id = await get_id_by_email(email=credentials.email, password=credentials.password, session=session)
    if not user_id:
        raise HTTPException(status_code=401, detail="Incorrect login or password")
    
    token = security.create_access_token(uid=f'{user_id}')
    response.set_cookie(conf_auth.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token}

# @router.post("/login")
# async def log_user(credentials: UserLogin, response: Response):
#     if credentials.login == "test" and credentials.password == "test":
#         token = security.create_access_token(uid="2")
#         response.set_cookie(conf_auth.JWT_ACCESS_COOKIE_NAME, token)
#         return {"access_token": token}
#     raise HTTPException(status_code=401, detail="Incorrect login or password")



# dependencies=[Depends(security.access_token_required)]  - делает обязательным наличие токена в куках, но выкидывает 500 except
@router.get("/protected")
async def protected(request: Request, session: AsyncSession = Depends(db_helper.session_getter)):
    token = request.cookies.get(conf_auth.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=403, detail="Not permission access")
    
    payload = jwt.decode(token, conf_auth.JWT_SECRET_KEY, algorithms=[conf_auth.JWT_ALGORITHM])

    cur_user = await get_current_user(payload, session=session)
    return {"current_user": cur_user}