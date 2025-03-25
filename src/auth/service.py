
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import HTTPException
from pydantic import EmailStr
from auth.schemas import UserCreate, UserLogin
from auth.schemas import UserPassSchema
from database.models import User, UserPasses
from utils.pass_worker import convert_pass_to_hash, generate_random_pass, verify_passwords
from utils.repository import AbstractRepository




class BaseService:
    def __init__(self, repo: AbstractRepository):
        self.repo: type[AbstractRepository] = repo



class UserService(BaseService):

    async def get_all(self):
        users = await self.repo.get_all()
        return users

    async def add_one(self, user: UserCreate) -> User:
        user_dict = user.model_dump()
        new_user = await self.repo.add_one(user_dict)
        return new_user
    
    async def get_by_id(self, id: int):
        user = await self.repo.get_by_id(id)
        return user
    
    async def get_current_user(self, payload: dict):
        user_id = int(payload.get("sub"))
        return await self.get_by_id(user_id)
    
    async def get_id_by_email(self, email: str):
        return await self.repo.get_id_by_email(email)
    

    def verify_user(self, crdnt: UserLogin, hash_pass: str):
        #user_id = await self.get_id_by_email(crdnt.email)

        if verify_passwords(crdnt.password, hash_pass):
            return True
        else:
            return False
    

class UserPassService(BaseService):  

    async def add_pass(self, user_id: int) -> str:

        passes = self.generate_pass_for_user()
        hash_pass = passes.get("hash_pass")
        rand_pass = passes.get("rand_pass")

        user_pass_data = UserPassSchema(user_id=user_id, hash_pass=hash_pass, date_pass=datetime.now())
        user_pass_dict = user_pass_data.model_dump()

        await self.repo.add_one(user_pass_dict)
        return rand_pass

    def generate_pass_for_user(self):
        rand_pass = generate_random_pass()
        hash_pass = convert_pass_to_hash(rand_pass)
        return {"hash_pass" : hash_pass, "rand_pass" : rand_pass}
    
    async def get_hash_by_id(self, user_id: int):
        return await self.repo.get_hash_by_id(user_id)


     
class SendMailService():

    def send_ya_mail_password(self, recipients_email: EmailStr, gen_pass: str):
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
    

