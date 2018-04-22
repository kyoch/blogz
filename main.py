from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:myblogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "thisismysecretkey"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)        
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

        
@app.before_request
def require_login():
    allowed_routes = ['login', 'getBlogs', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in", 'error')
            return redirect('/newpost')

        if user and user.password != password:    
            flash("Incorrect Password", 'error')
            return redirect('/login')

        else:
            flash("This username does not exist", 'error')
            return redirect('/login')
          
    return render_template('login.html')



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data
        if username.strip() == "" or password.strip() == "" :
            flash("Please enter a username and/or password.", 'error') 
            return render_template('signup.html') 

        elif password != verify or verify.strip() == "":
            flash("Passwords do not match.", 'error')
            return render_template('signup.html')

        elif len(username) < 3 or len(password) < 3:
            flash("Username and Password must have at least 3 characters.", 'error')
            return render_template('signup.html', username=username)

           
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash("Username already exists", 'error')
        
    return render_template('signup.html')

    

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/blog')
def getBlogs():

    entry_id = request.args.get('id')
    user_id = request.args.get('user')  

    if entry_id:
        post = Blog.query.get(entry_id)
        return render_template('singleblog.html', post=post)

    if user_id:
        entries = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('blogbyuser.html', entries=entries)

    else:
        posts = Blog.query.all()       
        return render_template('blog.html', posts=posts) 




@app.route('/')       
def index():
    
    users = User.query.all()
    return render_template('index.html', title="Home", users=users)


        

@app.route('/newpost', methods=['POST','GET'])
def addBlog(): 
    
    title_error = ''
    text_error = ''
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']  
        
        if title.strip() == "":
            title_error = "Please enter your blog title."
            title = ''

        if body.strip() == "":
            text_error = "Please enter your blog content."       
            body = ''

        if (title == "") or (body == ""):
            return render_template('addnew.html', title=title, body=body, title_error=title_error, text_error=text_error)
        
        else:
            new_entry = Blog(title, body, owner)
            db.session.add(new_entry)
            db.session.commit()
            
            
            url = "/blog?id=" + str(new_entry.id)
            #return render_template('blog.html', title="Build a Blog", posts=posts)
            #return redirect('/blog')
            return redirect(url)
    else:
         return render_template('addnew.html')   
    

      
if __name__ == '__main__':
    app.run()