from flask import render_template, session, request, redirect, url_for, flash,current_app
import os
from sqlalchemy import and_
from shop import app, db, photos, search
from flask_login import login_required
from datetime import datetime
from .models import Brand, Category , Products
from .forms import AddProducts
import secrets


def brands():
    brands = Brand.query.join(Products, (Brand.id == Products.brand_id)).all()
    return brands

def category():
    cats = Category.query.join(Products, (Category.id == Products.category_id)).all()
    return cats

#===================customer product view==================
@app.route('/products', methods=['GET', 'POST'], endpoint='products')
def products():
    endpoint = request.endpoint
    page=request.args.get('page',1,type=int)
    products = Products.query.filter(Products.stock > 0).order_by(Products.id.desc()).paginate(page=page, per_page=10)
    return render_template('product_temp/product.html', endpoint=endpoint,products=products, brands=brands(),category=category(),current_time=datetime.utcnow())

#=========search route================
@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    per_page = 1  # Number of results per page
    products_query = Products.query.msearch(keyword, fields=['product_name', 'description'])
    products = products_query.paginate(page=page, per_page=per_page)
    return render_template('product_temp/searchresult.html', products=products, brands=brands(),category=category(),current_time=datetime.utcnow())

# ==================get products by brand==================
@app.route('/brand/<int:id>', methods=['GET', 'POST'], endpoint='get_brand')
def get_brand(id):
    endpoint = request.endpoint
    page=request.args.get('page',1,type=int)
    brand = Brand.query.filter_by(id=id).first_or_404()
    products = Products.query.filter(and_(Products.brand_id==id,Products.stock>0)).order_by(Products.id.desc()).paginate(page=page, per_page=10)
    return render_template('product_temp/product.html', endpoint=endpoint,products=products, brands=brands(),brand=brand,category=category(),current_time=datetime.utcnow())

# =============get products in  category =====================
@app.route('/category/<int:id>', methods=['GET', 'POST'], endpoint='get_category')
def get_category(id):
    endpoint = request.endpoint
    page=request.args.get('page',1,type=int)
    cat = Category.query.filter_by(id=id).first_or_404()
    products = Products.query.filter(and_(Products.category_id==id,Products.stock>0)).order_by(Products.id.desc()).paginate(page=page, per_page=10)
    print(products)
    return render_template('product_temp/product.html', endpoint=endpoint,products=products, category=category(),cat=cat, brands=brands() ,current_time=datetime.utcnow())


#============== add brand view==========
@app.route('/addbrand',methods=['GET','POST'], endpoint='addbrand')
@login_required
def addBrand():
    # check the brand being added if it already exists and trow an apropraite error flash
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        if Brand.query.filter_by(name=getbrand).first():
            flash("The Brand {getbrand} already exists", 'danger')
            return redirect(url_for('addbrand'))
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash("The brand {} was added to the database".format(brand.name), 'success')
        db.session.commit()

    return render_template('product_temp/addbrand.html', endpoint=request.endpoint,current_time=datetime.utcnow())

@app.route('/deletebrand/<int:id>', methods=['POST'])
@login_required
def deletebrand(id):
    brand= Brand.query.get_or_404(id)
    if request.method =='POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f"{brand.name} deleted successfully", "success")
        return redirect(url_for("brands"))
    flash("Error deleting Brand","danger")
    return redirect(url_for("brands"))


@app.route('/deletecategory/<int:id>', methods=['POST'])
@login_required
def deletecategory(id):
    cat= Category.query.get_or_404(id)
    if request.method =='POST':
        db.session.delete(cat)
        db.session.commit()
        flash(f"{cat.name} deleted successfully", "success")
        return redirect(url_for("categories"))
    flash("Error deleting Category","danger")
    return redirect(url_for("categories"))


@app.route('/deleteproduct/<int:id>', methods=['POST'])
@login_required
def deleteproduct(id):
    prod= Products.query.get_or_404(id)
    prod_img = [prod.image_1,prod.image_2,prod.image_3,prod.image_4]

    if request.method =='POST':
        for img in prod_img:
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploads/images/" + img))
            except:
                pass

        db.session.delete(prod)
        db.session.commit()
        flash(f"{prod.product_name} deleted successfully", "success")
        return redirect(url_for("admin"))
    flash("Error deleting Product","danger")
    return redirect(url_for("admin"))

