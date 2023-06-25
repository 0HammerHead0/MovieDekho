from flask_restful import Resource,Api
from flask_restful import fields, marshal_with,reqparse
from application.database import db
from application.models import USERS,VENUES,SHOWS,USERS_SHOWS
from application.validation import NotFoundError,BusinnessValidationError


output_fields={
    "ID":fields.Integer,
    "username":fields.String,
    "name":fields.String
}

create_user_parser=reqparse.RequestParser()
create_user_parser.add_argument('username',type)
create_user_parser.add_argument('email')

venue_fields={
    "ID": fields.Integer,
    "name": fields.String,
    "capacity": fields.Integer,
    "place": fields.String
}
venue_parse = reqparse.RequestParser()
venue_parse.add_argument("name")
venue_parse.add_argument("place")
venue_parse.add_argument("ID")
venue_parse.add_argument("capacity")

class UserApi(Resource):
    @marshal_with(output_fields)
    def get(self,username):
        print("in userapi get method", username)
        user =db.session.query(USERS).filter(USERS.username==username).first()
        if user:
            return user
        else:
            raise NotFoundError(status_code=404)
    def post(self):
        args=create_user_parser.parse_args()
        username=args.get("username",None)
        name=args.get("name",None)
        password=args.get("password",None)
        if username is None:
            raise BusinnessValidationError(status_code=400,error_code="BE1001",error_message="username is required")
        if name is None:
            raise BusinnessValidationError(status_code=400,error_code="BE1002",error_message="name is required")
        
        user=db.session.query(USERS).filter((USERS.username==username)).first()
        if user:
            raise BusinnessValidationError(status_code=400,error_code="BE1003",error_message="Deuplicate")
        new_user=USERS(username=username,name=name,password=password)
        db.session.add(new_user)
        db.session.commit()
        return "",201

class VenueApi(Resource):
    @marshal_with(output_fields)
    def get(self,ID):
        # print("in userapi get method", username)
        venue=VENUES.query.filter(VENUES.ID==ID).first()
        if venue:
            return venue
        else:
            raise NotFoundError(status_code=404)
    @marshal_with(venue_fields)
    def put(self, ID):
        venue = VENUES.query.filter(VENUES.ID == ID).first()
        if venue is None:
            raise NotFoundError(status_code=404)
        args = venue_parse.parse_args()
        name = args.get("name", None)
        place=args.get("place")
        capacity=args.get("capacity")
        if name is None:
            raise NotFoundError(status_code=400)
        else:
            venue.name = name
            venue.place=place
            venue.capacity=capacity
            db.session.add(venue)
            db.session.commit()
            return venue

    def post(self):
        args=create_user_parser.parse_args()
        name=args.get("name",None)
        place=args.get("place")
        capacity=args.get("capcacity")
        if name is None:
            raise BusinnessValidationError(status_code=400,error_code="BE1002",error_message="name is required")
        new_venue=VENUES(name=name,place=place,capacity=capacity)
        db.session.add(new_venue)
        db.session.commit()
        return "",201
    def delete(self,ID):
        venue = VENUES.query.filter(VENUES.ID==ID).scalar()
        if venue is None:
            raise NotFoundError(status_code=404)
        shows=SHOWS.query.filter_by(VID=ID).all()
        for show in shows:
            db.session.query(USERS_SHOWS).filter_by(shows_id=show.ID).delete()
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
        return "", 200
