##### Setup
* -> got to vs code and create virtual enviromnet of python and then execute 
* -> python : create environment 

##### Conventions
* -> temlplate folder must have the  name as name  

##### RestFul Api 
* Request -> Api  -> Response .
* Communicate through HTTP,WEB and servers
* Methods-> GET POST PUT DELETE
* GET - > recieve resources
* POST - > add resources
* PUT - > update resources
* Delete - > delete resources

##### Boiler Code
```py
from flask import Flask , request ,jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

app =Flask(__name__)
api=Api(app)

@app.route('/')
def listenting () : 
    return {"message" : "hello world"}
         
if __name__ == "__main__":
    # for docker container expose the host 0.0.0.0
    app.run(debug=True, host="0.0.0.0") 
```

##### Packages
```py
# pip3 install $package-name
pip3 install flask-restful
```

##### Start Flask App
```js
export FLASK_APP=market.py
flask run
```

##### Download Requirements File
```js
pip3 install -r requirements.txt
```

##### Debugger Mode
```js
export FLASK_DEBUG=1
```

##### Git Commands
```js
git add . 
git commit -m "Message"
git push origin main
```

##### Python Docker containers
```py
# for docker container expose the host 0.0.0.0
if __name__ == "__main__":
    # for docker container expose the host 0.0.0.0
    app.run(debug=True, host="0.0.0.0") 
```

##### Connect With Mongo DB
```py
try : 
    client = MongoClient("mongodb://mongodb:27017")
    db=client.aNewDb
    users = db["Users"]
    print("Success Connections")
except : 
    print("Unable to Connect With Mongo Db")    
```







