# ThikanaApp

ThikanaApp is a Django-based web application designed for managing users and their family members. This application includes features for user authentication, family member management, and admin functionalities such as verifying and rejecting users.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
  - [User Authentication](#user-authentication)
  - [Family Member Management](#family-member-management)
  - [User Management](#user-management)
- [Usage](#usage)
- [License](#license)

## Features
- User signup and login functionality.
- Add, retrieve, edit, and delete family members.
- Admin functionalities to verify or reject users.
- Full name search for users.

## Technologies Used
- Django
- Django REST Framework
- SQLite (or any other database of your choice)
- Django REST Framework JWT or Token Authentication

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd thikanaapp
   ```


2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### User Authentication
- **Login**: `POST /api/auth/login/`
  - Request Body:
    ```json
    {
      "full_name": "John Doe",
      "mobile": "1234567890",
      "password": "your_password"
    }
    ```

- **Signup**: `POST /api/auth/signup/`
  - Request Body:
    ```json
    {
      "full_name": "John Doe",
      "mobile": "1234567890",
      "password": "your_password"
    }
    ```

### Family Member Management
- **Add Family Member**: `POST /api/users/<user_id>/family/add/`
  - Request Body:
    ```json
    {
      "full_name": "Family Member Name",
      "address": "Family Member Address",
      "thikana": "Thikana Location",
      "gender": "Male/Female",
      "education": "Education Level",
      "mobile": "Family Member Mobile",
      "date_of_birth": "YYYY-MM-DD"
    }
    ```

- **Get Family Members**: `GET /api/users/<user_id>/family/`

- **Edit Family Member**: `PATCH /api/users/<user_id>/family/<family_member_id>/`
  - Request Body (only the fields to be updated):
    ```json
    {
      "address": "Updated Address"
    }
    ```

- **Delete Family Member**: `DELETE /api/users/<user_id>/family/<family_member_id>/delete/`

### User Management
- **Get Users List**: `GET /api/users/`
  - Query Parameters:
    - `full_name`: Filter users by full name.

- **Verify User**: `PATCH /api/users/verify/<user_id>/<admin_id>/`

- **Reject User**: `PATCH /api/users/reject/<user_id>/<admin_id>/`

## Usage
- Use Postman or any other API testing tool to interact with the endpoints.
- Ensure you have the necessary headers (e.g., `Authorization: <your_token_here>`) where required.

## License
This project is licensed under the BSD 3-Clause License.


### Explanation:
- **Project Overview**: Provides a brief introduction to the project and its features.
- **Technologies Used**: Lists the technologies and frameworks utilized in the project.
- **Setup Instructions**: Step-by-step instructions for setting up the project locally, including how to clone the repository, create a virtual environment, install dependencies, and run the server.
- **API Endpoints**: Detailed descriptions of each API endpoint, including the methods, URLs, and request/response formats.
- **Usage**: Instructions on how to interact with the API.
- **License**: Information about the project’s license.
