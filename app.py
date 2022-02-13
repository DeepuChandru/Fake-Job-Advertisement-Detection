from flask import Flask,render_template,request,redirect,jsonify,json,url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import SelectField
from flask_wtf import FlaskForm
import re,os
from bs4 import BeautifulSoup #as soup, BeautifulStoneSoup
from urllib.request import urlopen as uReq
import requests,pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from serpapi import GoogleSearch

joblist1=[]
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
db=SQLAlchemy(app)
model=pickle.load(open('classifier.pkl','rb'))
df = pd.read_csv('fake_job_postings.csv')
titles=list(set(df['title'].tolist()))
titles.sort()
print(titles[0])
# titles=list(set(titles))
location1=list(set(df['location'].tolist()))
location1.remove(location1[0])
print(location1[0],1,sep="")
# location.sort()
department1=list(set(df['department'].tolist()))
department1.remove(department1[0])
# department.sort()
sal_range1=list(set(df['salary_range'].tolist()))
sal_range1.remove(sal_range1[0])
exp1=list(set(df['required_experience'].tolist()))
exp1.remove(exp1[0])
# exp.sort()
emp_type1=list(set(df['employment_type'].tolist()))
emp_type1.remove(emp_type1[0])
edu1=list(set(df['required_education'].tolist()))
edu1.remove(edu1[0])
industry1=list(set(df['industry'].tolist()))
industry1.remove(industry1[0])
function1=list(set(df['function'].tolist()))
function1.remove(function1[0])



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
        # cname=request.form['companyname']
        # cloc = City.query.filter_by(id=form.city.data).first()
        # country = Country.query.filter_by(id=form.country.data).first()
        # state = State.query.filter_by(id=form.state.data).first()
        # pincode=request.form['pincode']
        # job=request.form['jobname']
        # jobid=request.form['jobid']
        # payment=request.form['payment']
        # platform=request.form['platform']
        # website=request.form['website']
        # accountname=request.form['accountname']
        # postdate=request.form['postdate']
        # posttime=request.form['posttime']
        # email=request.form['email']
        title=request.form['title']
        location=request.form['location']
        department=request.form['department']
        sal_range=request.form['sal_range']
        exp=request.form['exp']
        emp_type=request.form['emp_type']
        edu=request.form['edu']
        industry=request.form['industry']
        function=request.form['function']
        # new_task=Todo(companyname=cname,city=cloc,state=state,country=country,pincode=pincode,job=job,jobid=jobid,payment=payment,platform=platform,website=website,accountname=accountname,postdate=postdate,posttime=posttime,email=email)
        # list=[job]+[cname]+[platform]+[accountname]+[website]
        list=[title]+[location]+[department]+[sal_range]+[exp]+[emp_type]+[edu]+[industry]+[function]
        encode=LabelEncoder()
        # encode.fit(list)
        x=encode.fit_transform(list)
        x= x.reshape(1,-1)
        # cv=TfidfVectorizer(max_features=100)
        # x=cv.fit_transform(list)
        prediction=model.predict_proba(x)
        output='{0:.{1}f}'.format(prediction[0][1],2)
        if(float(output)<0.5):
            return render_template('result.html',pred="This Advertisement is AUTHENTIC")
        else:
            return render_template('result.html',pred="This Advertisement is FAKE")
        # try:
        #     db.session.add(new_task)
        #     db.session.commit()
        #     return redirect('/form')
        # except:
        #     return "There was an issue entering details"
    else:
        return render_template('form.html',form = form,titles=titles,location=location1,dept=department1,sal=sal_range1,exp=exp1,emp_type=emp_type1,edu=edu1,industry=industry1,function=function1)

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

            if 'indeed' in link:
                for i in range(0,40,10):
                    c=extractindeed(link,i) 
                    transformindeed(c)
            if 'naukri' in link:
                    c=extractnaukri(link)
                    transformnaukri(c)
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
    #retrieve data from serp api
    filename = os.path.join(app.static_folder, 'data.json')
    params = {
        "engine": "google_jobs",
        "q": "analyst chennai",
        "hl": "en",
        "api_key": "38839121e0e43db924ae2d0f7967c5a03bd4448e9c8cac007234c4c39aca726d"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    try:
        jobs_results = results['jobs_results']
    except:
        return render_template('result.html',pred="There are no job results available")
    with open(filename, "w") as outfile:
        json.dump(jobs_results, outfile)
    # filename = os.path.join(app.static_folder, 'data.json')
    # loading json
    with open(filename) as data_file:
        data = json.load(data_file)
    #verify each json
    for i in jlist:
        #print(i)
        i['title']=i['title'].lower()
        i['company']=i['company'].lower()
        i['location']=i['location'].lower()
        for j in data:
            print(j['title'],j['company_name'],j['location'])
            j['title']=j['title'].lower()
            j['company_name']=j['company_name'].lower()
            j['location']=j['location'].lower()
            if (i['title'].count(j['title'])>0 and i['company']==j['company_name'] and j['location'].count(i['location'])>0):# and i['salary']==j['salary']):
                i['flag']='Authenticated'
                break
            else:
                i['flag']='Fake'

#To find the list of jobs from link for indeed(scraper) 
def extractindeed(link,page):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    url=link+'&start='+str(page)
    r=requests.get(url,headers)
    soup=BeautifulSoup(r.content,'html.parser')
    # print(soup)
    return soup

#To find the list of jobs from link for naukri(scraper) 
def extractnaukri(link):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    url=link
    r=requests.get(url,headers)
    soup=BeautifulSoup(r.content,'html.parser')
    # print(soup.prettify())
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

def transformnaukri(soup):
    divs=soup.find_all('div',class_='info fleft')
    # print("divs")
    # print(divs)
    for item in divs:
        title=item.find('a',class_='title fw500 ellipsis').text
        company=item.find('a',class_='subTitle ellipsis fleft').text
        location=item.find('span',class_='ellipsis fleft fs12 lh16 ').text
        try:
            salary=item.find('span',class_='ellipsis fleft fs12 lh16 ').text.strip()
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