from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    platform=db.Column(db.String(20),nullable=False)
    companyname=db.Column(db.String(50),nullable=False)
    accountname=db.Column(db.String(50),nullable=False)
    location=db.Column(db.String(200),nullable=False)
    state=db.Column(db.String(30),nullable=False)
    country=db.Column(db.String(50),nullable=False)
    job=db.Column(db.String(50),nullable=False)
    jobid=db.Column(db.String(50),nullable=False)
    postdate=db.Column(db.String(50),nullable=False)
    posttime=db.Column(db.String(50),nullable=False)
    payment=db.Column(db.String(50),nullable=False)
    
    def __repr__(self):
        return '<id %r>' %self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        platform=request.form['platform']
        cname=request.form['companyname']
        accountname=request.form['accountname']
        cloc=request.form['location']
        state=request.form['state']
        country=request.form['country']
        job=request.form['jobname']
        jobid=request.form['jobid']
        postdate=request.form['postdate']
        posttime=request.form['posttime']
        payment=request.form['payment']
        new_task=Todo(platform=platform,companyname=cname,accountname=accountname,location=cloc,state=state,country=country,job=job,jobid=jobid,postdate=postdate,posttime=posttime,payment=payment)
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