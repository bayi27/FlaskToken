import os
from flask import current_app,Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)

app.debug=True
app.config['SECRET_KEY']='This is diffcult'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')

db=SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True,index=True)

    def genter_auth_token(self,expiration=300):
        s=Serializer(current_app.config['SECRET_KEY'],salt='activate-salt',expires_in=expiration)
        return s.dumps({'code':self.name})

    @staticmethod
    def verify_auth_token(token):
        s=Serializer(current_app.config['SECRET_KEY'],salt='activate-salt')
        try:
            data=s.loads(token)
        except BadSignature:
            return None
        except SignatureExpired:
            return None
        return data

@app.route('/')
def index():
    user = User.query.filter_by(id=1).first()
    token=user.genter_auth_token()
    return jsonify({ 'token': token.decode('ascii')})

@app.route('/verify')
def verify():
    token=request.args.get("token")
    user = User.query.filter_by(id=1).first()
    verify = user.verify_auth_token(token)
    return jsonify({'result':verify})

if __name__=='__main__':
    db.create_all()
    app.run()