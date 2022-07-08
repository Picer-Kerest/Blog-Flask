import yaml
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL

app = Flask(__name__)


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def index():
    return render_template('about.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blogs/<int:blog_id>')
def blogs(blog_id):
    return render_template('blogs.html', blog_id=blog_id)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/write-blog/', methods=['GET', 'POST'])
def write_blog():
    return render_template('write-blog.html')

@app.route('/my-blogs/')
def my_blogs():
    return render_template('my-blogs.html')


@app.route('/edit-blog/', methods=['GET', 'POST'])
def edit_blog():
    return render_template('edit-blog.html')


@app.route('/delete-blog/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    return 'Success'



if __name__ == '__main__':
    app.run(debug=True)