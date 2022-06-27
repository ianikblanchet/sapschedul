from app import app, db
from app.models import User, Workorder, Workcenter, Capac, Sched, Stat



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Workorder' : Workorder, 'Workcenter' : Workcenter, 'Capac' : Capac, 'Sched' : Sched, 'Stat' : Stat }