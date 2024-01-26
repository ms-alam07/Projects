# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "home"
__date__ = "$26 Apr, 2021 6:30:58 PM$"

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import numpy as np
import os
import pandas as pd
import pygal
import pymysql
import random
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sqlalchemy import create_engine
import urllib.parse as urlparse
from urllib.parse import parse_qs
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = "1234"
app.password = ""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "heartdisease"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def getuserprofiledetails(self, username):
        strQuery = "SELECT PersonId,Firstname,Lastname,Phoneno,Address,Recorded_Date FROM personaldetails WHERE Username = '" + username + "' LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertdoctordetails(self, firstname, lastname, phone, email, address, username, password):
        print('insertdoctordetails::' + username)
        strQuery = "INSERT INTO doctordetails(Firstname, Lastname, Phoneno, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def insertpersonaldetails(self, firstname, lastname, phone, email, address, username, password):
        print('insertpersonaldetails::' + username)
        strQuery = "INSERT INTO personaldetails(Firstname, Lastname, Phoneno, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def insertquerydetails(self, PersonId, DoctorId, Comments):
        print('insertquerydetails::' + Comments)
        strQuery = "INSERT INTO querydetails(PersonId, DoctorId, Comments, Reply, Recorded_Date) values(%s, %s, %s, '-', now())"
        strQueryVal = (PersonId, DoctorId, Comments)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def updatequerydetails(self, queryId, Comments):
        print('updatequerydetails::' + queryId)
        strQuery = "UPDATE querydetails SET Reply = '" + Comments + "' WHERE QueryId = '" + queryId + "' "
        self.cur.execute(strQuery)
        self.con.commit()
        return ""
    def getpersonaldetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, PersonId FROM personaldetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getdoctorlogindetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, DoctorId FROM doctordetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getuserpersonaldetails(self, name):
        strQuery = "SELECT PersonId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM personaldetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getquerydetails(self, PersonId):
        strQuery = "SELECT d.Firstname, d.Lastname, q.Comments, q.Reply, q.Recorded_Date FROM querydetails AS q LEFT JOIN doctordetails AS d ON d.DoctorId = q.DoctorId WHERE q.PersonId = '" + str(PersonId) + "' ORDER BY Recorded_Date DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdoctorquerydetails(self, DoctorId):
        strQuery = "SELECT p.Firstname, p.Lastname, q.QueryId, q.Comments, q.Reply, q.Recorded_Date FROM querydetails AS q LEFT JOIN personaldetails AS p ON p.PersonId = q.PersonId WHERE q.DoctorId = '" + str(DoctorId) + "' ORDER BY Recorded_Date DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getvideodetails(self):
        strQuery = "SELECT v.VideoId, v.VideoUrl, c.Name, v.Recorded_Date FROM videodetails AS v LEFT JOIN categorydetails AS c ON c.CategoryId = v.CategoryId "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result    
    def getdoctordetails(self, name):
        strQuery = "SELECT DoctorId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM doctordetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdoctorlistdetails(self):
        strQuery = "SELECT DoctorId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM doctordetails LIMIT 10 "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result		
    def getuseranswerdetails(self, PersonId):
        strQuery = "SELECT ua.UserAnswerId, q.Question, ua.Answer, ua.Recorded_Date FROM useranswerdetails AS ua LEFT JOIN questiondetails AS q ON q.QuestionId = ua.QuestionId WHERE ua.PersonId = '" + str(PersonId) + "' AND ua.QuestionId IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19) GROUP BY ua.QuestionId ORDER BY Recorded_Date DESC "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getuseranswerdetailsbyquestionid(self, PersonId, QuestionId):
        strQuery = "SELECT ua.QuestionId, ua.Answer FROM useranswerdetails AS ua WHERE ua.PersonId = '" + str(PersonId) + "' AND ua.QuestionId IN ('" + str(QuestionId) + "') GROUP BY ua.QuestionId ORDER BY Recorded_Date DESC "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getstressdetails(self, id):
        strQuery = "SELECT StressId, Name, Recorded_Date FROM stressdetails WHERE StressId = '" + str(id) + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def gethealthdetails(self, PersonId):
        strQuery = "SELECT HealthId,PersonId,Age,Sex,CP,Trestbps,Cholestrol,Fbs,Restecg,Thalach,Exang,OldPeak,Slope,CA,Thal,Result,Recorded_Date FROM healthdetails WHERE PersonId = '" + str(PersonId) + "' ORDER BY HealthId DESC LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def gethealthdetailsbypersonId(self, PersonId):
        strQuery = "SELECT HealthId,PersonId,Age,Sex,CP,Trestbps,Cholestrol,Fbs,Restecg,Thalach,Exang,OldPeak,Slope,CA,Thal,Result,Recorded_Date FROM healthdetails WHERE PersonId = '" + str(PersonId) + "' ORDER BY HealthId DESC LIMIT 10"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertsurveydataset(self, PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19):
        print('insertsurveydataset::' + Email_Address)
        strQuery = "INSERT INTO surverydataset(PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return "" 
    def insertuseranswerdetails(self, PersonId, q1, a1):
        print('insertuseranswerdetails::' + str(PersonId))
        strQuery = "INSERT INTO useranswerdetails(PersonId, QuestionId, Answer, Recorded_Date) values(%s, %s, %s, now())"
        strQueryVal = (PersonId, q1, a1)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return "" 
    def updatehealthdetails(self, PersonId, result, HealthId):
        print('updatehealthdetails::' + str(PersonId))
        strQuery = "UPDATE healthdetails SET Result = '"+str(result)+"' WHERE HealthId = '"+str(HealthId)+"' AND PersonId = '"+str(PersonId)+"' "
        self.cur.execute(strQuery)
        self.con.commit()
        return "" 
    def deleteuseranswerdetails(self, PersonId):
        print('deleteuseranswerdetails::' + str(PersonId))
        strQuery = "DELETE FROM useranswerdetails WHERE PersonId = (%s) " 
        strQueryVal = (str(PersonId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def deletesurveydataset(self, loanId):
        print(loanId)
        strQuery = "DELETE FROM surverydataset WHERE Sno = (%s) " 
        strQueryVal = (str(loanId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def inserthealthdetails(self, PersonId, age, sex, cp, trestbps, cholestrol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
        print('inserthealthdetails::' + str(PersonId))
        strQuery = "INSERT INTO healthdetails(PersonId, Age, Sex, CP, Trestbps, Cholestrol, Fbs, Restecg, Thalach, Exang, OldPeak, Slope, CA, Thal, Recorded_Date) values('" + str(PersonId) + "', '" + str(age) + "', '" + str(sex) + "', '" + str(cp) + "', '" + str(trestbps) + "', '" + str(cholestrol) + "', '" + str(fbs) + "', '" + str(restecg) + "', '" + str(thalach) + "', '" + str(exang) + "', '" + str(oldpeak) + "', '" + str(slope) + "', '" + str(ca) + "', '" + str(thal) + "', now())"
        self.cur.execute(strQuery)
        self.con.commit()
        return ""
    def getsurveydatasetuploadeddetails(self):
        strQuery = "SELECT Sno, PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Recorded_Date "
        strQuery += "FROM surverydataset "
        strQuery += "ORDER BY Sno DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getgraphdetails(self, dataownername):
        strQuery = "SELECT COUNT(*) AS c, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Attack "        
        strQuery += "FROM kdddataset "        
        strQuery += "GROUP BY Protocol, Service, Flag, Attack "   
        print(strQuery)
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getallprotocoldetails(self):
        strQuery = "SELECT DISTINCT(Protocol) AS Protocol FROM kdddataset"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getkdddatasetdatabyname(self, protocol):
        strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
        strQuery += "FROM kdddataset "
        strQuery += "WHERE Protocol = '" + protocol + "'  "
        strQuery += "ORDER BY Sno DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertanalysisdetails(self, Accuracy, Algorithm):
        print('insertanalysisdetails::' + Algorithm)
        strQuery = "INSERT INTO analysisdetails(Accuracy, Algorithm, Recorded_Date) values(%s, %s, now())"
        strQueryVal = (str(Accuracy).encode('utf-8', 'ignore'), str(Algorithm).encode('utf-8', 'ignore'))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""  
    def getallknndetails(self):
        strQuery = "SELECT sum(Accuracy) as c FROM analysisdetails WHERE Algorithm = 'KNN'"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result    
    def getallkmeansdetails(self):
        strQuery = "SELECT sum(Accuracy) as c FROM analysisdetails WHERE Algorithm = 'K-Means'"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    
@app.route('/', methods=['GET'])
def loadindexpage():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/codeindex', methods=['POST'])
def codeindex():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['PersonId'];
                    def db_query():
                        db = Database()
                        emps = db.getuserprofiledetails(username)       
                        return emps
                    profile_res = db_query()
                    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('index.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('index.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('index.html')
        
    return render_template('index.html')

@app.route('/usersignin', methods=['GET'])
def usersignin():
    return render_template('usersignin.html')

@app.route('/codeusersignin', methods=['POST'])
def codeusersignin():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']    
    username = request.form['username']
    password = request.form['password']
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('email:', email)
    print('address:', address)
    print('username:', username)
    print('password:', password)
    
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and email is not "" and address is not "" and username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('usersignin.html')
                else:
                    def db_query():
                        db = Database()
                        emps = db.insertpersonaldetails(firstname, lastname, phone, email, address, username, password)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('index.html')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('usersignin.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('usersignin.html')
    
    return render_template('usersignin.html')

@app.route('/userprofile', methods=['GET'])
def userprofile():
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/signout', methods=['GET'])
def signout():    
    return render_template('signout.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['x']
    return render_template('index.html')

@app.route('/uploaddata', methods=['GET'])
def uploaddata():
    return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codeuploaddata', methods=['POST'])
def codeuploaddata(): 
    file = request.files['filepath']
    
    print('filename:' + file.filename)
       
    if 'filepath' not in request.files:
        flash ('Please fill all mandatory fields.')
        return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')
    
    if file.filename != '':

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            filepath = UPLOAD_FOLDER + "/" + file.filename

            print('filepath:' + filepath)
            
            data = pd.read_csv(filepath)
            
            # print info about columns in the dataframe 
            print(data.info()) 
            
            # Dropped all the Null, Empty, NA values from csv file 
            csvrows = data.dropna(axis=0, how='any') 

            count = len(csvrows);
            
            print('Length of Data::', count)

            for i in range(count): 
                
                if i == 0:
                    print(count)
                    
                else:  
                    db = Database()
                    db.insertsurveydataset(session['UID'], str(np.array(csvrows['Timestamp'])[i]), str(np.array(csvrows['Email_Address'])[i]), str(np.array(csvrows['Name'])[i]), str(np.array(csvrows['Q1'])[i]), str(np.array(csvrows['Q2'])[i]), str(np.array(csvrows['Q3'])[i]), str(np.array(csvrows['Q4'])[i]), str(np.array(csvrows['Q5'])[i]), str(np.array(csvrows['Q6'])[i]), str(np.array(csvrows['Q7'])[i]), str(np.array(csvrows['Q8'])[i]), str(np.array(csvrows['Q9'])[i]), str(np.array(csvrows['Q10'])[i]), str(np.array(csvrows['Q11'])[i]), str(np.array(csvrows['Q12'])[i]), str(np.array(csvrows['Q13'])[i]), str(np.array(csvrows['Q14'])[i]), str(np.array(csvrows['Q15'])[i]), str(np.array(csvrows['Q16'])[i]), str(np.array(csvrows['Q17'])[i]), str(np.array(csvrows['Q18'])[i]), str(np.array(csvrows['Q19'])[i])) 

            flash('File successfully uploaded!')
            return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

        else:
            flash('Allowed file types are .txt')
            return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')
    else:
        flash ('Please fill all mandatory fields.')           
        return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

@app.route('/viewuploadeddata', methods=['GET'])
def viewuploadeddata():
    def db_query():
        db = Database()
        emps = db.getsurveydatasetuploadeddetails()       
        return emps
    profile_res = db_query()
    return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/deletedata', methods=['GET'])
def deletedata():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    
    loanId = parse_qs(parsed.query)['index']
    print(loanId)
    
    try:
        if loanId is not "": 
            
            db = Database()
            db.deletesurveydataset(loanId[0])
            
            def db_query():
                db = Database()
                emps = db.getsurveydatasetuploadeddetails()    
                return emps
            profile_res = db_query()
            flash ('Dear Customer, Your request has been processed sucessfully!')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/graph', methods=['GET'])
def graph():
    
    def accepteddb_query():
        db = Database()
        emps = db.getgraphdetails(session['x'])       
        return emps
    res = accepteddb_query()
    
    graph = pygal.Line()
    
    graph.title = '% Comparison Graph Between Attacks vs Number of Counts.'
    
    graph.x_labels = ['c', 'de_bytes', 'nc_bytes']
    
    for row in res:
        
        print(row['c'])
        
        graph.add(row['Protocol'] + '-' + row['Service'] + '-' + row['Flag'] + '-' + row['Attack'], [int(row['c']), int(row['de_bytes']), int(row['nc_bytes'])])
        
    graph_data = graph.render_data_uri()
    
    return render_template('graph.html', sessionValue=session['x'], graph_data=graph_data)

@app.route('/searchknn', methods=['GET'])
def searchknn():    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    return render_template('searchknn.html', sessionValue=session['x'], protocolresult=protocolresult, content_type='application/json')

@app.route('/codesearchknn', methods=['POST'])
def codesearchknn():  
    
    protocolname = request.form['protocol']
    
    print('protocolname:' + protocolname)
    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    
    try:
        if protocolname is not "": 
            
            db_connection_str = 'mysql+pymysql://root:' + app.password + '@localhost/anomalydetection?charset=utf8'
            
            db_connection = create_engine(db_connection_str)

            strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
            strQuery += "FROM kdddataset "
            strQuery += "WHERE Protocol = '" + protocolname + "'  "
            strQuery += "ORDER BY Sno DESC "
            strQuery += "LIMIT 10" 
            
            print('Query::', strQuery)
        
            df = pd.read_sql(strQuery, con=db_connection)

            # you want all rows, and the feature_cols' columns
            X = df.iloc[:, 8: 42].values
            y = df.iloc[:, 5: 6].values

            print('X Data::', X)

            # Split into training and test set 
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 

            knn = KNeighborsClassifier(n_neighbors=7) 

            knn.fit(X_train, y_train) 

            # Predict on dataset which model has not seen before 
            y_knn = knn.predict(X_test);

            result = metrics.accuracy_score(y_test, y_knn)

            print("KNN Accuracy :", result); 
            
            algo = 'KNN'
            
            db = Database()
            db.insertanalysisdetails(result, algo) 
            
            def db_query():
                db = Database()
                emps = db.getkdddatasetdatabyname(protocolname)
                return emps
            profile_res = db_query()
            
            return render_template('codesearchknn.html', sessionValue=session['x'], result=profile_res, protocolresult=protocolresult, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('searchknn.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('searchknn.html', sessionValue=session['x'])
    
    return render_template('searchknn.html', sessionValue=session['x'])

@app.route('/searchkmeans', methods=['GET'])
def searchkmeans():    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    return render_template('searchkmeans.html', sessionValue=session['x'], protocolresult=protocolresult, content_type='application/json')

@app.route('/codesearchkmeans', methods=['POST'])
def codesearchkmeans():  
    
    protocolname = request.form['protocol']
    
    print('protocolname:' + protocolname)
    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    
    try:
        if protocolname is not "": 
            
            db_connection_str = 'mysql+pymysql://root:' + app.password + '@localhost/anomalydetection?charset=utf8'
            
            db_connection = create_engine(db_connection_str)

            strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
            strQuery += "FROM kdddataset "
            strQuery += "WHERE Protocol = '" + protocolname + "'  "
            strQuery += "ORDER BY Sno DESC "
            strQuery += "LIMIT 10" 
            
            print('Query::', strQuery)
        
            df = pd.read_sql(strQuery, con=db_connection)

            # you want all rows, and the feature_cols' columns
            X = df.iloc[:, 8: 42].values
            y = df.iloc[:, 5: 6].values

            print('X Data::', X)

            kmeans = KMeans(n_clusters=4)
            kmeans.fit(X)

            y_kmeans = kmeans.predict(X)
            
            print("y_kmeans :", y_kmeans); 
            
            result = y_kmeans[0] * 2
            
            algo = 'K-Means'
            
            print("K-Means Accuracy :", result); 
            
            db = Database()
            db.insertanalysisdetails(result, algo) 
            
            def db_query2():
                db = Database()
                emps = db.getkdddatasetdatabyname(protocolname)
                return emps
            profile_res = db_query2()
            
            return render_template('codesearchkmeans.html', sessionValue=session['x'], result=profile_res, protocolresult=protocolresult, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('searchkmeans.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('searchkmeans.html', sessionValue=session['x'])
    
    return render_template('searchkmeans.html', sessionValue=session['x'])

@app.route('/comparisongraph', methods=['GET'])
def comparisongraph():
    
    labels = ["KNN ALGORITHM", "K-MEANS ALGORITHM"]
    
    def kmeans_query():
        db = Database()
        emps = db.getallkmeansdetails()       
        return emps
    res = kmeans_query()

    kmeanscount = 0;

    for row in res:
        print(row['c'])
        kmeanscount = row['c']
        
    def knn_query():
        db = Database()
        emps = db.getallknndetails()       
        return emps
    res = knn_query()

    knncount = 0;

    for row in res:
        print(row['c'])
        knncount = row['c']
        
    values = [knncount, kmeanscount]

    return render_template('comparisongraph.html', sessionValue=session['x'], values=values, labels=labels)

@app.route('/quiz', methods=['GET'])
def quiz():
    return render_template('quiz.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz', methods=['POST'])
def codequiz():
    db = Database()
    db.deleteuseranswerdetails(session['UID'])    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_1', methods=['POST'])
def quiz_1():    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_1', methods=['POST'])
def codequiz_1():
    q1 = request.form['one']
    q2 = request.form['two']
    a1 = request.form['a']
    a2 = request.form['b']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_2', methods=['POST'])
def quiz_2():
    return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_2', methods=['POST'])
def codequiz_2():
    q1 = request.form['three']
    q2 = request.form['four']
    a1 = request.form['c']
    a2 = request.form['d']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_3', methods=['POST'])
def quiz_3():
    return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_3', methods=['POST'])
def codequiz_3():
    q1 = request.form['five']
    q2 = request.form['six']
    a1 = request.form['e']
    a2 = request.form['f']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_4.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_4', methods=['POST'])
def quiz_4():
    return render_template('quiz_4.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_4', methods=['POST'])
def codequiz_4():
    q1 = request.form['seven']
    q2 = request.form['eight']
    a1 = request.form['g']
    a2 = request.form['h']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_5.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_4.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_4.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_4.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_5', methods=['POST'])
def quiz_5():
    return render_template('quiz_5.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_5', methods=['POST'])
def codequiz_5():
    q1 = request.form['nine']
    q2 = request.form['ten']
    a1 = request.form['i']
    a2 = request.form['j']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_6.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_5.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_5.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_5.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_6', methods=['POST'])
def quiz_6():
    return render_template('quiz_6.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_6', methods=['POST'])
def codequiz_6():
    q1 = request.form['eleven']
    q2 = request.form['twelve']
    a1 = request.form['k']
    a2 = request.form['l']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_7.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_6.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_6.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_6.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_7', methods=['POST'])
def quiz_7():
    return render_template('quiz_7.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_7', methods=['POST'])
def codequiz_7():
    q1 = request.form['thirteen']
    q2 = request.form['fourteen']
    a1 = request.form['m']
    a2 = request.form['n']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_8.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_7.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_7.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_7.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_8', methods=['POST'])
def quiz_8():
    return render_template('quiz_8.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_8', methods=['POST'])
def codequiz_8():
    q1 = request.form['fifteen']
    q2 = request.form['sixteen']
    a1 = request.form['o']
    a2 = request.form['p']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_9.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_8.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_8.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_8.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_9', methods=['POST'])
def quiz_9():
    return render_template('quiz_9.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_9', methods=['POST'])
def codequiz_9():
    q1 = request.form['seventeen']
    q2 = request.form['eighteen']
    a1 = request.form['q']
    a2 = request.form['r']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_10.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_9.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_9.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_9.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_10', methods=['POST'])
def quiz_10():
    return render_template('quiz_10.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_10', methods=['POST'])
def codequiz_10():
    q1 = request.form['nighteen']
    a1 = request.form['s']
    
    print('q1:', q1)
    print('a1:', a1)
    
    try:
        if q1 is not "" and a1 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()  
            return redirect(url_for("results"))
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_10.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_10.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_10.html', sessionValue=session['x'], content_type='application/json')

@app.route('/results', methods=['GET'])
def results():
        
    #Load the data-set
    dataset = pd.read_csv('D:/Dataset/HeartDisease.csv') 

    #Print the count of rows and coulmns in csv file
    print("Dimensions of Dataset: {}".format(dataset.shape))

    # Dropped all the Null, Empty, NA values from csv file 
    new_dataset = dataset.dropna(axis=0, how='any') 

    print("Dimensions of Dataset after Pre-processing : {}".format(new_dataset.shape))
       
    X = dataset.iloc[:, 0:13].values
    y = dataset.iloc[:, 13:14].values
    
    #print(X)
    #print(y)
    
    # Import train_test_split function
    from sklearn.model_selection import train_test_split

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=109) # 70% training and 30% test

    # linear regression for multioutput regression
    from sklearn.datasets import make_regression
    from sklearn.linear_model import LinearRegression

    # define model
    classifier = LinearRegression()

    #Train the model using the training sets
    classifier.fit(X_train, y_train)
   

    def db_query():
        db = Database() 
        emps = db.gethealthdetails(session['UID']) 
        return emps
        
    res = db_query()  
        
    age = ''
    sex = ''
    cp = ''
    trestbps = ''
    cholestrol = ''
    fbs = ''
    restecg = ''
    thalach = ''
    exang = ''
    oldPeak = ''
    slope = ''
    ca = ''
    thal = ''
    healthid = ''

    for row in res:
        healthid = row['HealthId']
        age = row['Age']
        sex = row['Sex']
        cp = row['CP']
        trestbps = row['Trestbps']
        cholestrol = row['Cholestrol']
        fbs = row['Fbs']
        restecg = row['Restecg']
        thalach = row['Thalach']
        exang = row['Exang']        
        oldPeak = row['OldPeak']
        slope = row['Slope']
        ca = row['CA']
        thal = row['Thal']
    
    # make a prediction
    row = [[age, sex, cp, trestbps, cholestrol, fbs, restecg, thalach, exang, oldPeak, slope, ca, thal]]

    print("Row : {}".format(row));
    
    #Predict the response for test dataset
    y_pred = classifier.predict(row)

    print(" Prediction:", y_pred)
    
    # summarize prediction
    print(y_pred[0])
    
    results = 'No'
      
    if y_pred[0] < 0:
        results = 'No'
    else:
        results = 'Yes'
    
    def db_query1():
        db = Database()
        emps = db.updatehealthdetails(session['UID'], results,	healthid)    
        return emps
    res2 = db_query1() 
    
    return render_template('results.html', sessionValue=session['x'], result=res, result_1=results, content_type='application/json')

@app.route('/doctor', methods=['GET'])
def doctor():
    return render_template('doctor.html')

@app.route('/codedoctor', methods=['POST'])
def codedoctor():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getdoctorlogindetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['DoctorId'];
                    def db_query():
                        db = Database()
                        emps = db.getdoctordetails(username)       
                        return emps
                    profile_res = db_query()
                    return render_template('doctorprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('doctor.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('doctor.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('doctor.html')
        
    return render_template('doctor.html')

@app.route('/doctorsignin', methods=['GET'])
def doctorsignin():
    return render_template('doctorsignin.html')

@app.route('/codedoctorsignin', methods=['POST'])
def codedoctorsignin():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']    
    username = request.form['username']
    password = request.form['password']
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('email:', email)
    print('address:', address)
    print('username:', username)
    print('password:', password)
    
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and email is not "" and address is not "" and username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getdoctorlogindetails(username, password)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('doctorsignin.html')
                else:
                    def db_query():
                        db = Database()
                        emps = db.insertdoctordetails(firstname, lastname, phone, email, address, username, password)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('doctor.html')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('doctorsignin.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('doctorsignin.html')
    
    return render_template('doctorsignin.html')

@app.route('/doctorprofile', methods=['GET'])
def doctorprofile():
    def db_query():
        db = Database()
        emps = db.getdoctordetails(session['x'])       
        return emps
    profile_res = db_query()
    return render_template('doctorprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/viewdoctor', methods=['GET'])
def viewdoctor():
    def db_query():
        db = Database()
        emps = db.getdoctorlistdetails()       
        return emps
    profile_res = db_query()
    return render_template('viewdoctor.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/askquery', methods=['GET'])
def askquery():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    
    doctorId = parse_qs(parsed.query)['index']
    print(doctorId)
    
    try:
        if doctorId is not "":             
            return render_template('askquery.html', sessionValue=session['x'], result=doctorId[0], content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('askquery.html', sessionValue=session['x'], result=doctorId, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('askquery.html', sessionValue=session['x'], result=doctorId, content_type='application/json')
    
@app.route('/codeaskquery', methods=['POST'])
def codeaskquery():
    doctorId = request.form['doctorId']
    comments = request.form['comments']
    
    print('doctorId:' + doctorId)
    print('comments:' + comments)
    
    try:
        if doctorId is not "" and comments is not "": 
            def db_query():
                db = Database()
                emps = db.insertquerydetails(session['UID'], doctorId, comments)    
                return emps
            res = db_query()
            
            def db_query():
                db = Database()
                emps = db.getquerydetails(session['UID'])       
                return emps
            profile_res = db_query()
            flash ('Dear Customer, Your query has been submitted successfully.')
            return render_template('viewquery.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('askquery.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('askquery.html')
        
    return render_template('askquery.html')

@app.route('/viewquery', methods=['GET'])
def viewquery():
    def db_query():
        db = Database()
        emps = db.getquerydetails(session['UID'])       
        return emps
    profile_res = db_query()
    return render_template('viewquery.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/viewdoctorquery', methods=['GET'])
def viewdoctorquery():
    def db_query():
        db = Database()
        emps = db.getdoctorquerydetails(session['UID'])       
        return emps
    profile_res = db_query()
    return render_template('viewdoctorquery.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/replyquery', methods=['GET'])
def replyquery():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    
    queryId = parse_qs(parsed.query)['index']
    print(queryId)
    
    try:
        if queryId is not "":             
            return render_template('replyquery.html', sessionValue=session['x'], result=queryId[0], content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('replyquery.html', sessionValue=session['x'], result=queryId, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('replyquery.html', sessionValue=session['x'], result=queryId, content_type='application/json')
    
@app.route('/codereplyquery', methods=['POST'])
def codereplyquery():
    queryId = request.form['queryId']
    comments = request.form['comments']
    
    print('queryId:' + queryId)
    print('comments:' + comments)
    
    try:
        if queryId is not "" and comments is not "": 
            def db_query():
                db = Database()
                emps = db.updatequerydetails(queryId, comments)    
                return emps
            res = db_query()  
            
            def db_query():
                db = Database()
                emps = db.getdoctorquerydetails(session['UID'])       
                return emps
            profile_res = db_query()
            flash ('Dear Customer, Your query has been submitted successfully.')
            return render_template('viewdoctorquery.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('replyquery.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('replyquery.html')
        
    return render_template('replyquery.html')

@app.route('/viewvideo', methods=['GET'])
def viewvideo():
    def db_query():
        db = Database()
        emps = db.getvideodetails()       
        return emps
    profile_res = db_query()
    return render_template('viewvideo.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/addheartdetail', methods=['GET'])
def addheartdetail():  
    return render_template('addheartdetail.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codeaddheartdetail', methods=['POST'])
def codeaddheartdetail():  
    age = request.form['age']
    sex = request.form['sex']
    cp = request.form['cp']
    trestbps = request.form['trestbps']
    cholestrol = request.form['cholestrol']
    fbs = request.form['fbs']
    restecg = request.form['restecg']
    thalach = request.form['thalach']
    exang = request.form['exang']
    oldpeak = request.form['oldpeak']
    slope = request.form['slope']
    ca = request.form['ca']
    thal = request.form['thal']
    
    print('age:' + age)
    print('sex:' + sex)
    print('cp:' + cp)
    print('trestbps:' + trestbps)
    print('cholestrol:' + cholestrol)
    print('fbs:' + fbs)
    print('restecg:' + restecg)
    print('thalach:' + thalach)
    print('exang:' + exang)
    print('oldpeak:' + oldpeak)
    print('slope:' + slope)
    print('ca:' + ca)
    print('thal:' + thal)
    
    try:
        if age is not "" and sex is not "" and cp is not "" and trestbps is not "" and cholestrol is not "" and fbs is not "" and restecg is not "" and thalach is not "" and exang is not "" and oldpeak is not "" and slope is not "" and ca is not "" and thal is not "": 
            
            def db_query():
                db = Database()
                emps = db.inserthealthdetails(session['UID'], age, sex, cp, trestbps, cholestrol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)    
                return emps
            res = db_query()
                
            flash ('Dear Customer, Your record has been inserted successfully.')
            return redirect(url_for("results"))
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('addheartdetail.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('addheartdetail.html', sessionValue=session['x'], content_type='application/json')
        
    return render_template('addheartdetail.html', sessionValue=session['x'], content_type='application/json')

@app.route('/viewhistory', methods=['GET'])
def viewhistory():
    
    def db_query():
        db = Database() 
        emps = db.gethealthdetailsbypersonId(session['UID']) 
        return emps
        
    res = db_query()  
    
    return render_template('history.html', sessionValue=session['x'], result=res, content_type='application/json')
