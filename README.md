# LibSys

## Table of Contents

- [Installation](#Installation)
- [Documentation](#Documentation)


### College Project : SmartClass 

This Project is a part of my college project. The main aim of this project is to create a Virtual Learning Environment. The system will be able to manage students, teachers, and content. 

#### Technologies Used

- **Python and Django**:
  - Django: I used Django Rest Framework (DRF) to create the API.

- **SQLite**:
   - Database used to store data.

- **Swagger**:
   - Used to document the API.


#### How it works

1. **Implementation of the API in Django**:
   - Creation of an API using Django Rest Framework.

## Installation

### Prerequisites

Certify yourself to have the following installed on your local environment:
- [Python](https://www.python.org/) 
- [pip](https://pip.pypa.io/en/stable/installation/) 

### Step 1: Clone the Project Repository

Clone the `SmartClass-backend` project repository to your local machine:
    

### Step 2: Configure the Django Environment

1. **Create a Virtual Environment**
    Create a new Python virtual environment in the project directory:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows use `venv\Scripts\activate`
   ```

2. **Install Required Dependencies**
   Install all required dependencies using pip, they are listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Run the Project

1. **Run the Django Server**

   If it is the first time you are running the project, you will need to create the database and run the migrations:
   ```bash
   python manage.py makemigrations
   ```
  Then
  ```bash
  python manage.py migrate
  ```

   Run the Django development server using the `manage.py` script:
   ```bash
   python manage.py runserver
   ```

## Documentation

The documentation of the project can be accessed using swagger. To access the documentation, run the project and access the following URL in your browser:
```bash
http://127.0.0.1:8000/swagger/
```
This will open the Swagger documentation page with all the available endpoints and their descriptions.

### Author
Gustavo Alexandre dos Santos Silva
```bash
https://github.com/Gustalex
```
