# Installation Guide for Odoo Test Project

## Prerequisites

Before setting up the project, ensure you have installed the following dependencies:

- **Python**: 3.10.11
- **PostgreSQL**: Recommended version 13 or above
- **pgAdmin**: Latest version for PostgreSQL management
- **Odoo 16**: The base framework for the project

## 1. Install Dependencies

### Install Python 3.10.11

1. Download Python from the official website:
   [Python 3.10.11 Download](https://www.python.org/downloads/release/python-31011/)

2. During installation, select **Add Python to PATH**.

3. Verify installation with:

   ```
   python --version
   ```

### Install PostgreSQL

1. Download and install **PostgreSQL**:
   [PostgreSQL Download](https://www.postgresql.org/download/)

2. Set up a new 

   superuser

    with:

   - Username: `odoo_user`
   - Password: `odoo_password`
   - Default Database: `odoo`

3. Verify installation:

   ```
   psql -U odoo_user -d odoo -W
   ```

### Install pgAdmin (Optional)

1. Download and install **pgAdmin**:
   pgAdmin Download

------

## 2. Clone the Repository

Clone the project from GitHub:

```
git clone https://github.com/GavriloJovanovic/odoo_test_project.git
cd odoo_test_project
```

------

## 3. Set Up Odoo

### Install Required Python Packages

First, remove the dummy `odoo` folder inside `odoo_test_project`.

Clone the `odoo 16` from repo:

```
git clone https://github.com/odoo/odoo.git --branch 16.0 --depth 1
cd odoo
```

Create and activate a virtual environment:

```
python -m venv venv
venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required dependencies:

```
pip install -r requirements.txt
```

### Configure Odoo

Create an `odoo.conf` file in the project root:

```
[options]
addons_path = custom_addons
db_host = localhost
db_port = 5432
db_user = odoo_user
db_password = odoo_password
xmlrpc_port = 8069
```

------

## 4. Run Odoo

Start the Odoo server with:

```
python odoo-bin --config=../odoo.conf
```

To update your custom module:

```
python odoo-bin --config=../odoo.conf -u test_applicant --stop-after-init
```

------

# API Testing Guide with Postman

## Base URL for API Requests

All API requests should be sent to:

```
http://localhost:8069/api/
```

------

## **1. Authenticate and Retrieve Session ID**

Before making requests, you need to **authenticate** and get a **session_id**.

**Endpoint**:

```
POST http://localhost:8069/web/session/authenticate
```

**Headers**:

```
{
  "Content-Type": "application/json"
}
```

**Request Body**:

```
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "db": "odoo",
    "login": "admin",
    "password": "admin_password"
  }
}
```

**Expected Response**:

```
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "uid": 2,
    "session_id": "your_session_id_here",
    ...
  }
}
```

📌 **Note:** Save the `"session_id"` value from the response, as you will need it for all further API calls.

------

## **2. Create a Test Model Record (Using Session Authentication)**

**Endpoint**:

```
POST http://localhost:8069/api/test_model
```

**Headers**:

```
{
  "Content-Type": "application/json",
  "Cookie": "session_id=your_session_id_here"
}
```

**Request Body**:

```
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "name": "Masa"
    }
}
```

**Expected Response (201 Created)**:

```
{
    "jsonrpc": "2.0",
    "id": null,
    "result": {
        "id": 54,
        "reference_code": "TEST-0003",
        "state": "draft"
    }
}
```

------

## **3. Get a Test Model Record**

**Endpoint**:

```
GET http://localhost:8069/api/test_model
```

**Headers**:

```
{
  "Content-Type": "application/json"
}
```

**Expected Response (200 OK)**:

```
{
    "jsonrpc": "2.0",
    "id": null,
    "result": [
        {
            "id": 4,
            "name": "Gasa",
            "reference_code": "TEST-0001",
            "state": "done"
        },
        {
            "id": 5,
            "name": "Kaca",
            "reference_code": "TEST-0002",
            "state": "done"
        }
    ]
}
```

------

## Additional Notes

- If you receive an **authentication error**, ensure that you **logged in correctly** and received a **valid session_id**.
- Replace `"session_id=your_session_id_here"` in headers with the actual **session_id** obtained from authentication.
