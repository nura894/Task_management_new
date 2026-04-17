from schemas.category_schema import CategoryCreate, CategoryResponse
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from database.database_mongo import categories_collection, task_collection
from utils.dependencies import get_current_user


router= APIRouter( tags=["Category"])

@router.post("/categories")
async def create_category(category:CategoryCreate, 
                          current_user = Depends(get_current_user)):
    name = category.name
    existing = await categories_collection.find_one({"name":name})
    
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="category already exist")
        
    await categories_collection.insert_one({"name":name})    
    
    return {"message":"category created"}


@router.get("/categories", response_model=List[CategoryResponse])
async def get_category(current_user= Depends(get_current_user)):
    try:
        categories = await categories_collection.find(
            {}, {"_id": 0}
        ).to_list(length=None)

        return categories

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch categories"
        )
        





@router.put("/categories/{category_id}")
async def update_category(
    category_id: str,
    new_data: CategoryCreate,
    current_user=Depends(get_current_user)
):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(400, "Invalid category ID")

    new_name = new_data.name.strip().lower()

    # check duplicate
    existing = await categories_collection.find_one({"name": new_name})
    if existing:
        raise HTTPException(400, "Category already exists")

    result = await categories_collection.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": {"name": new_name}}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Category not found")

    return {"message": "Category updated"}





@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: str,
    current_user=Depends(get_current_user)
):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(400, "Invalid category ID")

    
    category = await categories_collection.find_one(
        {"_id": ObjectId(category_id)}
    )

    if not category:
        raise HTTPException(404, "Category not found")

    category_name = category["name"]

    
    task = await task_collection.find_one({"category": category_name})

    if task:
        raise HTTPException(400, "Category in use")

    
    result = await categories_collection.delete_one(
        {"_id": ObjectId(category_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(404, "Category not found")

    return {"message": "Category deleted"}