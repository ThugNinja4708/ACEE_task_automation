from flask import Flask,request
# import pCloudConsoleAPIs as pCloud
from psycopg2 import Error
import os
from datetime import datetime
from db_conn_pool import getConnPool
import time
import logging
from decouple import config
import helper2
from user_class import REQUEST

import threading


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, filename='app.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%m-%Y %H:%M:%S')

conn_pool = getConnPool()


def upload_files(files):
    file_list = list()
    for file in files:
        file_name = f"{time.time_ns()}_{file.filename}"
        file_path = os.path.join("database_files", file_name)
        file.save(file_path)
        file_list.append(file_name)
    return ",".join(file_list)

@app.route("/getRequests", methods=["POST"]) 
def getRequestsForClient() -> list() : 
    ############## REQUEST FORMDATA #################
    support_id = request.form['support_id']
    #################################################
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                queryToRetrieveRequest = f"SELECT * FROM service_requests WHERE support_id = (%s) ORDER BY task_id DESC; "
                cursor.execute(queryToRetrieveRequest, (support_id))
                rows = cursor.fetchall()
        list_of_tasks = list()
        
        for row in rows:
            list_of_tasks.append(REQUEST(*row).convert_to_json())
        logging.info(f"API: /getRequests MSG: Data retrieved from database successfully!")
    except (Exception, Error) as error:
        logging.error(f"API: /getRequests MSG: Error occured while retrieving data from the database - {error}")
        return {"err": f"Error occured while retrieving data from the database: {error}"}
    else:
        return {"response_data":list_of_tasks}

@app.route("/insertIntoDatabase", methods=['POST'])
def add_data() -> dict():
    ############## REQUEST FORMDATA #################
    support_id = request.form['support_id']
    customer_id = request.form['customer_id']
    type_of_task = request.form['type_of_task']
    description = request.form['description']
    created_date = str(datetime.now().date())
    #################################################
    # if task == ipwhitelist add or remove
    if type_of_task in ['1', '2']:
        task_data = request.form["task_data"]

    # task == ldap cert upload or psm cert
    elif type_of_task in ['3', '4']:
        task_data = upload_files(request.files.getlist('body'))

    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO service_requests (customer_id, support_id, type_of_task, task_data, description, created_date, status) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),'WAITING_FOR_APPROVAL');", (customer_id, support_id, type_of_task, task_data,description, created_date))
                conn.commit()
        logging.info("API: /insertIntoDatabase MSG: Data added successfully")
        return {"msg": "Data added successfully"}

    except (Exception, Error) as error:
        logging.error("API: insertIntoDatabase MSG: Error while adding data to database - %s", error)
        return {"err": "Error while adding data to database"}


@app.route('/approveRequest', methods=['POST'])
def approveRequest():
  
    ############## REQUEST FORMDATA #################
    task_id = request.form['task_id']
    approval_date = str(datetime.now().date())
    #################################################
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                queryToUpdateApprovedDate = "UPDATE service_requests SET approval_date = (%s) WHERE task_id = (%s);"
                cursor.execute(queryToUpdateApprovedDate, (approval_date,task_id))
                queryToGetRequest = "SELECT * FROM service_requests WHERE task_id = (%s) ;"
                cursor.execute(queryToGetRequest,(task_id,))
                conn.commit()
                row = cursor.fetchone()
        helper2.queueing(REQUEST(*row)) # REQUEST object
        logging.info("API: /approveRequest MSG: Data recevied from DB Successfully.!" )
        return {"msg": "Approved..!"}
    except (Exception, Error) as error:
        logging.error(f"API: /approveRequest MSG: Error occured while retrieving data from the database - {error}")
        return {"err": f"Error occured while retrieving data from the database: {error}"}
# app.run(debug=True)

############################################## TESTING DONT USE THESE #############################

@app.route("/verifyLogin", methods=["POST"])
def verifyLogin(): 
    ############## REQUEST FORMDATA #################
    user_name = request.form['user_name']
    password = request.form['password']  # decode the password
    #################################################
    
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                selectQueryToGetUserDetails = f"SELECT user_name, password FROM users WHERE user_name = (%s) AND password = (%s);"
                cursor.execute(selectQueryToGetUserDetails,(user_name, password))
                noOfRows = cursor.rowcount
        logging.info(f"API: /verifyLogin MSG: Data retrieved from database successfully!")
                
    except (Exception, Error) as error:
        logging.error(f"API: /verifyLogin MSG: Error occured while verifying the user details - {error}")
        return {"err": f"Error occured while verifying the user details - {error}"}
    
    if noOfRows == 1:
        return {"isFound": True}
    else:
        return {"isFound": False}


status_check_thread = threading.Thread(target=helper2.get_status, name="status check")
status_check_thread.start()


app.run(debug=True)
# if __name__ == '__main__':
#     get_status_thread = threading.Thread(target=start_get_status)
#     get_status_thread.start()
#     # get_status_thread.join()
#     app.run(debug=True, port=5000, host="127.0.0.1")
