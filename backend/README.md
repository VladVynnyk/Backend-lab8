# Thermometer API

A RESTful API built with Flask and SQLAlchemy for managing thermometers, categories, properties, and user authentication.

## Table of Contents
- [Setup](#setup)
- [Endpoints](#endpoints)
  - [User Endpoints](#user-endpoints)
  - [Category Endpoints](#category-endpoints)
  - [Property Endpoints](#property-endpoints)
  - [Thermometer Endpoints](#thermometer-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/thermometer-api.git
   cd thermometer-api
2. **Install dependencies:**
    ```bash 
   pip install -r requirements.txt

## Endpoints 
### User Endpoints

Add User
        
    POST /users
    Request Body:
    {
      "username": "user1",
      "password": "password123"
    }

    Response: User creation status

Get All Users

    GET /users
    Response: List of all users

Get User by ID

    GET /users/<user_id>
    Response: User details by ID

Update User

    PUT /users/<user_id>
    Request Body:
        {
          "username": "new_name",
          "password": "new_password"
        }

        Response: Update status

Delete User
    
    DELETE /users/<user_id>
    Response: Deletion status

### Category Endpoints

Add Category
    
    POST /categories
    Request Body:

    {
      "name": "Electronics"
    }

    Response: Category creation status

Get All Categories

    GET /categories
    Response: List of all categories

Get Category by ID

    GET /categories/<category_id>
    Response: Category details by ID

Update Category

    PUT /categories/<category_id>
    Request Body:

        {
          "name": "Updated Category"
        }

        Response: Update status

Delete Category

    DELETE /categories/<category_id>
    Response: Deletion status

### Property Endpoints

Add Property

    POST /properties
    Request Body:

    {
      "name": "Accuracy",
      "units": "Celsius"
    }

    Response: Property creation status

Get All Properties

    GET /properties
    Response: List of all properties

Get Property by ID

    GET /properties/<property_id>
    Response: Property details by ID

Update Property

    PUT /properties/<property_id>
    Request Body:

        {
          "name": "Updated Property",
          "units": "Updated Units"
        }

        Response: Update status

Delete Property

    DELETE /properties/<property_id>
    Response: Deletion status

### Thermometer Endpoints

Add Thermometer

    POST /thermometers
    Request Body:

    {
      "name": "ThermoPro TP-50",
      "vendor": "ThermoPro",
      "category": "Electronics",
      "min_temp": -50,
      "max_temp": 70,
      "accuracy": 0.1,
      "properties": ["Accuracy", "Temperature Range"]
    }

    Response: Thermometer creation status

Get All Thermometers

    GET /thermometers
    Response: List of all thermometers

Get Thermometer by ID

    GET /thermometers/<thermometer_id>
    Response: Thermometer details by ID

Update Thermometer

    PUT /thermometers/<thermometer_id>
    Request Body:

        {
          "name": "Updated Thermometer",
          "vendor": "Updated Vendor",
          "category": "Updated Category",
          "min_temp": -30,
          "max_temp": 80,
          "accuracy": 0.05,
          "properties": ["Updated Property 1", "Updated Property 2"]
        }

        Response: Update status

    Delete Thermometer
        DELETE /thermometers/<thermometer_id>
        Response: Deletion status

### Authentication Endpoints

User Login

    POST /login
    Request Body:

    {
      "username": "user1",
      "password": "password123"
    }

    Response: Login status and session details

User Logout

    POST /logout
    Response: Logout status

Check Authentication Status

    GET /status
    Response: Authentication status with username if logged in