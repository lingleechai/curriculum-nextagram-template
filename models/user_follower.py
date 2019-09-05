from models.base_model import BaseModel
from models.user import User
import peewee as pw
from werkzeug.security import generate_password_hash
import re


class User_follower(BaseModel):
    user = pw.ForeignKeyField(User)
    follower = pw.ForeignKeyField(User)
    is_approved = pw.BooleanField()