import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import uvicorn

app = FastAPI(
    title="Datin Validation Service",
    description="Data validation microservice for the Datin platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ValidationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    value: float = Field(..., ge=0)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Name must be alphanumeric (hyphens and underscores allowed)')
        return v.strip()

class ValidationError(BaseModel):
    field: str
    message: str

class ValidationResponse(BaseModel):
    valid: bool
    errors: Optional[List[ValidationError]] = None
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime: float
    version: str

# Global state
start_time = time.time()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        uptime=time.time() - start_time,
        version="1.0.0"
    )

@app.post("/validate", response_model=ValidationResponse)
async def validate_data(request: ValidationRequest):
    """
    Validate data according to Datin platform rules

    Rules:
    - Name must be alphanumeric (hyphens and underscores allowed)
    - Value must be non-negative
    - Value must be less than 1,000,000
    """
    errors: List[ValidationError] = []

    try:
        # Additional business logic validation
        if request.value > 1_000_000:
            errors.append(ValidationError(
                field="value",
                message="Value must be less than 1,000,000"
            ))

        # Check for reserved names
        reserved_names = ["admin", "root", "system", "test"]
        if request.name.lower() in reserved_names:
            errors.append(ValidationError(
                field="name",
                message=f"'{request.name}' is a reserved name and cannot be used"
            ))

        is_valid = len(errors) == 0

        return ValidationResponse(
            valid=is_valid,
            errors=errors if not is_valid else None,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )

    except ValueError as e:
        return ValidationResponse(
            valid=False,
            errors=[ValidationError(field="validation", message=str(e))],
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Datin Validation Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "validate": "/validate",
            "docs": "/docs",
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
