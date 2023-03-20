import os
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
current_dir=os.getcwd()

print("sqlite:///"+os.path.join(current_dir,"sqlite\\testdb.sqlite3"))
# __file__ contains the path of the the script file that is currently being executed

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,'sqlite\\testdb.sqlite3')
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

class User(db.Model) :
    __tablename__='user' #user is the name of the table (case sensitive)
    user_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    username=db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    #all these properties match for table 'user' in DBBrowser
    #text in DBBrowser is String here
class Article(db.Model):
    __tablename__='article'
    article_id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    title=db.Column(db.String)
    content=db.Column(db.String)
    authors=db.relationship("User",secondary="article_authors")
    #secondary-> many-many
class ArticleAuthors(db.Model):
    __tablename__='article_authors'
    article_id=db.Column(db.Integer,db.ForeignKey("article.article_id"), primary_key=True,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("user.user_id"),primary_key=False,nullable=False)


app.static_folder='templates'

@app.route("/", methods = ["GET","POST"])
#neeche agar html me {{ articles }} hota...to jinja kaam karta aur articles ki 
#list print hoti
# def articles():
#     articles = Article.query.all()
#     return render_template("user_login.html",articles=articles)

#jab /lagake url extend karoge to aisa ayega....user_name as a parameter jayega
# this will print details of all the articles by the username user_name
@app.route("/articles/<user_name>", methods=["GET","POST"])
def articles_by_author(user_name):
    articles=Article.query.filter(Article.authors.any(username=user_name))
    return render_template("articles_by_author.html",articles=articles)


    
if __name__=='__main__':
    # Run the flask app
    app.run()(debug=True)