from flask import Flask,render_template,flash, redirect, url_for
from app import app
from app import db
from app import api
import datetime
import json
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import pandas as pd
from flask import request
from app.models import User, Workorder, Workcenter, Capac, Sched, Stat, Cgvmsl
from app.forms import LoginForm,RegistrationForm
from flask_restful import Api, Resource, fields, marshal_with


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


#login Miguel
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('base')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, type = request.form['type'], name=request.form['name'], surname=request.form['surname'],numemploye=request.form['numemploye'] )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['POST'])
def uploader():
    #Importer le fichier excel et en faire un DF en ajoutant le combo ordre opération
   if request.method == 'POST':
      f = request.files['file']
      df = pd.read_excel(f)
      df['numcom']  = df['Order'].astype(str) + df['Activity'].astype(str)
      
    #je fais une query pour importer la base de données et je créer ma liste de combo ordre opération pour comp. futur
      listglobal = Workorder.query.all()    
      numordre = []
      for order in listglobal:
          numordre.append(str(order.Order_Num) + str(order.Order_Op))      

    
      for ind in df.index:
          #je valide si le Workcenter exist sinon je le créer
          if Workcenter.query.filter_by(Ticker= df['Oper.WorkCenter'][ind]).first() != None :              
              wc = Workcenter.query.filter_by(Ticker= df['Oper.WorkCenter'][ind]).first()
          else:
              db.session.add(Workcenter(Ticker = df['Oper.WorkCenter'][ind]))
              db.session.commit()
              wc = Workcenter.query.filter_by(Ticker= df['Oper.WorkCenter'][ind]).first()
          #je load l'objet base de donné et fonction de filtre provenant de l'élément du DF
          wo = Workorder.query.filter_by(Order_Num = df['Order'][ind].astype(str), Order_Op =df['Activity'][ind].astype(str)).first()
          #je valide si l'element exist dans la base de donnée si oui j'update certain champ, sinonje le créer
          if df['numcom'][ind] in numordre:
              
              wo.Order_Desc = df['Opr. short text'][ind]
              wo.Est_Hours = df['Work'][ind]
              wo.Prio = df['Priority'][ind]
              wo.Actual_Hours = df['Actual work'][ind]
              wo.Order_Status = df['System status'][ind] 
              wo.Workcenter_id = wc.id
              wo.Func_Loc = df['Functional loc.'][ind]
              db.session.commit()
              print('il est là')
          else:
              db.session.add(Workorder(Order_Desc=df['Opr. short text'][ind], Order_Num= df['Order'][ind].astype(str), Order_Op=df['Activity'][ind].astype(str), Func_Loc=df['Functional loc.'][ind], Prio=df['Priority'][ind], Order_Status=df['System status'][ind], Est_Hours=df['Work'][ind] , Actual_Hours=df['Actual work'][ind], Crea_Date=df['Created on'][ind],Basic_Start=df['Bas. start date'][ind], Workcenter_id= wc.id ))
              db.session.commit()
              print('pas là')

      
      return 'file uploaded successfully'

