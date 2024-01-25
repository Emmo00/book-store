# Book-store app

A book store app with flask

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

3. Set env variables

### Environment variables

```bash
SECRET_KEY=
DATABASE_URI=

UPLOADS_FOLDER=

ADMIN_USER=
ADMIN_PASS=


FLW_PUBLIC_KEY=
FLW_SECRET_KEY=

APP_NAME=
APP_URL=
```

4. Start application

```bash
flask run -h 0.0.0.0
```
