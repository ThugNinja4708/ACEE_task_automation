import json
import requests
import logging
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'eyJraWQiOiJSbENXRENCQ2NRbGdtTGVPcDlCcnMwV2VPQTluS1ZHZUNFTnJFQWJaeGlvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiOUtmSHdiVTJRRklIc1NORVBIcVZjQSIsInN1YiI6ImQ3Njk5YTgzLTNkNTctNDdmZS04NTczLWNiZWIwYjE4YWJmZSIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9kVkdSY2RLUTFfY3liZXJhcmstaWRlbnRpdHkiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZFZHUmNkS1ExIiwiY29nbml0bzp1c2VybmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5X3NraWxhbWJpQGN5YmVyYXJrLmNvbSIsIm5vbmNlIjoiaDNValhIeGZtQnJPdmVUN3p4elVwN0FkYkt4dHJaeGZZNGNRb3VLUF9KbjZRbzJyNUF5eVRnc0NzaGJmSXNONjY4eGVRemhnNEZVYkxkVm4xTFA2RHMxMXh6OVNaMHNFTzQzeFVleWpXNWhIaTlsVkoyQm5ENU1Zb1J0TVVfby1Ea1llMnQ1ZnIybF9VSzlHVVdFUzZMbk9EeWRNTGRoVlJlY3huazBWZ04wIiwiYXVkIjoiNnFxbnBsbzViY2Zha2g0Y2pmcDhobW90bnAiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiJza2lsYW1iaUBjeWJlcmFyay5jb20iLCJwcm92aWRlck5hbWUiOiJjeWJlcmFyay1pZGVudGl0eSIsInByb3ZpZGVyVHlwZSI6IlNBTUwiLCJpc3N1ZXIiOiJodHRwczpcL1wvYWFlNDIyMi5teS5pZGFwdGl2ZS5hcHBcLzE3NmM0MDliLTA1NGEtNDhmNC05ZGMyLWM5ZTcyMzhkOGQ5YSIsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNjcyODM1MjQ4ODA3In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY4MzU0MjY5MywiY3VzdG9tOlVTRVJfR1JPVVBTIjoicENsb3VkQ29uc29sZU9wc1BSRCIsImV4cCI6MTY4MzU1NzA5MywiaWF0IjoxNjgzNTQyNjkzfQ.IdwXJbSyGAAEXBJwoDZxyvaOkrS919HKg2W_YHIdgRqOJovGRqHL3lVCoBAqOBpj535KJb2qoH6OlMw9PgLoOseoGg0gTIvyfdaH0CNpqOEPz-KRXx2Mxpxs3KcMe510gHt0yk-1ywqmr6iX1pAwbLi6g_iIpKG5FTqjZ-mvYzEfDCrox3AC3IEnnkca0z8PkM4nIjttOFplnsq2rHck0dZGOXbjWXIK2mv-NPCeSZifqGtJCq1ti8vZ16n51LFsyqyEB-e_kNq5HEM9rMt64xxVffjvDssVdHCpu7ZQcGL2c9YhSYy-g387IcDQ8IW8niNxsPh_tgyftqmZMSvkAw',
}
CONSOLE_URL = 'https://console.privilegecloud.cyberark.com'

logging.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S")
session = requests.Session()




