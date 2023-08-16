from shop import db
from datetime import datetime


class Products(db.Model):
    __searchable__ = ['product_name', 'colors', 'description']

    id = db.Column(db.Integer, primary_key=True)
    
    product_name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Numeric(10,2), unique=False, nullable=False)
    discount = db.Column(db.Integer, unique=False, nullable=True, default=0)
    stock = db.Column(db.Integer, unique=False, nullable=False)
    colors = db.Column(db.Text, unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_1 = db.Column(db.String(180), nullable=False, default='product.jpg')
    image_2 = db.Column(db.String(180), nullable=False, default='product.jpg')
    image_3 = db.Column(db.String(180), nullable=False, default='product.jpg')
    image_4 = db.Column(db.String(180), nullable=False, default='product.jpg')
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('brands', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('posts', lazy=True))



    def __repr__(self):
        return '<Products %r>' % self.username


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),nullable=False, unique=True)

    def __repr__(self):
        return '<Brand %r>' % self.name

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),nullable=False, unique=True)

    def __repr__(self):
        return '<Category %r>' % self.name


