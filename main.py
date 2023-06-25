import os
from flask import Flask
from application import config,controllers
from application.config import LocalDevelopConfig
from application.database import db
from flask_restful import Resource, Api
from flask_login import LoginManager
app=None
def create_app():
    app=Flask(__name__,template_folder='templates')
    if os.getenv('ENV',"development")=="production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopConfig)
    db.init_app(app)
    #user login
    login_manager=LoginManager()
    login_manager.init_app(app)
    login_manager.login_view='controllers.home'
    api= Api(app)
    app.app_context().push()
    return app,api

app,api=create_app()

#Import all the controllers so they are loaded
from application.controllers import *
from application.api import UserApi
api.add_resource(UserApi, "/api/user" ,"/api/user/<string:username>" ,"/api/venue/<ID>","/api/venue")
if __name__=="__main__":
    #Run the flask app
    app.run(host='0.0.0.0',port=8080)