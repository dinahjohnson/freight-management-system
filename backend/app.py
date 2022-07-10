
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/load-manager'
db = SQLAlchemy(app)

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
    return f"Load: {self.id} {self.origin} {self.destination}"

  def __init__(self,id,ship_date,customer,origin,arrive_by_date,destination,carrier,status,delayed,rate) -> None:
    self.id = id
    self.ship_date = ship_date
    self.customer = customer
    self.origin = origin
    self.arrive_by_date = arrive_by_date
    self.destination = destination
    self.carrier = carrier
    self.status = status
    self.delayed = delayed
    self.rate = rate

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  user_type = db.Column(db.String(100),nullable=False)

  def __init__(self,id,name, user_type) -> None:
    self.id = id
    self.name = name
    self.user_type = user_type


def format_user(user):
  return {
    "id": user.id,
    "name": user.name,
    "user_type": user.user_type
  }

def format_load(load):
  return {
    "id": load.id,
    "origin": load.origin,
    "destination": load.destination,
    "status": load.status
  }
  
@app.route('/')
def hello():
  return "Hey"

@app.route("/users",methods=['POST'])
def create_user():
   user_id = request.json['id']
   name = request.json['name']
   user_type = request.json['user_type']
   user = User(user_id,name,user_type)
   db.session.add(user)
   db.session.commit()

   return format_user(user) 
  
@app.route("/loads",methods=['POST'])
def create_load():
    id = request.json['id']
    ship_date =request.json['ship_date']
    customer = request.json['customer']
    origin = request.json['origin']
    arrive_by_date = request.json['arrive_by_date']
    destination = request.json['destination']
    carrier = request.json['carrier']
    status = request.json['status']
    delayed = request.json['delayed']
    rate = request.json['rate']
    load = Load(id,ship_date,customer,origin,arrive_by_date,destination,carrier,status,delayed,rate)
    db.session.add(load)
    db.session.commit()

    return format_load(load)
# ran this to set up postgres user /usr/local/opt/postgres/bin/createuser -s postgres 

if __name__== '__main__':
  app.run()
