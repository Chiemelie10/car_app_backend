## GetAdverts

This API endpoint defines an API endpoint to retrieve a list of active CarAdvert instances from the database.

**Endpoint**: `/api/adverts/`

**HTTP Method**: `GET`

#### Parameters

This API endpoint does not require any parameters.

#### Response

- **Status Code**: 200 OK
- **Content Type**: JSON

##### Successful Response Example

```json
[
    {
        "id": 1,
        "title": "2020 Toyota Camry",
        "description": "Excellent condition Toyota Camry.",
        "price": 25000.00,
        "is_active": true,
        "created_at": "2023-09-19T12:00:00Z",
        "updated_at": "2023-09-20T09:30:00Z",
        "brand": "Toyota",
        "model": "Camry",
        "manufacture_year": 2020,
        "state": "New York"
    },
    {
        "id": 2,
        "title": "2019 Honda Civic",
        "description": "Low mileage Honda Civic for sale.",
        "price": 22000.00,
        "is_active": true,
        "created_at": "2023-09-18T14:30:00Z",
        "updated_at": "2023-09-19T10:15:00Z",
        "brand": "Honda",
        "model": "Civic",
        "manufacture_year": 2019,
        "state": "California"
    }
]
```

##### Error Response Example

```json
{
    "error": "Internal server error."
}
```





## ImagesByAdvert

This API endpoint defines a method to get images for a specific car advert.

### Endpoints

#### Get Images for a Car Advert

