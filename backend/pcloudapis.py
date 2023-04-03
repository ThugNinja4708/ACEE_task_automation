import json
import requests
import logging
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'eyJraWQiOiJSbENXRENCQ2NRbGdtTGVPcDlCcnMwV2VPQTluS1ZHZUNFTnJFQWJaeGlvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiWVV6UVE0aEFGdkVmNWpzMWFxVlRMQSIsInN1YiI6ImI3MjUwZWE0LTZmMzAtNDliOC1iZWRlLTYwYTQ0M2EzMDg2NyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9kVkdSY2RLUTFfY3liZXJhcmstaWRlbnRpdHkiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZFZHUmNkS1ExIiwiY29nbml0bzp1c2VybmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5X3JrYW50aGFAY3liZXJhcmsuY29tIiwibm9uY2UiOiIyY1lyS3Z0NDM3bVBXU0tEbHVoSEhaQ2pqelpydk1adTJRVDBnbXJKbkJ4TzB1V0VXQWI1NW9HS1pRbEhHYlYxOHpYR01lTXRHX0RQQS1iNVktU2pYXzluSk5wSVR1THo1RzFKQVlUclAxdTJrLUFlX0xGSldXRTVBV2p3VDJCNFVDN3VRQWZwR3RLWC1lUnhWWXFuS0d2YjE1clZpNXhLVXppSGpYcVZvTDgiLCJhdWQiOiI2cXFucGxvNWJjZmFraDRjamZwOGhtb3RucCIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6InJrYW50aGFAY3liZXJhcmsuY29tIiwicHJvdmlkZXJOYW1lIjoiY3liZXJhcmstaWRlbnRpdHkiLCJwcm92aWRlclR5cGUiOiJTQU1MIiwiaXNzdWVyIjoiaHR0cHM6XC9cL2FhZTQyMjIubXkuaWRhcHRpdmUuYXBwXC8xNzZjNDA5Yi0wNTRhLTQ4ZjQtOWRjMi1jOWU3MjM4ZDhkOWEiLCJwcmltYXJ5IjoidHJ1ZSIsImRhdGVDcmVhdGVkIjoiMTY3Mjg0MzMwMDQzNSJ9XSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2ODA0OTYzOTYsImN1c3RvbTpVU0VSX0dST1VQUyI6InBDbG91ZENvbnNvbGVPcHNQUkQiLCJleHAiOjE2ODA1MTA3OTYsImlhdCI6MTY4MDQ5NjM5Nn0.a5pQBSrARkMCkr5eX8L9d4hfy7DTC_MdV0TEdbnf-EbID8nSpl3n1N3QRM8QnV7TuBKXju3sv39iU4SUAkWOwqS1ZjVGtoUwfOy1e6Y7CWaBdP3c-OSu6d6uct3m77dvwPHfiw8TRD0_F8ACa-uMtu8goFGf3IVEmdh6l7_n9EWREJl5QAVOcDEhcMAwZ7MfwTjkDFaghik4CNwxZNujBpLdKohuRrRcINbkXe6RLA169v5FNXD6h0me4e8m2yL1nvkKTSdxeEogFpK43Nu4_i_aC2Sus2ZnGiGfwEbqZ_JHEKHWznAwgyMQ3KU9GddjltTWGafdaGqVa7kxORrWmg',
}
CONSOLE_URL = 'https://console.privilegecloud.cyberark.com'

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S")
session = requests.Session()


def get_all_tenants():
    url = f'{CONSOLE_URL}/tenants/v1/lean'
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()  # raise exception if status code is not 2xx
    except (Exception) as error:
        logging.error(f"GET_ALL_TENANTS MSG: Error Retreiving all tenants - {error}")

    logging.info(f"GET_ALL_TENANTS MSG: Data Retreival Successful")
    return response.json()


def get_tenants_by_region(region):
    url = f'{CONSOLE_URL}/tenants/v1?region={region}'
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()  # raise exception if status code is not 2xx

    except (Exception) as error:
        logging.error(f"GET_TENANT_BY_REGION MSG: Error Retreiving tenants by region - {error}")

    logging.info(f"GET_TENANT_BY_REGION")
    return response.json()


def get_tenant_by_customer_id(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/{customer_id}'
    try:
        response = session.get(url, headers=HEADERS)
        # response.raise_for_status()  # raise exception if status code is not 2xx
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



def update_public_ips(customer_id: str(), ips_to_add: list()):
    try:
        current_ips = get_public_ips(customer_id)
        updated_ips = current_ips + ips_to_add
        logging.info(f"UPDATE_PUBLIC_IPS MSG: Retrieve public IPs SUCCESSFUL - {customer_id}")
    except (Exception) as err:
        logging.error(f'UPDATE_PUBLIC_IPS failed to fetch public ips of customer ID {customer_id}-{err}')
        return {'err': f"Error occured while retrieving public IPs - {err}"}

    url = f"{CONSOLE_URL}/tenants/v1/{customer_id}/config"
    payload = json.dumps({"customerPublicIPs": updated_ips})

    try:
        response = session.patch(url, headers=HEADERS, data=payload)
        # response.raise_for_status()
    except (Exception) as err:
        logging.error(f'UPDATE_PUBLIC_IPS Msg: Failed to update public Ips - {err}')
        return {'err': f"Error occured while updating public IPs"}

    logging.info(f"UPDATE_PUBLIC_IPS MSG: Public Ips Update SUCCESSFUL for Customer - {customer_id}")
    return response.json()


def get_task_status(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/tasks?mainObjectId={customer_id}'
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
    except (Exception) as err:
        logging.error(f'GET_TASK_STATUS MSG: Failed to fetch task status - {err}')
        return None
    logging.info(f'GET_TASK_STATUS MSG: Task status fetch SUCCESSFUL')
    latest_task = response.json()[0]
    # print(latest_task)
    return latest_task

def deploy_feature_H5GW(customer_id):
    url = f"{CONSOLE_URL}tenants/v1/{customer_id}/features/html5gw"
    try:
        response = session.post(url, headers=HEADERS, data={})
        response.raise_for_status()
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
        response = session.post(url, headers=HEADERS,data=payload, files=files)
        response.raise_for_status()

    except (Exception) as err:
        logging.error(
            "INSTALL_PSM_CERTIFICATE MSG: Error occured while installing PSM certs - {error}")
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
        # print("fileName: " , fileName)
        # print("path: " , path + "\\" + file_name)
        files.append(('files', (fileName, open(
            path + "\\" + file_name, 'rb'), 'application/octet-stream')))

    url = f"{CONSOLE_URL}/files/v1/installCertificate/{customer_id}"
    files = [('files', (file_name[file_name.index("_")+1:], open(f"database_files/{file_name}", 'rb'), 'application/octet-stream')) for file_name in ldap_files]

    try:
        response = session.post(url, headers=HEADERS,
                                 data=payload, files=files)

    except (Exception) as err:
        logging.error(
            f"INSTALL_LDAP_CERTS MSG: POST API call failed with error - {err}")
        return {'err': "install_LDAP_certs failed with error - {err}"}

    logging.info(f"INSTALL_LDAP_CERTS MSG: SUCCESSFUL - {customer_id}")
    return response.json()
