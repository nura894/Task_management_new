from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, Annotated, List
from datetime import datetime

class TaskCreate(BaseModel):
    title: Annotated[str, Field(..., min_length=3, max_length=100, description="add title")]
    description: Optional[str] = Field(None, min_length=5)
    
    category: str = Field(..., description="Task category (must exist)")
    tags: List[str] = Field(default_factory=list, description="List of tags")

    status: Literal["pending", "completed"] = Field(
        default="pending",
        description="Status of the task. Allowed values: 'pending', 'completed'",
        example="pending")
    
    due_date: datetime = Field(..., description= "add your due date")
    priority: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Priority level of the task. Allowed values: 'low', 'medium', 'high'",
        example="high")
    

    @field_validator("title", "description")
    def validate_not_blank(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be blank")
        return v
        
    
    @field_validator("status", "priority", "category" , mode= "before")
    def normalize_values(cls, v):
        if isinstance(v,str):
            v= v.lower().strip()
            if not v:
                raise ValueError("Field cannot be empty")
            return v
        raise ValueError("Value must be a string")
    
    @field_validator("tags", mode="before")
    def clean_tags(cls, v):
        if not isinstance(v,list):
            raise ValueError("each tag must be a string")
        
        cleaned=[]
        
        for tag in v:
            if not isinstance(tag, str):
                raise ValueError("each tag must be a string")
            
            tag = tag.strip().lower()
            if tag:
                cleaned.append(tag)
        return list(set(cleaned))        
    
    
    
    
    
class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]= None
    
    category: str
    tags: List[str]
    
    status: Literal["pending", "completed"]
    due_date: Optional[datetime] = None
    priority: Literal["low", "medium", "high"]
    
    created_at: datetime
    updated_at: Optional[datetime] = None

   
        


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    
    category: Optional[str] = None
    tags: Optional[List[str]]= None
    
    status: Optional[Literal["pending", "completed"]] = Field(
        default=None,
        description="Status of the task. Allowed values: 'pending', 'completed'",
        example="pending")
    
    due_date: Optional[datetime] = None
    priority: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description="Priority level of the task. Allowed values: 'low', 'medium', 'high'",
        example="high")      
    
    @field_validator("title", "description")
    def validate_not_blank(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be blank")
        return v
    
    @field_validator("status", "priority" , mode= "before")
    def normalize_values(cls, v):
        if v is None:
            return v
        
        if isinstance(v,str):
            return v.lower().strip()
        
        raise ValueError("Value must be a string")
    
    

  