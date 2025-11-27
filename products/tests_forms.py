from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import ProductForm


class TestProductForms(TestCase):

    def test_add_product_form_valid(self):
        form = ProductForm({
            'name': "Test Product",
            'description': "This is a test product.",
            'has_sizes': False,
            'price': 10.00,
            'rating': 4.5
        })
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_add_product_form_invalid(self):
        form = ProductForm({
            'name': "",
            'description': "",
        })
        self.assertFalse(form.is_valid(), msg='Form is valid')

    def test_name_is_required(self):
        form = ProductForm({
            'name': "",
            'description': "This is a test product.",
            'has_sizes': False,
            'price': 10.00,
            'rating': 4.5
        })
        self.assertFalse(form.is_valid(), msg='Name was not provided, but form is valid')

    def test_description_is_required(self):
        form = ProductForm({
            'name': "Test Product",
            'description': "",
            'has_sizes': False,
            'price': 10.00,
            'rating': 4.5
        })
        self.assertFalse(form.is_valid(), msg='Description was not provided, but form is valid')

    def test_price_is_required(self):
        form = ProductForm({
            'name': "Test Product",
            'description': "This is a test product.",
            'has_sizes': False,
            'price': "",
            'rating': 4.5
        })
        self.assertFalse(form.is_valid(), msg='Price was not provided, but form is valid')

    def test_price_in_range(self):
        form = ProductForm({
            'name': "Test Product",
            'description': "This is a test product.",
            'has_sizes': False,
            'price': 10.25,
            'rating': 4.5
        })
        self.assertTrue(form.is_valid(), msg='form is not valid')

    def test_price_out_of_range(self):
        form = ProductForm({
            'name': "Test Product",
            'description': "This is a test product.",
            'has_sizes': False,
            'price': 999999,
            'rating': 4.5
        })
        self.assertFalse(form.is_valid(), msg='price in range, form is valid')