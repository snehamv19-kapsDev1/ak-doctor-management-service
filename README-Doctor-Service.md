# Doctor Management Service

A comprehensive AWS Lambda-based REST API service for managing doctor information, built with Python and using AWS S3 for data persistence.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Data Model](#data-model)
- [Setup & Deployment](#setup--deployment)
- [Environment Variables](#environment-variables)
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

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AWS API       │────│   AWS Lambda    │────│  Service Logic  │
│   Gateway       │    │   Handler       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Validation    │    │   Repository    │
                       │                 │    │   (S3-based)    │
                       └─────────────────┘    └─────────────────┘
                                                │
                                                ▼
                                       ┌─────────────────┐
                                       │   AWS S3        │
                                       │   Bucket        │
                                       └─────────────────┘
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

### Running Tests

```bash
# Run all tests
python -m pytest service/tests/ -v

# Run specific test file
python -m pytest service/tests/test_lambda_handler.py -v

# Run with coverage
python -m pytest service/tests/ --cov=service --cov-report=html
```

### Test Categories

1. **API Endpoint Tests** (`test_lambda_handler.py`)
   - All CRUD operations
   - Error scenarios
   - Edge cases

2. **Repository Tests** (`test_repository.py`)
   - S3 read/write operations
   - Error handling
   - Data serialization

3. **Validation Tests** (`test_validation.py`)
   - Input validation logic
   - Error message generation

4. **Service Logic Tests** (`test_service_logic.py`)
   - Business logic validation
   - Integration testing

## 📁 Project Structure

```
ak-doctor-management-service/
├── service/
│   ├── lambda_handler.py      # AWS Lambda entry point
│   ├── ServiceLogic.py        # Business logic layer
│   ├── repository.py          # Data persistence layer
│   ├── Validation.py          # Input validation
│   ├── Response.py            # Response formatting
│   └── tests/
│       ├── test_lambda_handler.py
│       ├── test_repository.py
│       ├── test_service_logic.py
│       └── test_validation.py
├── cft/
│   └── cft-doctor-service-infra.yaml  # CloudFormation template
├── requirements.txt           # Python dependencies
├── local_server.py           # Local development server
├── ReadMe                     # Basic readme
└── README-Doctor-Service.md   # This file
```


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

**Last Updated:** May 4, 2026
**Version:** 1.0.0
**Status:** ✅ Production Ready</content>
<parameter name="filePath">/Users/sneha/KAPS/jsvm-backend/ak-doctor-management-service/README-Doctor-Service.md
