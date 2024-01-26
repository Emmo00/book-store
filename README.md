# Book-store app

A book store app with flask

## Features

### Admin

- Add, Edit books
- Add, Edit pickup locations
- View Orders (Pending and other)
- View Shopping list (a list of all books that are ordered, for admin to buy them in bulk from wholesaler/retailer)

### Client

- View Books
- Add books to cart
- View items in cart
- Place an order and pay with Flutterwave checkout
- View previously make orders

## Setup

1. clone the project and `cd` into the directory.

1. Create a virtual env

```bash
python -m venv venv
```

2. Run the following command to install dependencies.

```bash
python -m pip install -r requirements.txt
```

3. Run the following command to setup `pre-commit` and `black` for code formatting.

```bash
pre-commit install
```

4. Set env variables

### Environment variables

```bash
SECRET_KEY=
DATABASE_URI=

# location to save uploaded files
UPLOADS_FOLDER=

# admin username and password
ADMIN_USER=
ADMIN_PASS=

# flutterwave API keys
FLW_PUBLIC_KEY=
FLW_SECRET_KEY=

# app name and url
APP_NAME=
APP_URL=
```

5. Start application

```bash
flask run -h 0.0.0.0
```
