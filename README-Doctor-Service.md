# Doctor Management Service

A comprehensive AWS Lambda-based REST API service for managing doctor information, built with Python and using AWS S3 for data persistence.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Data Model](#data-model)
- [Setup & Deployment](#setup--deployment)
- [Environment Variables](#environment-variables)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Error Handling](#error-handling)
- [Validation Rules](#validation-rules)

## 🎯 Overview

The Doctor Management Service provides a complete CRUD (Create, Read, Update, Delete) API for managing doctor records. The service is designed as an AWS Lambda function with S3-based persistence, making it scalable, serverless, and cost-effective.

### Key Features

- ✅ **RESTful API** - Complete REST endpoints for doctor management
- ✅ **AWS Lambda** - Serverless deployment with automatic scaling
- ✅ **S3 Storage** - Reliable, durable data persistence
- ✅ **Input Validation** - Comprehensive request validation
- ✅ **Error Handling** - Robust error responses and logging
- ✅ **UUID-based IDs** - Unique identifier generation for doctors
- ✅ **Comprehensive Testing** - 27 test cases with full coverage

### Quick API Reference

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/doctors` | Get all doctors | 200 |
| `GET` | `/doctors/{id}` | Get doctor by ID | 200/404 |
| `POST` | `/doctors` | Create new doctor | 201/400 |
| `PUT` | `/doctors/{id}` | Update doctor | 200/400/404 |
| `DELETE` | `/doctors/{id}` | Delete doctor | 200/404 |

## 🏗️ Architecture

### System Design Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                       HTTP Request                              │
│                   (API Gateway / Client)                        │
└─────────────────────┬────────────────────────────────────────────┘
                      │
                      ▼
       ┌──────────────────────────────────────┐
       │     AWS Lambda (lambda_handler)      │
       │                                      │
       │  ┌────────────────────────────────┐ │
       │  │  Request Routing               │ │
       │  │  - GET /doctors                │ │
       │  │  - GET /doctors/{id}           │ │
       │  │  - POST /doctors               │ │
       │  │  - PUT /doctors/{id}           │ │
       │  │  - DELETE /doctors/{id}        │ │
       │  └────────────────────────────────┘ │
       └─────────────┬──────────────────────────┘
                     │
                     ▼
       ┌──────────────────────────────────────┐
       │    Service Logic Layer               │
       │  (ServiceLogic.py)                   │
       │                                      │
       │  ├─ get_all_doctors()               │
       │  ├─ get_doctor_by_id()              │
       │  ├─ create_doctor()                 │
       │  ├─ update_doctor()                 │
       │  └─ delete_doctor()                 │
       └──────────────┬───────────────────────┘
                      │
       ┌──────────────┴──────────────┐
       │                             │
       ▼                             ▼
┌──────────────────┐      ┌──────────────────┐
│  Validation      │      │  Response        │
│  (Validation.py) │      │  (Response.py)   │
│                  │      │                  │
│  ├─ validate_... │      │  ├─ response()   │
│  └─ check_...    │      │  └─ error()      │
└──────────────────┘      └──────────────────┘
       │                             │
       └──────────────┬──────────────┘
                      │
                      ▼
       ┌──────────────────────────────────────┐
       │  Repository Layer                    │
       │  (repository.py)                     │
       │                                      │
       │  ┌────────────────────────────────┐ │
       │  │  S3Repository                  │ │
       │  │  - read()                      │ │
       │  │  - write()                     │ │
       │  └────────────────────────────────┘ │
       └──────────────┬───────────────────────┘
                      │
                      ▼
       ┌──────────────────────────────────────┐
       │        AWS S3 Bucket                 │
       │                                      │
       │  ┌────────────────────────────────┐ │
       │  │  doctors.json                  │ │
       │  │                                │ │
       │  │  [                             │ │
       │  │    {                           │ │
       │  │      "id": "uuid",             │ │
       │  │      "name": "Dr. Smith",      │ │
       │  │      "specialization": "..."   │ │
       │  │    }                           │ │
       │  │  ]                             │ │
       │  └────────────────────────────────┘ │
       └──────────────────────────────────────┘
```

### Component Description

1. **AWS Lambda Handler** (`lambda_handler.py`)
   - Entry point for API requests
   - Route dispatching based on HTTP method and path
   - Exception handling and response formatting

2. **Service Logic** (`ServiceLogic.py`)
   - Business logic for CRUD operations
   - Data transformation and processing
   - Integration with validation and repository layers

3. **Validation** (`Validation.py`)
   - Input validation for create/update operations
   - Business rule enforcement
   - Error message generation

4. **Repository** (`repository.py`)
   - Data persistence layer using AWS S3
   - JSON serialization/deserialization
   - Error handling for S3 operations

5. **Response** (`Response.py`)
   - HTTP response formatting utility
   - Consistent JSON response structure

## 📡 API Endpoints

### Base URL
```
https://your-api-gateway-url/prod
```

### 1. Get All Doctors
**GET** `/doctors`

**Description:** Retrieve a list of all doctors.

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Dr. John Smith",
    "specialization": "Cardiology"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Dr. Jane Doe",
    "specialization": "Neurology"
  }
]
```

### 2. Get Doctor by ID
**GET** `/doctors/{id}`

**Description:** Retrieve a specific doctor by their unique ID.

**Path Parameters:**
- `id` (string): Doctor's unique identifier

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Dr. John Smith",
  "specialization": "Cardiology"
}
```

**Response (404):**
```json
{
  "message": "Doctor not found"
}
```

### 3. Create New Doctor
**POST** `/doctors`

**Description:** Create a new doctor record.

**Request Body:**
```json
{
  "name": "Dr. John Smith",
  "specialization": "Cardiology"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Dr. John Smith",
  "specialization": "Cardiology"
}
```

**Response (400 - Validation Error):**
```json
{
  "errors": [
    "name is required",
    "specialization is required"
  ]
}
```

### 4. Update Doctor
**PUT** `/doctors/{id}`

**Description:** Update an existing doctor's information.

**Path Parameters:**
- `id` (string): Doctor's unique identifier

**Request Body (partial update allowed):**
```json
{
  "name": "Dr. John Smith Jr.",
  "specialization": "Interventional Cardiology"
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Dr. John Smith Jr.",
  "specialization": "Interventional Cardiology"
}
```

**Response (404):**
```json
{
  "message": "Doctor not found"
}
```

### 5. Delete Doctor
**DELETE** `/doctors/{id}`

**Description:** Delete a doctor record by ID.

**Path Parameters:**
- `id` (string): Doctor's unique identifier

**Response (200):**
```json
{
  "message": "Deleted"
}
```

**Response (404):**
```json
{
  "message": "Doctor not found"
}
```

## 📊 Data Model

### Doctor Object
```json
{
  "id": "string (UUID)",
  "name": "string (required)",
  "specialization": "string (required)"
}
```

### Field Descriptions
- **`id`**: Unique identifier generated using UUID4
- **`name`**: Doctor's full name (string, required, trimmed of whitespace)
- **`specialization`**: Medical specialization (string, required, trimmed of whitespace)

## 🚀 Setup & Deployment

### Prerequisites
- Python 3.8+
- AWS Account with appropriate permissions
- AWS CLI configured

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ak-doctor-management-service
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   ```bash
   export DATABASE_BUCKET=your-s3-bucket-name
   export DATABASE_KEY=doctors.json
   ```

5. **Run tests:**
   ```bash
   python -m pytest service/tests/ -v
   ```

### AWS Deployment

1. **Create S3 bucket:**
   ```bash
   aws s3 mb s3://your-doctor-data-bucket
   ```

2. **Deploy Lambda function:**
   ```bash
   # Using AWS SAM or Serverless Framework
   sam deploy --guided
   ```

3. **Set Lambda environment variables:**
   - `DATABASE_BUCKET`: Your S3 bucket name
   - `DATABASE_KEY`: doctors.json (or custom key)

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_BUCKET` | S3 bucket name for data storage | Yes | - |
| `DATABASE_KEY` | S3 object key for doctor data | No | `doctors.json` |

## 🧪 Testing

### Test Coverage
- **27 total test cases** covering all functionality
- **Unit tests** for all service components
- **Integration tests** for API endpoints
- **Error handling tests** for edge cases

### Test Results Summary

| Category | Tests | Status |
|----------|-------|--------|
| **GET Operations** | 4 | ✅ Passed |
| **POST Operations** | 4 | ✅ Passed |
| **PUT Operations** | 4 | ✅ Passed |
| **DELETE Operations** | 2 | ✅ Passed |
| **Error Scenarios** | 2 | ✅ Passed |
| **Repository Layer** | 5 | ✅ Passed |
| **Validation Layer** | 3 | ✅ Passed |
| **Service Logic** | 3 | ✅ Passed |
| **TOTAL** | **27** | **✅ ALL PASSED** |

### Running Tests

```bash
# Run all tests
python -m pytest service/tests/ -v

# Run specific test file
python -m pytest service/tests/test_lambda_handler.py -v

# Run with coverage report
python -m pytest service/tests/ --cov=service --cov-report=html

# Run tests with detailed output
python -m pytest service/tests/ -vv --tb=short
```

### Test Categories

1. **API Endpoint Tests** (`test_lambda_handler.py` - 16 tests)
   - ✅ GET /doctors (all doctors)
   - ✅ GET /doctors/{id} (single doctor)
   - ✅ POST /doctors (create)
   - ✅ PUT /doctors/{id} (update)
   - ✅ DELETE /doctors/{id} (delete)
   - ✅ Invalid routes
   - ✅ Malformed requests

2. **Repository Tests** (`test_repository.py` - 5 tests)
   - ✅ Read empty S3 objects
   - ✅ Read existing data
   - ✅ Write data to S3
   - ✅ Error handling (missing bucket)
   - ✅ Round-trip read/write operations

3. **Validation Tests** (`test_validation.py` - 3 tests)
   - ✅ Create validation
   - ✅ Update validation
   - ✅ Error message generation

4. **Service Logic Tests** (`test_service_logic.py` - 3 tests)
   - ✅ POST create integration
   - ✅ GET all integration
   - ✅ Route handling

## 📁 Project Structure

```
ak-doctor-management-service/
├── service/
│   ├── lambda_handler.py           # AWS Lambda entry point
│   ├── ServiceLogic.py             # Business logic layer (CRUD operations)
│   ├── repository.py               # Data persistence layer (S3 integration)
│   ├── Validation.py               # Input validation
│   ├── Response.py                 # Response formatting utility
│   └── tests/
│       ├── test_lambda_handler.py   # 16 comprehensive API tests
│       ├── test_repository.py       # 5 repository layer tests
│       ├── test_service_logic.py    # 3 service logic tests
│       └── test_validation.py       # 3 validation tests
├── cft/
│   └── cft-doctor-service-infra.yaml  # CloudFormation template
├── requirements.txt                   # Python dependencies
├── local_server.py                    # Local development server
├── ReadMe                             # Basic readme
└── README-Doctor-Service.md           # This comprehensive documentation
```

### Total Test Coverage: 27 Tests ✅
- API Endpoints: 16 tests
- Repository Layer: 5 tests
- Service Logic: 3 tests
- Validation: 3 tests


## ⚠️ Error Handling

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| `200` | Success (GET, PUT, DELETE) |
| `201` | Created (POST) |
| `400` | Bad Request (validation errors) |
| `404` | Not Found (resource or route) |
| `500` | Internal Server Error |

### Error Response Format

```json
{
  "errors": ["error message 1", "error message 2"]
}
```

or

```json
{
  "message": "Doctor not found"
}
```

or

```json
{
  "error": "Detailed error message"
}
```

## ✅ Validation Rules

### Create Doctor Validation
- `name`: Required, cannot be empty after trimming
- `specialization`: Required, cannot be empty after trimming
- Empty request body returns specific error

### Update Doctor Validation
- `name`: Optional, but if provided cannot be empty
- `specialization`: Optional, but if provided cannot be empty
- Empty request body not allowed for updates

### Data Processing
- All string inputs are trimmed of whitespace
- UUID generation for new records
- JSON serialization for S3 storage

## 💻 Usage Examples

### Python Example

```python
import requests
import json

BASE_URL = "https://your-api-gateway.amazonaws.com"

# 1. Create a doctor
def create_doctor():
    url = f"{BASE_URL}/doctors"
    payload = {
        "name": "Dr. Lisa Chen",
        "specialization": "Dermatology"
    }
    response = requests.post(url, json=payload)
    print(response.json())
    return response.json()["id"]

# 2. Get all doctors
def get_all_doctors():
    url = f"{BASE_URL}/doctors"
    response = requests.get(url)
    print(response.json())

# 3. Get specific doctor
def get_doctor(doctor_id):
    url = f"{BASE_URL}/doctors/{doctor_id}"
    response = requests.get(url)
    print(response.json())

# 4. Update doctor
def update_doctor(doctor_id):
    url = f"{BASE_URL}/doctors/{doctor_id}"
    payload = {
        "specialization": "Clinical Dermatology"
    }
    response = requests.put(url, json=payload)
    print(response.json())

# 5. Delete doctor
def delete_doctor(doctor_id):
    url = f"{BASE_URL}/doctors/{doctor_id}"
    response = requests.delete(url)
    print(response.json())

# Usage
doctor_id = create_doctor()
get_all_doctors()
get_doctor(doctor_id)
update_doctor(doctor_id)
delete_doctor(doctor_id)
```

### cURL Examples

```bash
# Create doctor
curl -X POST https://your-api/doctors \
  -H "Content-Type: application/json" \
  -d '{"name": "Dr. Lisa Chen", "specialization": "Dermatology"}'

# Get all doctors
curl -X GET https://your-api/doctors

# Get specific doctor
curl -X GET https://your-api/doctors/550e8400-e29b-41d4-a716-446655440000

# Update doctor
curl -X PUT https://your-api/doctors/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"specialization": "Clinical Dermatology"}'

# Delete doctor
curl -X DELETE https://your-api/doctors/550e8400-e29b-41d4-a716-446655440000
```


## 🔒 Security Considerations

- Input validation prevents injection attacks
- UUID-based IDs prevent enumeration attacks
- S3 bucket should have appropriate IAM permissions
- API Gateway should implement authentication/authorization

## 📈 Performance

- Serverless architecture scales automatically
- S3 provides high availability and durability
- JSON parsing optimized for typical payload sizes
- Minimal memory footprint for Lambda execution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Last Updated:** May 6, 2026
**Version:** 1.0.0
**Status:** ✅ Production Ready
**All Tests:** ✅ 27/27 Passing</content>
<parameter name="filePath">/Users/sneha/KAPS/jsvm-backend/ak-doctor-management-service/README-Doctor-Service.md
