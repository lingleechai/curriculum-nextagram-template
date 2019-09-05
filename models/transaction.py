from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw
from werkzeug.security import generate_password_hash
import re


class Transaction(BaseModel):
    user = pw.ForeignKeyField(User, backref="user_transaction")
    image= pw.ForeignKeyField(Image, backref="image_transaction" )
    transcation_history = pw.CharField(null=True)
    amount = pw.DecimalField(null=True, decimal_places=2)