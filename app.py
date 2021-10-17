from flask import Flask,render_template,request,redirect,jsonify,json,url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import SelectField
from flask_wtf import FlaskForm
import re,os
from bs4 import BeautifulSoup #as soup, BeautifulStoneSoup
from urllib.request import urlopen as uReq
import requests

joblist1=[]
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
db=SQLAlchemy(app)

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    sortname = db.Column(db.String(3))
    name = db.Column(db.String(60))
  
class State(db.Model):
    __tablename__ = 'state'
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    country_id = db.Column(db.Integer)
  
class City(db.Model):
    __tablename__ = 'city'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    stateid = db.Column(db.Integer) 

class Form(FlaskForm):
    country = SelectField('country', choices=[])
    state = SelectField('state', choices=[])
    city = SelectField('city', choices=[])

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    companyname=db.Column(db.String(50),nullable=False)
    city=db.Column(db.String(200),nullable=False)
    state=db.Column(db.String(30),nullable=False)
    country=db.Column(db.String(50),nullable=False)
    pincode=db.Column(db.Integer,nullable=True)
    job=db.Column(db.String(50),nullable=False)
    jobid=db.Column(db.String(50),nullable=False)
    payment=db.Column(db.String(3),nullable=False)
    platform=db.Column(db.String(10),nullable=False)
    website=db.Column(db.String(10),nullable=True)
    accountname=db.Column(db.String(50),nullable=True)
    postdate=db.Column(db.String(50),nullable=True)
    posttime=db.Column(db.String(50),nullable=True)
    email=db.Column(db.String(70),nullable=True)
    
    def __repr__(self):
        return '<id %r>' %self.id

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form',methods=['POST','GET'])
def index():
    form = Form()
    form.country.choices = [(country.id, country.name) for country in Country.query.all()]
    if request.method=='POST':
        cname=request.form['companyname']
        cloc = City.query.filter_by(id=form.city.data).first()
        country = Country.query.filter_by(id=form.country.data).first()
        state = State.query.filter_by(id=form.state.data).first()
        # cloc=request.form['city']
        # state=request.form['state']
        # country=request.form['country']
        pincode=request.form['pincode']
        job=request.form['jobname']
        jobid=request.form['jobid']
        payment=request.form['payment']
        platform=request.form['platform']
        website=request.form['website']
        accountname=request.form['accountname']
        postdate=request.form['postdate']
        posttime=request.form['posttime']
        email=request.form['email']
        new_task=Todo(companyname=cname,city=cloc,state=state,country=country,pincode=pincode,job=job,jobid=jobid,payment=payment,platform=platform,website=website,accountname=accountname,postdate=postdate,posttime=posttime,email=email)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/form')
        except:
            return "There was an issue entering details"
    else:
        return render_template('form.html',form = form)

@app.route('/state/<get_state>')
def statebycountry(get_state):
    state = State.query.filter_by(country_id=get_state).all()
    stateArray = []
    for city in state:
        stateObj = {}
        stateObj['id'] = city.id
        stateObj['name'] = city.name
        stateArray.append(stateObj)
    return jsonify({'statecountry' : stateArray})
  
@app.route('/city/<get_city>')
def city(get_city):
    state_data = City.query.filter_by(stateid=get_city).all()
    cityArray = []
    for city in state_data:
        cityObj = {}
        cityObj['id'] = city.id
        cityObj['name'] = city.name
        cityArray.append(cityObj)
    return jsonify({'citylist' : cityArray}) 

@app.route('/url')
def url():
    return render_template('url.html')

#validator (if url is valid or not)
@app.route('/validate',methods=['POST'])
def validate():
    form=Form()
    if request.method=="POST":
        link=request.form["url"]
        regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
    # Compile the ReGex
        p = re.compile(regex)
 
    # If the string is empty
    # return false
        if (link== None):
            return False
 
    # Return if the string
    # matched the ReGex
        if(re.search(p, link)):
            for i in range(0,40,10):
                c=extract(link,i) ## error for monster
                if 'indeed' in link:
                    transformindeed(c)
                if 'monsterindia' in link:
                    transformmonster(c)
            verify(joblist1)
            return redirect(url_for('display'))
            #elif 'naukri' in link:

            #return "Valid"
        else:
            return "invalid"
     
#display in display.html
@app.route('/display')
def display():
    return render_template('display.html',joblist1=joblist1) 

#verify the json list with original data    
def verify(jlist):
    filename = os.path.join(app.static_folder, 'data.json')
    with open(filename) as data_file:
        data = json.load(data_file)
    #verify each json
    for i in jlist:
        #print(i)
        for j in data:
            if (i['title']==j['title'] and i['company']==j['company'] and i['location']==j['location'] and i['salary']==j['salary']):
                i['flag']='Authenticated'
                break
            else:
                i['flag']='Fake'

#To find the list of jobs from link(scraper)
def extract(link,page):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    url=link+'&start='+f'{page}'
    r=requests.get(url,headers)
    soup=BeautifulSoup(r.content,'html.parser')
    return soup

def transformindeed(soup):
    divs=soup.find_all('div',class_='job_seen_beacon')
    for item in divs:
        title=item.find('h2').text 
        #title=item.find('div',class_='heading4 color-text-primary singleLineTitle tapItem-gutter').text
        company=item.find('span',class_='companyName').text.strip()
        location=item.find('div',class_='companyLocation').text.strip()
        try:
            salary=item.find('span',class_='salary-snippet').text.strip()
        except:
            salary='Not found'
        job={
            "title":title.replace('new',''),
            "company":company,
            "location":location.replace('•'," "),
            "salary":salary.replace('₹','')
        }
        joblist1.append(job)
    return

def transformmonster(soup):
    divs=soup.find_all('div',class_='job-tittle')
    print(divs)
    for item in divs:
        title=item.find('h3',class_='medium').text.strip()
        company=item.find('span',class_='company-name').text.strip()
        location=item.find('span',class_='loc').text.strip()
        try:
            salary=item.find('i',class_='mqfi-coin-stack fs-18').text.strip()
        except:
            salary='Not found'
        job={
            "title":title.replace('new',''),
            "company":company,
            "location":location.replace('•'," "),
            "salary":salary.replace('₹','')
        }
        joblist1.append(job)
if __name__=="__main__":
    app.run(debug=True)