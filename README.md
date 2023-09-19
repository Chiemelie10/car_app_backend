### MarketerRegistration

#### Description

This API endpoint allows the creation of a new user, specifically a marketer, with the provided data. It also supports referral codes for team manager association.

#### Endpoint

`POST /api/register-marketer/`

#### Parameters

- `email` (string, required): The email address of the user.
- `username` (string, required): The username of the user.
- `password` (string, required): The password for the user. It will be securely hashed before saving.
- `first_name` (string, required): The first name of the user.
- `last_name` (string, required): The last name of the user.
- `phone_number` (string, required): The phone number of the user.
- `referral_code` (string, optional): A referral code for team manager association.

#### Permissions

- Only admin users are allowed to create marketers using this API.

#### Return Value

- Success (HTTP 201):

  ```
  {
      "message": "Account created successfully."
  }
  ```
- Error (HTTP 400):

  - If the referral code is invalid:
    ```
    {
        "error": "Invalid referral code, remove field if not certain."
    }
    ```
  - If the email is not available:
    ```
    {
        "error": "Email not available."
    }
    ```
  - If the username is not available:
    ```
    {
        "error": "Username not available."
    }
    ```
  - For other errors:
    ```
    {
        "error": "Error message describing the issue."
    }
    ```

#### Example

**Request:**

```json
POST /api/register-marketer/
{
    "email": "newmarketer@example.com",
    "username": "newmarketer",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "referral_code": "team123"
}
```

**Response (Success):**

```json
HTTP/1.1 201 Created
{
    "message": "Account created successfully."
}
```

**Response (Invalid Referral Code):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "Invalid referral code, remove field if not certain."
}
```

**Response (Email Already Exists):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "Email not available."
}
```

**Response (Username Already Exists):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "Username not available."
}
```

**Response (Other Error):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "Error message describing the issue."
}
```

### VerifyEmail

#### Description

This API endpoint allows users to confirm their email verification by clicking on a verification link sent to their email.

#### Endpoint

- `GET /api/verify-email/`: Confirm email verification.

#### Parameters

- `token` (Query Parameter): The verification token provided in the verification link.

#### Return Value

- **Success (HTTP 200)**: If the email verification is successful, it returns a JSON response with a success message.

  Example:

  ```json
  {
      "message": "Email verified successfully."
  }
  ```
- **Error (HTTP 400)**:

  - If the verification link has expired:

    Example:

    ```json
    {
        "error": "The link has expired."
    }
    ```
  - If the verification link is invalid:

    Example:

    ```json
    {
        "error": "The link is invalid"
    }
    ```

### SendEmailVerificationLink

#### Description

This API endpoint allows authenticated users to request a new email verification link to be sent to their registered email address.

#### Endpoint

- `GET /api/send-email/`: Send a new email verification link.

#### Authentication

- Requires a valid JWT token to be included in the request headers for authentication.

#### Return Value

- **Success (HTTP 200)**: If the email verification link is sent successfully, it returns a JSON response with a success message.

  Example:

  ```json
  {
      "message": "The verification link was sent successfully"
  }
  ```
- **Error (HTTP 400)**:

  - If the content type of the request is not JSON:

    Example:

    ```json
    {
        "error": "The Content-Type must be json."
    }
    ```
  - If the user associated with the provided token is not found in the database:

    Example:

    ```json
    {
        "error": "The user authenticated with the provided token was not found in the database."
    }
    ```
  - If there's an error while sending the email verification link:

    Example:

    ```json
    {
        "error": "An error occurred while sending the email verification link."
    }
    ```

### UserLogin

#### Description

This API endpoint allows users to log in by providing their username and password. If the provided credentials are valid, it returns access and refresh tokens for the user, which can be used for authentication in subsequent requests.

#### Endpoint

`POST /api/login/`

#### Parameters

- `username` (string, required): The username of the user.
- `password` (string, required): The password for the user.

#### Return Value

- Success (HTTP 200):

  ```
  {
      "access": "access_token"
  }
  ```

  The `access_token` is a JSON Web Token (JWT) that can be used for authentication.
- Error (HTTP 400):

  - If the request Content-Type is not JSON:
    ```
    {
        "error": "The Content-Type must be json."
    }
    ```
  - If the username is not provided:
    ```
    {
        "error": "Username must be provided."
    }
    ```
  - If the password is not provided:
    ```
    {
        "error": "Password must be provided."
    }
    ```
  - If the provided credentials are invalid (user not found):
    ```
    {
        "error": "User not found."
    }
    ```

#### Example

**Request:**

```json
POST /api/login/
{
    "username": "john_doe",
    "password": "secret_password"
}
```