**GET /api/adverts/{advert_id}/images/**

- `advert_id` (Path Parameter): The ID of the car advert for which you want to retrieve images.

##### Parameters

- None

##### Returns

- 200 OK: Returns a list of image details for the specified car advert in JSON format.
- 400 Bad Request: If the car advert with the provided `advert_id` does not exist.

##### Example

Request:

```http
GET /api/adverts/1/images/
```

Response:

```json
[
    {
        "id": 1,
        "url": "https://example.com/image1.jpg",
        "advert": 1
    },
    {
        "id": 2,
        "url": "https://example.com/image2.jpg",
        "advert": 1
    },
    {
        "id": 3,
        "url": "https://example.com/image3.jpg",
        "advert": 1
    }
]
```



## GetDeleteUpdateAdvert

This API endpoint defines methods to get, delete, or update a single car advert in the database.

### Authentication

- Authentication: JWT (JSON Web Token)
- Permissions: IsAuthenticatedOrReadOnly

### Endpoints

#### Get a Car Advert

**GET /api/adverts/{pk}/**

- `pk` (Path Parameter): The primary key (ID) of the car advert to retrieve.

##### Parameters

- None

##### Returns

- 200 OK: Returns the details of the car advert in JSON format.
- 400 Bad Request: If the provided `pk` does not match any adverts in the database.

##### Example

Request:

```http
GET /api/adverts/1/
```

Response:

```json
{
    "id": 1,
    "title": "Sample Car Advert",
    "description": "This is a sample car advert.",
    "price": 15000,
    "year": 2022,
    "brand": "Toyota",
    "model": "Camry",
    "state": "California",
    "city": "Los Angeles",
    "user": 1
}
```

#### Delete a Car Advert

**DELETE /api/adverts/{pk}/**

- `pk` (Path Parameter): The primary key (ID) of the car advert to delete.

##### Parameters

- None

##### Returns

- 200 OK: If the car advert is successfully deleted.
- 400 Bad Request: If the provided `pk` does not match any adverts in the database.

##### Example

Request:

```http
DELETE /api/adverts/1/
```

Response:

```json
{
    "message": "Advert 1 deleted successfully."
}
```

#### Update a Car Advert

**PUT /api/adverts/{pk}/**

- `pk` (Path Parameter): The primary key (ID) of the car advert to update.

##### Parameters

- Request Body (JSON): Contains the updated car advert data.

##### Returns

- 200 OK: If the car advert is successfully updated.
- 400 Bad Request: If the request body contains invalid data.
- 403 Forbidden: If the user does not have permission to update the advert.

##### Example

Request:

```http
PUT /api/adverts/1/
```

Request Body:

```json
{
    "title": "Updated Car Advert",
    "description": "This is an updated car advert.",
    "price": 18000,
    "year": 2023,
    "brand": "Toyota",
    "model": "Camry",
    "state": "California",
    "city": "Los Angeles"
}
```

Response:

```json
{
    "id": 1,
    "title": "Updated Car Advert",
    "description": "This is an updated car advert.",
    "price": 18000,
    "year": 2023,
    "brand": "Toyota",
    "model": "Camry",
    "state": "California",
    "city": "Los Angeles",
    "user": 1
}
```





## AdvertsByBrand

#### Description

This API endpoint retrieves all active adverts associated with a specific car brand.

#### Endpoint

- `GET /api/adverts/brands/{brand_id}/`: Retrieve all active adverts for a given car brand.

#### Parameters

- `brand_id` (int): The unique identifier of the car brand.

#### Return Value

- **Success (HTTP 200)**: If the request is successful, it returns a JSON response with a list of active adverts for the specified car brand.

  Example:

  ```json
  [
      {
          "id": 1,
          "title": "Car Advert 1",
          "brand": 1,
          "is_active": true
      },
      {
          "id": 2,
          "title": "Car Advert 2",
          "brand": 1,
          "is_active": true
      },
      ...
  ]
  ```
- **Error (HTTP 400)**: If the specified car brand does not exist, it returns a JSON response with an error message.

  Example:

  ```json
  {
      "error": "Car brand not found."
  }
  ```

### AdvertsByManufactureYear

#### Description

This API endpoint retrieves all active adverts associated with a specific car manufacture year.

#### Endpoint

- `GET /api/adverts/years/{year_id}/`: Retrieve all active adverts for a given car manufacture year.

#### Parameters

- `year_id` (int): The unique identifier of the car manufacture year.

#### Return Value

- **Success (HTTP 200)**: If the request is successful, it returns a JSON response with a list of active adverts for the specified car manufacture year.

  Example:

  ```json
  [
      {
          "id": 1,
          "title": "Car Advert 1",
          "manufacture_year": 1,
          "is_active": true
      },
      {
          "id": 2,
          "title": "Car Advert 2",
          "manufacture_year": 1,
          "is_active": true
      },
      ...
  ]
  ```
- **Error (HTTP 400)**: If the specified car manufacture year does not exist, it returns a JSON response with an error message.

  Example:

  ```json
  {
      "error": "Car manufacture year not found."
  }
  ```

## AdvertsByModel

#### Description

This API endpoint retrieves all active adverts associated with a specific car model.

#### Endpoint

- `GET /api/adverts/models/{model_id}/`: Retrieve all active adverts for a given car model.

#### Parameters

- `model_id` (int): The unique identifier of the car model.

#### Return Value

- **Success (HTTP 200)**: If the request is successful, it returns a JSON response with a list of active adverts for the specified car model.

  Example:

  ```json
  [
      {
          "id": 1,
          "title": "Car Advert 1",
          "model": 1,
          "is_active": true
      },
      {
          "id": 2,
          "title": "Car Advert 2",
          "model": 1,
          "is_active": true
      },
      ...
  ]
  ```
- **Error (HTTP 400)**: If the specified car model does not exist, it returns a JSON response with an error message.

  Example:

  ```json
  {
      "error": "Car model not found."
  }
  ```

## AdvertsByState

#### Description

This API endpoint retrieves all active adverts associated with a specific state.

#### Endpoint

- `GET /api/adverts/states/{state_id}/`: Retrieve all active adverts for a given state.

#### Parameters

- `state_id` (int): The unique identifier of the state.

#### Return Value

- **Success (HTTP 200)**: If the request is successful, it returns a JSON response with a list of active adverts for the specified state.

  Example:

  ```json
  [
      {
          "id": 1,
          "title": "Car Advert 1",
          "state": 1,
          "is_active": true
      },
      {
          "id": 2,
          "title": "Car Advert 2",
          "state": 1,
          "is_active": true
      },
      ...
  ]
  ```
- **Error (HTTP 400)**: If the specified state does not exist, it returns a JSON response with an error message.

  Example:

  ```json
  {
      "error": "State not found."
  }
  ```
