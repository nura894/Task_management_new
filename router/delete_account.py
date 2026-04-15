from fastapi import APIRouter, Depends, HTTPException, status
from utils.dependencies import get_current_user
from sqlalchemy.orm import Session
from database.db_postgres import get_db
from database.database_mongo import task_collection



router = APIRouter(prefix="/user", tags=["User_Update"])

@router.delete('/delete', status_code=status.HTTP_200_OK)
def delete_account(
    db : Session = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        task_collection.delete_many({
            "user_id": user.id
        })
        
        db.delete(user)
        db.commit()
        
        return {"message": "user successfully deleted"}
    
    except HTTPException as e:
        db.rollback()
        raise e
    
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        