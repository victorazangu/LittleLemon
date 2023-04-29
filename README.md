# Installation


Activate the virtual environment

```jsx
source env/bin/activate
```

install the dependencies
```jsx
pip install -r requirements.txt
```

<br>

# Setup
The default database settings are

```jsx
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LittleLemon',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"

        }
    }
}

```
💡 Change those settings according to your local setup.
<br>
<br>

Apply the migrations
```jsx
python manage.py migrate
```
<br>


# API Endpoints

<br>

### Endpoints for `api` app
```jsx
http:127.0.0.1:8000/restaurant/menu/items
http:127.0.0.1:8000/restaurant/menu/items/{menu-itemId}
http:127.0.0.1:8000/restaurant/booking/tables
http:127.0.0.1:8000/restaurant/booking/tables/{bookingId}
```
<br>

http:127.0.0.1:8000/restaurant/menu/items
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves all menu items | No | 200 |
| POST | Creates a menu item | Yes | 201 |
<br>

http:127.0.0.1:8000/restaurant/menu/items/{menu-itemId}
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves the menu item details | NO | 200 |
| PUT | Update the menu item | Yes | 200 |
| PATCH | Partially update the menu item | Yes | 200 |
| DELETE | Delete the menu item | Yes | 200 |
<br>

http:127.0.0.1:8000/restaurant/booking/tables/
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves all bookings | Yes | 200 |
| POST | Creates a booking | Yes | 201 |
<br>

http:127.0.0.1:8000/restaurant/booking/tables/{bookingId}
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves the booking details | Yes | 200 |
| PUT | Update the booking | Yes | 200 |
| PATCH | Partially update the booking | Yes | 200 |
| DELETE | Delete the booking | Yes | 200 |
<br>

### Endpoints for `djoser` app
```jsx
http://127.0.0.1:8000/auth/users/
http://127.0.0.1:8000/auth/users/me/
http://127.0.0.1:8000/auth/users/confirm/
http://127.0.0.1:8000/auth/users/resend_activation/
http://127.0.0.1:8000/auth/users/set_password/
http://127.0.0.1:8000/auth/users/reset_password/
http://127.0.0.1:8000/auth/users/reset_password_confirm/
http://127.0.0.1:8000/auth/users/set_username/
http://127.0.0.1:8000/auth/users/reset_username/
http://127.0.0.1:8000/auth/users/reset_username_confirm/
```
<br>

http://127.0.0.1:8000/auth/users/
| Method | Action | STATUS CODE | TOKEN AUTH |
| --- | --- | --- | --- |
| GET | Retrieves all users | 200 | No |
| POST | Creates a user | 201 | No |

💡 Please refer to the [Djoser documentation](https://djoser.readthedocs.io/en/latest/getting_started.html#available-endpoints) for further usage on these endpoints.
<br> <br>

```



# There are a total of 29 tests to ensure that each API endpoint and each of its allowed HTTP methods work properly.



It should output something similar to this
```jsx
Found 29 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............
----------------------------------------------------------------------
Ran 29 tests in 7.024s

OK
Destroying test database for alias 'default'...
```
<br>
