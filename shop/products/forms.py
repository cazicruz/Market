from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired,FileSize
from .models import Brand, Category
from shop import photos

# brands = Brand.query.all()
# categories = Category.query.all()




#========= form class to get the product details from the user ==========
class AddProducts(FlaskForm):
    name = StringField('product name', validators=[DataRequired()], render_kw={"placeholder": "product name"})
    price = FloatField('price', validators=[DataRequired()],render_kw={"placeholder": "product price"})
    discount = IntegerField('Discount', default=0, render_kw={"placeholder": "discount on product"})
    stock = IntegerField('Stuck', validators=[DataRequired()],render_kw={"placeholder": "Stock"})
    description = TextAreaField('Description', validators=[DataRequired()],render_kw={"placeholder": "describe"})
    colors = TextAreaField('Color', validators=[DataRequired()],render_kw={"placeholder": "colors"})
    #========== select field =============
    brand = SelectField('Brand',  validators=[DataRequired()],render_kw={"placeholder": "Select brand"})
    category = SelectField('Category',  validators=[DataRequired()],render_kw={"placeholder": "Select category"})
#=============== form fields to collect product images ============
    image_1 = FileField('Image 1', validators=[ FileAllowed(['jpg, png']), FileSize(5*1024*1024)], render_kw={"placeholder": "Images only please"})
    image_2 = FileField('Image 2', validators=[FileAllowed(photos), FileSize(5*1024*1024)], render_kw={"placeholder": "Images only please"})
    image_3 = FileField('Image 3', validators=[ FileAllowed(photos), FileSize(5*1024*1024)], render_kw={"placeholder": "Images only please"})
    image_4 = FileField('Image 4', validators=[FileAllowed(photos), FileSize(5*1024*1024)],render_kw={"placeholder": "Images only please"})
    submit = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        super(AddProducts, self).__init__(*args, **kwargs)
        self.brand.choices = [(choice.id, choice.name) for choice in Brand.query.all()]
        # self.brand.choices=[('',"--Select brand--")] + self.brand.choices
        self.category.choices = [(choice.id, choice.name) for choice in Category.query.all()]