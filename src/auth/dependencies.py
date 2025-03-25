
from auth.repositories import UserPassRepository, UserRepository
from auth.service import SendMailService, UserPassService, UserService


def user_service():
    return UserService(UserRepository)

def send_mail_service():
    return SendMailService()

def passes_service():
    return UserPassService(UserPassRepository)