@app.route('/stat', methods = ['POST'])
def stat():
    #Importer le fichier excel et en faire un DF en ajoutant le combo ordre opération
   if request.method == 'POST':
      f = request.files['stat']
      df = pd.read_excel(f)      
      df['Mois']  = pd.DatetimeIndex(df['Created on']).month
      df['Annee'] = pd.DatetimeIndex(df['Created on']).year
      df['Age'] = (datetime.datetime.now() - df['Created on']).dt.days
      print(df)
      
    #je fais une query pour importer la base de données et je créer ma liste de combo ordre opération pour comp. futur
      liststat = Stat.query.all()    
      numordre = []
      for order in liststat:
          numordre.append(order.Order_Num)   
        
      print(numordre)
      for ind in df.index:
          
          #je load l'objet base de donné et fonction de filtre provenant de l'élément du DF
          wo = Stat.query.filter_by(Order_Num = df['Order'][ind].astype(str)).first()
          #je valide si l'element exist dans la base de donnée si oui j'update certain champ, sinonje le créer
          if df['Order'][ind].astype(str) in numordre:
              
              wo.Description = df['Description'][ind]              
              wo.Prio = df['Priority'][ind].astype(str)             
              wo.Statututil = df['User status'][ind]
              wo.Statutsys = df['System status'][ind]               
              wo.Func_Loc = df['Functional Loc.'][ind]
              wo.Basic_Start = df['Bas. start date'][ind]
              wo.Pdt = df['Main WorkCtr'][ind]
              wo.Mois = df['Mois'][ind].astype(str)
              wo.Annee = df['Annee'][ind].astype(str)
              wo.Age = df['Age'][ind].astype(str)
              db.session.commit()
              print('il est là')
          else:
              db.session.add(Stat(Description=df['Description'][ind], Order_Num= df['Order'][ind].astype(str),  Func_Loc=df['Functional Loc.'][ind], Prio=df['Priority'][ind].astype(str), Statututil=df['User status'][ind], Statutsys=df['System status'][ind],  Crea_Date=df['Created on'][ind],Basic_Start=df['Bas. start date'][ind], Pdt= df['Main WorkCtr'][ind], Annee= df['Annee'][ind].astype(str), Mois= df['Mois'][ind].astype(str), Age= df['Age'][ind].astype(str) ))
              db.session.commit()
              print('pas là')

      
      return 'Les ordres pour les stats sont mise à jour'

@app.route('/statordre', methods = ['POST'])
def statordre():
    #Importer le fichier excel et en faire un DF en ajoutant le combo ordre opération
   if request.method == 'POST':
      f = request.files['statordre']
      df = pd.read_excel(f)      
      df['Mois']  = pd.DatetimeIndex(df['Created on']).month
      df['Annee'] = pd.DatetimeIndex(df['Created on']).year
      df['Age'] = (datetime.datetime.now() - df['Created on']).dt.days
      print(df)
      
    #je fais une query pour importer la base de données et je créer ma liste de combo ordre opération pour comp. futur
      listordre = Cgvmsl.query.filter_by(Dataname = 'Ordre').first() 
      listordre.Livedata = df.to_json(orient = "records")
      listordre.Datemaj = datetime.datetime.now()
      db.session.commit()
      
      return 'Les ordres pour les stats sont mise à jour'

@app.route('/statavis', methods = ['POST'])
def statavis():
    #Importer le fichier excel et en faire un DF en ajoutant le combo ordre opération
   if request.method == 'POST':
      f = request.files['statavis']
      df = pd.read_excel(f)     
      
      print(df)
      
    #je fais une query pour importer la base de données et je créer ma liste de combo ordre opération pour comp. futur
      listavis = Cgvmsl.query.filter_by(Dataname = 'Avis').first() 
      listavis.Livedata = df.to_json(orient = "records")
      listavis.Datemaj = datetime.datetime.now()
      db.session.commit()
      
      return 'Les avis pour les stats sont mise à jour'

@app.route('/statpm', methods = ['POST'])
def statpm():
    #Importer le fichier excel et en faire un DF en ajoutant le combo ordre opération
   if request.method == 'POST':
      f = request.files['statpm']
      df = pd.read_excel(f)     
      
      print(df)
      
    #je fais une query pour importer la base de données et je créer ma liste de combo ordre opération pour comp. futur
      listpm = Cgvmsl.query.filter_by(Dataname = 'Pm').first() 
      listpm.Livedata = df.to_json(orient = "records")
      listpm.Datemaj = datetime.datetime.now()
      db.session.commit()
      
      return 'Les pm pour les stats sont mise à jour'


@app.route('/statpt', methods = ['POST'])
def statpt():
    #Importer le fichier excel et en faire un DF en ajoutant le combo ordre opération
   if request.method == 'POST':
      f = request.files['statpt']
      df = pd.read_excel(f)     
      
      print(df)
      
    #je fais une query pour importer la base de données et je créer ma liste de combo ordre opération pour comp. futur
      listpt = Cgvmsl.query.filter_by(Dataname = 'Zzxref').first() 
      listpt.Livedata = df.to_json()
      listpt.Datemaj = datetime.datetime.now()
      db.session.commit()
      
      return 'Les zzxref pour les stats sont mise à jour'


