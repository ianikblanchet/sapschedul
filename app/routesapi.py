from flask import Flask
from app import app
from app import db
from datetime import datetime
import json
from flask_login import current_user, login_user, logout_user, login_required
import pandas as pd
from flask import request
from app.models import User, Workorder, Workcenter, Capac, Sched, Stat
from flask_restful import Api, Resource, fields, marshal_with
from app import api


class MyDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%m/%d/%Y')

resource_stat = {'id': fields.Integer,
                    'Order_Num': fields.String,
                    'Description': fields.String,
                    'Func_Loc': fields.String,
                    'Prio': fields.String,
                    'Statututil': fields.String,
                    'Statutsys': fields.String,
                    'Crea_Date' : MyDateFormat,
                    'Basic_Start' : MyDateFormat,
                    'Pdt': fields.String,                    
                    'Annee': fields.String,
                    'Mois' : fields.String,
                    'Age' : fields.String
}

class Rstat(Resource):
    @marshal_with(resource_stat)    
    def get(self):
        
        result = Stat.query.all()
        #result = Stat.query.filter(Stat.Pdt.contains('MFAC')).all()
        return result
        

api.add_resource(Rstat, '/rstat')