def get_tenant_by_customer_id(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/{customer_id}'
    try:
        response = session.get(url, headers=HEADERS)
        if response.ok:
            response=response.json()
            response["api_status"]="OK"
            return response
        else:
            err_msg={"Api":"/tenants/v1/customer_id","api_status":"NOTOK","status":response.json().get("status",404),"svcMessage":response.json().get("svcMessage","svcMessageNotFound"),"errorCategory":response.json().get("errorCategory","errorCategoryNotFound"),"error":"ApiError"} 
            raise Exception(err_msg)
    except (Exception) as error:
        logging.error(f"GET_TENANT_BY_CUSTOMER_ID MSG: Error Retreiving tenant by customer ID - {error}")
        raise
   


def get_public_ips(customer_id):
    try:
        response = get_tenant_by_customer_id(customer_id)
        if response.get('customerPublicIPs') != None:
            customer_public_ips = response.get('customerPublicIPs', [])
            logging.info(f"GET_PUBLIC_IPS MSG: Retrieve public IPs SUCCESSFUL - {customer_id}")
            return customer_public_ips
        else:
            err_msg={"error":"CustomerPublicIPs' not present in response"}
            raise Exception(err_msg)
    except Exception as error:
        logging.error(f"GET_PUBLIC_IPS MSG: Error fetching public IPs - {error}")
        raise


def update_public_ips(customer_id: str, ips_to_add: list, add_or_remove: bool) -> dict:
    err_msg={}
    try:
        current_ips = get_public_ips(customer_id)
        logging.info(f"UPDATE_PUBLIC_IPS MSG: Retrieve public IPs SUCCESSFUL - {customer_id}")
    
        if (add_or_remove == True):
            updated_ips = current_ips + ips_to_add
        else:
            updated_ips = current_ips.remove(ips_to_add)

        # except (Exception) as err:
        #     logging.error(f'FAILED to update public ips of customer ID {customer_id}-{err}')
        #     return {'err': f"Error occured while updating public IPs - {err}"}

        url = f"{CONSOLE_URL}/tenants/v1/{customer_id}/config"
        payload = json.dumps({"customerPublicIPs": updated_ips})

        # try:
        response = session.patch(url, headers=HEADERS, data=payload)
        
        if response.ok:
            response=response.json()
            response["api_status"]="OK"
            return response
        else:
            response=response.json()
            
            if response.get("Message") != None:
                err_msg={"Api":"/tenants/v1/customer_id/config","api_status":"NOTOK","status":response.get("status",404),"Message":response.get("Message"),"error":"ApiError"}
                raise Exception(err_msg)
            else:
                err_msg={"Api":"/tenants/v1/customer_id/config","api_status":"NOTOK","status":response.get("status",404),"svcMessage":response.get("svcMessage","svcMessageNotFound"),"errorCategory":response.get("errorCategory","errorCategoryNotFound"),"error":"ApiError"} 
                raise Exception(err_msg)
            
            #
            # return {'err': f"Error occured while updating public IPs"}
            logging.info(f"UPDATE_PUBLIC_IPS MSG: Public Ips Update SUCCESSFUL for Customer - {customer_id}")
            
    except (Exception) as err:
        logging.error(f'UPDATE_PUBLIC_IPS Msg: Failed to update public Ips - {err}')
        
        
        return err_msg


def get_task_status(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/tasks?mainObjectId={customer_id}'
    try:
        response = session.get(url, headers=HEADERS)

    except (Exception) as err:
        logging.error(f'GET_TASK_STATUS MSG: Failed to fetch task status - {err}')
        return {"err": 'GET_TASK_STATUS MSG: Failed to fetch task status - {err}'}
    logging.info(f'GET_TASK_STATUS MSG: Task status fetch SUCCESSFUL')
    # print(response.json())
    latest_task = response.json()[0]
    print(latest_task)
    # print(latest_task)
    return latest_task


# def deploy_feature_H5GW(customer_id):
#     url = f"{CONSOLE_URL}tenants/v1/{customer_id}/features/html5gw"
#     try:
#         response = session.post(url, headers=HEADERS, data={})

#         logging.info(f"DEPLOY_FEATURE_H5GW MSG: Deploy HTML5GW feature SUCCESSFUL - {customer_id}")
#         return response.json()
#     except (Exception) as err:
#         logging.error(
#             f"DEPLOY_FEATURE_H5GW MSG: failed to deploy HTML5GW feature to customer - {customer_id} - error - {err}")

#     logging.info(
#         f"DEPLOY_FEATURE_H5GW MSG: Deploy HTML5GW feature SUCCESSFUL - {customer_id}")
#     return response.json()


def install_PSM_certs(customer_id, psm_files):
    payload = {'description': 'this is file description'}
    files = []
    path = "database_files"
    for file_name in psm_files:
        fileName = file_name[file_name.index("_")+1:]
        files.append(('files', (fileName, open(
            path + "\\" + file_name, 'rb'), 'application/octet-stream')))

    url = f"{CONSOLE_URL}files/v1/installPsmCertificate/{customer_id}"
    try:
        HEADERS.pop('Content-Type')
        response = session.post(url, headers=HEADERS,
                                data=payload, files=files)

    except (Exception) as err:
        logging.error(
            f"INSTALL_PSM_CERTIFICATE MSG: Error occured while installing PSM certs - {err}")
        return {'err': f"Error occured while updating PSM CERTS - {err}"}

    logging.info(
        f"INSTALL_PSM_CERTIFICATE MSG: Certificates installation SUCCESSFUL - {customer_id}")
    return response.json()


def install_LDAP_certs(customer_id, ldap_files):
    payload = {'description': 'this is file description'}
    files = list()
    path = "database_files"

    for file_name in ldap_files:
        fileName = file_name[file_name.index("_")+1:]
        files.append(('files', (fileName, open(
            path + "\\" + file_name, 'rb'), 'application/octet-stream')))

    url = f"{CONSOLE_URL}/files/v1/installCertificate/{customer_id}"
    files = [('files', (file_name[file_name.index("_")+1:],
              open(f"database_files/{file_name}", 'rb'), 'application/octet-stream')) for file_name in ldap_files]
    try:
        HEADERS.pop('Content-Type')
        response = session.post(url, headers=HEADERS,data=payload, files=files)

    except (Exception) as err:
        logging.error(f"INSTALL_LDAP_CERTS MSG: POST API call failed with error - {err}")
        return {'err': f"install_LDAP_certs failed with error - {err}"}
    logging.info(f"INSTALL_LDAP_CERTS MSG: SUCCESSFUL - {customer_id}")
    return response.json()