@app.route('/afermer', methods = [ 'POST'])
def afermer():
   if request.method == 'POST':
      f = request.files['file']
      df = pd.read_excel(f)
      df['numcom']  = df['Order'].astype(str) + df['Activity'].astype(str)
      #df = df.astype({'numcom': str})
      listglobal = Workorder.query.all()
     

      for order in listglobal:
          num = str(order.Order_Num) + str(order.Order_Op)
          print(num)
          if num in df.values :
              
              print('numéro trouver')          
          else:
              if order.Order_Status != 'CNF':                                   
                  order.Order_Status = 'CNF'
                  db.session.commit()
                  print('non trouvé')
              print('rien updaté')
      return 'validation terminé'


@app.route('/listglobal', methods = [ 'GET','POST'])
def listglobal():
        
    print(datetime.date(2022,1,3).isocalendar()[1])
    print(datetime.datetime.today().isocalendar()[1])
    listglobal = Workorder.query.all()
    date1 = Workorder.query.first()
    #date2 = datetime.datetime.strptime(str(date1.Crea_Date),'%Y-%m-%d')
    #date2 = datetime.datetime(date1.Crea_Date)
    date2= date1.Crea_Date
    date3 = datetime.datetime.date((Workorder.query.first()).Crea_Date).isocalendar()[1]
    print(date3)
    return render_template("listglobal.html",today = datetime.date.today(), listglobal=listglobal)

@app.route('/sched', methods = [ 'GET', 'POST'])
def sched():
    
    sem = (datetime.datetime.today().isocalendar()[1])
    listcheck = []
    

#la méthode pour modifier les heures planifiés
    if 'changheure' in request.form:
        sem = int(request.form['semaine1'])
        listcheck = request.form['listcheck3']
        d = request.form['jour']
        h = request.form['heure']
        n= request.form['numordre']
        no = request.form['numope']
        id = Workorder.query.filter(Workorder.Order_Num == n[0:7]).filter(Workorder.Order_Op == no).first()
        if Sched.query.filter(Sched.Workorder_id == id.id).filter(Sched.Daily == datetime.datetime.strptime(d, "%a %y/%m/%d")).first():
            toup = Sched.query.filter(Sched.Workorder_id == id.id).filter(Sched.Daily == datetime.datetime.strptime(d, "%a %y/%m/%d")).first()
            toup.Plan_hours = h
            db.session.commit()
        else:
            db.session.add(Sched(Workorder_id = id.id , Daily = datetime.datetime.strptime(d, "%a %y/%m/%d"), Plan_hours = h))
            db.session.commit()
        print(id)
        print('ok-ca marche ' + d +'-'+ h + '-' + n)


#méthode pour pousser d'une semaine
    if 'move' in request.form:    
        j= (request.form['jour']).split(",")
        n = (request.form['numordre']).split(",")
        listcheck = request.form['listcheck2']
        
        sem = datetime.datetime.strptime(j[1], "%a %y/%m/%d").isocalendar()[1]
        
        lundi = datetime.datetime.fromisocalendar(2022, sem + 1, 1)
        mardi = datetime.datetime.fromisocalendar(2022, sem + 1, 2)
        mercredi = datetime.datetime.fromisocalendar(2022, sem + 1, 3)
        jeudi = datetime.datetime.fromisocalendar(2022, sem + 1, 4)
        vendredi = datetime.datetime.fromisocalendar(2022, sem + 1, 5)
        semsuiv= [lundi, mardi, mercredi, jeudi, vendredi]
        print(lundi)
        print(n,j)
                    
        for num in n:
            id = Workorder.query.filter(Workorder.Order_Num == num[0:7]).filter(Workorder.Order_Op == num[7:9]).first()
            print(id.id)
            
            for jour in j:
                print(datetime.datetime.strptime(jour, "%a %y/%m/%d"))
                print(jour)  
                
                if Sched.query.filter(Sched.Workorder_id == id.id).filter(Sched.Daily == datetime.datetime.strptime(jour, "%a %y/%m/%d")).first():
                    todel = Sched.query.filter(Sched.Workorder_id == id.id).filter(Sched.Daily == datetime.datetime.strptime(jour, "%a %y/%m/%d")).first()
                    print('oui')
                    db.session.delete(todel)
                    db.session.commit()
            if Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == lundi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == mardi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == mercredi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == jeudi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == vendredi)).first():
                print('déja la')
            else:
                db.session.add(Sched(Workorder_id = id.id , Daily = semsuiv[1] , Plan_hours = 0))
                db.session.commit()





