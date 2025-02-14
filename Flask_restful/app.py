from flask import Flask, request
from flask_restful import Api ,Resource

app=Flask(__name__)
api=Api(app)

@app.route('/')
def hello_world() : 
    return 'Hello world'


# function to check the arguments
def check_posted_Data(postedData , functionName) :
    if functionName == "add"  or functionName =="mul" or functionName=="sub":
        if "x" not in postedData or "y" not in postedData : 
            return 301
        else : 
            return 200
    
    
    if functionName =="divide" : 
        if "x" not in postedData or "y" not in postedData :
            return 301
        elif postedData["y"] == 0 :
            return 302
        else : 
            return 200
        

# creating resources
class Add(Resource)  :
    def post(self) : 
        # take value from the user
        userNum =  request.get_json()
        status_code=check_posted_Data(userNum,"add")
        if status_code !=200 : 
            return {"message"  :"invalid arguments"},301
        x=userNum["x"]
        y=userNum["y"]
        x=int(x)
        y=int(y)
        return {"result of this operation" : x+y},200
        
    def get(self) :
        pass
        
    def put(self) :
        pass
        
    def delete(self) : 
        pass
                 

class Subtract(Resource) :
    def post(self) : 
        # take value from the user
        userNum =  request.get_json()
        status_code=check_posted_Data(userNum,"sub")
        if status_code !=200 : 
            return {"message"  :"invalid arguments"},301
        x=userNum["x"]
        y=userNum["y"]
        x=int(x)
        y=int(y)
        return {"result of this operation" : x-y},200
    

class Multiply(Resource) : 
    def post(self) : 
        # take value from the user
        userNum =  request.get_json()
        status_code=check_posted_Data(userNum,"sub")
        if status_code !=200 : 
            return {"message"  :"invalid arguments"},301
        x=userNum["x"]
        y=userNum["y"]
        x=int(x)
        y=int(y)
        return {"result of this operation" : x*y},200


class Divide(Resource) : 
    def post(self) : 
        userArg = request.get_json()
        status_code = check_posted_Data(userArg,"divide")
        if status_code !=200 : 
            return {"message" : "invalid arguments"},status_code
        num1=userArg["x"]
        num2=userArg["y"]
        return {"result of opr is " : int(num1) / int(num2)},200
        
        
    
    


# bind the resources reqoeust with the endpoint
api.add_resource(Add,"/add")
api.add_resource(Divide,"/div")
api.add_resource(Multiply,"/mul")
api.add_resource(Subtract,"/sub")




if __name__ == "__main__":
    app.run(debug=True)