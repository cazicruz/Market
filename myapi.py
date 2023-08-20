from shop import app, db
from shop.admin_shop.models import Users, Roles

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        Roles.insert_roles()
    app.run(debug=True)