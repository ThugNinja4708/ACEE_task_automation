import json
import requests
import logging
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'eyJraWQiOiJSbENXRENCQ2NRbGdtTGVPcDlCcnMwV2VPQTluS1ZHZUNFTnJFQWJaeGlvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoicUhXVnhFVkFZcV9JS3ZDVXFIcFktdyIsInN1YiI6ImI3MjUwZWE0LTZmMzAtNDliOC1iZWRlLTYwYTQ0M2EzMDg2NyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9kVkdSY2RLUTFfY3liZXJhcmstaWRlbnRpdHkiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZFZHUmNkS1ExIiwiY29nbml0bzp1c2VybmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5X3JrYW50aGFAY3liZXJhcmsuY29tIiwibm9uY2UiOiIwdl9iQWJXT0ROZFctUXltYkpRTEphRmpKdlBNdkhuV3lzQ3UwWF9pd0Zra0hfdkUwcFpmbG1ZQ2M5dDM0Y1hXWFg2V1pwdl9tcE8wRUZFalNiMmZSV2xRa3VvOEcxZjBXaTJ0RHJUNUoyMklwOU43c2JESXlMY0Znc29jTXNwcEJMSWMwZkdpZWZRTUpOenI0OHFjVzJvX180d2FVVmQ0T2YxaVRJX0JaOTgiLCJhdWQiOiI2cXFucGxvNWJjZmFraDRjamZwOGhtb3RucCIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6InJrYW50aGFAY3liZXJhcmsuY29tIiwicHJvdmlkZXJOYW1lIjoiY3liZXJhcmstaWRlbnRpdHkiLCJwcm92aWRlclR5cGUiOiJTQU1MIiwiaXNzdWVyIjoiaHR0cHM6XC9cL2FhZTQyMjIubXkuaWRhcHRpdmUuYXBwXC8xNzZjNDA5Yi0wNTRhLTQ4ZjQtOWRjMi1jOWU3MjM4ZDhkOWEiLCJwcmltYXJ5IjoidHJ1ZSIsImRhdGVDcmVhdGVkIjoiMTY3Mjg0MzMwMDQzNSJ9XSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2ODA1MTcwMjIsImN1c3RvbTpVU0VSX0dST1VQUyI6InBDbG91ZENvbnNvbGVPcHNQUkQiLCJleHAiOjE2ODA1MzE0MjIsImlhdCI6MTY4MDUxNzAyMn0.SZ9zbtsp7A7C_-zCbJqv5wzcPz1RPQvdGtul1ZbVp1VZOWKOhLFJTxBXg8limtkDi0eOQpyhTV3QwRZBiyjKHS8EBKGvhLoFUgyUxaGzHv5PB1qJxTg28CJI5-0EAWENM7fz2ijGc0rDasx-jQbGpcHcyuOfBta28NCPacw2ID8SnKpIGhA0xAMIh1jR-Yw_ycAxmu00m05X0xedrYCui-4J-M9IMj0DNVqJW-oLbNvulJwdIiaGuGsY0360ljvPr1dLnE4dAGWt0OE2d3QxYSYRin1TWDNBjtK1JaQbDRnu0QW1SYO8g4qfAUDK5h_GSH1P8h8jyooMirL6K-_e9Q',
}
CONSOLE_URL = 'https://console.privilegecloud.cyberark.com'

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S")
session = requests.Session()


def get_all_tenants():
    url = f'{CONSOLE_URL}/tenants/v1/lean'
    try:
        response = session.get(url, headers=HEADERS)
          # raise exception if status code is not 2xx
    except (Exception) as error:
        logging.error(f"GET_ALL_TENANTS MSG: Error Retreiving all tenants - {error}")

    logging.info(f"GET_ALL_TENANTS MSG: Data Retreival Successful")
    return response.json()


def get_tenants_by_region(region):
    url = f'{CONSOLE_URL}/tenants/v1?region={region}'
    try:
        response = session.get(url, headers=HEADERS)
          # raise exception if status code is not 2xx

    except (Exception) as error:
        logging.error(f"GET_TENANT_BY_REGION MSG: Error Retreiving tenants by region - {error}")

    logging.info(f"GET_TENANT_BY_REGION")
    return response.json()


