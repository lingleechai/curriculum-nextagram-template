from models.base_model import BaseModel
from models.user import User
import peewee as pw
from werkzeug.security import generate_password_hash
import re


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref="user_images")
    userImg = pw.CharField(null=True)
