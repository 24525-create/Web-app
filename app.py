from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)


def get_db():  
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# #Initialize the database and sample data
# def init_db():
#     conn = get_db_connection()
#     conn.execute(''' CREATE TABLE IF NOT EXISTS cars(
#                  id INTEGER PRIMARY KEY,
#                  maker TEXT,
#                  model TEXT'
#                  YEAR INTEGER,
#                  cost INTEGER
#                  ))))

#      #Add sample Japanese cars
#     conn.execute("Delete from cars")
#     sample_cars = [
#         ('Toyota', 'Camry', 2020, 24000),
#         ('Honda', 'Civic', 2019, 20000),
#         ('Nissan', 'Altima', 2021, 25000),
#         ('Mazda', '3', 2020, 22000),
#         ('Subaru', 'Impreza', 2018, 21000)
#     ]
#     conn.executemany('INSERT INTO cars (maker, model, year, cost) VALUES (?, ?, ?, ?)', sample_cars)
#     conn.commit()
#     conn.close()
                 

#Home page with search
# @app.route('/')
# def home():
#     research = request.args.get('research')
#     conn = get_db_connection()
#     if research:
#         cars = conn.execute('SELECT * FROM cars WHERE maker LIKE ? OR model LIKE ?', ('%' + research + '%', '%' + research + '%')).fetchall()
#     else:
#         cars = conn.execute('SELECT * FROM cars').fetchall()
#     conn.close()
#     return render_template('home.html', cars=cars)

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
    #just one bike based on the id
    sql = """SELECT * FROM model
    JOIN manufacturer ON manufacturer.manufacturer_id=model.manufacturer_id
    WHERE model.model_id = ?;"""
    car = query_db(sql, (id,), True)
    return render_template("car.html", car = car)

@app.route('/manufacturer/<int:id>')
def manufacturer(id):
    sql = """SELECT * FROM model
    JOIN manufacturer ON manufacturer.manufacturer_id=model.manufacturer_id
    WHERE model.model_id = ?;"""
    manufacturer = query_db(sql, (id,),True)
    return render_template ("manufacuturer.html", manufacturer = manufacturer)


if __name__ == '__main__':
    app.run(debug=True)