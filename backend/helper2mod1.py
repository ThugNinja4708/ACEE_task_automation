import time
from datetime import datetime
import logging
from psycopg2 import Error
from decouple import config
from pcloudapis import update_public_ips,install_LDAP_certs,install_PSM_certs
from db_conn_pool import getConnPool
from pcloudapis import get_task_status, update_public_ips


conn_pool = getConnPool()
queue = list()
lockedCustomers = list()


def fprint(process,process_state,taskId,task_status):
    print(f"--| {process} {process_state} for taskId: {taskId} \t| task_status {task_status} ")
    

def queueing(task):
    task.status = "WAITING_IN_QUEUE"
    queue.append(task)
    fprint("Queueing","started",task.task_id,task.status)
    do_task(task)
    

def do_task(task):
    if task.customer_id not in lockedCustomers:
        task.status="PCLOUD_API_CALLED"
        lockedCustomers.append( task.customer_id)
        fprint("lock","started",task.task_id,task.status)
        api_call(task)
    else:
        return


def api_call(task):
    dbmsg={}
    fprint("API_call","started",task.task_id,task.status)
    if task.type_of_task == 1:
        response = update_public_ips(task.customer_id, task.task_data.split(','), add_or_remove=True)
    elif task.type_of_task == 2:
        response = update_public_ips(task.customer_id, task.task_data.split(','), add_or_remove=False)
    elif task.type_of_task == 3:
        response = install_PSM_certs(task.customer_id,task.task_data.split(','))
    elif task.type_of_task == 4:
        response = install_LDAP_certs(task.customer_id,task.task_data.split(','))
    else:
        return

    if response["api_status"]=="OK":
        task.status="IN_PROGRESS"
    else:
        task.status="API_CALL_FAIL"
        lockedCustomers.remove(task.customer_id)
        queue.remove(task)
        dbmsg["error_message"]=response.get("svcMessage")
        # print("+",type(response),response)
    dbmsg["status"]=task.status

    fprint("API_call","completed",task.task_id,task.status)
    db_update(task,dbmsg)


def db_update(task,msg):
    fprint("DB_update","started",task.task_id,task.status)
    task_id = task.task_id
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                print(type(msg),msg)
                for key,val in msg.items():
                    queryToUpdateApprovedDate = "UPDATE service_requests SET " + key + " = %s WHERE task_id = %s;"
                    cursor.execute(queryToUpdateApprovedDate, (val,task_id))
                    print(key,val)

                conn.commit()
        fprint("DB_update","completed",task.task_id,task.status)

    except (Error)  as error:
        print(error)
        fprint("DB_update","Failed",task.task_id,task.status)
        



#----------------


def get_status():
        for task in list(queue):
            dbmsg={}
             
            if task.status == "IN_PROGRESS":
                fprint("Status","checking",task.task_id,task.status)
                response = get_task_status(task.customer_id)
                if response["status"]=="FAILED":
                    task.status = "FAILED"
                    task.error_message = response.get("params", None).get("flowErrorDescription", "flowNotCreated")
                    task.completed_date = str(datetime.now().date())
                    dbmsg={"status":task.status,"error_message":task.error_message,"completed_date":task.completed_date}
                elif response["status"]=="SUCCESS":
                    task.status = "SUCCESS"
                    dbmsg={"status":task.status,"completed_date":task.completed_date}
                else:
                    continue

                fprint("Task","ended",task.task_id,task.status)
                lockedCustomers.remove(task.customer_id)
                queue.remove(task)
                db_update(task,dbmsg)
                for nextTask in list(queue):
                    if nextTask.customer_id==task.customer_id:
                        do_task(nextTask)
                    else:
                        continue

