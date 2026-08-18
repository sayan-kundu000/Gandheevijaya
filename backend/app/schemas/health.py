from typing import Optional

from pydantic import BaseModel, Field


class LivenessResponse(BaseModel):
    status: str = Field(default="ok", description="Process liveness status")
    app: str = Field(..., description="Application name")


class HealthResponse(BaseModel):
    status: str = Field(default="ok", description="Application status")
    service: str = Field(..., description="Service identifier")
    version: str = Field(..., description="Service semantic version")
    environment: str = Field(..., description="Active runtime environment (development, testing, production)")


class DBHealthResponse(BaseModel):
    status: str = Field(..., description="Overall health status ('ok' or 'unhealthy')")
    service: str = Field(..., description="Service identifier")
    database: str = Field(..., description="Database connectivity status ('connected' or 'disconnected')")
    version: str = Field(..., description="Service semantic version")
    error: Optional[str] = Field(None, description="Detailed error message if database check failed")
