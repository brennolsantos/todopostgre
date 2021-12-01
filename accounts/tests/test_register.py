from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterTest(APITestCase):

    def test_register(self):
        """
        This test registers 10 users
        and check the len on User queryset
        """

        username_test = 'user'
        password_test = '@Test12345678'
        firstn_test = 'John'
        lastn_test = 'Dove'
        email_test = "test@"

        for i in range(1, 11):
            response = self.client.post(reverse('accounts:register-list'),
                                        {
                "username": username_test + str(i),
                "password": password_test,
                "password2": password_test,
                "email": email_test + str(i) + "test.com",
                "first_name": firstn_test,
                "last_name": lastn_test
            }, format='json')

            self.client.login(username=username_test +
                              str(i), password=password_test)
            self.client.logout()

        count = User.objects.count()
        self.assertEqual(count, 10)
