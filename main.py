from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:myblogpage@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(2000))

    def __init__(self, title):
        self.title = title
        self.body = body


@app.route('/', methods=['POST','GET'])
def index():

    title = request.form['title']
    body = request.form['body']
    title_error = ''
    text_error = ''

    if request.method == 'POST':
        title = request.form['title']
        new_title = Blog(title)
        db.session.add(new_title)
        db.session.commit()

    if request.method == 'POST':
        text = request.form['body']
        new_text = Blog(text)
        db.session.add(new_text)
        db.session.commit()

    if len(title) == 0:
        title_error = "Please enter your blog title."

    if len(body) == 0:
        text_error = "Please enter your blog content."
    

    posts = Blog.query.all()

    if len(title_error) == 0 and len(text_error) == 0:     
        return render_template('index.html', title="Build a Blog", posts=posts)

    else:
        return render_template('addnew.html', title_error=title_error, text_error=text_error) 

    


        
if __name__ == '__main__':
    app.run()