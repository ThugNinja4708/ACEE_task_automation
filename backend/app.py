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


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

conn_pool = getConnPool()


@app.route("/insertIntoDatabase", methods=['POST'])
def add_data():

    support_id = request.form['support_id']
    customer_id = request.form['customer_id']
    type_of_task = request.form['type_of_task']
   # description = request.form['description']
    created_date = str(datetime.now().date())

    # if task == ipwhitelist add or remove
    if (type_of_task == "1" or type_of_task == "2"):
        task_data = ','.join(request.form["task_data"])

    # task == ldap cert upload or psm cert
    elif (type_of_task == "3" or type_of_task == "4"):
        list = []
        files = request.files.getlist('body')
        for file in files:
            fileName = f"{str(time.time_ns())}_{file.filename}"
            file.save("database_files\\" + fileName)
            list.append(fileName)
        task_data = ",".join(list)

    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO service_requests (customer_id, support_id, type_of_task, task_data, created_date,status) VALUES ((%s),(%s),(%s),(%s),(%s),'WAITING_FOR_APPROVAL');", (
                    customer_id, support_id, type_of_task, task_data, created_date))
                conn.commit()
            logging.info(
                "API: /insertIntoDatabase MSG: Data added successfully")
            return {"msg": "Data added successfully"}

    except (Exception, Error) as error:
        logging.error(
            "API: insertIntoDatabase MSG: Error while adding data to database - %s", error)
        return {"err": "Error while adding data to database"}


@app.route('/approveRequest', methods=['POST'])
def approveRequest():

    cid = request.form['customer_id']
    tid = request.form['task_id']
    task = REQUEST(type_of_task=1, task_data="10.10.10.10", support_id=1,
                   customer_id=cid, task_id=tid, status="WAITING_FOR_APPROVAL")
    task.approval_date = str(datetime.now().date())
    task.created_date = str(datetime.now().date())
    helper2.queueing(task)
    return "bye"
    # ############## REQUEST FORMDATA #################
    # task_id = request.form['task_id']
    # # list_task_id = [(x,) for x in list_task_id]
    # #################################################
    # try:
    #     with conn_pool.getconn() as conn:
    #         with conn.cursor() as cursor:
    #             queryToGetRequest = "SELECT customer_id, type_of_task, task_data FROM requests WHERE task_id = (%s) ;"
    #             cursor.execute(queryToGetRequest)
    #             conn.commit()
    #             row = cursor.fetchall()
    #             print(row)
    # except (Exception, Error) as error:
    #     logging.error(f"API: /approveRequest MSG: Error occured while retrieving data from the database - {error}")
    #     return {"err": f"Error occured while retrieving data from the database: {error}"}
app.run(debug=True)

############################################## TESTING DONT USE THESE #############################

# async def main():
    
#     app.run(debug=True)
#     task = asyncio.create_task(helper2.get_status())
#     await task
#     print("ghg")


# if __name__ == "__main_":
#     asyncio.run(main())