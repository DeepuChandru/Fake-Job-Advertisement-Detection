from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    companyname=db.Column(db.String(50),nullable=False)
    location=db.Column(db.String(200),nullable=False)
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

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        cname=request.form['companyname']
        cloc=request.form['location']
        state=request.form['state']
        country=request.form['country']
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
        new_task=Todo(companyname=cname,location=cloc,state=state,country=country,pincode=pincode,job=job,jobid=jobid,payment=payment,platform=platform,website=website,accountname=accountname,postdate=postdate,posttime=posttime,email=email)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue entering details"
    else:
        return render_template('index.html')
    
if __name__=="__main__":
    app.run(debug=True)