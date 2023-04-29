from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from restaurant.models import Menu, Booking
from restaurant.serializers import MenuSerializer, BookingSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json


class MenuItemsViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.menu_item_1 = Menu.objects.create(
            title='Spaghetti Carbonara',
            price=12.99,
            inventory=5
        )
        self.menu_item_2 = Menu.objects.create(
            title='Fettuccine Alfredo',
            price=9.99,
            inventory=2
        )
        self.valid_payload = {
            'title': 'Penne Arrabbiata',
            'price': 10.99,
            'inventory': 3
        }
        self.invalid_payload = {
            'title': 'Penne Arrabbiata',
            'price': -10.99,
            'inventory': -3
        }

    def test_get_all_menu_items(self):
        """
        Test that the MenuItemsView returns all menu items.
        """
        response = self.client.get(reverse('menu_items'))
        menu_items = Menu.objects.all()
        serializer = MenuSerializer(menu_items, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_menu_item(self):
        """
        Test that the MenuItemsView can create a valid menu item.
        """
        response = self.client.post(
            reverse('menu_items'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_create_invalid_menu_item(self):
    #     """
    #     Test that the MenuItemsView can't create an invalid menu item.
    #     """
    #     response = self.client.post(
    #         reverse('menu_items'),
    #         data=json.dumps(self.invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SingleMenuItemViewTestCase(APITestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            title='Spaghetti Carbonara',
            price=10.99,
            inventory=5
        )

    def test_retrieve_menu_item(self):
        url = reverse('single_menu_item', args=[self.menu_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = MenuSerializer(self.menu_item).data
        self.assertEqual(response.data, serialized_data)

    def test_update_menu_item(self):
        url = reverse('single_menu_item', args=[self.menu_item.id])
        data = {
            'title': 'Spaghetti Bolognese',
            'price': '12.99',
            'inventory': 10
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, data['title'])
        self.assertEqual(self.menu_item.price, Decimal(data['price']))
        self.assertEqual(self.menu_item.inventory, data['inventory'])

    def test_delete_menu_item(self):
        url = reverse('single_menu_item', args=[self.menu_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(id=self.menu_item.id).exists())


class BookingViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
        self.booking = Booking.objects.create(
            name='Test booking',
            number_of_guest=2,
            booking_date='2022-05-20'
        )

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_list_bookings(self):
        url = reverse('tables-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        serialized_data = BookingSerializer(self.booking).data
        self.assertEqual(response.data[0], serialized_data)

    def test_create_booking(self):
        url = reverse('tables-list')
        data = {
            'name': 'New booking',
            'number_of_guest': 4,
            'booking_date': '2022-06-15'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
        booking = Booking.objects.get(name='New booking')
        self.assertEqual(booking.number_of_guest, data['number_of_guest'])

    def test_retrieve_booking(self):
        url = reverse('tables-detail', args=[self.booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = BookingSerializer(self.booking).data
        self.assertEqual(response.data, serialized_data)

    def test_update_booking(self):
        url = reverse('tables-detail', args=[self.booking.id])
        data = {
            'name': 'Updated booking',
            'number_of_guest': 3,
            'booking_date': '2022-06-20'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.name, data['name'])
        self.assertEqual(self.booking.number_of_guest, data['number_of_guest'])

    def test_delete_booking(self):
        url = reverse('tables-detail', args=[self.booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)
