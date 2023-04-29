from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from restaurant.models import Menu
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import MenuSerializer


class TestViews(TestCase):
    def test_index(self):
        response = self.client.get('/restaurant/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Welcome To Little Lemon Restaurant')

    def test_MenuItemsView(self):
        response = self.client.get('/restaurant/menu/items/')
        self.assertEqual(response.status_code, 200)


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
        response = self.client.put(
            f'/restaurant/menu/items/{menu_item.id}/', data)
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


class MenuItemsViewTestCase(APITestCase):
    def setUp(self):
        self.menu_item_data = {
            "title": "Spaghetti",
            "price": Decimal(9.99),
            "inventory": 1
        }
        self.url = reverse("menu_items")

    # def test_create_menu_item(self):
    #     response = self.client.post(self.url, self.menu_item_data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Menu.objects.count(), 1)
    #     menu_item = Menu.objects.get()
    #     self.assertEqual(menu_item.title, self.menu_item_data["title"])
    #     self.assertEqual(menu_item.price, Decimal(
    #         self.menu_item_data["price"]))
    #     self.assertEqual(menu_item.inventory, self.menu_item_data["inventory"])

    def test_list_menu_items(self):
        menu_item = Menu.objects.create(**self.menu_item_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MenuSerializer([menu_item], many=True)
        self.assertEqual(response.data, serializer.data)


class SingleMenuItemViewTestCase(APITestCase):
    def setUp(self):
        self.menu_item_data = {
            "title": "Spaghetti",
            "price": 9.99,
            "inventory": 1,
        }
        self.menu_item = Menu.objects.create(**self.menu_item_data)
        self.url = reverse("single_menu_item",
                           kwargs={"pk": self.menu_item.pk})

    def test_retrieve_menu_item(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MenuSerializer(self.menu_item)
        self.assertEqual(response.data, serializer.data)

    def test_update_menu_item(self):
        updated_menu_item_data = {
            "title": "Fettuccine Alfredo",
            "price": 12.99,
            "inventory": 1,
        }
        response = self.client.put(self.url, updated_menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        serializer = MenuSerializer(self.menu_item)
        updated_menu_item_data["price"] = str(updated_menu_item_data["price"])
        # self.assertEqual(serializer.data, updated_menu_item_data)

    def test_delete_menu_item(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(pk=self.menu_item.pk).exists())
