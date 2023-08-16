from flask import render_template, session, request, redirect, url_for, flash,current_app
from datetime import datetime
from shop import app, db, photos
from shop.products.models import Brand, Category, Products
from shop.products.routes import brands, category
from . import cart_functions



@app.route('/addcart', methods=['POST'])
def addcart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        product = Products.query.filter_by(id=product_id).first()
        if product_id and quantity and color and request.method=='POST':
            cartitems = {product_id:cart_functions.cart_dict(product,quantity,color)} 
            if 'shoppingcart' in session:
                print(session['shoppingcart'])
                cart = session['shoppingcart']
                if product_id in cart:
                        if color in cart[product_id]["colors"]:
                            if quantity == '-1':
                                session['shoppingcart'][product_id]['colors'][color] -= 1
                                session['shoppingcart'][product_id]['quantity'] -= 1
                                flash(f"the quantity of {color} {product.product_name} in cart reduced by {quantity}", "warning")
                                return redirect(request.referrer)
                            else:
                                mesure =session['shoppingcart'][product_id]['quantity']
                                if mesure >= product.stock:
                                    disable=True
                                    flash(f' {product.product_name} is out of stock','danger')
                                    return redirect(url_for('get_cart'))
                                session['shoppingcart'][product_id]['colors'][color] +=  int(quantity)
                                session['shoppingcart'][product_id]['quantity'] += int(quantity)
                                flash(f"the quantity of {color} {product.product_name} in cart increased by {quantity}", "success")
                                return redirect(request.referrer)
                        else:
                            session['shoppingcart'][product_id]['quantity'] += int(quantity)
                            session['shoppingcart'][product_id]['colors'][color] =  int(quantity)  # Update the quantity if the product already exists
                            flash(f"{quantity} {color} {product.product_name} added to cart", "success")
                            return redirect(request.referrer)
                else:
                    session['shoppingcart']={ **session['shoppingcart'], **cartitems}
                    flash(f"this product added", "success")
                    return redirect(request.referrer)

            else: 
                session['shoppingcart'] = cartitems
                flash(f"new product added", "success")
                return redirect(request.referrer)
               

    except Exception as e:
        print(e)
        return e
    finally:
        return redirect(request.referrer)
    
@app.route('/cart', methods=['POST','GET'])
def get_cart():
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        flash(f'Cart is empty','warning')
        return redirect(url_for('products'))
    cart = session['shoppingcart']
    subtotal=0
    grandtotal = 0
    for key, prod in  cart.items():
        price= prod['price']
        subtotal+= float( price) * prod['quantity']
        tax= ("%.2f" % (.06*float(subtotal)))
        grandtotal = float("%.2f" %(1.06 * subtotal))
    return render_template('cart_temp/cart.html',grandtotal=grandtotal,tax=tax, cart=cart, category=category(), brands=brands(),current_time=datetime.utcnow())

@app.route('/removecart/<int:id>,<string:color>')
def remove_cart(id,color):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('products'))
    try:
        session.modified=True
        for key, product in session['shoppingcart'].items():
            if int(key) == id:
                qty=product['colors'][color]
                if len(product['colors']) > 1:
                    for value, quantity in product['colors'].items():
                        if str(value) == color:
                            session['shoppingcart'][key]['colors'].pop(value, None)
                            session['shoppingcart'][key]['quantity'] -= qty
                            flash(f"{color} {product['name']} has been removed from cart",'warning')
                            return redirect(url_for('get_cart'))
                else:
                    session['shoppingcart'].pop(key,None)
                    flash(f"{product['name']} has been removed from cart",'warning')

                    return redirect(url_for('get_cart'))
    except Exception as e:
        print({'error':e})
        flash(f"Error occured while removing item in cart Please contact Support",'danger')

        return redirect(url_for('get_cart'))
    
@app.route('/clearcart', methods=['GET'])
def clear_cart():
    try:
        session.pop('shoppingcart', None)
        return redirect(url_for('products'))
    except Exception as e:
        print(e)