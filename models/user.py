from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import re
from playhouse.hybrid import hybrid_property

class User(UserMixin, BaseModel):
    name = pw.CharField(unique=True , null=False)
    username = pw.CharField(null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    image = pw.CharField(null=True)
    status = pw.CharField(null=True)

    
    def validate(self):
        duplicate_username_user = User.get_or_none(User.username == self.username)
        duplicate_email_user = User.get_or_none(User.email == self.email)
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
        if duplicate_username_user and not (duplicate_username_user.id == self.id):
            self.errors.append("Username already exists!")
        if duplicate_email_user and not (duplicate_email_user.id == self.id):
            self.errors.append("Email already exists!")
        else:
            self.password = generate_password_hash(self.password)

    @hybrid_property
    def followers(self):
        from models.user_follower import User_follower
        return [u for u in User.select().join(User_follower, on=(User_follower.follower_id == User.id)).where(self.id == User_follower.user_id)]

    @hybrid_property
    def following(self):
        from models.user_follower import User_follower
        return [u for u in User.select().join(User_follower, on=(User_follower.user_id == User.id)).where(self.id == User_follower.follower_id)]