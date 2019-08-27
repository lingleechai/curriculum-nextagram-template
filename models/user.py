from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import re

class User(UserMixin, BaseModel):
    name = pw.CharField(unique=True , null=False)
    username = pw.CharField(null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)

    
    def validate(self):
        pw_pattern = "^(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z]).{8,}$"
        check_pw = re.match(pw_pattern, self.password)

        if not len(self.name):
            self.errors.append("Name cannot be empty!")
        if not len(self.username):
            self.errors.append("Username cannot be empty!")
        if not len(self.email):
            self.errors.append("Email cannot be empty!")
        if not len(self.password):
            self.errors.append("Password cannot be empty!")
        if not check_pw:
            self.errors.append("Password does not match requirements!")
        else:
            self.password = generate_password_hash(self.password)