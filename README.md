# Real-Time Feed Subscription System with Django

This repository contains a Django application for building a real-time feed subscription system. The system allows users to subscribe to channel groups and receive live feed updates using the Binance WebSocket API.

## Features

1. **User Authentication:** Users can register and log in to the application.
2. **Subscription:** Upon logging in, users can subscribe to channel groups to receive live feed updates.
3. **WebSocket Integration:** Django Channels is used to handle WebSocket connections and send live feed messages to subscribed users.
4. **Scalability:** The application is designed to handle a large number of concurrent users subscribing to the feed.

## Technologies Used

- Python
- Django
- Django Rest Framework
- Django Channels
- Redis

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Akhtar21yr/RealTime-Feed-Subscription
   cd realtime_feed_subscription
   ```
2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up PostgreSQL database according to settings in settings.py.
    ```bash
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'Enter Your Database Name',
            'USER': 'Enter Your Username',
            'PASSWORD': 'Enter You Password',
            'HOST': 'localhost',  
        }
    }
    ```
4. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  Run the development server:
    ```bash
    python manage.py runserver
    ```
## Usage

1. **User Registration:** Navigate to `/api/register/` to register a new user by providing email, full name, age, and password.
 
    **How to Use:**
    - Add email, full_name, password, password2, age, city as a  json data in Body/raw to register your self as a user.

    ```bash
    {
    "email":"admin@gmail.com",
    "full_name" : "admin",
    "password":"admin",
    "password2":"admin",
    "age" : 21,
    "city" : "mumbai"
    }
    ```
    - If everything is ok then is provide access and refresh token, copy the access token for further use.

2. **User Login:** Go to `/api/login/` to log in with the registered credentials.

    **How to Use:**
    - Add email, password in Body/raw as a  json data to login in system.
    ```bash
    {
    "email":"sahil2@gmail.com",
    "password":"1234"
    }
    ```
    - If everything is ok then is provide access and refresh token, copy the access token for further use.

3. **Subscription:** After logging in, access ``/api/subscribe/`` to subscribe to channel groups for live feed updates.
    
    **How to Use:**
    - First Provide latest token in header `authorization` as key and  `Bearer <Your-copied-access-token>` as a value.

    ![Example Image](readme-media/image/Screenshot-(10).png)
    - Provide gc_name as a json data in which group you want to subscribe.
    ```bash
    {
        "gc_name" : "binance"
    }
    ```
    - Make sure to subscribe `binance` group.
    



## WebSocket Connection Usage

**WebSocket connection:** established websocket connection to get the data from Binance at `ws://127.0.0.1:8000/ws/binance/` .

**How To Use:**
- First Provide token in header `authorization` as key and  `Bearer <Your-copied-access-token>` as a value.

![Example Image](readme-media/image/Screenshot-(11).png)

- Make sure you have already subscribed `binance` group.

- Connect to the websocket and enjoy real-time feed data from binance.





