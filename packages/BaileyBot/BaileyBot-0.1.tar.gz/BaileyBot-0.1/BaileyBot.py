'''

This bot allows you to input your email/password. then it sends email

'''

import yagmail

class EmailObj:
    def __init__(self, email, password ):
        self.email = email
        self.password = password

    def setEmail(self, newEmail):
        self.email = newEmail

    def setPassword(self, newPassword):
        self.password = newPassword

    def viewCreds(self):
        print(f'[SECRET]\nEmail:    {self.email}\nPassword: {self.password}')

    def sendEmail(self, reciever, subject, body):
        yag = yagmail.SMTP(self.email, self.password)
        yag.send(
            to=reciever,
            subject=subject,
            contents=body
        )

def signIn(email,password):
    return EmailObj(email,password)

#USE SETUPTOOLS TO MAKE THIS PROJECT INTO A PACKAGE!!!! WOOOO
