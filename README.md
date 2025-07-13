# Product Review System (Django REST API)

A RESTful API for product reviews with user authentication and admin capabilities.

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL/MariaDB
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/product_review_system.git
cd product_review_system
```
### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Database
#### 1. Create MySQL database:
 ```sql
 CREATE DATABASE reviews;
```
#### 2. Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reviews',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
### 5. Run Migrations
```bash
python manage.py migrate
```
### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
### 7. Run Development Server
```bash
python manage.py runserver
```
## API Endpoint to test in POSTMAN

### Authentication
### User Registration
#### 1. Endpoint : http://127.0.0.1:8000/api/register/
#### method : POST
#### (Body)Input : {"username": "testuser", "email": "test@example.com", "password": "password123", "is_admin":1}
#### output : {
      "id": 8,
      "username": "testuser",
      "email": "test@example.com",
      "is_admin": true
}

#### 2. Endpoint : http://127.0.0.1:8000/api/login/
#### method : POST
#### (Body)Input :{"username": "testuser", "password": "password123"}
#### output : {
      "token": "dbb3db1f716756b75d0ac6fddc4ba94c570cd41a", 
      "user_id": 8,
      "is_admin": true
}

#### 3. Endpoint : http://127.0.0.1:8000/api/login/
#### method : POST
#### (Headers)Input : `Authorization: Token <your_token>`

### Products
### List Products
#### 1. Endpoint : http://127.0.0.1:8000/api/products/
#### method : GET
#### Output : []
### Create product
#### 2. Endpoint : http://127.0.0.1:8000/api/products/  (only for admin)
#### method : POST
#### Input : (Body) : {"name":"Premium Product 2","description":"Admin created last","price":39.99}, (Headers) : `Authorization: Token <your_token>`
#### output :{
    "id": 3,
    "name": "Premium Product 2",
    "description": "Admin created last",
    "price": "39.99",
    "created_by": 8,
    "average_rating": 0,
    "review_count": 0,
    "created_at": "2025-07-13T08:14:25.971850Z",
    "updated_at": "2025-07-13T08:14:25.971850Z"
}
### Product Detail
#### 3. Endpoint : http://127.0.0.1:8000/api/products/3/
#### method : GET
#### Output : {
    "id": 3,
    "name": "Premium Product 2",
    "description": "Admin created last",
    "price": "39.99",
    "created_by": 8,
    "average_rating": 0,
    "review_count": 0,
    "created_at": "2025-07-13T08:14:25.971850Z",
    "updated_at": "2025-07-13T08:14:25.971850Z"
}
### Update Product (Admin only)
#### 4. Endpoint : http://127.0.0.1:8000/api/products/3/
#### method : PUT
#### input : (Body) {"name":"Premium Product 2","description":"Admin created last","price":41.99}, (Headers) : `Authorization: Token ` (change anything in body and send it)
#### output :{
    "id": 3,
    "name": "Premium Product 2",
    "description": "Admin created last",
    "price": "41.99",
    "created_by": 8,
    "average_rating": 0,
    "review_count": 0,
    "created_at": "2025-07-13T08:14:25.971850Z",
    "updated_at": "2025-07-13T08:28:52.831268Z"
}
### Delete Product (Admin only)
#### Endpoint : http://127.0.0.1:8000/api/products/1/
#### method : DELETE

### Reviews
#### 1. List Reviews for a Product
#### Endpoint : http://127.0.0.1:8000/api/products/3/reviews/
#### method : GET
#### input :  (Headers) : `Authorization: Token <your_token>`
#### output : 
        []
#### 2. Create a New Review
####  Endpoint : http://127.0.0.1:8000/api/products/3/reviews/
#### method : POST
#### input : (body) : {"rating": 5, "feedback": "Excellent product!"} , (Headers) : `Authorization: Token <your_token>`
#### output : {
    "id": 2,
    "product": 3,
    "user": {
        "id": 8,
        "username": "testuser",
        "email": "test@example.com",
        "is_admin": true
    },
    "rating": 5,
    "feedback": "Excellent product!",
    "created_at": "2025-07-13T08:40:35.490304Z",
    "updated_at": "2025-07-13T08:40:35.490304Z"
}

#### 3.Verify Review Creation
#### Endpoint : http://127.0.0.1:8000/api/products/3/reviews/
#### method : GET
#### input :  (Headers) : `Authorization: Token <your_token>`
#### output : [
    {
        "id": 2,
        "product": 3,
        "user": {
            "id": 8,
            "username": "testuser",
            "email": "test@example.com",
            "is_admin": true
        },
        "rating": 5,
        "feedback": "Excellent product!",
        "created_at": "2025-07-13T08:40:35.490304Z",
        "updated_at": "2025-07-13T08:40:35.490304Z"
    }
]
#### 4.Attempt Duplicate Review
####  Endpoint : http://127.0.0.1:8000/api/products/3/reviews/
#### method : POST
#### input : (body) : {"rating": 5, "feedback": "Excellent product!"} , (Headers) : `Authorization: Token <your_token>`
#### output : [
    "You have already reviewd this product"
]
#### 5. Check Product's Average Rating
#### Endpoint : http://127.0.0.1:8000/api/products/3/
####  method : GET
#### input :(Headers) : `Authorization: Token <your_token>`
#### output : {
    "id": 3,
    "name": "Premium Product 2",
    "description": "Admin created last",
    "price": "41.99",
    "created_by": 8,
    "average_rating": 5.0,
    "review_count": 1,
    "created_at": "2025-07-13T08:14:25.971850Z",
    "updated_at": "2025-07-13T08:28:52.831268Z"
}











