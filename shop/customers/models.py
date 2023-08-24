from shop import db
from datetime import datetime
import json

class jsonEncodedDict(db.TypeDecorator):
    impl= db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return "{}"
        else:
            return json.dumps(value)
        
    def process_result_value(self,value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)
        


class CustomerOrders(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    transaction_id = db.Column(db.String(20), default=0,)
    status= db.Column(db.String(20),  default="pending", nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(jsonEncodedDict)

    def __repr__(self):
        return'<CustomerOrders %r>' %self.invoice 
