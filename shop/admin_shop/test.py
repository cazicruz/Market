from models import Users

print (Users.query.all())

class UserModelTestCase(unittest.TestCase):
 # ...
    def test_user_role(self):
        u = Users(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.CUSTOMER))
        self.assertTrue(u.can(Permission.SALES_MANAGER))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.CUSTOMER))
        self.assertFalse(u.can(Permission.SALES_MANAGER))
        self.assertFalse(u.can(Permission.ADMIN))