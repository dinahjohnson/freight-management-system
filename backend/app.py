
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask app 
app = Flask(__name__,template_folder='../templates')

# Configure db connection 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/load-manager'

# Create db object using SQLA class passing the app instance to connect the Flask app with SQLA
db = SQLAlchemy(app) # use db to interact with database

# Declaring a table
# pass db.Model to inherit from base class 
# TODO Add docstrings to Load class
class Load(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ship_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  customer = db.Column(db.Integer, nullable=False)
  origin = db.Column(db.String(100), nullable=False)
  arrive_by_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  destination = db.Column(db.String(100), nullable=False)
  carrier = db.Column(db.Integer, nullable=False)
  status = db.Column(db.String(100), nullable=False)
  delayed = db.Column(db.Boolean, nullable=False)
  rate = db.Column(db.Float,nullable=False)

  def __repr__(self) -> str:
    return f"Load: {self.id}"

  def __init__(self,ship_date,customer,origin,arrive_by_date,destination,carrier,status,delayed,rate) -> None:
    self.ship_date = ship_date
    self.customer = customer
    self.origin = origin
    self.arrive_by_date = arrive_by_date
    self.destination = destination
    self.carrier = carrier
    self.status = status
    self.delayed = delayed
    self.rate = rate

# TODO Add docstrings to User class
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True,nullable=False)
  user_type = db.Column(db.String(100),nullable=False)

  def __repr__(self) -> str:
    return f'<User {self.id}>'

  def __init__(self,name, email,user_type) -> None:
    self.name = name
    self.email = email
    self.user_type = user_type


# TODO Add annotations to format_load
def format_load(load):
  return {
    "id": load.id,
    "ship_date": load.ship_date,
    "customer": load.customer,
    "origin": load.origin,
    "arrive_by_date": load.arrive_by_date,
    "destination": load.destination,
    "carrier":load.carrier,
    "status": load.status,
    "delayed": load.delayed,
    "rate": load.rate
  }

# TODO Add annotations to format_user
def format_user(user):
  return {
    "id": user.id,
    "name": user.name,
    "email": user.email,
    "user_type": user.user_type
  }


# TODO Add annotations to index
# Create index() view function to query db for all loads and pass to index.html template
@app.route('/')
def index():
  loads = Load.query.filter_by(status='Available').order_by(Load.ship_date.asc()).all()
  return render_template('index.html', loads=loads)

# TODO Add annotations to create_user
@app.route("/users",methods=['POST'])
def create_user():
   name = request.json['name']
   email = request.json['email']
   user_type = request.json['user_type']
   user = User(name, email,user_type)
   db.session.add(user)
   db.session.commit()

   return format_user(user) 

@app.route("/users/<id>",methods=['GET'])
def get_user(id):
  user = User.query.filter_by(id=id).one()
  user = format_user(user)
  return {
    "user": user
  }

# TODO Add annotations to get_users
@app.route("/users",methods=['GET'])
def get_users():
  users = User.query.order_by(User.id.asc()).all()
  users_list = []
  for user in users:
    users_list.append(format_user(user))
  return {
    "users": users_list
  }

# TODO Add annotations to get_user


@app.route("/users/<id>", methods=['PUT'])
def update_user(id):
  user = User.query.filter_by(id=id)
  name = request.json['name']
  email = request.json['email']
  user.update(dict(name=name, email=email))
  db.session.commit()

  return { "user": format_user(user.one()) }

@app.route("/users/<id>",methods=['DELETE'])
def delete_user(id):
  user = User.query.filter_by(id=id).one()
  db.session.delete(user)
  db.session.commit()
  return f"User {id} deleted"

# Load Routes
@app.route("/loads",methods=['POST'])
def create_load():
    ship_date =request.json['ship_date']
    customer = request.json['customer']
    origin = request.json['origin']
    arrive_by_date = request.json['arrive_by_date']
    destination = request.json['destination']
    carrier = request.json['carrier']
    status = request.json['status']
    delayed = request.json['delayed']
    rate = request.json['rate']
    load = Load(ship_date,customer,origin,arrive_by_date,destination,carrier,status,delayed,rate)
    db.session.add(load)
    db.session.commit()

    return format_load(load)

@app.route("/loads",methods=['GET'])
def get_loads():
  loads = Load.query.order_by(Load.id.asc()).all()
  loads_list = []
  for load in loads:
    loads_list.append(format_load(load))
  return {
    "loads": loads_list
  }

@app.route("/loads/<id>",methods=['GET'])
def get_load(id):
  load = Load.query.filter_by(id=id).one()
  load = format_load(load)
  return {
    "load": load
  }

@app.route("/loads/<id>", methods=['PUT'])
def update_load(id):
  load = Load.query.filter_by(id=id)
  ship_date =request.json['ship_date']
  customer = request.json['customer']
  origin = request.json['origin']
  arrive_by_date = request.json['arrive_by_date']
  destination = request.json['destination']
  carrier = request.json['carrier']
  status = request.json['status']
  delayed = request.json['delayed']
  rate = request.json['rate']
  load.update(dict(ship_date=ship_date,customer=customer,origin=origin,
  arrive_by_date=arrive_by_date, destination=destination,carrier=carrier,
  status=status,delayed=delayed,rate=rate))
  db.session.commit()

  return { "user": format_load(load.one()) }


@app.route("/loads/<id>",methods=['DELETE'])
def delete_load(id):
  load = Load.query.filter_by(id=id).one()
  db.session.delete(load)
  db.session.commit()
  return f"Load {id} deleted"

# ran this to set up postgres user /usr/local/opt/postgres/bin/createuser -s postgres 
# update
if __name__== '__main__':
  app.run()
