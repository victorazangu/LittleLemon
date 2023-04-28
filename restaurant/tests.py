from django.test import TestCase
from rest_framework.test import APIClient
from restaurant.models import Menu


class TestViews(TestCase):
    def test_index(self):
        response = self.client.get('/restaurant/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Welcome To Little Lemon Restaurant')

    def test_MenuItemsView(self):
        response = self.client.get('/restaurant/menu/items/')
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'menu_list.html')


class MenuItemsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test data
        Menu.objects.create(title='Burger', price=10.0, inventory=1)
        Menu.objects.create(title='Fries', price=5.0, inventory=2)

    def test_list(self):
        # Test GET request to list all menu items
        response = self.client.get('/restaurant/menu/items/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        # Test POST request to create a new menu item
        data = {'title': 'Drink', 'price': 2.5, 'inventory': 5}
        response = self.client.post('/restaurant/menu/items/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menu.objects.count(), 3)
        self.assertEqual(Menu.objects.last().title, 'Drink')

    def test_retrieve(self):
        # Test GET request to retrieve a single menu item
        menu_item = Menu.objects.last()
        response = self.client.get(f'/restaurant/menu/items/{menu_item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Fries')
        self.assertEqual(response.data['price'], 5.0)
        self.assertEqual(response.data['inventory'], 2)

    def test_update(self):
        # Test PUT request to update a menu item
        menu_item = Menu.objects.first()
        data = {'title': 'Cheeseburger', 'price': 12.0, 'inventory': 1}
        response = self.client.put(f'/restaurant/menu/items/{menu_item.id}/', data)
        self.assertEqual(response.status_code, 200)
        menu_item.refresh_from_db()
        self.assertEqual(menu_item.title, 'Cheeseburger')
        self.assertEqual(menu_item.price, 12.0)
        self.assertEqual(menu_item.inventory, 1)

    def test_delete(self):
        # Test DELETE request to delete a menu item
        menu_item = Menu.objects.first()
        response = self.client.delete(f'/restaurant/menu/items/{menu_item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Menu.objects.count(), 1)
