from flask import Flask
import os
from  flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_migrate import Migrate
from flask_msearch import Search
from flask_mail import Mail

#from flask_uploads import UploadSet, IMAGES, configure_uploads




app = Flask(__name__)
app.config['SECRET_KEY'] = "hardtoguessstring"
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']= \
 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['UPLOAD_PROFILE_PHOTOS']= 'static/uploads/profile'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/uploads/images')
app.config['FLASKY_ADMIN']= 'davidonwuli8@gmail.com'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
#================ setting the max size of files to 16MB =================
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
#==============flask mail config=============
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'casmird70@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'rrtgcnljlnqnadkv'
app.config['MARKET_MAIL_SUBJECT_PREFIX'] = '[Market]'
app.config['MARKET_MAIL_SENDER'] = 'casmird70@gmail.com'
# app.config['MAIL_DEFAULT_SENDER '] = 'casmird70@gmail.com'


# profile_photo = UploadSet('photos', IMAGES)
# products_photo = UploadSet('products', IMAGES)
# configure_uploads(app, profile_photo)
# configure_uploads(app, products_photo)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app,db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
search = Search()
search.init_app(app)
mail = Mail(app)


from shop.admin_shop import routes
from shop.products import routes
from shop.carts import routes
from shop.customers import routes
