from datetime import datetime
from incollege import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

friends = db.Table('friends', 
db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    friend = db.relationship('User',
            secondary = friends, 
            primaryjoin = (friends.c.user_id == id), 
            secondaryjoin = (friends.c.friend_id == id), 
            lazy = 'dynamic')

    def befriend(self,user):
        if user not in self.friend:
            self.friend.append(user)
            user.friend.append(self)
    
    def unfriend(self, user):
        if user in self.friend:
            self.friend.remove(user)
            user.friend.remove(self)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.fname}', '{self.lname}', {self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

