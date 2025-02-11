from flask import Flask , request
from flask_restful import Api,Resource ,reqparse

app = Flask(__name__)

api = Api(app)


names = {"dhruv" : {"age" : 45 , "gender" : "Male"},
         "dev" : {"age" : 4 , "gender" : "Female"}  } 



# requesting arguments from the user through api body as raw json 
video_put_args =reqparse.RequestParser()

video_put_args.add_argument("name",type=str,help="Name of the video is requried",required=True)
video_put_args.add_argument("likes",type=int,help="Likes of the video is requried",required=True)
video_put_args.add_argument("views",type=int,help="Views of the video is requried",required=True)

videos = {}


def abort_if_video_id_not_exhist(video_id) : 

    if video_id not in videos : 
        raise Exception("This Video id not exhsit !!")
        

class Video(Resource)  :

    # calling the video from the local memory
    def get (self,video_id) :

        
        res = {}
        try :
            abort_if_video_id_not_exhist(video_id)
            res=videos[video_id] 
        except : 
            return  {"message" : "Not able to find the movie "},404
        else : 
            return res , 200
  
             
    # storing the video locally   
    def put(self,video_id) : 

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
 

if __name__ == "__main__":
    # run only when in developer mode not production 
    app.run(debug=True)