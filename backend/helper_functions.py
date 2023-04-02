from collections import OrderedDict
import time
import asyncio
import datetime
import logging
from decouple import config
from pcloudapis import get_task_status
from db_conn_pool import getConnPool

conn_pool = getConnPool()


class QUEUE:

    def __init__(self):
        self.general_queue = []
        self.running_queue = []
        self.waiting_queue = []

    def queueing(self, task):
        print("method: queueing start")
        task.status = "ADDED_TO_QUEUE"
        # UPDATE STATUS IN DB
        self.general_queue.append(task)

        for general_item in self.general_queue:
            general_item_in_running_queue = -1
            for running_item in self.running_queue:
                if general_item.customer_id == running_item.customer_id:
                    general_item_in_running_queue = 1
                    break

            if general_item_in_running_queue == -1:
                print(f"general_item_in_running_queue == -1 for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
                self.running_queue.append(general_item)
                self.general_queue.remove(general_item)
                api_call(general_item)
            elif general_item_in_running_queue == 1:
                print(
                    f"general_item_in_running_queue == 1 for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
                self.waiting_queue.append(general_item)
                self.general_queue.remove(general_item)
        print("method: queueing finish")
    

    # async def main():
    # task = asyncio.create_task(get_status())

    # await main()

    async def get_status(self):
        print("method: get_status first call")
        while True:
            for taskitem in self.running_queue:
                if taskitem.status == "IN_PROGRESS":
                    # task history api call || api_call(taskitem)
                    response = get_task_status(taskitem.customer_id)
                    print(
                        f"method: after get_task_status for -- taskid: {taskitem.task_id} on cust_id:{taskitem.customer_id} status:{taskitem.status}")
                    if response["status"] == "SUCCESS" or response["status"] == "FAILED":
                        self.running_queue.remove(taskitem)
                        taskitem.status = response["status"]
                        taskitem.completed_date = datetime.now().date()
                        if response["status"] == "FAILED":
                            taskitem.error_message = response["params"]["flowErrorDescription"]
                        print(
                            f"method: after STATUS = SUCCES OR FAILURE for -- taskid: {taskitem.task_id} on cust_id:{taskitem.customer_id} status:{taskitem.status}")
                        # db update
                        update_db(taskitem)
                        print(
                            f"method: update_db msg:  update_db method COMPLETED for -- taskid: {taskitem.task_id} on cust_id:{taskitem.customer_id} status:{taskitem.status}")
                        if taskitem.customer_id in self.waiting_queue:
                            self.waiting_queue.remove(taskitem)
                            self.running_queue.append(taskitem)
                            print(f"method: moved from waiting q to running q for  ")
            await asyncio.sleep(5)
            print("method: get_status after asyncio 120sec")


def api_call(task):
    print(f"method: api_call msg: api called for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
    time.sleep(5)
    task.status = "IN_PROGRESS"
    print(f"method: api_call msg: api call FINISH for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")


def update_db(task):
    print(f"method: update_db msg: INSIDE updatedb for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")

    task_id = task.task_id
    customer_id = task.customer_id
    support_id = task.support_id
    type_of_task = task.type_of_task
    task_data = task.task_data
    status = task.status
    created_date = task.created_date
    description = task.description
    error_message = task.error_message
    approval_date = task.approval_date
    completed_date = task.completed_date

    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE {} SET task_id = (%s),customer_id= (%s),support_id= (%s),type_of_task= (%s),task_data,status= (%s),created_date= (%s),description= (%s),error_message= (%s),approval_date= (%s),completed_date= (%s) WHERE task_id = (%s) ;".format(
                    config('DATABASE_TABLE')), (task_id, customer_id, support_id, type_of_task, task_data, status, created_date, description, error_message, approval_date, completed_date,task_id))
                conn.commit()

            logging.info(f"DB: Update MSG: {task.id} Data updated successfully")
            print(f"method: update_db msg:  DB UPDATED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")

            return {"msg": "Data updated successfully"}

    except Exception as error:
        logging.error("API: insertIntoDatabase MSG: Error while adding data to database - %s", error)
        print(f"method: update_db msg:  DB UPDATED FAILED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
        return {"err": "Error while adding data to database"}
