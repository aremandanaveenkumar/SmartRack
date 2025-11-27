from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category

class TestProductsViews(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='naveen', email='admin@test.com')
        self.user = User.objects.create_user(username='naveen', password='kumar', email='naveen@test.com')
        self.category = Category.objects.create(name="test_category", friendly_name="Test Category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            description="This is a test product.",
            has_sizes=False,
            price=10.00,
            rating=4.5
        )
        self.superuser.save()
        self.category.save()
        self.product.save()
    
    def test_render_products_page_nouser(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.content)
        self.assertIn(b"1 Products", response.content)
        self.assertIn(b"Test Product", response.content)
        self.assertIn(b"Test Category", response.content)
        self.assertIn(b"10.00", response.content)
        self.assertIn(b"4.50", response.content)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_render_product_detail_page_nouser(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Product", response.content)
        self.assertIn(b"This is a test product.", response.content)
        self.assertIn(b"10.00", response.content)
        self.assertIn(b"4.50", response.content)
        self.assertIn(b"Quantity", response.content)
        self.assertIn(b"Keep Shopping", response.content)
        self.assertIn(b"Add to Bag", response.content)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_render_product_detail_page_user(self):
        self.client.login(username='naveen', password='kumar')
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Product", response.content)
        self.assertIn(b"This is a test product.", response.content)
        self.assertIn(b"10.00", response.content)
        self.assertIn(b"4.50", response.content)
        self.assertIn(b"Quantity", response.content)
        self.assertIn(b"Keep Shopping", response.content)
        self.assertIn(b"Add to Bag", response.content)
        self.assertNotIn(b"Edit", response.content)
        self.assertNotIn(b"Delete", response.content)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_render_products_page_user(self):
        self.client.login(username='naveen', password='kumar')
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.content)
        self.assertIn(b"1 Products", response.content)
        self.assertIn(b"Test Product", response.content)
        self.assertIn(b"Test Category", response.content)
        self.assertIn(b"10.00", response.content)
        self.assertIn(b"4.50", response.content)
        self.assertNotIn(b"Edit", response.content)
        self.assertNotIn(b"Delete", response.content)
        self.assertTemplateUsed(response, 'products/products.html') 

    def test_render_products_page_superuser(self):
        self.client.login(username='admin', password='naveen')
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.content)
        self.assertIn(b"1 Products", response.content)
        self.assertIn(b"Test Product", response.content)
        self.assertIn(b"Test Category", response.content)
        self.assertIn(b"10.00", response.content)
        self.assertIn(b"4.50", response.content)
        self.assertIn(b"Edit", response.content)
        self.assertIn(b"Delete", response.content)
        self.assertTemplateUsed(response, 'products/products.html') 

    def test_render_product_detail_page_superuser(self):
        self.client.login(username='admin', password='naveen')
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Product", response.content)
        self.assertIn(b"This is a test product.", response.content)
        self.assertIn(b"10.00", response.content)
        self.assertIn(b"4.50", response.content)
        self.assertIn(b"Quantity", response.content)
        self.assertIn(b"Keep Shopping", response.content)
        self.assertIn(b"Add to Bag", response.content)
        self.assertIn(b"Edit", response.content)
        self.assertIn(b"Delete", response.content)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_render_edit_product_page_superuser(self):
        self.client.login(username='admin', password='naveen')
        response = self.client.get(reverse('edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product Management", response.content)
        self.assertIn(b"Edit a Product", response.content)
        self.assertIn(b"Test Product", response.content)
        self.assertIn(b"This is a test product.", response.content)
        self.assertIn(b"10.00", response.content)
        self.assertIn(b"4.50", response.content)
        self.assertIn(b"Sku", response.content)
        self.assertIn(b"Select Image", response.content)
        self.assertIn(b"Update Product", response.content)
        self.assertTemplateUsed(response, 'products/edit_product.html')

    def test_render_add_product_page_superuser(self):
        self.client.login(username='admin', password='naveen')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product Management", response.content)
        self.assertIn(b"Add a Product", response.content)
        self.assertIn(b"Test Category", response.content)
        self.assertIn(b"Name", response.content)
        self.assertIn(b"Description", response.content)
        self.assertIn(b"Price", response.content)
        self.assertIn(b"Sku", response.content)
        self.assertIn(b"Select Image", response.content)
        self.assertIn(b"Add Product", response.content)
        self.assertTemplateUsed(response, 'products/add_product.html')