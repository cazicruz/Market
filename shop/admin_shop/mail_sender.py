from flask import render_template,session
from flask_mail import Message
from shop import mail, app
from datetime import datetime
import secrets

def send_email(to, subject, template, **kwargs):
 msg = Message(app.config['MARKET_MAIL_SUBJECT_PREFIX'] + subject,
 sender=app.config['MARKET_MAIL_SENDER'], recipients=[to])
 msg.body = render_template(template + '.html', **kwargs)
 msg.html = render_template(template + '.html', **kwargs)
 mail.send(msg)


def send_otp_mail(user_id,to, **kwargs):
    otp = secrets.token_hex(5)
    #session.modified=True
    session['otp'] = {'otp':otp,
                        'date_created':datetime.utcnow(),
                        'user_id':user_id
                        }
    send_email(to,  'Password Reset Request', 'admin_temp/otp_mail', otp=otp,admin=app.config['MARKET_MAIL_SENDER'], **kwargs)