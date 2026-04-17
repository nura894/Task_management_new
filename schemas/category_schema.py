from pydantic import BaseModel, Field, field_validator


class CategoryCreate(BaseModel):
    name: str  = Field(..., description="Task category (must exist)")
    
    @field_validator("name")
    def validate(cls,v):
        if v is not None:
            v.strip().lower()
            return v
    
    
    
class CategoryResponse(BaseModel):
    name :str    
    