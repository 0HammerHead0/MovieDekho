import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
Base=declarative_base()
# this is ORM mapping?
class User(Base) :
    __tablename__='user' #user is the name of the table (case sensitive)
    user_id=Column(Integer, autoincrement=True, primary_key=True)
    username=Column(String, unique=True)
    email = Column(String, unique=True)
    #all these properties match for table 'user' in DBBrowser
    #text in DBBrowser is String here
class Article(Base):
    __tablename__='article'
    article_id=Column(Integer, primary_key=True,autoincrement=True)
    title=Column(String)
    content=Column(String)
    authors=relationship("User",secondary="article_authors")
    #secondary-> many-many
class ArticleAuthors(Base):
    __tablename__='article_authors'
    article_id=Column(Integer,ForeignKey("article.article_id"), primary_key=True,nullable=False)
    user_id=Column(Integer, ForeignKey("user.user_id"),primary_key=False,nullable=False)
#go to SQLAlchemy documentation for better understanding
#basic relationship patterns
#out movie ticket application is going to be a one-many relationship
#why?
#one venue can have multiple shows
#but the shows will be limited to the current venue only 
# 
#to connect to a DB use Engine
#create_engine
#                              |  PATH HERE   |
engine=create_engine("sqlite:///sqlite/testdb.sqlite")
"""
if __name__=='__main__':
    with Session(engine) as session:
        articles=session.query(Article).filter(Article.article_id==1).all()
        for article in articles:
            print("Article: {} ".format(article.title))
            for author in article.authors:
                print("Author: {}".format(author.username))
"""
#we dont create connection everytime 
#use session instead
#only one session

"""
if __name__ == '__main__':
    stmt=select(User)
    print("------------------Query------------------")
    print(stmt)
    with engine.connect() as conn:
        print("------------------Result------------------")
        for row in conn.execute(stmt):
            print(row)
"""
#session establishes all conversations with the databse and represents a holding zone
# for all the objects that you've loaded or associated with during its lifespan
"""
if __name__=="__main__":
    with Session(engine,autoflush=False) as session:
        #autoflush is a way to send commands to database and execute them
        #the command below is APPENDING !!! to the table
        session.begin()
        try:
            article=Article(title='my new title', content="my new article content")
            session.add(article)
            session.flush()
            print(article.article_id)
            article_authors=ArticleAuthors(user_id=1,article_id=article.article_id)
            session.add(article_authors)
        except:
            print("rolling back")
            session.rollback()
            #rollback restores the data to your last commit
            raise
        else:
            print("commit")
            #lets a user permanently save all the changes 
            #made in the transaction of a database or table
            session.commit()
"""
#using relationships

if __name__=="__main__":
    #all changes made within this with block wil be grouped as a single transaction
    #that can be committed or rolled back
    with Session(engine,autoflush=False) as session:
        session.begin()
        try:
            x='shashwat'
            author=session.query(User).filter(User.username==x).one() #one because we expect there to be only one 
                                                                        # user with this username
                                                                        #if no matching or more than one matching
                                                                        # exception will be raised

            article=Article(title="Using relationship",content="Use relationship to insert. It's easy")
            #article.authors.append(author)   ->   
            # session.add(article)            -> adds article object of Article class 
                                                # to the list of objects to be committed
            # session is like a list of objects
        except:
            print("Exception, rolling back")
            session.rollback()
            raise
        else:
            print("No exceptions, hence commit")
            session.commit()