import flask
import os
import sqlite3

app = flask.Flask(__name__)

'''The database consist of 2 tables: LOCATIONS and EMAIL_LIST
DATABASE STRUTURE
    EMAIL_LIST:
        EMAIL | MAJOR
    LOCATIONS: 
        MAJOR | CITY | AVERAGE_SALARY | SALARY_RANGE | IN_THE_USA
'''

#sqlite3 database connection
database_path = './FS_Database.db'
def get_db():
    db = getattr(flask, '_database', None)
    if db is None:
        db = flask._database = sqlite3.connect(database_path)
    return db

#fetches data from the database based on the major the user selected and whether or not they are in the US
def query_db(major, in_USA):
    if in_USA.lower() == "yes":
        db = get_db().execute("SELECT * FROM LOCATION WHERE MAJOR='"+major+"' AND IN_THE_USA='"+in_USA.lower()+"';")
    else:
        db = get_db().execute("SELECT * FROM LOCATION WHERE MAJOR='"+major+"' AND IN_THE_USA='"+in_USA.lower()+"';")
    db_data = db.fetchall()
    db.close()
    return db_data #returns a list that contains a list

#insert an email into the database
def insert_db(email, major):
    db = get_db().execute("INSERT INTO EMAIL_LIST (EMAIL, MAJOR) VALUES ('"+email+"', '"+major+"');")   
    get_db().commit() #save changes
    db.close()

@app.route('/', methods=['GET','POST'])
def index():
    if flask.request.method == 'GET':
        #print(query_db("Cyber Security","yes"))
        return flask.render_template("index.html")
    elif flask.request.method == "POST": #user submits from the index page
        #parse the answers the user submited
        major = flask.request.json.get('Major')
        in_the_US = flask.request.json.get('Location')
        #use them to fetch data from the database
        database_data = query_db(major,in_the_US)
        #create the body for the response
        response_body = []
        for i in range(len(database_data)):
            json_data = {
                'major' : database_data[i][0],
                'city' : database_data[i][1],
                'average_salary' : database_data[i][2],
                'salary_range' : database_data[i][3]
            }
            #each database record we retrieve is added to the response body
            response_body.append(json_data)
        #flask will print an error if you jsonify your response
        response = flask.jsonify(response_body)
        return response
    else:
        return flask.render_template("Error.html")

@app.route('/NOTA', methods=['GET','POST'])
def NOTA():
    if flask.request.method == 'GET':
        return flask.render_template("NOTA-Email-Submit.html")
    elif flask.request.method == "POST": #user submits to NOTA page
        #parses the user email and major
        email = flask.request.form['Email']
        major = flask.request.form['Major']
        #adds them to the database
        insert_db(email,major)
        #sends back the thanks.html
        return flask.render_template("thanks.html")
    else:
        return flask.render_template("Error.html")

app.run(
    port = int(os.getenv('PORT',8080)),
    host = os.getenv('IP', '0.0.0.0'),
    debug = True)

#closes the database once the application is terminated
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask,'_database', None)
    if db is not None:
        db.close()