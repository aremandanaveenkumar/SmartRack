from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import AddressField, UserProfile
from .forms import UserProfileForm, AddressFieldForm


class TestProfileForms(TestCase):

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

    def test_my_profile_form_valid(self):
        form = UserProfileForm({
            'default_phone_number': "123456789"
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_default_address_form_notvalid(self):
        form = AddressFieldForm(
            data = {
        }
        )
        self.assertFalse(form.is_valid(), msg='Form is valid')