#pour changer de semaine on lance cette condition avant de générer la cédule de la semaine
    # if 'semaine' in request.form:
    #     sem = int(request.form['semaine'])
    #     listcheck = request.form['listcheck3']

#pour filtrer avec les checkbox
    if 'refresh' in request.form: 
        sem = int(request.form['semaine'])   
        listcheck = request.form['listcheck']
    #else:
        #listcheck = []
        

#le code pour générer la cédule
    lundi = datetime.date.fromisocalendar(2022, sem, 1)
    mardi = datetime.date.fromisocalendar(2022, sem, 2)
    mercredi = datetime.date.fromisocalendar(2022, sem, 3)
    jeudi = datetime.date.fromisocalendar(2022, sem, 4)
    vendredi = datetime.date.fromisocalendar(2022, sem, 5)
    samedi = datetime.date.fromisocalendar(2022, sem, 6)
    
    
    
    column_names = ["num", "op", "numcom" ,"desc", "pdt", "datecre", "dateplan", "estime","Priorité", lundi, mardi, mercredi, jeudi, vendredi]
    df = pd.DataFrame(columns = column_names)
    
    #print(df)
    schedule = Sched.query.filter(Sched.Daily >= lundi).filter(Sched.Daily < samedi).all()
    semcour = [lundi,mardi,mercredi, jeudi,vendredi]
    #capacite = db.session.query(Capac).filter(Capac.Daily in un).all()
    capacite = Capac.query.filter(Capac.Daily.in_(semcour) ).all()
    cpacjson = {}
    for capacpdt in capacite:
        if capacpdt.workcenter.Ticker in cpacjson.keys():
            cpacjson[capacpdt.workcenter.Ticker][str(capacpdt.Daily)] = capacpdt.cap
        else:
            cpacjson.update({capacpdt.workcenter.Ticker:{str(capacpdt.Daily) : capacpdt.cap}})

    print(cpacjson)  

    numordre = []
    for ordre in schedule:
        num = str(ordre.workorder.Order_Num) + str(ordre.workorder.Order_Op)
        if num not in numordre:
            numordre.append(str(ordre.workorder.Order_Num) + str(ordre.workorder.Order_Op))
            neworder={"num":ordre.workorder.Order_Num,"op":ordre.workorder.Order_Op, "desc":ordre.workorder.Order_Desc , "pdt":ordre.workorder.workcenter.Ticker, "datecre":ordre.workorder.Crea_Date , "dateplan":ordre.workorder.Basic_Start, "estime":ordre.workorder.Est_Hours, "Priorité":ordre.workorder.Prio, lundi:0, mardi:0, mercredi:0, jeudi:0, vendredi:0}
            df = df.append(neworder, ignore_index=True)
    df['numcom']  = df['num'].astype(str) + df['op'].astype(str)
    

    for ordre in schedule:
        num = str(ordre.workorder.Order_Num) + str(ordre.workorder.Order_Op)
        
        
        if num in df.values:           
            
            df.loc[df['numcom']== num, datetime.datetime.date(ordre.Daily)] = ordre.Plan_hours
            
           
        
    
    df1 = df.drop(columns=['numcom'])
    df1['Total'] = df1[lundi] + df1[mardi] + df1[mercredi] + df1[jeudi] + df1[vendredi]
    
    
    df1.rename(columns={'num':'Numéro', 'op':'Opération', 'desc': 'Description','pdt':'Poste de Travail', 'datecre':'Créer le', 'dateplan':'Début Prévu', 'estime':'Estimé',  lundi: lundi.strftime("%a %y/%m/%d"), mardi: mardi.strftime("%a %y/%m/%d"), mercredi: mercredi.strftime("%a %y/%m/%d"), jeudi: jeudi.strftime("%a %y/%m/%d"), vendredi: vendredi.strftime("%a %y/%m/%d")}, inplace=True)
    js = df1.to_json(orient = 'records', date_format= 'iso')
    
    
    cappdt = json.dumps(cpacjson)
    semcourante = json.dumps(semcour, default=str)

    return render_template("sched.html",today = datetime.date.today(), schedule=schedule, capacite=capacite, sem= sem, df=df, js=js, listcheck=listcheck, cappdt= cappdt, semcourante = semcourante)


