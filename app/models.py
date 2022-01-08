from datetime import datetime
from app import db
#login miguel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from flask_login import current_user, login_user, logout_user, login_required



def User_query():
    return User.query


    
#user miguel
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(32), index=True)
    surname = db.Column(db.String(32), index=True)
    numemploye = db.Column(db.String(15), index=True)
    type = db.Column(db.String(64), index=True)
    valide = db.Column(db.Boolean, default=False)


    password_hash = db.Column(db.String(128))
    
    def __repr__(self):
        return 'username={} {} {}'.format(self.numemploye, self.name, self.surname  )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class Workorder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Order_Desc = db.Column(db.String(100), index = True)
    Desc_Ordre = db.Column(db.String(100), index = True)
    Order_Num = db.Column(db.String(20), index = True)    
    Order_Op =  db.Column(db.String(10), index = True)
    Func_Loc = db.Column(db.String(30), index = True)
    Prio = db.Column(db.String(10), index = True)
    Order_Status = db.Column(db.String(30), index = True)
    Est_Hours = db.Column(db.Float, index = True)
    Actual_Hours = db.Column(db.Float, index = True)
    Crea_Date = db.Column(db.DateTime, index = True)
    Basic_Start = db.Column(db.DateTime, index =True)
    Workcenter_id = db.Column(db.Integer, db.ForeignKey('workcenter.id'))
    
    Sched = db.relationship('Sched', backref = 'workorder', lazy = 'dynamic')

    def __repr__(self):
        return '{} {}'.format(self.Order_Num, self.Order_Desc)


class Workcenter(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Ticker = db.Column(db.String(10), index = True)
    Wc_Descr = db.Column(db.String(100), index = True)
    Descr_PD = db.Column(db.String(100), index = True)
    Capac = db.Column(db.Float, index = True)    

    Workorder = db.relationship('Workorder', backref = 'workcenter', lazy = 'dynamic')
    Capac = db.relationship('Capac', backref = 'capac', lazy = 'dynamic')


class Capac(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Daily = db.Column(db.DateTime, index = True)
    Leave = db.Column(db.Float, index = True)
    Workcenter_id = db.Column(db.Integer, db.ForeignKey('workcenter.id'))

class Sched(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Daily = db.Column(db.DateTime, index = True)
    Plan_hours = db.Column(db.Float, index = True)
    Comment = db.Column(db.String(40), index = True)
    equip_id = db.Column(db.Integer, db.ForeignKey('equip.id'))
    Workorder_id = db.Column(db.Integer, db.ForeignKey('workorder.id'))


class Equip(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Num_equi = db.Column(db.String(15), index = True)
    Wc_Descr = db.Column(db.String(40), index = True)    
    
    Sched = db.relationship('Sched', backref = 'equip', lazy = 'dynamic')