from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)


def get_db():  
    #to connect database with the website
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    #make connection between database and website  
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    #check if the query match with database
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    #home page- just the ID, Maker, Model and Image URL
    sql = """
            SELECT model.model_id,manufacturer.name,model.name, model.image_url FROM model
JOIN manufacturer 
ON model.manufacturer_id=manufacturer.manufacturer_id"""
    results = query_db(sql)
    return render_template("home.html", results=results)  

@app.route('/car/<int:id>')
def car(id):
    #just one car based on the id
    sql = """SELECT * FROM model
    JOIN manufacturer ON manufacturer.manufacturer_id=model.manufacturer_id
    WHERE model.model_id = ?;"""
    car = query_db(sql, (id,), True)
    return render_template("car.html", car = car)

@app.route('/manufacturer/<int:id>')
def manufacturer(id):
    #just each car match with each manufacturer
    sql = """SELECT * FROM model
    JOIN manufacturer ON model.manufacturer_id = manufacturer.manufacturer_id
    WHERE model.manufacturer_id= ?;"""
    cars = query_db(sql, (id,))
    print(cars)
    return render_template ("manufacturer.html", results = cars)


if __name__ == '__main__':
    #activate debug in the program
    app.run(debug=True)