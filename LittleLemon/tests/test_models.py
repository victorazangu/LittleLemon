from decimal import Decimal
from django.test import TestCase, Client
from restaurant.models import Menu, Booking
from restaurant.serializers import MenuSerializer, BookingSerializer
from datetime import date
from django.urls import reverse
import json
from rest_framework import status


class MenuModelTestCase(TestCase):

    def setUp(self):
        self.menu = Menu.objects.create(
            title='Spaghetti Carbonara',
            price=Decimal('9.99'),
            inventory=10
        )

    def test_title_field(self):
        """
        Test that the title field of the Menu model is correctly defined.
        """
        menu = Menu.objects.get(pk=self.menu.pk)
        self.assertEqual(menu.title, 'Spaghetti Carbonara')

    def test_price_field(self):
        """
        Test that the price field of the Menu model is correctly defined.
        """
        menu = Menu.objects.get(pk=self.menu.pk)
        self.assertEqual(menu.price, Decimal('9.99'))

    def test_inventory_field(self):
        """
        Test that the inventory field of the Menu model is correctly defined.
        """
        menu = Menu.objects.get(pk=self.menu.pk)
        self.assertEqual(menu.inventory, 10)

    def test_str_method(self):
        """
        Test that the __str__() method of the Menu model returns the expected value.
        """
        menu = Menu.objects.get(pk=self.menu.pk)
        self.assertEqual(str(menu), 'Spaghetti Carbonara')


class BookingModelTestCase(TestCase):

    def setUp(self):
        self.booking = Booking.objects.create(
            name='John Doe',
            number_of_guest=5,
            booking_date=date(2023, 5, 10)
        )

    def test_name_field(self):
        """
        Test that the name field of the Booking model is correctly defined.
        """
        booking = Booking.objects.get(pk=self.booking.pk)
        self.assertEqual(booking.name, 'John Doe')

    def test_number_of_guest_field(self):
        """
        Test that the number_of_guest field of the Booking model is correctly defined.
        """
        booking = Booking.objects.get(pk=self.booking.pk)
        self.assertEqual(booking.number_of_guest, 5)

    def test_booking_date_field(self):
        """
        Test that the booking_date field of the Booking model is correctly defined.
        """
        booking = Booking.objects.get(pk=self.booking.pk)
        self.assertEqual(booking.booking_date, date(2023, 5, 10))

    def test_str_method(self):
        """
        Test that the __str__() method of the Booking model returns the expected value.
        """
        booking = Booking.objects.get(pk=self.booking.pk)
        self.assertEqual(str(booking), 'John Doe')



class SingleMenuItemViewTestCase(TestCase):

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

    def test_get_valid_single_menu_item(self):
        """
        Test that the SingleMenuItemView returns a valid menu item.
        """
        response = self.client.get(
            reverse('single_menu_item', kwargs={'pk': self.menu_item_1.pk})
        )
        menu_item = Menu.objects.get(pk=self.menu_item_1.pk)
        serializer = MenuSerializer(menu_item)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_menu_item(self):
        """
        Test that the SingleMenuItemView returns a HTTP 404 status code for an invalid menu item.
        """
        response = self.client.get(
            reverse('single_menu_item', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_menu_item(self):
        """
        Test that the SingleMenuItemView can update a valid menu item.
        """
        response = self.client.put(
            reverse('single_menu_item', kwargs={'pk': self.menu_item_1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_invalid_menu_item(self):
    #     """
    #     Test that the SingleMenuItemView can't update an invalid menu item.
    #     """
    #     response = self.client.put(
    #         reverse('single_menu_item', kwargs={'pk': self.menu_item_1.pk}),
    #         data=json.dumps(self.invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_menu_item(self):
        """
        Test that the SingleMenuItemView can delete a valid menu item.
        """
        response = self.client.delete(
            reverse('single_menu_item', kwargs={'pk': self.menu_item_1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_menu_item(self):
        """
        Test that the SingleMenuItemView returns a HTTP 404 status code for deleting an invalid menu item.
        """
        response = self.client.delete(
            reverse('single_menu_item', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)