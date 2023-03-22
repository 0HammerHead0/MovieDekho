import os
from flask import Flask,url_for
from flask import render_template,redirect
from flask import request
from flask_sqlalchemy import SQLAlchemy

current_dir=os.getcwd()

# print("sqlite:///"+os.path.join(current_dir,"db_directory\\TicketBooking.sqlite3"))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,'db_directory\\TicketBooking.sqlite3')
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

# class USERS_SHOWS(db.Model):
#     __tablename__='users_shows'
#     users_id=db.Column(db.Integer,db.ForeignKey('users.ID'),nullable=False)
#     shows_id=db.Column(db.Integer,db.ForeignKey('shows.ID'),nullable=False)

class SHOWS(db.Model):
    __tablename__='shows'
    ID=db.Column(db.Integer,autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    rating=db.Column(db.Integer)
    tags=db.Column(db.String)
    price=db.Column(db.Integer)
    VID=db.Column(db.Integer)

class VENUE(db.Model):
    __tablename__='venue'
    ID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String)
    place=db.Column(db.String)
    capacity=db.Column(db.Integer)

class USERS(db.Model):
    __tablename__='users'
    ID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String)
    username=db.Column(db.String,unique=True)
    password=db.Column(db.String)
    # visits=db.relationship('SHOWS',secondary=USERS_SHOWS,backref='audience')
db.create_all()

#home page apna banega user login

@app.route("/",methods=["GET","POST","DELETE"])

def home():
    if request.method=='GET':
        return render_template("user_login.html")
    elif request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        if not username or not password:
            return "fields are empty"
        existing_user=USERS.query.filter_by(username=username).first()
        if existing_user:
            #check pass
            user=USERS.query.filter_by(username=username).first()
            if(password==user.password):
                return redirect(url_for('user_dash',user=user.name))
            return "password doesnt match . try again"
        return redirect(url_for('user_register'))
    else:
        print("error check")

@app.route("/user_register",methods=["GET","POST","DELETE"])
def user_register():
    if request.method=='GET':
        return render_template("user_register.html")
    elif request.method=="POST":
        name=request.form['name']
        username=request.form['username']
        password=request.form['password']
        if not username or not password or not name:
            return "fields cannot be empty"
        existing_user=USERS.query.filter_by(username=username).first()
        if existing_user:
            return "existing user"
        else:
            db.session.add(USERS(name=name,username=username,password=password))
            db.session.commit()           
            return render_template("user_dash.html")
    else:
        return("error check")

# @app.route("/user_dash",methods=["GET","POST","DELETE"])
# def dash():

#using user to display
@app.route("/user_dash/<user>",methods=["GET","POST"])
def user_dash(user):
    if request.method=='GET':
        return render_template("user_dash.html",user=user)
    elif request.method=="POST":
        return ""
    else:
        print("error check")

if __name__=='__main__':
    app.debug=True
    app.run()