
from flask import *
from datetime import timedelta
from models import *
from forms import *
import click
import os
import feedparser

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(12)



#---------- Route -------------
''' Page pricipale : affiche tout les flux '''
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        liste = []
        for news in News.select():
            feed = feedparser.parse(news.url)
            liste.append(feed)
        return render_template('home.html', listfeed=liste)

''' Page personnalisée : affiche uniquement les abonnements du user '''
@app.route('/my-news', methods=['GET', 'POST', ])
def my_news():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        dbsub = Subscription()
        dbnews = News()
        dbuser = Users()
        if request.method == 'POST':     
            dbsub.user = dbuser.get(email= session['user'])
            dbsub.news = dbnews.get(url = request.form['Feed'])
            dbsub.save()
            flash('Now you following this flow')
            return redirect(url_for('home'))
        else:
            liste = []
            '''mysubs = dbsub.get( user = dbuser.get(email = session['user']))'''
            for sub in dbsub.select():
                if sub.user.email == session['user']:
                    feed = feedparser.parse(sub.news.url)
                    liste.append(feed)
            return render_template('mynews.html', listfeed=liste)
    
''' Page de connexion '''    
@app.route('/login', methods=['POST'])
def do_admin_login():
    for user in Users.select():
        if request.form['password'] == user.password and request.form['username'] == user.email:
            session['logged_in'] = True
            session['user'] = user.email
            # Manage session timeout
            session.permanent = True
            current_app.permanent_session_lifetime = timedelta(minutes=60)
            session.modified = True 
            return redirect(url_for('home'))
    flash('wrong password!')
    return redirect(url_for('do_admin_login'))

''' Page d'inscription '''
@app.route('/SignUp', methods=['GET','POST', ])
def signup():
    user = Users()
    form = SignupForm()
    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()
        flash('Account created !')
        return home()
    return render_template('signup.html', form=form)

''' Page de déconnexion '''
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

''' Page d'administration : affiche les flux et permet d'ajouter un flux '''
@app.route('/administration', methods=['GET', 'POST', ])
def admin():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        liste = []
        for news in News.select():
            feed = feedparser.parse(news.url)
            liste.append(news)
        news = News()
        form = NewsForm()
        user = Users()
        if form.validate_on_submit():
            news.user = user.get(email= session['user'])
            form.populate_obj(news)
            news.save()
            flash('News created !')
            return redirect(url_for('admin'))
        return render_template('admin.html', form=form, listfeed=liste)


#---------- click -- Command -------------

@app.cli.command()
def initdb():
    """Create database"""
    create_tables()
    click.echo('Initialized the database')

@app.cli.command()
def dropdb():
    """Drop database tables"""
    drop_tables()
    click.echo('Dropped tables from database')

@app.cli.command()
def fakedata():
    from faker import Faker
    from slugify import slugify

    fake = Faker()

    for pk in range(0, 3):
        name = fake.company()
        Users.create(firstname = name,
                    lastname = name,
                    email = fake.email(),
                    password = fake.password())

                    
                      
           
    