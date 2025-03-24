from datetime import datetime, timezone
import os
from fastapi import HTTPException
from sqlalchemy import select

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database import User, UserPasses
from utils.pass_worker import generate_random_pass, convert_pass_to_hash, verify_passwords




async def get_all(session: AsyncSession):
        query = select(User).order_by(User.id)
        result = await session.execute(query)
        records = result.scalars().all()
        return records


async def add_one(session: AsyncSession, **values):
    new_instance = User(**values)
    session.add(new_instance)

    try:
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise e

    rand_pass = generate_random_pass()
    hash_pass = convert_pass_to_hash(rand_pass)
    new_record_pass = UserPasses(user_id=new_instance.id, hash_pass=hash_pass, date_pass=datetime.now())
    session.add(new_record_pass)

    try:
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise e
    
    send_ya_mail_password(new_instance.email, rand_pass)

    return new_instance


def send_ya_mail_password(recipients_email: EmailStr, gen_pass: str):
    login = 'amisolutions@yandex.ru'
    password = 'qoctwbqbrskcczte' # os.getenv('MAIL_PASSWORD')

    msg = MIMEMultipart()
    # msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = Header('Авторизация АППО', 'utf-8')
    msg['From'] = login 
    msg['To'] = ''.join(recipients_email)

    text = f"Данное письмо высылается автоматически при регистрации, на него не нужно отвечать. \nПри регистрации в АППО для вас был сгенерирован пароль для входа через ваш email. Никому его не показывайте! \nВаш пароль: {gen_pass} \nСмените его на свой сразу после входа в своем профиле"
    msg.attach(MIMEText(text, 'plain'))
    
    smtp_server = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)

    try:
        smtp_server.starttls()
        smtp_server.login(login, password)
        smtp_server.sendmail(msg['From'], recipients_email, msg.as_string())
        print("Message sent successfully!")
    except Exception as ex:
        print("Sending message error: ", ex)
    finally:
        smtp_server.quit()



async def get_id_by_email(email: str, password: str, session: AsyncSession):
    query_user = select(User.id).filter_by(email=email)
    result_user = await session.execute(query_user)
    user_id = result_user.scalars().first()
    query_pass = select(UserPasses.hash_pass).filter_by(user_id=user_id).order_by(UserPasses.date_pass.desc()).limit(1)
    result_pass = await session.execute(query_pass)
    hashed_pass = result_pass.scalars().first()

    if verify_passwords(password, hashed_pass):
        return user_id
    else:
         raise HTTPException(status_code=403, detail="Incorrect login or password")


async def get_current_user(payload: dict, session: AsyncSession):
    user_id = int(payload.get("sub"))
    return await get_user_by_id(user_id, session=session)



async def get_user_by_id(id: int, session: AsyncSession):
        query = select(User).filter_by(id=id)
        result = await session.execute(query)
        # records = result.scalar_one_or_none()
        records = result.scalars().first()
        
        return records
