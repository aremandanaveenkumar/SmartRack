from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import AddressField, UserProfile

class TestProfileViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='naveen', password = 'kumar', email='naveen@test.com')
        self.address = AddressField.objects.create(
            user = self.user,
            street_address1 = 'mystreet',
            street_address2 = '',
            town_or_city = 'mytown',
            state = 'mystate',
            postcode = '666666',
        )
        self.address.save()

        self.profile = UserProfile.objects.get_or_create(user = self.user)[0]
        self.profile.default_phone_number = '123456789'
        self.profile.default_address = self.address
        self.profile.save()

    def test_render_profile_page(self):
        self.client.login(username='naveen', password='kumar', email='naveen@test.com')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My Profile", response.content)
        self.assertIn(b"naveen", response.content)
        self.assertIn(b"naveen@test.com", response.content)
        self.assertTemplateUsed(response, 'profiles/profile.html')