def get_tenant_by_customer_id(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/{customer_id}'
    try:
        response = session.get(url, headers=HEADERS)
        #   # raise exception if status code is not 2xx
    except (Exception) as error:
        logging.error(f"GET_TENANT_BY_CUSTOMER_ID MSG: Error Retreiving tenant by customer ID - {error}")
        return None
    return response.json()

def get_public_ips(customer_id):
    try:
        res = get_tenant_by_customer_id(customer_id)
        if res is None:
            logging.warning(f"No tenant found for customer ID {customer_id}")
            return []
        customer_public_ips = res.get('customerPublicIPs', [])
        logging.info(f"GET_PUBLIC_IPS MSG: Retrieve public IPs SUCCESSFUL - {customer_id}")
        return customer_public_ips
    except Exception as e:
        logging.error(f"GET_PUBLIC_IPS MSG: Error fetching public IPs - {e}")
        return []



def update_public_ips(customer_id: str(), ips_to_add: list(), add_or_remove: bool):
    try:
        current_ips = get_public_ips(customer_id)
        logging.info(f"UPDATE_PUBLIC_IPS MSG: Retrieve public IPs SUCCESSFUL - {customer_id}")
    except (Exception) as err:
        logging.error(f'UPDATE_PUBLIC_IPS failed to fetch public ips of customer ID {customer_id}-{err}')
        return {'err': f"Error occured while retrieving public IPs - {err}"}
    
    try:
        if(add_or_remove == True):
            updated_ips = current_ips + ips_to_add
        else:
            updated_ips = current_ips.remove(ips_to_add)
        
    except (Exception) as err:
        logging.error(f'FAILED to update public ips of customer ID {customer_id}-{err}')
        return {'err': f"Error occured while updating public IPs - {err}"}


    url = f"{CONSOLE_URL}/tenants/v1/{customer_id}/config"
    payload = json.dumps({"customerPublicIPs": updated_ips})

    try:
        response = session.patch(url, headers=HEADERS, data=payload)
        
        # 
    except (Exception) as err:
        logging.error(f'UPDATE_PUBLIC_IPS Msg: Failed to update public Ips - {err}')
        return {'err': f"Error occured while updating public IPs"}

    logging.info(f"UPDATE_PUBLIC_IPS MSG: Public Ips Update SUCCESSFUL for Customer - {customer_id}")
    return response.json()


def get_task_status(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/tasks?mainObjectId={customer_id}'
    try:
        response = session.get(url, headers=HEADERS)
        
    except (Exception) as err:
        logging.error(f'GET_TASK_STATUS MSG: Failed to fetch task status - {err}')
        return {"err":'GET_TASK_STATUS MSG: Failed to fetch task status - {err}'}
    logging.info(f'GET_TASK_STATUS MSG: Task status fetch SUCCESSFUL')
    # print(response.json())
    latest_task = response.json()[0]
    print(latest_task)
    # print(latest_task)
    return latest_task

def deploy_feature_H5GW(customer_id):
    url = f"{CONSOLE_URL}tenants/v1/{customer_id}/features/html5gw"
    try:
        response = session.post(url, headers=HEADERS, data={})
        
        logging.info(f"DEPLOY_FEATURE_H5GW MSG: Deploy HTML5GW feature SUCCESSFUL - {customer_id}")
        return response.json()
    except (Exception) as err:
        logging.error(
            f"DEPLOY_FEATURE_H5GW MSG: failed to deploy HTML5GW feature to customer - {customer_id} - error - {err}")

    logging.info(
        f"DEPLOY_FEATURE_H5GW MSG: Deploy HTML5GW feature SUCCESSFUL - {customer_id}")
    return response.json()


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
        response = session.post(url, headers=HEADERS,data=payload, files=files)
        

    except (Exception) as err:
        logging.error(
            f"INSTALL_PSM_CERTIFICATE MSG: Error occured while installing PSM certs - {err}")
        return {'err': 'INSTALL_PSM_CERTIFICATE UNSUCCESSFUL'}

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
    files = [('files', (file_name[file_name.index("_")+1:], open(f"database_files/{file_name}", 'rb'), 'application/octet-stream')) for file_name in ldap_files]

    try:
        HEADERS.pop('Content-Type')
        response = session.post(url, headers=HEADERS,
                                 data=payload, files=files)
        

    except (Exception) as err:
        logging.error(
            f"INSTALL_LDAP_CERTS MSG: POST API call failed with error - {err}")
        return {'err': f"install_LDAP_certs failed with error - {err}"}

    logging.info(f"INSTALL_LDAP_CERTS MSG: SUCCESSFUL - {customer_id}")
    return response.json()
