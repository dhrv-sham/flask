"""
This Api includes -:
Registration of a User
Each user gets 10 tokens
Store a sentence on our databse for 1 token 
Retreive his stored sentence for 1 token
"""
#Register
#Store
#Retrieve

from flask import Flask , jsonify , request
from flask_restful import Api, Resource
import bcrypt
import os

from pymongo import MongoClient

app=Flask(__name__)
api = Api(app)

try : 
    client = MongoClient("mongodb://mongodb:27017")
    db=client.aNewDb
    users = db["Users"]
    print("Success Connections")
except : 
    print("Unable to Connect With Mongo Db")    


class Register(Resource) :
    def post(self) :
        try : 
            # step 1 is to get the posted data by the user 
            postedData = request.get_json()
            # got the data 
            username = postedData["username"]
            password = postedData["password"]
        
            # store the username and pw into db 
            # hashing the password (neeed to encode the password)
            hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        
            # store data in mongo
            users.insert_one(
                {
                    "Username" : username,
                    "Password" : hashed_pw,
                    "Sentence" : "",
                     "Tokens" : 6
                }
            )
        
            retJson = {
                "status" : 200,
                "message" : "SuccessFully Created user"
            }
            return retJson
        
        except Exception as  e :
            return {
                "error" : e
            }
        

def verifyPw(username , password) : 
    hashed_pw=users.find({
        "Username" : username
    })[0]["Password"]
    
    if bcrypt.checkpw(password.encode('utf8'),hashed_pw) :
        return True 
    else : 
        return False    

def countTokens (username) : 
    tokens = users.find({
        "Username" : username
    })[0]["Tokens"]
    
    return tokens


class Store(Resource):
    def post(self) : 
        # step 1 : get the posted data
        postedData = request.get_json()
        # step 2 : read data from the request
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]
        
        # step 3 : verify username and password auth
        correct_pw = verifyPw(username,password)
        
        if not correct_pw : 
            retJson = {
                "status" : 302
                
            }
            return retJson
        
        
        # step 4 : verify user had enough tokens
        num_tokens = countTokens(username)
        
        if num_tokens <=0 : 
            retJson = {
                "status" : 301
            }
            return retJson
        
        #
             
        # step 5 : stores sentence and updates the user details
        # make use pay for service
        users.update_one({
            "Username" : username
        },{
            "$set":{
                "Sentence" : sentence,
                "Tokens" : num_tokens-1
            }
        })
        
        retJson = {
            "status" : 200,
            "message" : " Sentence Saved Successfully"
            
        }
        
        return retJson


class Get(Resource)  :
    def post(self) : 
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        
        correct_pw = verifyPw(username,password)
        
        if not correct_pw : 
            retJson = {
                "status" : 302
                
            }
            return retJson
        
        num_tokens = countTokens(username)
        
        if num_tokens <=0 : 
            retJson = {
                "status" : 301
            }
            return retJson
        
        # make user pay for services
        
        users.update_one({
            "Username" : username
        },{
            "$set":{
                "Tokens" : num_tokens-1
            }
        }) 
        
        sentence = users.find({
            "Username" : username
        })[0]["Sentence"]
        
        return {
            "status" : 200 , 
            "sentence" : sentence
            
        }
        
        
            
 
api.add_resource(Register , "/register")
api.add_resource(Store,"/store")   
api.add_resource(Get,"/get")     
        
@app.route('/')
def listenting () : 
    return {"message" : "hello world"}
         
if __name__ == "__main__":
    # for docker container expose the host 0.0.0.0
    app.run(debug=True, host="0.0.0.0") 