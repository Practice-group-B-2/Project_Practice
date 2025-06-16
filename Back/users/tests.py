from django.test import TestCase
from users.forms import BaseRegisterForm
# Create your tests here.
class UserCrateTest(TestCase):
    def crates_user(self):
        user = BaseRegisterForm(first_name="Testkoler",
                                lats_name="TestGena" ,
                                username = "testname",
                                password1 = "secretspasswrod",
                                password2 = "secretspasswrod",
                                email="test@gmail.com")
        self.assertEqual(user.username,"testname" )
        self.assertEqual(user.first_name,"Testkoler")
        self.assertEqual(user.last_name,"TestGena")
        self.assertEqual(user.email,"test@gmail.com")
        self.assertTrue(user.check_password(user.password2))
       