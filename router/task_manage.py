from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.task_schema import TaskCreate,TaskResponse, TaskUpdate
from datetime import datetime, timezone
from database.database_mongo import task_collection
from utils.dependencies import get_current_user


router= APIRouter(prefix="/user", tags=["Task"])

@router.post("/tasks", status_code= status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user = Depends(get_current_user)
):
    try:
        task_dict = task.model_dump()   
        
        task_dict["user_id"] = current_user.id
        task_dict["created_at"] = datetime.now(timezone.utc)

        result = await task_collection.insert_one(task_dict)

        return {"msg": "Task created",
                "task_id": str(result.inserted_id)}
        
    except HTTPException :
        raise
    
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "Failed to make task")


@router.get("/tasks", response_model = List[TaskResponse])
async def get_tasks(current_user = Depends(get_current_user)):
    try:
        tasks = await task_collection.find({
            "user_id": current_user.id 
        }).to_list(100)
        
        if not tasks:
            return []

        for task in tasks:
            task["id"] = str(task["_id"])
            del task['_id']
            
        return tasks
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Failed to fetch tasks"
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
