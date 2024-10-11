from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse,fields,marshal_with,abort

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api =Api(app)



#step 1 model the database
#remember to create the db file by running create_db.py
class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    name= db.Column(db.String(80),unique =True, nullable=False)
    email= db.Column(db.String(80),unique =True, nullable=False)

    def __repr__(self):
        return f'User(name = {self.name}, email ={self.email})'

#step 2 validate the url inputs using requestparser
user_args= reqparse.RequestParser()
user_args.add_argument('name',type=str, required=True, help="name connot be blank")
user_args.add_argument('email',type=str, required=True, help="email connot be blank")

#step 5: Gives a structure to return data in json format
userFields ={
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String
}
#step 3: set up fist end point
class Users(Resource):   
    @marshal_with(userFields) #step 6: use marshall_with decorator to send back in a serialized manner
    def get(self):
        users = UserModel.query.all()
        return users
    
    #function to post data to db
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name =args['name'], email= args['email'])
        db.session.add(user)
        db.session.commit()
        users =UserModel.query.all()
        return users, 201
   
class User(Resource):
    @marshal_with(userFields)
     #function to fetch specified user from db
    def get(self, id):
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,"User not found" )
        return user
     #function to update user from db
    
    @marshal_with(userFields)
    def patch(self, id): 
        args = user_args.parse_args()
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,"User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user
     #function to delete user from db
    @marshal_with(userFields)
    def delete(self, id): 
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return 204

        
# step 4 api library resource comes here  
api.add_resource(Users,'/api/users')
api.add_resource(User,'/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__=='__main__':
    app.run(debug=True)