@app.route('/testfetch', methods = ['GET', 'POST'])
def testfetch():
    capacite = Capac.query.all()
    postjson = request.json
    postdata= postjson['test2']['item1']
    print(postdata)
    print(postjson)
    
    test = 'oktest'
    tesfetch = json.dumps(test)
    return tesfetch



@app.route('/pousse', methods = ['GET', 'POST'])
def pousse():
    
    
    if request.form['move']:    
        j= (request.form['jour']).split(",")
        n = (request.form['numordre']).split(",")
        
        sem = datetime.datetime.strptime(j[1], "%a %y/%m/%d").isocalendar()[1]

        lundi = datetime.datetime.fromisocalendar(2022, sem + 1, 1)
        mardi = datetime.datetime.fromisocalendar(2022, sem + 1, 2)
        mercredi = datetime.datetime.fromisocalendar(2022, sem + 1, 3)
        jeudi = datetime.datetime.fromisocalendar(2022, sem + 1, 4)
        vendredi = datetime.datetime.fromisocalendar(2022, sem + 1, 5)
        semsuiv= [lundi, mardi, mercredi, jeudi, vendredi]
        print(lundi)
        print(n,j)
                    
        for num in n:
            id = Workorder.query.filter(Workorder.Order_Num == num[0:7]).filter(Workorder.Order_Op == num[7:9]).first()
            print(id.id)
            
            for jour in j:
                print(datetime.datetime.strptime(jour, "%a %y/%m/%d"))
                print(jour)  
                
                if Sched.query.filter(Sched.Workorder_id == id.id).filter(Sched.Daily == datetime.datetime.strptime(jour, "%a %y/%m/%d")).first():
                    todel = Sched.query.filter(Sched.Workorder_id == id.id).filter(Sched.Daily == datetime.datetime.strptime(jour, "%a %y/%m/%d")).first()
                    print('oui')
                    db.session.delete(todel)
                    db.session.commit()
            if Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == lundi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == mardi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == mercredi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == jeudi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == vendredi)).first():
                print('déja la')
            else:
                db.session.add(Sched(Workorder_id = id.id , Daily = semsuiv[1] , Plan_hours = 0))
                db.session.commit()
            #toup = Sched.query.filter(Sched.Workorder_id == id.id).filter(Sched.Daily == datetime.datetime.strptime(d, "%a %y/%m/%d")).first()
            #toup.Plan_hours = h
            #db.session.commit()
        #else:
        #     db.session.add(Sched(Workorder_id = id.id , Daily = datetime.datetime.strptime(d, "%a %y/%m/%d"), Plan_hours = h))
        #     db.session.commit()
        # print(id)
        # print('ok-ca marche ' + d +'-'+ h + '-' + n)
    # sem = 2
    # lundi = datetime.date.fromisocalendar(2022, sem, 1)
    # mardi = datetime.date.fromisocalendar(2022, sem, 2)
    # mercredi = datetime.date.fromisocalendar(2022, sem, 3)
    # jeudi = datetime.date.fromisocalendar(2022, sem, 4)
    # vendredi = datetime.date.fromisocalendar(2022, sem, 5)
    # samedi = datetime.date.fromisocalendar(2022, sem, 6)

    # schedule = Sched.query.filter(Sched.Daily >= lundi).filter(Sched.Daily < samedi).all()  

        
    #return render_template("sched.html",today = datetime.date.today(), schedule=schedule, sem= sem)
    return redirect('/sched')
    #return redirect(url_for('sched') )



    # if 'changer' in request.form:
    #     sem = int(request.form['semaine'])
    
    # lundi = datetime.date.fromisocalendar(2022, sem, 1)
    # mardi = datetime.date.fromisocalendar(2022, sem, 2)
    # mercredi = datetime.date.fromisocalendar(2022, sem, 3)
    # jeudi = datetime.date.fromisocalendar(2022, sem, 4)
    # vendredi = datetime.date.fromisocalendar(2022, sem, 5)


