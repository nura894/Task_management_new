from pydantic import BaseModel, Field, field_validator

class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

    @field_validator("name")
    def clean_name(cls, v):
        v = v.strip().lower()
        if not v:
            raise ValueError("Tag cannot be empty")
        return v
    
    
    
class TagsResponse(BaseModel):
    name : str
