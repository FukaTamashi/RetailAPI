# RetailAPI - Integration with RetailCRM

This project includes the API that allows managing customers, orders, payments.

---

## Prerequisites

Before getting started, ensure that you have the following installed:

- **Docker** and **Docker Compose** (for containerization)
- **Python 3.11** (for development without Docker)
- **Git** (for version control)
- **pip** (for dependency management)
- **pytest** for testing

---

## How to Run the Project

### Running with Docker

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/FukaTamashi/RetailAPI.git
    ```
    
2. Create an .env file in the project root based on .env.example.
    
3. Build and start the project using Docker Compose:

    ```bash
    docker-compose up --build
    ```

    - This will build the Docker image and start the project with all its dependencies.
    - The project will be available on `http://127.0.0.1:8088`.

4. You can now visit the documentation at:
    - API Documentation http://127.0.0.1:8088/docs
    - ReDoc Documentation http://127.0.0.1:8088/redoc

---

### Running Locally (Without Docker)

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/retailapi.git
    cd retailapi
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv .venv
    source .venv\Scripts\activate
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:
   
    Copy the `.env.sample` to `.env` and adjust the settings:

    ```bash
    cp .env.sample .env
    ```

5. **Run the application**:

    Start the FastAPI server:

    ```bash
    python app/main.py
    ```

    - The project will be available at `http://127.0.0.1:8088`.

---

## Running Tests

The project uses `pytest` for unit and integration tests.

1. **Install test dependencies**:

    If you don't have `pytest` installed yet, use the following command:

    ```bash
    pip install pytest pytest-asyncio
    ```

2. **Run the tests**:

    Run the tests in your terminal with:

    ```bash
    pytest
    ```

    This will run all the tests located in the `tests/` directory.

---

## Project Structure

### **Directory Layout**

- **`app/`**: The main backend logic.
    - **`server/`**: FastAPI application and settings.
    - **`api/`**: The API layer for interacting with RetailCRM.
    - **`config/`**: Configuration files for various environments.
    - **`utils/`**: Utility functions like exception handling.

- **`docker/`**: Docker-specific files including the `Dockerfile`.
- **`tests/`**: Contains all the unit and integration tests for the project.

---

## API Endpoints

The following API endpoints are available:

### **Customers**
- **GET /api/retailCRM/customers**: Get a list of all customers.
- **POST /api/retailCRM/customers**: Create a new customer.
- **GET /api/retailCRM/customers/{customer_id}**: Retrieve a customer by ID.

### **Orders**
- **POST /api/retailCRM/orders**: Create a new order.
- **GET /api/retailCRM/orders/by-customer/{customer_id}**: Get orders by customer ID.

### **Payments**
- **POST /api/retailCRM/orders/payments**: Add a payment to an order.

---

## Configuration

All the configuration values are managed through environment variables stored in the `.env` file. Key variables include:

- **`APP_PORT`**: The port on which the FastAPI server will run.
- **`WORKERS`**: The number of workers to run the application with.
- **`API_KEY`**: API key used for interacting with RetailCRM.
- **`BASE_URL`**: Base URL of the RetailCRM API.
- **`SITE_CODE`**: The site code used to identify the CRM instance.