@app.route('/ceduler', methods = ['GET', 'POST'])
def ceduler():
    n = (request.form['numordre']).split(",")
        
    sem = int(request.form['semaine'])
    lundi = datetime.datetime.fromisocalendar(2022, sem , 1)
    mardi = datetime.datetime.fromisocalendar(2022, sem , 2)
    mercredi = datetime.datetime.fromisocalendar(2022, sem , 3)
    jeudi = datetime.datetime.fromisocalendar(2022, sem , 4)
    vendredi = datetime.datetime.fromisocalendar(2022, sem , 5)
    print(n)
    for num in n:

        id = Workorder.query.filter(Workorder.Order_Num == num[0:7]).filter(Workorder.Order_Op == num[8:10]).first()
        print(id.id)
                
        if Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == lundi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == mardi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == mercredi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == jeudi)).first() or Sched.query.filter(Sched.Workorder_id == id.id).filter((Sched.Daily == vendredi)).first():
            print('déja la')
        else:
            db.session.add(Sched(Workorder_id = id.id , Daily = datetime.datetime.fromisocalendar(2022, sem , 1) , Plan_hours = 0))
            db.session.commit()

    print(request.form['semaine'])
    print(request.form['numordre'])
    return redirect(url_for('listglobal') )

@app.route('/capacite', methods = ['GET', 'POST'])
def capacite():

    sem = 9 #int(request.form['sem'])
    lundi = datetime.datetime.fromisocalendar(2022, sem , 1)
    mardi = datetime.datetime.fromisocalendar(2022, sem , 2)
    mercredi = datetime.datetime.fromisocalendar(2022, sem , 3)
    jeudi = datetime.datetime.fromisocalendar(2022, sem , 4)
    vendredi = datetime.datetime.fromisocalendar(2022, sem , 5)
    jour = [lundi, mardi, mercredi,jeudi,vendredi]
    listposte = ['MSERMAI','MSEREL','MSERSYH','MSERMEC','MREPELC','MREPELT', 'MREPMAI','MREPMEC' ,'MFACELP','MFACLAB' ]

    if 'crecapsem' in request.form:    
        sem = int(request.form['sem'])
        lundi = datetime.datetime.fromisocalendar(2022, sem , 1)
        mardi = datetime.datetime.fromisocalendar(2022, sem , 2)
        mercredi = datetime.datetime.fromisocalendar(2022, sem , 3)
        jeudi = datetime.datetime.fromisocalendar(2022, sem , 4)
        vendredi = datetime.datetime.fromisocalendar(2022, sem , 5)
        jour = [lundi, mardi, mercredi,jeudi,vendredi]
        listposte = ['MSERMAI','MSEREL','MSERSYH','MSERMEC','MREPELC','MREPELT', 'MREPMAI','MREPMEC' ,'MFACELP','MFACLAB' ]
        for post in listposte:
            for j in jour:
                db.session.add(Capac(Workcenter_id = (Workcenter.query.filter_by(Ticker= post).first()).id , Daily = j , cap=(Workcenter.query.filter_by(Ticker= post).first()).Heure_jour))
                db.session.commit()

    if 'crecappos' in request.form:
        post = Workcenter.query.filter_by(Ticker= request.form['postecap']).first()
        post.Heure_jour = request.form['capposte']
        db.session.commit()
    
    capposte = []
    for post in listposte:
        arraypost = []
        arraypost.append(post)
        for j in jour:
            if Capac.query.filter_by(Workcenter_id = (Workcenter.query.filter_by(Ticker= post).first()).id).filter_by(Daily = j).first() != None:
                arraypost.append(Capac.query.filter_by(Workcenter_id = (Workcenter.query.filter_by(Ticker= post).first()).id).filter_by(Daily = j).first().cap)
            else:
                arraypost.append(0)
        capposte.append(arraypost)
     
    capacite = capposte
    


    return render_template("capacite.html", capacite = capacite, jour = jour)