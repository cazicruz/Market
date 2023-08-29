import os
from flask import render_template, session, request, redirect, url_for, flash,abort
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user, LoginManager, logout_user
from shop import app, db, bcrypt
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from .forms import LoginForm, SignUpForm
from .models import Users, Permission
from .decorators import admin_required, permission_required
from shop.products.models import Products, Brand, Category
from .mail_sender import send_email, send_otp_mail
import secrets

@app.shell_context_processor
def make_shell_context():
 return dict(db=db, Users=Users)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(int(user_id))
    return user    


#================= home view================
@app.route('/', endpoint='home')
def home():
    products = Products.query.all()
    brands = Brand.query.join(Products, (Brand.id == Products.brand_id)).all()
    return render_template('index.html',brands=brands,products=products, current_time=datetime.utcnow(), endpoint=request.endpoint)

#==============admin product route========
@app.route('/admin', methods=['GET', 'POST'], endpoint='admin')
@login_required
@admin_required
def admin():
    endpoint = request.endpoint
    products = Products.query.all()
    return render_template('admin_temp/products.html', endpoint=endpoint,products=products,current_time=datetime.utcnow())


#========= brands view ========
@app.route('/brands', methods=['GET','POST','PUT','DELETE'])
@login_required
@admin_required
def brands():
   brands = Brand.query.order_by(Brand.id.desc())
   return render_template('admin_temp/brands.html', brands=brands, current_time=datetime.utcnow())

#========= category view ========
@app.route('/categories', methods=['GET','POST','PUT','DELETE'])
@login_required
@admin_required
def categories():
   categories = Category.query.order_by(Category.id.desc())
   return render_template('admin_temp/brands.html', categories=categories, current_time=datetime.utcnow())

#================ sign-up view=================
@app.route('/sign-up', methods=['GET', 'POST'], endpoint='signUp')
def signUp():
    form = SignUpForm()
    try:
        if form.validate_on_submit():
            hash_password = bcrypt.generate_password_hash(form.password1.data)

            img = request.files['profile_img']
            if img:
                filename = secure_filename(img.filename)
                path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
                if os.path.exists(path):
                    flash('Image already exists')
                    ''' remember to add a random string to the filename to avoid overwriting existing files
                    or add current_user to the filename to avoid overwriting existing files'''
                if img:
                    img.save(path)
                user = Users(fname=request.form.get('fname'), lname=form.lname.data, username=form.username.data, email=form.email.data, password=hash_password,profile_img=path)
                db.session.add(user)
                db.session.commit()
                flash('Welcome, thank you for registering.', 'success')
                return redirect(url_for('home'))
            else:
                user = Users(fname=request.form.get('fname'), lname=form.lname.data, username=form.username.data, email=form.email.data, password=hash_password)
                db.session.add(user)
                db.session.commit()
                flash('Welcome, thank you for registering.', 'success')
                return redirect(url_for('home'))
    except Exception as e:
       flash(f'error occured while signing you up{e}','danger')
           
    return render_template("admin_temp/register.html", form=form,current_time=datetime.utcnow(), endpoint=request.endpoint)

# ===========login view============
@app.route('/login', methods=['GET', 'POST'], endpoint='login' )
def login():

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('user logged in successfully', 'success')
#=============== if user was redirected by protected route =================
#=============== access that route after a successful auth =================
            next_route = request.args.get('next')
            if next_route:
               return redirect(next_route) 
            #====== else go to home route =========           
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin_temp/login.html',form=form, current_time=datetime.utcnow(), endpoint=request.endpoint)



# =========================logout view======================= 
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
   logout_user()
   flash('user logged out successfully', 'success')
   return redirect(url_for('login'))
   

#++++++++++++++++++++++++++++++++++++++++++++++++++++forgot password route++++++++++++++++++++
@app.route('/forgotpassword', methods=['POST','GET'])
def forgot_pass():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        try:
            user = Users.query.filter_by(email=email, username=username).first()
            if user:
                print(user)
                otp = secrets.token_hex(5)
                session['otp'] = {'otp':otp, 
                                'date_created':datetime.utcnow(),
                                'user_id':user.id
                                }
                send_email(user.email, 'Password Reset Request', 'admin_temp/otp_mail', user=user.username, otp=otp, admin=app.config['MARKET_MAIL_SENDER'])
                flash(f'An OTP has been sent to your email address', 'success')
                return redirect(url_for('reset_pass'))
        except Exception as e:
           print(e)
           flash(f'An unexpected error occurred', 'danger')
    return render_template('admin_temp/forgotpassword.html')


#+++++++++++++++++++++resend otp route+++++++++++++++++++++++++++++++
@app.route('/resendotp', methods=['POST'])
def resend_otp():
    try:
        if request.method == 'POST':
            user = Users.query.filter_by(id=session['otp']['user_id']).first()
            send_otp_mail(session['otp']['user_id'],user.email,user=user.username)
            flash(f'A new OTP has been sent to your email address', 'success')
        else:
            flash(f'invalid request ', 'danger') 
            abort(400)
    except Exception as e:
        print(e)
        flash(f'An unexpected error occurred', 'danger')
    return redirect(request.referrer)

#++++++++++++++++++++++++++++++reset password route+++++++++++++++++++++++++++++++
@app.route('/resetpassword', methods=['POST','GET'])
def reset_pass():
    form = SignUpForm()
    if request.method == 'POST':
        otp = request.form.get('otp')
        password = request.form.get('password1')
        confirm_password = request.form.get('password2')
        try:
            if password == confirm_password:
                if session['otp']['otp'] == otp:
                    if session['otp']['date_created'].replace(tzinfo=None) + timedelta(minutes=5) > datetime.utcnow():
                        user = Users.query.filter_by(id=session['otp']['user_id']).first()
                        user.password = bcrypt.generate_password_hash(password)
                        db.session.add(user)
                        db.session.commit()
                        session.pop('otp')
                        flash(f'Password reset successfully', 'success')
                        return redirect(url_for('login'))
                    else:
                        flash(f'OTP expired', 'danger')
                        return redirect(url_for('forgot_pass'))
                else:
                    flash(f'OTP does not match', 'danger')
                    return redirect(url_for('forgot_pass'))
            else:
                flash(f'Passwords do not match', 'danger')
                return redirect(url_for('reset_pass'))
        except Exception as e:
            print(e)
            flash(f'An unexpected error occurred while resetting your Password', 'danger')
            db.session.rollback()
            return redirect(url_for('forgot_pass'))
    return render_template('admin_temp/resetpassword.html',form=form)


#==================== handles errors 404 and 500================= 
@app.errorhandler(404)
def page_not_found(e):
 return "this is a 404 error page", 404
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500