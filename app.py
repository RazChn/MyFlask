from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import articles_export
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)

#config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'myflask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MySql

mysql = MySQL(app)

Articles = articles_export()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.data_required(),
        validators.equal_to('confirm',message='Passwords Do NOT Match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods= ['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit
        mysql.connection.commit()

        #Close Connection
        cur.close()

        flash('YOU ARE REGISTERED !', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'sercret'
    app.run(debug=True)


