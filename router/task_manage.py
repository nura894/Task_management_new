from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.task_schema import TaskCreate,TaskResponse, TaskUpdate
from datetime import datetime, timezone
from database.database_mongo import task_collection, categories_collection
from utils.dependencies import get_current_user
import asyncio
from services.reminder_service import schedule_reminder, send_reminder, cancel_reminder
from services.webhook_service import send_webhook

router= APIRouter(tags=["Task"])

@router.post("/tasks", status_code= status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user = Depends(get_current_user)
):
    try:
        category_exists = await categories_collection.find_one({
            "name": task.category
        })

        if not category_exists:
            raise HTTPException(400, "Invalid category")
        
        task_dict = task.model_dump()   
        
        task_dict["user_id"] = current_user.id
        task_dict["created_at"] = datetime.now(timezone.utc)

        result = await task_collection.insert_one(task_dict)
        task_id = str(result.inserted_id)
        
        if task.status != "completed":
            print("🚀 create_task API hit")
            asyncio.create_task(send_reminder(task_id, task.due_date))
        
            print(f"[REMINDER] Task {task_id} is due soon!")

        return {"msg": "Task created",
                "task_id": str(result.inserted_id)}
        
    except HTTPException :
        raise
    
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "Failed to make task")


from typing import List, Optional
from fastapi import Query

@router.get("/tasks", response_model=List[TaskResponse])
async def filter_tasks(
    category: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    current_user=Depends(get_current_user)
):
    try:
        query = {
            "user_id": current_user.id
        }

        
        if category:
            query["category"] = category.strip().lower()

       
        if tags:
            cleaned_tags = [tag.strip().lower() for tag in tags]
            query["tags"] = {"$in": cleaned_tags}

        tasks = await task_collection.find(query).to_list(length=None)

       
        for task in tasks:
            task["id"] = str(task["_id"])
            del task["_id"]

        return tasks

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch tasks"
        )
        
        
        
        

@router.get("/tasks/{task_id}", response_model =TaskResponse)
async def get_task(
    task_id: str,
    current_user =  Depends(get_current_user)
    ):
    try:

        if not ObjectId.is_valid(task_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

        task = await task_collection.find_one({
            "_id": ObjectId(task_id),
            "user_id" : current_user.id
        })

        if not task:
            return []

        task["id"] = str(task["_id"])
        del task['_id']

        return task
    
    except HTTPException :
        raise 
    except Exception as e:
        raise HTTPException(
           status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Failed to fetch task"
        )




@router.patch("/tasks/{task_id}")
async def update_task(
    task_id: str,
    task: TaskUpdate,
    current_user = Depends(get_current_user)
):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
        
        update_data = task.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided")
        
        existing_task = await task_collection.find_one({
                    "_id": ObjectId(task_id)
                })
        
        if not existing_task :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
        
        update_data['updated_at'] = datetime.now(timezone.utc)
        
        result = await task_collection.update_one(
            {
                "_id": ObjectId(task_id),
                "user_id": current_user.id
            },
            {
                "$set": update_data
            }
        )
        
        if result.matched_count ==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task no found")
        
        
        if update_data.get("status") == "completed":
            cancel_reminder(task_id)
            
            payload = {
                "task_id": task_id,
                "title": existing_task["title"],
                "user_id": str(current_user.id),
                "completed_at": datetime.now(timezone.utc).isoformat()
    }

            asyncio.create_task(send_webhook(payload))

        
        elif "due_date" in update_data:
            schedule_reminder(task_id, update_data["due_date"])
            
        
        return {"message": "task updated successfully"}
        
    except HTTPException:
        raise

    except Exception as e:
       raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )
       
       
    
@router.delete('/tasks/{task_id}')   
async def delete_task(
    task_id: str,
    current_user = Depends(get_current_user)
    ):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details="Invalid ID")
        
        result = await task_collection.delete_one({
            "_id":ObjectId(task_id),
            "user_id": current_user.id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task not found")
        
        return {"msg":"Task deleted successfully"}
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )


