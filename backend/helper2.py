import time
import datetime
import logging
import asyncio
from decouple import config
from pcloudapis import get_task_status
from db_conn_pool import getConnPool
from pcloudapis import get_task_status

conn_pool = getConnPool()

queue = []
lockedCustomers = []


def queueing(task):
    task.status = "WAITING_IN_QUEUE"
    queue.append(task)
    print(
        f"queing started for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
    do_task()


def do_task():
    while True:
        for task in queue:
            if task.customer_id not in lockedCustomers:
                task.status = "PCLOUD_API_CALLED"
                lockedCustomers.append(task.customer_id)
                print(f"LOCKED_CUSTOMER with cust_id:{task.customer_id}")
                print(
                    f"PCLOUD_API_CALLED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
                api_call(task)
                print(
                    f"PCLOUD_API_CALL_FINISH for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
                db_update(task, "IN_PROGRESS")


async def get_status():
    while True:
        for task in queue:
            if task.status == "PCLOUD_API_CALLED":
                print(
                    f"STATUS_CHECKING for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
                response = get_task_status(task.customer_id)
                if response["status"] == "SUCCESS" or response["status"] == "FAILED":
                    task.status = response["status"]
                    task.completed_date = str(datetime.now().date())
                    if response["status"] == "FAILED":
                        task.error_message = response["params"]["flowErrorDescription"]
                    print(
                        f"TASK_ENDED on -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
                    queue.remove(task)
                    # if task.customer_id in lockedCustomers:
                    lockedCustomers.remove(task.customer_id)
                    print(
                        f"FREED_CUSTOMER_ID on cust_id:{task.customer_id} status:{task.status}")
                    db_update(task, response["status"])
                    do_task()
            await asyncio.sleep(10)


def api_call(task):
    print(
        f"API_CALLED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
    time.sleep(5)


def db_update(task, status):
    task_id = task.task_id
    customer_id = task.customer_id
    support_id = task.support_id
    type_of_task = task.type_of_task
    task_data = task.task_data
    status = status
    created_date = task.created_date
    description = task.description
    error_message = task.error_message
    approval_date = task.approval_date
    completed_date = task.completed_date

    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:

                cursor.execute("UPDATE service_requests SET customer_id= (%s),support_id= (%s),type_of_task= (%s),task_data=(%s),status= (%s),created_date= (%s),description= (%s),error_message= (%s),approval_date= (%s),completed_date= (%s) WHERE task_id=(%s) ;", (
                    customer_id, support_id, type_of_task, task_data, status, created_date, description, error_message, approval_date, completed_date, task_id))
                conn.commit()

            print(
                f"DB UPDATED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
            return {"msg": "Data updated successfully"}

    except Exception as error:
        logging.error(
            " MSG: Error while UPDATING data to database - %s", error)
        print(
            f"DB UPDATED FAILED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
        return {"err": "Error while UPDATING data to database"}



async def main():
    # Create a task for get_status coroutine
    status_task = asyncio.create_task(get_status())
    
    # Create a task for do_task coroutine
    task_task = asyncio.create_task(do_task())
    
    # Run the event loop until all tasks are completed
    await asyncio.gather(status_task, task_task)

if __name__ == '__main__':
    asyncio.run(main())