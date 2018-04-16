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

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog')
def getBlogs():

    entry_id = request.args.get('id')

    if (entry_id):
        post = Blog.query.get(entry_id)
        return render_template('singleblog.html', post=post)

    else:
        posts = Blog.query.all()       
        return render_template('blog.html', posts=posts) 



@app.route('/newpost', methods=['POST','GET'])
def addBlog(): 
    
    title_error = ''
    text_error = ''

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
            new_entry = Blog(title, body)
            db.session.add(new_entry)
            db.session.commit()
            #posts = Blog.query.all()
            
            url = "/blog?id=" + str(new_entry.id)
            #return render_template('blog.html', title="Build a Blog", posts=posts)
            #return redirect('/blog')
            return redirect(url)
    else:
         return render_template('addnew.html')   
    

      
if __name__ == '__main__':
    app.run()