**Response (Success):**

```json
HTTP/1.1 200 OK
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (Invalid Content-Type):**

```json
HTTP/1.1 415 Unsupported Media Type
{
    "error": "The Content-Type must be json."
}
```

**Response (Username Missing):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "Username must be provided."
}
```

**Response (Password Missing):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "Password must be provided."
}
```

**Response (Invalid Credentials):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "User not found."
}
```

### UserLogout

#### Description

This API endpoint allows authenticated users to log out, which involves blacklisting the refresh token, making it invalid for further authentication.

#### Endpoint

`POST /api/logout/`

#### Parameters

- `refresh` (string, required): The refresh token obtained during the user's login.

#### Authentication

- This endpoint requires JWT (JSON Web Token) authentication.

#### Permissions

- Only authenticated users can log out.

#### Return Value

- Success (HTTP 200):

  ```
  {
      "message": "Logged out successfully."
  }
  ```
- Error (HTTP 400):

  - If the request Content-Type is not JSON:
    ```
    {
        "error": "The Content-Type must be json."
    }
    ```
  - For other errors, a JSON response with an error message is returned.

#### Example

**Request:**

```json
POST /api/logout/
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (Success):**

```json
HTTP/1.1 200 OK
{
    "message": "Logged out successfully."
}
```

**Response (Invalid Content-Type):**

```json
HTTP/1.1 415 Unsupported Media Type
{
    "error": "The Content-Type must be json."
}
```

**Response (Other Error):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "Error message describing the issue."
}
```

### GetUsers

#### Description

This API endpoint allows users to retrieve a list of all registered users in the application.

#### Endpoint

`GET /api/users/`

#### Parameters

- None

#### Return Value

- Success (HTTP 200):

  - A JSON array containing user data.

    Example:

    ```json
    [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "is_marketer": false
        },
        {
            "id": 2,
            "username": "jane_smith",
            "email": "jane@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "phone_number": "+9876543210",
            "is_marketer": true
        }
    ]
    ```
- Success (HTTP 200, Empty List):

  - If no users are found, an empty JSON array is returned.

    Example:

    ```json
    []
    ```

#### Example

**Request:**

```json
GET /api/users/
```

**Response (Success with Users):**

```json
HTTP/1.1 200 OK
[
    {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+1234567890",
        "is_marketer": false
    },
    {
        "id": 2,
        "username": "jane_smith",
        "email": "jane@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "phone_number": "+9876543210",
        "is_marketer": true
    }
]
```

**Response (Success, Empty List):**

```json
HTTP/1.1 200 OK
[]
```

### GetDeleteUpdateUser

#### Description

This API endpoint allows users to retrieve, delete, or update user data in the database. It provides functionality for viewing, modifying, or deleting user profiles based on user permissions.

#### Endpoint

- `GET /api/users/<str:pk>/`: Retrieve user data by user ID.
- `DELETE /api/users/<str:pk>/`: Delete user data by user ID.
- `PUT /api/users/<str:pk>/`: Update user data by user ID.

#### Parameters

- `pk` (Path Parameter): The unique identifier of the user.

#### Authentication

- Requires JWT (JSON Web Token) authentication.
- Users can only modify their own profiles unless they are superusers or managers.

#### Return Value

- **GET Request: Retrieve User Data**

  - Success (HTTP 200): A JSON object containing the user's data.

    Example:

    ```json
    {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+1234567890",
        "is_marketer": false
    }
    ```
  - Error (HTTP 400):

    - If the provided user ID does not match any user in the database:

      Example:

      ```json
      {
          "error": "User not found"
      }
      ```
- **DELETE Request: Delete User Data**

  - Success (HTTP 200): A JSON message confirming the deletion.

    Example:

    ```json
    {
        "message": "Account for john_doe has been deleted successfully."
    }
    ```
  - Error (HTTP 400):

    - If the provided user ID does not match any user in the database:

      Example:

      ```json
      {
          "error": "User not found"
      }
      ```
    - If the user does not have permission to delete the account:

      Example:

      ```json
      {
          "error": "You do not have the permission to perform this action."
      }
      ```
- **PUT Request: Update User Data**

  - Success (HTTP 200): A JSON object containing the updated user's data.

    Example:

    ```json
    {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+1234567890",
        "is_marketer": true
    }
    ```
  - Error (HTTP 400):

    - If the provided user ID does not match any user in the database:

      Example:

      ```json
      {
          "error": "User not found"
      }
      ```
    - If the Content-Type is not JSON:

      Example:

      ```json
      {
          "error": "Content-Type must be json."
      }
      ```
    - If the user does not have permission to perform the update:

      Example:

      ```json
      {
          "error": "You do not have the permission to perform this action."
      }
      ```
    - If there are validation errors in the request data, the error details will be included in the response.

