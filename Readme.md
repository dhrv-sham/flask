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







