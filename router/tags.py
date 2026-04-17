from schemas.tags_schema import TagCreate
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.tags_schema import TagsResponse
from database.database_mongo import tags_collection, task_collection
from utils.dependencies import get_current_user


router= APIRouter(tags=["Tags"])
@router.post("/tags")
async def create_tag(tag: TagCreate,user = Depends(get_current_user)):
    name = tag.name.strip().lower()

    existing = await tags_collection.find_one({"name": name})
    if existing:
        raise HTTPException(400, "Tag already exists")

    await tags_collection.insert_one({"name": name})

    return {"message": "Tag created"}


@router.get("/tags", response_model=List[TagsResponse])
async def get_tags(user = Depends(get_current_user)):
    return await tags_collection.find({}, {"_id": 0}).to_list(None)





@router.put("/tags/{tag_id}")
async def update_tag(
    tag_id: str,
    new_data: TagCreate,
    user=Depends(get_current_user)
):
    
    if not ObjectId.is_valid(tag_id):
        raise HTTPException(400, "Invalid tag ID")

   
    existing = await tags_collection.find_one({
        "name": new_data.name.lower()
    })

    if existing:
        raise HTTPException(400, "Tag already exists")

    
    result = await tags_collection.update_one(
        {"_id": ObjectId(tag_id)},
        {"$set": {"name": new_data.name.lower()}}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Tag not found")

    return {"message": "Tag updated"}




@router.delete("/tags/{tag_id}")
async def delete_tag(tag_id: str, user=Depends(get_current_user)):

    if not ObjectId.is_valid(tag_id):
        raise HTTPException(400, "Invalid tag ID")

    
    existing = await tags_collection.find_one({"_id": ObjectId(tag_id)})
    if not existing:
        raise HTTPException(404, "Tag not found")

    tag_name = existing["name"]

    
    await task_collection.update_many(
        {},
        {"$pull": {"tags": tag_name}}
    )

    
    await tags_collection.delete_one({"_id": ObjectId(tag_id)})

    return {"message": "Tag deleted and removed from all tasks"}