#### Example

**GET Request: Retrieve User Data**

```http
GET /api/users/1/
```

**Response (Success with User Data):**

```json
HTTP/1.1 200 OK
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "is_marketer": false
}
```

**DELETE Request: Delete User Data**

```http
DELETE /api/users/1/
```

**Response (Success with Deletion Confirmation):**

```json
HTTP/1.1 200 OK
{
    "message": "Account for john_doe has been deleted successfully."
}
```

**PUT Request: Update User Data**

```http
PUT /api/users/1/
```

**Request Body (JSON):**

```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "is_marketer": true
}
```

**Response (Success with Updated User Data):**

```json
HTTP/1.1 200 OK
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "is_marketer": true
}
```

### GetUserAdvert

#### Description

This API endpoint allows users to retrieve an advertisement (advert) belonging to a specific user based on the provided `user_id` and `advert_id`.

#### Endpoint

- `GET /api/users/<str:user_id>/adverts/<str:advert_id>/`: Retrieve an advert by `user_id` and `advert_id`.

#### Parameters

- `user_id` (Path Parameter): The unique identifier of the user.
- `advert_id` (Path Parameter): The unique identifier of the advert.

#### Return Value

- **GET Request: Retrieve Advert Data**
  - Success (HTTP 200): A JSON object containing the advert's data.

    Example:

    ```json
    {
        "id": 1,
        "user": 3,
        "title": "Used Car for Sale",
        "description": "A well-maintained used car for sale.",
        "price": 15000.0,
        "location": "New York, NY",
        "date_posted": "2023-09-19T12:00:00Z"
    }
    ```
  - Error (HTTP 400):

    - If the provided `user_id` and `advert_id` do not match any advert in the database:

      Example:

      ```json
      {
          "error": "Advert not found"
      }
      ```

#### Example

**GET Request: Retrieve Advert Data**

```http
GET /api/users/3/adverts/1/
```

**Response (Success with Advert Data):**

```json
HTTP/1.1 200 OK
{
    "id": 1,
    "user": 3,
    "title": "Used Car for Sale",
    "description": "A well-maintained used car for sale.",
    "price": 15000.0,
    "location": "New York, NY",
    "date_posted": "2023-09-19T12:00:00Z"
}
```

**Response (Error when Advert Not Found):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "Advert not found"
}
```

### GetUserAdverts

#### Description

This API endpoint allows users to retrieve a list of advertisements (adverts) belonging to a specific user based on the provided `user_id`.

#### Endpoint

- `GET /api/users/<str:user_id>/adverts/`: Retrieve a list of adverts by `user_id`.

#### Parameters

- `user_id` (Path Parameter): The unique identifier of the user for whom you want to retrieve adverts.

#### Return Value

- **GET Request: Retrieve User's Adverts**
  - Success (HTTP 200): A JSON array containing the advert data of the user.

    Example:

    ```json
    [
        {
            "id": 1,
            "user": 3,
            "title": "Used Car for Sale",
            "description": "A well-maintained used car for sale.",
            "price": 15000.0,
            "location": "New York, NY",
            "date_posted": "2023-09-19T12:00:00Z"
        },
        {
            "id": 2,
            "user": 3,
            "title": "SUV for Rent",
            "description": "Spacious SUV available for rent.",
            "price": 80.0,
            "location": "Los Angeles, CA",
            "date_posted": "2023-09-20T10:30:00Z"
        }
    ]
    ```
  - Error (HTTP 400):

    - If the provided `user_id` does not match any user in the database:

      Example:

      ```json
      {
          "error": "User not found."
      }
      ```

#### Example

**GET Request: Retrieve User's Adverts**

```http
GET /api/users/3/adverts/
```

**Response (Success with Advert Data):**

```json
HTTP/1.1 200 OK
[
    {
        "id": 1,
        "user": 3,
        "title": "Used Car for Sale",
        "description": "A well-maintained used car for sale.",
        "price": 15000.0,
        "location": "New York, NY",
        "date_posted": "2023-09-19T12:00:00Z"
    },
    {
        "id": 2,
        "user": 3,
        "title": "SUV for Rent",
        "description": "Spacious SUV available for rent.",
        "price": 80.0,
        "location": "Los Angeles, CA",
        "date_posted": "2023-09-20T10:30:00Z"
    }
]
```

**Response (Error when User Not Found):**

```json
HTTP/1.1 400 Bad Request
{
    "error": "User not found."
}
```
