import os
from flask import Flask , request
from flask_restful import Api,Resource ,reqparse , abort , fields , marshal_with
from flask_sqlalchemy import SQLAlchemy , Model


app = Flask(__name__)

api = Api(app)

# configuring the database 
# create databse in the same directory as the main.py file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

# creating a db model in data base 
class videoModel(db.Model) : 
    # creating attributes for the model
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String(100),nullable = False)
    views=db.Column(db.Integer,nullable=False)
    likes=db.Column(db.Integer,nullable=False)
    
    # no need to create a constructor for the model already created by the db.Model
    # def __init__(self,name,views,likes) :
    #     self.name=name
    #     self.views=views
    #     self.likes=likes
    
    # repr method is used for string representation of the object
    def __repr__(self) : 
        return f"Video(name={self.name},views = {self.views}),likes = {self.likes}"

if not os.path.exists("database.db") : 
    print("Creating the database !!")
    db.create_all()    



names = {"dhruv" : {"age" : 45 , "gender" : "Male"},
         "dev" : {"age" : 4 , "gender" : "Female"}  } 



# requesting arguments from the user through api body as raw json 
# it is like a dictionary 
video_put_args =reqparse.RequestParser()

video_put_args.add_argument("name",type=str,help="Name of the video is requried",required=True)
video_put_args.add_argument("likes",type=int,help="Likes of the video is requried",required=True)
video_put_args.add_argument("views",type=int,help="Views of the video is requried",required=True)

videos = {}


# creating the args for custom updates every field here is not requried 
video_update_args = reqparse.RequestParser()

video_update_args.add_argument("name",type=str , help="Name of the video is required")
video_update_args.add_argument("likes" , type=int,help="Likes of the video is required")
video_update_args.add_argument("views",type=int,help="Views of the video is required")



def abort_if_video_id_exhist(video_id)  :
    if video_id in videos : 
        abort(409,message="Video id already exhist !!")


def abort_if_video_id_not_exhist(video_id) : 
    if video_id not in videos : 
        # no need to return message send the message when condition matches
        abort(404,message="Video id is not valid !!")
        # raise Exception("This Video id not exhsit !!")

# resource field  is used to serialize the data import fields and marshal_with
# keys should be same as the variable name in the model
resource_fields = {
    'id' : fields.Integer,
    'name' :fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer  
}





# stroing the video in the database
class Video_perm_db(Resource) : 
    
    # patch is used to update the data in the database
    @marshal_with(resource_fields)
    def patch(self,video_id) :
        args=video_update_args.parse_args()
        result = videoModel.query.filter_by(id=video_id).first()
        
        # video id is not exhist
        if not result : 
            abort(404,message="Video not found !!")
            
        
        # you can also write as if args["name"] : 
        if args["name"]  is not None : 
            result.name = args["name"]
            
        if args["views"] is not None :
            result.views = args["views"]
            
        if args["likes"] is not None:
            result.likes = args["likes"]
        
        # no need to do as it directly reflect ot the databse 
        # db.session.add(result)
        db.session.commit()  
        
        
        return result , 200           
            
            
            
    
    # marshal_WITH is used to serialize the data as this function the object but we neeed to convert into the json 
    @marshal_with(resource_fields)
    def get(self,video_id)  :
        try :
            # return the first query of the video model whose is same as the video id
            result = videoModel.query.filter_by(id=video_id).first()
            if not result : 
                abort(404,message="Video not found ")
            
            
        except : 
            abort(404,message="Video id is not valid !!")    
        # return instace of the video model need to convert the data
        return result 
    @marshal_with(resource_fields)
    def put(self,video_id) : 
        args = video_put_args.parse_args()
        # no need to this but as as extra
        result=videoModel.query.filter_by(id=video_id).first()
        
        if result : 
            abort(404,message="Video id already exhist !!")
        video = videoModel(id=video_id,name=args["name"],views=args["views"],likes=args["likes"])
        try :
            db.session.add(video)
            db.session.commit()
        except :
            abort(409,message="Video id already exhist !!") 


        return video , 201
    
                

# hardcoding the data in the local memory
class Video(Resource)  :
    # deleteing the  video
    def delete(self,video_id)  :
        abort_if_video_id_not_exhist(video_id)
        del videos[video_id]
        # return {"message" : "Video deleted successfully !!"},404
        
        

    # calling the video from the local memory
    def get (self,video_id) :
        res = {}
        # checking if the video id is valid or not
        abort_if_video_id_not_exhist(video_id)
        res=videos[video_id]
        return res , 200
    
        # or using try and except block
        # try :
        #     abort_if_video_id_not_exhist(video_id)
        #     res=videos[video_id] 
        # except : 
        #     return  {"message" : "Not able to find the movie "},404
        # else : 
        #     return res , 200
  
             
    # storing the video locally   
    def put(self,video_id) : 
        abort_if_video_id_exhist(video_id)
        #  request the arguments from the user 
        args=video_put_args.parse_args()
        # usually args are stored in the form of dictionary 
        videos[video_id] = args 
        # sending the status code after the request is completed 
        return {video_id : args} , 200

class server_listen(Resource) : 
    def get(self) : 
        return{"message" : "Server is running successfully !!"}

class data_api(Resource):
    # method overloading is not possible in python
    def get(self,name,age=None) : 
        if age is None : 
            return names[name]
        return {"name" : name , "age" : age} 
    
class HelloWorld(Resource):

    # post mehtod request 
    def post(self):
        return {"message" : "Data posted successfully !!"}
    
    # get method request 
    def get(self):
        # json serializable is must 
        return {"data":"hello"}
    


# creating end points 
api.add_resource(HelloWorld,"/helloworld")  
api.add_resource(server_listen,"/")

# cant be done as overwriting an existing endpint  
# api.add_resource(data_api,"/data")
# use endpoint to create multiple end points from the same class
api.add_resource(data_api,"/data/<string:name>/<int:age>", endpoint = "with_age")
api.add_resource(data_api, "/data/<string:name>", endpoint="fetched_local")
api.add_resource(Video,"/video/<int:video_id>")
api.add_resource(Video_perm_db,"/video_db/<int:video_id>")
 

if __name__ == "__main__":
    # run only when in developer mode not production 
    app.run(debug=True)