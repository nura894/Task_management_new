import asyncio
from datetime import datetime, timezone, timedelta


async def send_reminder(task_id: str, due_date: datetime):
    try:
        if due_date.tzinfo is None:
            due_date = due_date.replace(tzinfo=timezone.utc)
            
        now = datetime.now(timezone.utc)

        # calculate time until reminder (1 hour before)
        reminder_time = due_date - timedelta(hours=1)

        delay = (reminder_time - now).total_seconds()
        
        print(f"NOW: {now}")
        print(f"REMINDER TIME: {reminder_time}")
        print(f"DELAY: {delay}")
        # if already past → don't schedule
        if delay <= 0:
            return

        await asyncio.sleep(delay)

        print(f"Reminder: Task {task_id} is due soon!")
    
    except asyncio.CancelledError:
        print(f"[CANCELLED] Reminder for task {task_id}")
 
 
 
    
reminder_jobs = {}    
    
def cancel_reminder(task_id: str):
    task = reminder_jobs.get(task_id)

    if task:
        task.cancel()   # stops the async task
        del reminder_jobs[task_id]




def schedule_reminder(task_id: str, due_date: datetime):
    
    # cancel old reminder if exists
    cancel_reminder(task_id)

    task = asyncio.create_task(send_reminder(task_id, due_date))

    reminder_jobs[task_id] = task
    