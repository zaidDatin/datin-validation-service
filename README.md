# Datin Validation Service

Python FastAPI microservice for data validation in the Datin platform.

## 🚀 Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11
- **Server**: Uvicorn
- **Validation**: Pydantic

## 📋 Prerequisites

- Python 3.11+
- pip

## 🛠️ Local Development

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run development server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or using Python directly:

```bash
python -m app.main
```

The service will be available at [http://localhost:8000](http://localhost:8000)

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🐳 Docker

### Build image

```bash
docker build -t datin-validation-service .
```

### Run container

```bash
docker run -p 8000:8000 datin-validation-service
```

## 📡 API Endpoints

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "uptime": 123.456,
  "version": "1.0.0"
}
```

### Validate Data

```bash
POST /validate
Content-Type: application/json

{
  "name": "test-record",
  "value": 123
}
```

Response (valid):
```json
{
  "valid": true,
  "errors": null,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

Response (invalid):
```json
{
  "valid": false,
  "errors": [
    {
      "field": "name",
      "message": "'admin' is a reserved name and cannot be used"
    }
  ],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## ✅ Validation Rules

- **Name**:
  - Must be 1-100 characters
  - Alphanumeric only (hyphens and underscores allowed)
  - Cannot be empty or whitespace
  - Cannot be reserved names: admin, root, system, test

- **Value**:
  - Must be non-negative (>= 0)
  - Must be less than 1,000,000

## 📦 Deployment

This repository is configured with GitHub Actions for automated deployment to AWS ECS Fargate.

### Required GitHub Secrets

- `AWS_ROLE_ARN`: IAM role ARN for OIDC authentication

### Deployment Flow

1. Push to `main` branch
2. GitHub Actions builds Docker image
3. Image is pushed to AWS ECR
4. ECS task definition is updated
5. ECS service is deployed with new image

### Manual Deployment

```bash
# Trigger workflow manually
gh workflow run deploy.yml
```

## 🔍 Health Checks

- **Endpoint**: `/health`
- **Docker Health Check**: Runs every 30s
- **Response**: Service status and uptime information

## 📁 Project Structure

```
datin-validation-service/
├── app/
│   ├── __init__.py
│   └── main.py
├── .github/
│   └── workflows/
│       └── deploy.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🤝 Contributing

See [CODEOWNERS](./CODEOWNERS) for team ownership information.

## 📄 License

Proprietary - Datin Platform
