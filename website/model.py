from ._init_ import db, app
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import URLSafeTimedSerializer 


class Using(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150),  nullable=False)
    email = db.Column(db.String(150), unique=True,  nullable=False)
    password_hash = db.Column(db.String(255),  nullable=False)
    name = db.Column(db.String(150), nullable=False)
    handphone = db.Column(db.String(150))
    bio = db.Column(db.String(150))
    profile_picture = db.Column(db.String(), nullable=True, default = 'static/default/default_user.png')
    #histories = db.relationship('History', backref='using', lazy=True)

    # @property
    # def password(self):
    #     return self.password

    # @password.setter
    # def password(self, plain_text_password):
    #     self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # def check_password_correction(self, attempted_password):
    #     return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def get_token(self):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps({'id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expired_time=300):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            id = serializer.loads(token, max_age=expired_time)
        except:
            return None
        return Using.query.get(id)
            

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('using.id'), nullable=False)
    name = db.Column(db.String(150),  nullable=False)
    subject = db.Column(db.String(150),  nullable=False)
    classes = db.Column(db.String(150),  nullable=False)
    room = db.Column(db.String(150),  nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now,  nullable=False)
    time = db.Column(db.Time(timezone=True), default=func.now, nullable=False)
    screenshots = db.relationship('Screenshot', backref='history', lazy=True)

    #user = db.relationship('Using', backref=db.backref('histories', lazy=True))

class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'), nullable=False)
    path = db.Column(db.String(255), nullable=True)

