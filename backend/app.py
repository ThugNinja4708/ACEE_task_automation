from flask import Flask, render_template, request, redirect, url_for, jsonify
# import pCloudConsoleAPIs as pCloud
import json
from psycopg2 import Error
import psycopg2
import psycopg2.pool
import os
from datetime import datetime
from db_conn_pool import getConnPool
import time
import logging
from decouple import config
from collections import OrderedDict
import helper2
from user_class import REQUEST
import asyncio
import threading


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

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
                queryToRetrieveRequest = f"SELECT * FROM service_requests WHERE support_id = (%s) ORDER BY created_date DESC; "
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
    # Data Formatting 
    # list_of_service_requests list()
    # for row in rows:
    #     service_request = {}
    #     service_request['task_id'],service_request['customer_id'],service_request['task'], service_request['task_data'], service_request['status'], service_request['create_date'], service_request['complete_date'] = row
    #     list_of_service_requests.append(service_request)

@app.route("/insertIntoDatabase", methods=['POST'])
def add_data() -> dict():
    support_id = request.form['support_id']
    customer_id = request.form['customer_id']
    type_of_task = request.form['type_of_task']
   # description = request.form['description']
    created_date = str(datetime.now().date())

    # if task == ipwhitelist add or remove
    if type_of_task in ['1', '2']:
        task_data = request.form["task_data"]

    # task == ldap cert upload or psm cert
    elif type_of_task in ['3', '4']:
        task_data = upload_files(request.files.getlist('body'))

    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO service_requests (customer_id, support_id, type_of_task, task_data, created_date,status) VALUES ((%s),(%s),(%s),(%s),(%s),'WAITING_FOR_APPROVAL');", (customer_id, support_id, type_of_task, task_data, created_date))
                conn.commit()
        logging.info("API: /insertIntoDatabase MSG: Data added successfully")
        return {"msg": "Data added successfully"}

    except (Exception, Error) as error:
        logging.error("API: insertIntoDatabase MSG: Error while adding data to database - %s", error)
        return {"err": "Error while adding data to database"}


@app.route('/approveRequest', methods=['POST'])
def approveRequest():

    # cid = request.form['customer_id']
    # tid = request.form['task_id']
    # task = REQUEST(type_of_task=1, task_data="10.10.10.10", support_id=1,
    # customer_id=cid, task_id=tid, status="WAITING_FOR_APPROVAL")
    # task.approval_date = str(datetime.now().date())
    # task.created_date = str(datetime.now().date())
  

    ############## REQUEST FORMDATA #################
    task_id = request.form['task_id']
    approval_date = str(datetime.now().date())
    # task_data = request.form['task_data']
    # list_task_id = [(x,) for x in list_task_id]
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



def start_get_status():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(helper2.get_status())
    print("hi")


# def upload_files(files):
#     file_list = list()
#     for file in files:
#         file_name = f"{time.time_ns()}_{file.filename}"
#         file_path = os.path.join("database_files", file_name)
#         file.save(file_path)
#         file_list.append(file_name)
#     return ",".join(file_list)

if __name__ == '__main__':
    get_status_thread = threading.Thread(target=start_get_status)
    get_status_thread.start()
    # get_status_thread.join()
    app.run(debug=True, port=5000, host="127.0.0.1")