# similarity of text api compare two texts which tells the similarity
# register a user -> /register
# detect similarity of two docs -> /detect
# refill token -> /refill

from  flask import Flask, jsonify , request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import  spacy

app = Flask(__name__)
api =Api(app)

try : 
    client = MongoClient("mongodb://mongodb:27017")
    db=client.Similar
    users = db["Users"]
    print("Success Connections")
except : 
    print("Unable to Connect With Mongo Db")   
    
    
def userExhist(username) : 
    if users.find({"Username" : username}).count() == 0 : 
        return False
    
    return True    
   
def verfiyPw(username , password) : 
    hashed_pw=users.find({
        "Username" : username
    })[0]["Password"]
    
    if bcrypt.checkpw(password.encode('utf8'),hashed_pw) :
        return True 
    else : 
        return False    
  
def count_Token(username) : 
    tokens = users.find({
        "Username" : username
    })[0]["Tokens"]
    
    return tokens
        
class Register(Resource) : 
    def post(self)  :
        postedData = request.get_json()
        username = postedData["username"] 
        password = postedData["password"]
        
        if(userExhist(username)) : 
            retJson = {
                "status": 301,
                "msg" : "Invalid Username"
            }   
            
        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        
        users.insert_one({
            "Username" : username,
            "Password" : hashed_pw,
            "Tokens" : 6
        })    
        
        retJson = {
            "status" : 200,
            "msg" : "You Have A successfully sign up"
        }
        
        
        return retJson

class Detect(Resource) : 
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]
        
        if not userExhist(username) :
            retJson = {
                "status" : 301,
                "msg" : "Invalid Username"
            }
            return retJson
        
        correct_pw = verfiyPw(username,password)
        
        if not correct_pw : 
            retJson = {
                "status" : 302,
                "msg" : "Invalid Password"
            }
            return retJson
        
        num_tokens = count_Token(username)
        
        if num_tokens <=0 :
            retJson = {
                "status" : 303,
                "msg" : "You are out of tokens , please refill"
            }
            return num_tokens
        
        # comaprision
        nlp = spacy.load('spacy-models-en_core_web_sm')
        text1 = nlp(text1)
        text2 = nlp(text2)
        
        ratio = text1.similarity(text2)
        
        retJson = {
            "status" : 200 ,
            "similarity" : ratio,
            "msg" : "Similartiy Calculateed Sucessfully"
        }
        
        # deduction of tokens
        users.update_one({
            "Username" : username
        },{
            "$set" : {
                "Tokens" : num_tokens-1
            }
        })
        
        return retJson
        
class Refill(Resource) : 
    def post(self) : 
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amt = postedData["refill"]
        
        if not userExhist(username) :
            retJson = {
                "status" : 301,
                "msg" : "Invalid Username"
            }
            return retJson
        
        correct_pw = "abc123"
        
        if not password == correct_pw : 
            retJson = {
                "status" : 304,
                "msg" : "Invlaid Admin Password"
            }
        
        
        current_Tokens = count_Token(username)
        users.update_one({
            "Username" : username
        },{
            "$set":{
                "Tokens" : current_Tokens + refill_amt
            }
        })    
        
        retJson = {
            "status" : 200,
            "msg" : "Refilled successffully"
        }
        
        return retJson
    
    
 
api.add_resource(Register,'/register') 
api.add_resource(Detect , '/detect')
api.add_resource(Refill , '/refill')
  
               
        
        
if __name__ == "__main__":
    # for docker container expose the host 0.0.0.0
    app.run(debug=True, host="0.0.0.0")              
