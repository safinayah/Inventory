# from flask import Flask, Blueprint
#
# from .extensions import *
# from .views import *
#
#
# def create_app(config_file='settings.py'):
#     app = Flask(__name__)
#
#     app.config.from_pyfile(config_file)
#
#     db.init_app(app)
#
#     app.register_blueprint(main)
#
#     return app


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://inventory:inventory@localhost/inventory'
app.secret_key = "Secret Key"

db = SQLAlchemy(app)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://inventory:inventory@localhost/inventory'
app.secret_key = "Secret Key"

db = SQLAlchemy(app)


class Product(db.Model):
    product_id = db.Column(db.String(100), primary_key=True)

    def __init__(self, product_id):
        self.product_id = product_id


class Location(db.Model):
    location_id = db.Column(db.String(120), primary_key=True)

    def __init__(self, location_id):
        self.location_id = location_id


class Product_Movement(db.Model):
    movement_id = db.Column(db.String(120), primary_key=True)
    timestamp = db.Column(db.TIME)
    from_location = db.Column(db.String(120), db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String(120), db.ForeignKey('location.location_id'))
    product_id = db.Column(db.String(120), db.ForeignKey('product.product_id'))
    qty = db.Column(db.INTEGER)

    def __init__(self, movement_id, timestamp, from_location, to_location, product_id, qty):
        self.movement_id = movement_id
        self.timestamp = timestamp
        self.from_location = from_location
        self.to_location = to_location
        self.product_id = product_id
        self.qty = qty


@app.route("/")
def index():
    product_data = Product.query.all()
    location_data = Location.query.all()
    product_movements = Product_Movement.query.all()

    return render_template("index.html", products=product_data, locations=location_data, movements=product_movements)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_data = Product(product_id)
        db.session.add(product_data)
        db.session.commit()

        flash("product Inserted Successfully")

        return redirect(url_for('index'))


# this route is for inserting data to mysql database via html forms
@app.route('/insertlocaton', methods=['POST'])
def insert_location():
    if request.method == 'POST':
        location_id = request.form['location_id']

        movement_id = request.form['movement_id']
        timestamp = request.form['timestamp']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product_id = request.form['product_id']
        qty = request.form['qty']
        movement_data = Location(movement_id, timestamp,from_location,to_location,product_id,qty)
        db.session.add(movement_data)
        db.session.commit()
        flash("Movement Inserted Successfully")

        return redirect(url_for('index'))

# this route is for inserting data to mysql database via html forms
@app.route('/insertmovement', methods=['POST'])
def insert_movement():
    if request.method == 'POST':
        location_id = request.form['location_id']
        location_data = Location(location_id)
        db.session.add(location_data)
        db.session.commit()
        flash("Location Inserted Successfully")

        return redirect(url_for('index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        # TODO check product_data since it cause an error
        product_data = Product.query.get(request.form.get('product_id'))

        product_data.product_id = request.form['product_id']
        db.session.commit()
        flash("Product Updated Successfully")
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
