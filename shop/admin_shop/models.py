from shop import db,app
from datetime import datetime
from flask_login import UserMixin, login_manager, AnonymousUserMixin

@app.context_processor
def inject_permissions():
 return dict(Permission=Permission)


class Users(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20),unique=False, nullable=False)
    lname = db.Column(db.String(20), unique=False,nullable=False)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(50),unique=True, nullable=False)
    address = db.Column(db.String(50),nullable=True)
    state = db.Column(db.String(50),nullable=True)
    password = db.Column(db.String(80), nullable=False)
    profile_img = db.Column(db.String(180), nullable=True, default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Roles', backref=db.backref('users', lazy=True))


    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        if self.role is None:
            if self.email == app.config['FLASKY_ADMIN']:
                self.role = Roles.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Roles.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False
login_manager.anonymous_user = AnonymousUser


class Permission:
    CUSTOMER = 1
    SALES_MANAGER = 2
    ADMIN = 4
class Roles(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    default = db.Column(db.Boolean, default=False, index=True)
    name = db.Column(db.String, unique=True, nullable=False)
    permissions = db.Column(db.Integer, unique=True,)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Roles, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
    
    def reset_permissions(self):
        self.permissions = 0
    
    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    @staticmethod
    def insert_roles():
        u_roles = {'User': [Permission.CUSTOMER],
                 'Moderator': [Permission.CUSTOMER,Permission.SALES_MANAGER],
                 'Administrator': [Permission.CUSTOMER,Permission.SALES_MANAGER,Permission.ADMIN],
                 }
        default_role = 'User'
        for r in u_roles:
            role = Roles.query.filter_by(name=r).first()
            if role is None:
                role = Roles(name=r)
            role.reset_permissions()
            for perm in u_roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
            db.session.commit()
    
#db.create_all()