import yaml
from flask import Flask, render_template, flash, session, request, redirect
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor

app = Flask(__name__)
Bootstrap(app)
CKEditor(app)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['SECRET_KEY'] = 'fa9b49f1c8f85c54f2fd7ff56dd7e003a4357a3ce6b7bec15bf7bf80'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    result_value = cursor.execute('SELECT * FROM blog')
    if result_value > 0:
        blogs = cursor.fetchall()
        cursor.close()
        return render_template('index.html', blogs=blogs)
    else:
        cursor.close()
    return render_template('index.html', blogs=None)

@app.route('/blogs/<int:blog_id>')
def blogs(blog_id):
    cursor = mysql.connection.cursor()
    result_value = cursor.execute('SELECT * FROM blog WHERE blog_id={};'.format(blog_id))
    if result_value > 0:
        blog = cursor.fetchone()
        cursor.close()
        return render_template('blogs.html', blog=blog)
    else:
        cursor.close()
        return 'Blog is not found.'

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_details = request.form
        if user_details['password1'] != user_details['password2']:
            flash('Password do not match. Try again.', 'danger')
            return render_template('register.html')
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO user(first_name, last_name, username, email, password) values (%s, %s, %s, %s, %s);',
                           (user_details['firstname'], user_details['lastname'], user_details['username'],
                            user_details['email'], generate_password_hash(user_details['password1'])))
            mysql.connection.commit()
            cursor.close()
            flash('Registration is successful. Please login', 'success')
            return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_details = request.form
        username = user_details['username']
        cursor = mysql.connection.cursor()
        result_value = cursor.execute('SELECT * FROM user WHERE username = %s;', ([username]))
        if result_value > 0:
            user = cursor.fetchone()
            if check_password_hash(user['password'], user_details['loginpassword']):
                session['login'] = True
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                flash('Welcome ' + session['first_name'] + '. You have been successfully logged in!', 'success')
            else:
                cursor.close()
                flash('Password is incorrect.', 'danger')
                return render_template('login.html')
        else:
            cursor.close()
            flash('User is not exists.', 'danger')
            return render_template('login.html')
        cursor.close()
        return redirect('/')
    return render_template('login.html')

@app.route('/write-blog/', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        blogpost = request.form
        title = blogpost['title']
        body = blogpost['body']
        author = session['first_name'] + ' ' + session['last_name']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO blog(title, author, body) VALUES (%s, %s, %s);', (title, author, body))
        mysql.connection.commit()
        cursor.close()
        flash('Your blog post is successfully posted', 'success')
        return redirect('/')
    return render_template('write-blog.html')

@app.route('/my-blogs/')
def my_blogs():
    author = session['first_name'] + ' ' + session['last_name']
    cursor = mysql.connection.cursor()
    result_value = cursor.execute('SELECT * FROM blog where author = %s;', ([author]))
    if result_value > 0:
        myblogs = cursor.fetchall()
        cursor.close()
        return render_template('my-blogs.html', myblogs=myblogs)
    else:
        cursor.close()
        return render_template('my-blogs.html', myblogs=None)

@app.route('/edit-blog/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        title = request.form['title']
        body = request.form['body']
        cursor.execute('UPDATE blog SET title=%s, body = %s WHERE blog_id=%s;', (title, body, blog_id))
        mysql.connection.commit()
        cursor.close()
        flash('Blog is updated successfully', 'success')
        return redirect('/blogs/{}'.format(blog_id))
    else:
        cursor = mysql.connection.cursor()
        result_value = cursor.execute('SELECT * FROM blog WHERE blog_id = {};'.format(blog_id))
        if result_value > 0:
            blog = cursor.fetchone()
            blog_form = {}
            blog_form['title'] = blog['title']
            blog_form['body'] = blog['body']
            return render_template('edit-blog.html', blog_form=blog_form)
        cursor.close()

@app.route('/delete-blog/<int:blog_id>')
def delete_blog(blog_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM blog WHERE blog_id={};'.format(blog_id))
    mysql.connection.commit()
    flash('Your blog has been deleted', 'success')
    return redirect('/my-blogs')

@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out!", "info")
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

