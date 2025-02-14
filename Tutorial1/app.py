# importing flask
from flask import Flask , jsonify , request
# name of the file convention as __name__
app = Flask(__name__)




# 127.0.0.1:5000/
@app.route('/')
def hello_world() : 
    return {"message" : "hello world"}

"""

Status code : 
Response -> response code 
200 : success
404 : Not found
500 : internal server error


HTTP Methods :
Request - > (Get) : demands  a specific resource in response 
        - > (Post) : send data to server and expect response 
                Post message have a body
        ->Delete
        ->Update         
"""


""" About json can send String , int ,null or boolean
{
    key:value,
    key : {
        "age": 3,
        "name" : "dhruv",
        "boolean" : 1,
        "array" : [1,2,3,4,5,"annuj"],
        "array of object " : [
            {
                "field1" : 1
            },
            {
                "field2":2            
            }
        ],
        "array of nested object" : [
            "nested array" : [
                {
                    "field 1" : 1,
                    "name" : "dhruv"
                }
            ],
            "nested object" : {
                "field 2" : 2,
                "name" : "annuj"
            }
        ]
    }
}
"""

@app.route('/hi')
def greeting() :
    retjson = {
        "greeting" : "Good Evening",
        "message" : "Hi there"  
    } 
    return retjson


@app.route('/name')
def name() : 
    profile = {
        "name"  : "Dhruv" , 
        "Age" : 20,
        "phones"  : [
            {
                "phone_name" : "Oneplus",
                "version" : 8
            
            },
            {
                "phone_name" : "Iphone",
                "version" : 12
            }
        ]
    }
    
    return  jsonify(profile)


@app.route('/add' , methods=["POST"])
def add() : 
    # get x and y from the posted data
    # add x and y
    # prepare json of result 
    # return json
    
    # request data from body of request 
    try : 
        dataDict = request.get_json()
        num1 = dataDict["x"]
        num2 =dataDict["y"]
        return {"solution" : num1+num2},200
    except  :
        return {"message" : "number not found "},404
        
        
    

    

# all communicatino between server and server are done by text trhough TCP proctocol 
# json handles by webservices and frontend render by webapplication
# server recieve a request and returns the response 
# Get Post Del Put ar https methods/request
if __name__ == "__main__" : 
    app.run(debug=True)