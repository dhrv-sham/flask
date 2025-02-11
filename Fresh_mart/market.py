from flask import Flask , render_template


app = Flask(__name__)


#  set the debug mode to true
app.config['DEBUG'] = True


# decorator to tell the app which URL should trigger our function
@app.route('/')
def hello_world() : 
    return '<h1>Server is  up  and running </h1>'


@app.route('/about')
def about_page() : 
    return '<h1> This is the about page </h1>'

# Using an f-string to include the user_name variable in the response
@app.route('/about/<user_name>')
def about_user(user_name) : 
    return f'<h1>Hello {user_name} welcome back !!</h1>'


# Using the render_template function to render the HTML file
#givng multiple routes to the same function
@app.route('/home')
@app.route('/index')
def home_page() : 
    return render_template('home.html')



# sending the data to the html file
@app.route('/market')
def market_page()  :
    return render_template('market.html' , item_name='Phone')


# if __name__ == '__main__' : 
#     app.run()