from django.core.mail import EmailMessage


def validate_username(username):
    numupper =0
    for c in username:
        if c.isupper():
            numupper = numupper + 1

    numlower =0
    for c in username:
        if c.islower():
            numlower = numlower + 1

    if len(username)<6:
        reason = ('username must be greater than or equal to 6 characters')
        return '',reason
    
    if len(username)>16:
        reason = ('username must be less than or equal to 16 characters')
        return '',reason

    numdigit=0
    for c in username:
        if c.isdigit():
            numdigit = numdigit + 1

    if numdigit <= 0:
        reason= ('username must contain at least one number')
        return '',reason

    else:
        return username, ''

def validate_password(password,username='-'):
    numupper =0
    for c in password:
        if c.isupper():
            numupper = numupper + 1

    if numupper <= 0:
        pwreason=('password must contain at least one uppercase character')
        return '',pwreason

    numlower =0
    for c in password:
        if c.islower():
            numlower = numlower + 1

    if numlower <= 0:
        pwreason=('password must contain at least one lowercase character')
        return '', pwreason

    if len(password)<12:
        pwreason = ('password must be greater than or equal to 12 characters')
        return '',pwreason
    
    if len(password)>16:
        pwreason = ('password must be less than or equal to 16 characters')
        return '',pwreason

    numdigit=0
    for c in password:
        if c.isdigit():
            numdigit = numdigit + 1

    if numdigit <= 0:
        pwreason= ('password must contain at least one number')
        return '',pwreason

    
    if username in password:
        pwreason=('username cannot be used as part of your password')
        return '',pwreason

    else:
        return password, ''


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'],
                             body=data['email_body'], to=[data['to_email']])
        email.send()
