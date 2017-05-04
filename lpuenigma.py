import os
import sqlite3
from collectionfunction import collectionfunction
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'lpuFinal.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    print ('Hello World')
    return render_template ('index.html')
    # try:
    #     db = get_db()
    #     entries = db.execute('select * from entries').fetchall()
    #     return render_template('index.html', entries = entries)
    # except sqlite3.Error as e:
    #     error = "No se pudo completar la consulta: "+e.args[0]
    #     print error
    #     return render_template('index.html', error = error)
    #

@app.route('/list')
def list():
    try:
        db = get_db()
        entries = db.execute('select * from devices').fetchall()
        return render_template('list.html', entries = entries)
    except sqlite3.Error as e:
        error = "Could not complete query: "+e.args[0]
        return render_template('list.html', error = error)


@app.route('/dashboard')
def dashboard():
    try:
        db = get_db()
        entries = db.execute('select device, category, FoC, lpu, capexLPU from interfaces').fetchall()
        return render_template('dashboard.html', entries = entries)
    except sqlite3.Error as e:
        error = "Could not complete query: "+e.args[0]
        return render_template('dashboard.html', error = error)


@app.route('/adddevice', methods=['GET','POST'])
def adddevice():
    if request.method =='GET':
        return render_template('adddevice.html')
        #print 'GET'
    elif request.method == 'POST':
        try:
            db = get_db()
            vals = [request.form['device'], request.form['ipAddress'],request.form['site']]
            ipAddress = str(vals[1])
            print (ipAddress)
            db.execute('insert into devices (device, ipAddress, site) values (?,?,?)',vals)
            db.commit()
            lista_out_int = []
            lista_out = []
            lista_out_int = collectionfunction(ipAddress)
            print (lista_out_int)
        except sqlite3.Error as e:
            error = "Could not create the service: "+e.args[0]
            return render_template('adddevice.html', error = error)
        #print 'POST'

    return render_template('adddevice.html')


if __name__ == '__main__':
    app.run(debug=True)
