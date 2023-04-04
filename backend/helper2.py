import time
from datetime import datetime
import logging

from decouple import config
from pcloudapis import update_public_ips,install_LDAP_certs,install_PSM_certs
from db_conn_pool import getConnPool
from pcloudapis import get_task_status, update_public_ips

conn_pool = getConnPool()

queue = list()
lockedCustomers = list()


def queueing(task):
    task.status = "WAITING_IN_QUEUE"
    queue.append(task)
    print(f"queing started for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
    do_task()


def do_task():
    for task in list(queue):
        if task.customer_id not in lockedCustomers:
            task.status = "PCLOUD_API_CALLED"
            lockedCustomers.append(task.customer_id)
            print(f"LOCKED_CUSTOMER with cust_id:{task.customer_id}")
            print(f"PCLOUD_API_CALLED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
            task = api_call(task)
            print(f"PCLOUD_API_CALL_FINISH for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
            db_update(task, task.status)
        else:
            print("")
            continue


def get_status():
    while True:
        for task in list(queue):
            if task.status == "PCLOUD_API_CALLED":
                print(f"STATUS_CHECKING for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
                response = get_task_status(task.customer_id)
                if response["status"] in ["SUCCESS", "FAILED"]:
                    task.status = response["status"]
                    task.completed_date = str(datetime.now().date())
                    if task.status == "FAILED":
                        task.error_message = response["params"]["flowErrorDescription"]
                    print(
                        f"TASK_ENDED on -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")

                    
                    # if task.customer_id in lockedCustomers:
                    lockedCustomers.remove(task.customer_id)
                    print(f"FREED_CUSTOMER_ID on cust_id:{task.customer_id} status:{task.status}")
                    db_update(task, task.status)
                    do_task()
                    queue.remove(task)
                else:
                    continue



def api_call(task):
    # update_public_ips(task.customer_id, task.task_data.split(","))
    if task.type_of_task == 1:
        response = update_public_ips(task.customer_id, task.task_data.split(','), add_or_remove=True)
    elif task.type_of_task == 2:
        response = update_public_ips(task.customer_id, task.task_data.split(','), add_or_remove=False)
    elif task.type_of_task == 3:
        response = install_PSM_certs(task.customer_id,task.task_data.split(','))
    elif task.type_of_task == 4:
        response = install_LDAP_certs(task.customer_id,task.task_data.split(','))

    print(response)
    if response["status"] != "IN_PROGRESS":
        task.status = "FAILED"
    else:
        task.status = response['status']

    print(f"API_CALLED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
    
    return task


def db_update(task, status):
    task_id = task.task_id
    status = status
    description = task.description
    error_message = task.error_message
    completed_date = task.completed_date

    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:

                cursor.execute("UPDATE service_requests SET status = (%s),description = (%s),error_message = (%s),completed_date = (%s) WHERE task_id=(%s) ;", (status, description, error_message, completed_date, task_id))
                conn.commit()

            print(f"DB UPDATED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
            return {"msg": "Data updated successfully"}

    except Exception as error:
        logging.error("MSG: Error while UPDATING data to database - %s", error)
        print(f"DB UPDATED FAILED for -- taskid: {task.task_id} on cust_id:{task.customer_id} status:{task.status}")
        return {"err": "Error while UPDATING data to database"}
