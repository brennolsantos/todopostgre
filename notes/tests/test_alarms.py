from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse
from rest_framework import status
from notes.models import Alarm
from notes.views import check_alarms
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class TestAlarms(APITestCase):

    def test_creation(self):
        """
        This test creates 4 alarms, 
        2 expired, checking its model count 
        before and after check view 
        """
        factory = APIRequestFactory()

        response = self.client.post(reverse('accounts:register-list'),
                                    {
            'username': 'test',
            'password': '@Test12345678',
            'password2': '@Test12345678',
            'email': 'teste@teste.com',
            'first_name': 'John',
            'last_name': 'Dove'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.login(username='test', password='@Test12345678')

        user = User.objects.all().filter(username='test').first()

        for i in range(1, 5):
            if i % 2 == 0:
                date = timezone.now() - timedelta(days=5)
            else:
                date = timezone.now() + timedelta(days=1)

            response = self.client.post(reverse('notes:alarm-list'),
                                        {
                'title': 'Alarm' + str(i),
                'desc': 'Some alarm',
                'alarm_date': date.strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
                'user': user.pk
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        alarms = Alarm.objects.all()

        self.assertEqual(len(alarms), 4)

        # This next step checks if 2 alarms are deleted
        # Because the delete() in view makes no difference
        # in test database
        request = factory.get('/api/check-alarms')

        force_authenticate(request, user=user)

        response = check_alarms(request)
        response.render()

        j = json.loads(response.content)
        deleted = j['Deleted']

        self.assertEqual(deleted, 2)