@app.route('/addcategory',methods=['GET','POST'], endpoint='addcategory')
@login_required
def addCategory():
        # check the brand being added if it already exists and trow an apropraite error flash
    if request.method == 'POST':
        getCat = request.form.get('category')
        if Category.query.filter_by(name=getCat).first():
            flash("The category {} already exists".format(getCat), 'danger')
            return redirect(url_for('addCategory'))
        cat = Category(name=getCat)
        db.session.add(cat)
        flash("The brand {} was added to the database".format(cat.name), 'success')
        db.session.commit()

    return render_template('product_temp/addbrand.html', endpoint=request.endpoint,current_time=datetime.utcnow())


@app.route('/addproducts', methods=['GET','POST'])
@login_required
def addProduct():
    form = AddProducts(request.form)
    cats= Category.query.all()
    brands= Brand.query.all()

    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        colors = form.colors.data
        brand = form.brand.data
        category = form.category.data
        try:
            #it saves images befor if flashes the image required msg
            image_1 =photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")
            image_2 =photos.save(request.files['image_2'], name=secrets.token_hex(10) + ".")
            image_3 =photos.save(request.files['image_3'], name=secrets.token_hex(10) + ".")
            image_4 =photos.save(request.files['image_4'], name=secrets.token_hex(10) + ".")

            addproduct = Products(product_name=name, price=price,description=description,discount=discount,stock=stock,colors=colors,brand_id=brand, category_id=category,
                                image_1=image_1,image_2=image_2, image_3=image_3, image_4=image_4)
            db.session.add(addproduct)
            flash("the product " + name +" has been added to the database", 'success')
            db.session.commit()
            return redirect(url_for('home'))
        except:
            flash('image required','danger')


    return render_template('product_temp/addproducts.html',category=cats, brands=brands, form=form, current_time=datetime.utcnow())

#=========== updating categories===========

@app.route('/updatecategory/<int:id>', methods=['GET','POST'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    new_cat = request.form.get('category')
    old_cat = category.name
    if request.method =='POST':
        category.name= new_cat
        flash(f'you have changed {old_cat} to {new_cat}', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('/product_temp/updatebrands.html', category=category, current_time=datetime.utcnow())

#=========== updating brands===========
@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
@login_required
def update_brand(id):
    brand = Brand.query.get_or_404(id)
    new_brand = request.form.get('brand')
    old_brand = brand.name
    if request.method =='POST':
        brand.name= new_brand
        flash(f'you have changed {old_brand} to {new_brand}', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('/product_temp/updatebrands.html', brand=brand, current_time=datetime.utcnow()) 

#============ updating product====================

@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
@login_required
def update_product(id):
    brands = Brand.query.all()
    category = Category.query.all()
    product = Products.query.get_or_404(id)
    form = AddProducts(request.form)
    if request.method =='POST':
        product.product_name = form.name.data
        product.price = request.form['price']
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.description = form.description.data
        product.colors = form.colors.data
        product.brand_id = form.brand.data
        product.category_id = form.category.data

        if request.files['image_1']:
            try:
                # delete image b4 updating it
                os.unlink(os.path.join(current_app.root_path, "static/uploads/images/" + product.image_1))
                product.image_1 =photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")
            except:
                product.image_1 =photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")

        if request.files['image_2']:
            try:
                # delete image b4 updating it
                os.unlink(os.path.join(current_app.root_path, "static/uploads/images/" + product.image_2))
                product.image_2 =photos.save(request.files['image_2'], name=secrets.token_hex(10) + ".")
            except:
                product.image_2 =photos.save(request.files['image_2'], name=secrets.token_hex(10) + ".")

        if request.files['image_3']:
            try:
                # delete image b4 updating it
                os.unlink(os.path.join(current_app.root_path, "static/uploads/images/" + product.image_3))
                product.image_3 =photos.save(request.files['image_3'], name=secrets.token_hex(10) + ".")
            except:
                product.image_3 =photos.save(request.files['image_3'], name=secrets.token_hex(10) + ".")

        if request.files['image_4']:
            try:
                # delete image b4 updating it
                os.unlink(os.path.join(current_app.root_path, "static/uploads/images/" + product.image_4))
                product.image_4 =photos.save(request.files['image_4'], name=secrets.token_hex(10) + ".")
            except:
                product.image_4 =photos.save(request.files['image_4'], name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'you have changed details on {product.product_name} ', 'success')
        return redirect(url_for('admin'))
    
    form.name.data =product.product_name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.description
    form.colors.data = product.colors
    form.brand.data = product.brand_id
    form.category.data = product.category_id
    flash(f'Error', 'danger')

    return render_template('product_temp/updateproduct.html',form=form,product=product, brands=brands, category=category, current_time=datetime.utcnow())

@app.route('/details/<int:id>', methods=['GET','POST'])
def product_details(id):
    product = Products.query.get_or_404(id)
    return render_template('product_temp/productdetails.html', product=product, brands=brands(),category=category(), current_time=datetime.utcnow())