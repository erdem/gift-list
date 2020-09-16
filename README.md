[![Build Status](https://travis-ci.com/erdem/gift-list.svg?token=xpn1DuY8g3um8VkA87Y5&branch=master)](https://travis-ci.com/github/erdem/gift-list/)

# Gift List

Basic gift list inventory management system REST API implementation. Simplified scenario is a couple creates a wedding list and adds 
different types of products to that which become available to their wedding guests for purchase as a present.

The user client able to:

- Add a gift to the list
- Remove a gift from the list
- List the already added gifts of the list 
- Purchase a gift from the list
- Generate a report from the list which will print out the gifts and their statuses.


Setup
-----

1. Clone this repository.
2. Create a virtualenv and activate.
3. Install requirement packages(`pip install -r requirements.txt`).
4. Set `FLASK_ENV` environment variable as `development`. (`export FLASK_ENV=development`)
5. Start the Flask application on your original terminal window: `flask run`.

API ENDPOINTS
-------------

- User Registration endpoint. 

*Allowed Method*: POST

*Endpoint*: `/api/users/`

The endpoint allows the client create a new user.

**Example Usage:**

Payload:

```json
{
    "email": "user@mail.com",
    "first_name": "Mike",
    "last_name": "Ronacher",
    "password": "123123"
}
```

```shell script
curl -X POST \
  http://localhost:5000/api/users/ \
  -H 'Content-Type: application/json' \
  -d '
  	{
		"email": "user@mail.com",
		"first_name": "Mike",
		"last_name": "Ronacher",
		"password": "123123"
	}'

```

Response:

```json
{
    "first_name": "Mike",
    "created_at": "2020-09-16T02:04:52.243648",
    "last_name": "Ronacher",
    "email": "user@mail.com",
    "id": 1,
    "token": "c13fa813847b4c658859ea1cff79e098"
}
```


- User Authentication endpoint. 

*Allowed Method*: POST

*Endpoint*: `/api/users/authenticate/`

The endpoint allows the client authenticate an user.

**Example Usage:**

Payload:

```json
{
    "email": "user@mail.com",
    "password": "123123"
}
```

```shell script
curl -X POST \
  http://localhost:5000/api/users/authenticate/ \
  -H 'Content-Type: application/json' \
  -d '
  	{
        "email": "user@mail.com",
        "password": "123123"
	}'

```

Response:

```json
{
  "key": "c13fa813847b4c658859ea1cff79e098"
}
```


- User list endpoint. 

*Allowed Method*: GET

*Endpoint*: `/api/users/`

The endpoint allows the client get user list.

**Example Usage:**

```shell script
curl -X GET \
  http://localhost:5000/api/users/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer c13fa813847b4c658859ea1cff79e098'
```

Response:

```json
[
  {
    "first_name": "Mike",
    "created_at": "2020-09-16T02:04:52.243648",
    "last_name": "Ronacher",
    "email": "user@mail.com",
    "id": 1
  }
]
```

- Create and list product endpoints. 

*Allowed Method*: GET, POST

*Endpoint*: `/api/products/`

**Example Usage: Creating a product item **

Payload:

```json
{
    "name": "Polka Bedding Set, King, Silver",
    "brand": "BEAU LIVING",
    "price": "105.00GBP",
    "in_stock_quantity": 5
}
```

```shell script
curl -X POST \
http://localhost:5000/api/products/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer c13fa813847b4c658859ea1cff79e098' \
-d '
	{
    "name": "Polka Bedding Set, King, Silver",
    "brand": "BEAU LIVING",
    "price": "105.00GBP",
    "in_stock_quantity": 5
}'

```

Response:

```json
{
  "brand": "BEAU LIVING",
  "in_stock_quantity": 5,
  "name": "Polka Bedding Set, King, Silver",
  "price": "105.00GBP",
  "id": 1,
  "created_at": "2020-09-16T10:19:18.722665"
}
```

**Example Usage: Get list of product items.**

```shell script
curl -X GET \
  http://localhost:5000/api/products/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer c13fa813847b4c658859ea1cff79e098'

```


```json
[
  {
    "brand": "BEAU LIVING",
    "in_stock_quantity": 5,
    "name": "Polka Bedding Set, King, Silver",
    "price": "105.00GBP",
    "id": 1,
    "created_at": "2020-09-16T10:19:18.722665"
  }
]
```

- Create and Retrieve List endpoint. 

*Allowed Method*: GET, POST

*Endpoint*: `/api/lists/`

Payload:

```json
{
    "name": "Wedding list",
}
```

```shell script
curl -X POST \
http://localhost:5000/api/lists/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer c13fa813847b4c658859ea1cff79e098' \
-d '
	{
	"name": "Wedding list"
	}'
```

Response:

```json
{
  "id": 1,
  "name": "Wedding list",
  "owner": {
    "first_name": "Mike",
    "last_name": "Ronacher",
    "id": 1,
    "email": "user@mail.com",
    "created_at": "2020-09-16T02:04:52.243648"
  },
  "list_items": [],
  "created_at": "2020-09-16T10:29:48.158307"
}
```

- Create list item endpoint. 

*Allowed Method*: POST

*Endpoint*: `/api/lists/1/list-items/`

Payload:

```json
{
	"product": 1,
	"quantity": 2
}
```

```shell script
curl -X POST \
http://localhost:5000/api/lists/1/list-items/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer c13fa813847b4c658859ea1cff79e098' \
-d '
	{
		"product": 1,
		"quantity": 2
	}'
```

Response:

```json
{
  "id": 1,
  "list": {
    "id": 1,
    "name": "Wedding list",
    "owner": {
      "first_name": "Mike",
      "email": "user@mail.com",
      "id": 1,
      "last_name": "Ronacher",
      "created_at": "2020-09-16T02:04:52.243648"
    },
    "created_at": "2020-09-16T10:29:48.158307"
  },
  "product": {
    "in_stock_quantity": 3,
    "brand": "BEAU LIVING",
    "id": 1,
    "name": "Polka Bedding Set, King, Silver",
    "price": "105.00GBP",
    "created_at": "2020-09-16T10:19:18.722665"
  },
  "quantity": 2,
  "is_purchased": "<bound method ListItem.is_purchased of <ListItem 1>>",
  "purchased_item": null,
  "created_at": "2020-09-16T10:39:52.979812"
}
```


- Purchased endpoint for list items. (`/api/lists/1/list-items/1/purchased/`)

 
*Allowed Method*: POST

*Endpoint*: `/api/lists/1/list-items/2/purchased/`

```shell script
curl -X POST \
http://localhost:5000/api/lists/1/list-items/1/purchased/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer c13fa813847b4c658859ea1cff79e098'
```

 - List Report endpoint
*Allowed Method*: GET
*Endpoint*: `/api/lists/<list-id>/`

```shell script
curl -X GET \
  http://localhost:5000/api/lists/1/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer c13fa813847b4c658859ea1cff79e098'
```

Response:
```json
{
  "id": 1,
  "name": "Wedding list",
  "owner": {
    "email": "user@mail.com",
    "first_name": "Mike",
    "last_name": "Ronacher",
    "id": 1,
    "created_at": "2020-09-16T02:04:52.243648"
  },
  "list_items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "created_at": "2020-09-16T10:19:18.722665",
        "brand": "BEAU LIVING",
        "price": "105.00GBP",
        "in_stock_quantity": 3,
        "name": "Polka Bedding Set, King, Silver"
      },
      "quantity": 2,
      "is_purchased": "<bound method ListItem.is_purchased of <ListItem 1>>",
      "purchased_item": {
        "id": 1,
        "purchased_by": {
          "email": "guest@mail.com",
          "first_name": "Guest",
          "last_name": "User",
          "id": 2,
          "created_at": "2020-09-16T10:46:55.130671"
        },
        "created_at": "2020-09-16T10:47:09.766179"
      },
      "created_at": "2020-09-16T10:39:52.979812"
    }
  ],
  "created_at": "2020-09-16T10:29:48.158307"
}
```