from flask import render_template,render_template_string, session, request, redirect, url_for, flash,current_app,make_response
from flask_login import login_required, current_user
import secrets
from datetime import datetime
import pdfkit
from shop import app, db, photos
from shop.products.models import Brand, Category, Products
from shop.products.routes import brands, category
from shop.customers.models import CustomerOrders
from shop.admin_shop.models import Users
from .pdf_temp import temp_pdf

pdfkit_config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')


@app.route('/addorder')
@login_required
def add_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice=secrets.token_hex(5)
        try:
            order = CustomerOrders(invoice=invoice,
                                   customer_id = customer_id,
                                   orders= session['shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('shoppingcart')
            flash(f'Your order has been sent','success')
            return redirect(url_for('order',invoice=invoice))
        except Exception as e:
            print(e)
            flash(f'some error occured while getting orders','danger')
            return redirect(url_for('get_cart'))
    else:
        return redirect(url_for('login'))
        

@app.route('/orders/<invoice>')
@login_required
def order(invoice):
    if current_user.is_authenticated:
        grandtotal=0
        subtotal=0
        customer_id = current_user.id
        customer= Users.query.filter_by(id=customer_id).first()
        orders= CustomerOrders.query.filter_by(customer_id=customer_id, invoice=invoice).first()
        for key, prod in orders.orders.items():
            price= prod['price']
            subtotal+= float( price) * int(prod['quantity'])
            tax= ("%.2f" % (.06*float(subtotal)))
            grandtotal = float("%.2f" %(1.06 * subtotal))
    else:
        return redirect(url_for('login'))
    return render_template('customer_temp/order.html',invoice=invoice, tax=tax, subtotal=subtotal,grandtotal=grandtotal,customer=customer,orders=orders,current_time=datetime.utcnow())



@app.route('/orders')
@login_required
def get_order():
    if current_user.is_authenticated:
        grandtotal=0
        subtotal=0
        customer_id = current_user.id
        customer= Users.query.filter_by(id=customer_id).first()
        orders= CustomerOrders.query.filter_by(customer_id=customer_id).order_by(CustomerOrders.date_created.desc()).first()
        if orders:
            for key, prod in orders.orders.items():
                price= prod['price']
                subtotal+= float( price) * int(prod['quantity'])
                tax= ("%.2f" % (.06*float(subtotal)))
                grandtotal = float("%.2f" %(1.06 * subtotal))
        else:
            flash(f"you haven't placed any orders yet","warning")
            return redirect(request.referrer)
    else:
        return redirect(url_for('login'))
    return render_template('customer_temp/order.html',invoice=orders.invoice, tax=tax, subtotal=subtotal,grandtotal=grandtotal,customer=customer,orders=orders,current_time=datetime.utcnow())




@app.route('/getpdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandtotal=0
        subtotal=0
        customer_id = current_user.id
        if request.method=="POST":
            customer= Users.query.filter_by(id=customer_id).first()
            orders= CustomerOrders.query.filter_by(customer_id=customer_id, invoice=invoice).first()
            for key, prod in orders.orders.items():
                price= prod['price']
                subtotal+= float( price) * int(prod['quantity'])
                tax= ("%.2f" % (.06*float(subtotal)))
                grandtotal = float("%.2f" %(1.06 * subtotal))

            
            rendered = render_template_string(temp_pdf,invoice=orders.invoice, tax=tax,grandtotal=grandtotal,customer=customer,orders=orders)
           
            pdf = pdfkit.from_string(rendered,False, configuration=pdfkit_config, options={"enable-local-file-access": ""})
            res = make_response(pdf)
            res.headers['Content-Type']= 'application/pdf'
            res.headers['Content-disposition']='inline:filename=invoice.pdf'
            return res
    return request(url_for('get_order'))


