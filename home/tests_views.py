from django.test import TestCase
from django.urls import reverse

class TestHomeViews(TestCase):
    
    def test_render_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertIn(b"SmartRack", response.content)
        self.assertContains(response, 'class="ml-embedded"')
        self.assertContains(response, 'data-form="JDx4O8"')

    def test_render_login_page(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign In", response.content)
        self.assertIn(b"Google", response.content)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_render_signup_page(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign Up", response.content)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_render_empty_bag_page(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Shopping Bag", response.content)
        self.assertIn(b"Your bag is empty.", response.content)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_render_products_page(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.content)
        self.assertIn(b"0 Products", response.content)
        self.assertTemplateUsed(response, 'products/products.html')
    
