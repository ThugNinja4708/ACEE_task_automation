  
import json
import requests
import logging
HEADERS = {
    'Authorization':"eyJraWQiOiJSbENXRENCQ2NRbGdtTGVPcDlCcnMwV2VPQTluS1ZHZUNFTnJFQWJaeGlvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiUE13LXBDYXF0SmIyWk9pbnozVVVwQSIsInN1YiI6ImQ3Njk5YTgzLTNkNTctNDdmZS04NTczLWNiZWIwYjE4YWJmZSIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9kVkdSY2RLUTFfY3liZXJhcmstaWRlbnRpdHkiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZFZHUmNkS1ExIiwiY29nbml0bzp1c2VybmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5X3NraWxhbWJpQGN5YmVyYXJrLmNvbSIsIm5vbmNlIjoiZmFYYk9OWVRGVkJ3SmRRTE1SZGhDNXhPRnJxNzZPWjRrWWhKaDc4YkdnazE2MUVtb2xJT1pnMmZKeHluNS1WaTJpb3Z1X2VnNjhFVGFjcG5jcjZyMXJCdm1BUVNjcGxuMVFRUDdtcGxCOGUwQ3pjSnphVUo2UUF1dXNRWV83ME9hNDdELXVEN0dqbWludFJrVWlic0kzNkFQWldONGhENzZvU1NVWW0xczNRIiwiYXVkIjoiNnFxbnBsbzViY2Zha2g0Y2pmcDhobW90bnAiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiJza2lsYW1iaUBjeWJlcmFyay5jb20iLCJwcm92aWRlck5hbWUiOiJjeWJlcmFyay1pZGVudGl0eSIsInByb3ZpZGVyVHlwZSI6IlNBTUwiLCJpc3N1ZXIiOiJodHRwczpcL1wvYWFlNDIyMi5teS5pZGFwdGl2ZS5hcHBcLzE3NmM0MDliLTA1NGEtNDhmNC05ZGMyLWM5ZTcyMzhkOGQ5YSIsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNjcyODM1MjQ4ODA3In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY4MDE4MDQxMSwiY3VzdG9tOlVTRVJfR1JPVVBTIjoicENsb3VkQ29uc29sZU9wc1BSRCIsImV4cCI6MTY4MDE5NDgxMSwiaWF0IjoxNjgwMTgwNDExfQ.cyajM12y3xPR96PkcRbVo5TNIcLqFdixlc5UxcYRpPpNs8rIwffmfYQzXTz23zDRRE-MYNycJEB-DqDu68ZBGoX1pixQcbHmx9fCJgkCXJ90h8QsQVKMATxg0vC1lmP26YgD_TpbsJxqSVwHBRXCvPL55m0S3hHg3urimSaRspvs1FEaHPPClJ-_oL2GEpcu4tppyrIz9_nT8RyCox5zqcYUYLlgysPdKTsaEvIIbxqWj6nl42VrBO8e_gTpqrIFWGlFN40gXSTtdEcx3M5fK46D9XZVr84zt4ztMMCjsgDj1yYxmhK0zGCZPUnHcOlT8_ZeKIZEBgZRb4TWqQ-KGA",
    'content-type': 'application/json'
}

CONSOLE_URL = 'https://console.privilegecloud.cyberark.com'


# create a requests session object to reuse the same TCP connection
session = requests.Session()

# configure logging to include function name and line number
logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S")



def get_all_tenants():
    url = f'{CONSOLE_URL}/tenants/v1/lean'
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()  # raise exception if status code is not 2xx
    except (Exception) as error:
        logging.error(
            f"GET_ALL_TENANTS MSG: Error Retreiving all tenants - {error}")

    logging.info(f"GET_ALL_TENANTS MSG: Data Retreival Successful")
    return response.json()


def get_tenants_by_region(region):
    url = f'{CONSOLE_URL}/tenants/v1?region={region}'
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()  # raise exception if status code is not 2xx
    except (Exception) as error:
        logging.error(
            f"GET_TENANT_BY_REGION MSG: Error Retreiving tenants by region - {error}")
    logging.info(f"GET_TENANT_BY_REGION")
    return response.json()


def get_tenant_by_customer_id(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/{customer_id}'
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()  # raise exception if status code is not 2xx
    except (Exception) as error:
        logging.error(
            f"GET_TENANT_BY_CUSTOMER_ID MSG: Error Retreiving tenant by customer ID - {error}")
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



def update_public_ips(customer_id, ips_to_add):
    try:
        current_ips = get_public_ips(customer_id)
        updated_ips = current_ips + ips_to_add
        logging.info(f"UPDATE_PUBLIC_IPS MSG: Retrieve public IPs SUCCESSFUL - {customer_id}")
    except Exception as e:
        logging.error(f"UPDATE_PUBLIC_IPS MSG: Failed to retrieve public IPs for customer ID {customer_id} - {e}")
        return {'err': f"Error occurred while retrieving public IPs - {e}"}

    url = f"{CONSOLE_URL}/tenants/v1/{customer_id}/config"
    payload = json.dumps({"customerPublicIPs": updated_ips})

    try:
        response = session.patch(url, headers=HEADERS, data=payload)
        response.raise_for_status()
        logging.info(f"UPDATE_PUBLIC_IPS MSG: Public IPs update SUCCESSFUL for customer - {customer_id}")
        return response.json()
    except Exception as e:
        logging.error(f"UPDATE_PUBLIC_IPS MSG: Failed to update public IPs for customer - {customer_id} - {e}")
        return {'err': f"Error occurred while updating public IPs - {e}"}


def get_task_status(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/tasks?mainObjectId={customer_id}'
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
    except (Exception) as err:
        logging.error(
            f'GET_TASK_STATUS MSG: Failed to fetch task status - {err}')
        return None
    logging.info(f'GET_TASK_STATUS MSG: Task status fetch SUCCESSFUL')
    last_task=response[0]
    return last_task



def deploy_feature_H5GW(customer_id):
    url = f"{CONSOLE_URL}tenants/v1/{customer_id}/features/html5gw"
    try:
        response = session.post(url, headers=HEADERS, data={})
        response.raise_for_status()
        logging.info(f"DEPLOY_FEATURE_H5GW MSG: Deploy HTML5GW feature SUCCESSFUL - {customer_id}")
        return response.json()
    except (Exception) as err:
        logging.error(f"DEPLOY_FEATURE_H5GW MSG: Failed to deploy HTML5GW feature to customer - {customer_id} - error - {err}")
        return {'err': f'DEPLOY_FEATURE_H5GW UNSUCCESSFUL - {err}'}


def install_PSM_certs(customer_id: str, psm_files: List[str]) -> Union[Dict[str, str], Any]:
    payload = {'description': 'this is file description'}
    files = []
    path = "database_files"
    for file_name in psm_files:
        fileName = file_name[file_name.index("_")+1:]
        with open(os.path.join(path, file_name), 'rb') as f:
            files.append(('files', (fileName, f, 'application/octet-stream')))
    url = f"{CONSOLE_URL}files/v1/installPsmCertificate/{customer_id}"
    try:
        response = session.post(url, headers=HEADERS, data=payload, files=files)
        response.raise_for_status()
    except Exception as error:
        logging.error(f"INSTALL_PSM_CERTIFICATE MSG: Error occurred while installing PSM certs - {error}")
        return {'err': 'INSTALL_PSM_CERTIFICATE UNSUCCESSFUL'}
    logging.info(f"INSTALL_PSM_CERTIFICATE MSG: Certificates installation SUCCESSFUL - {customer_id}")
    return response.json()


def install_LDAP_certs(customer_id, ldap_files):
    url = f"{CONSOLE_URL}/files/v1/installCertificate/{customer_id}"
    files = [('files', (file_name[file_name.index("_")+1:], open(f"database_files/{file_name}", 'rb'), 'application/octet-stream')) for file_name in ldap_files]

    try:
        response = session.post(url, headers=HEADERS, data={'description': 'this is file description'}, files=files)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(f"INSTALL_LDAP_CERTS MSG: POST API call failed with error - {err}")
        return {'err': f"install_LDAP_certs failed with error - {err}"}

    logging.info(f"INSTALL_LDAP_CERTS MSG: SUCCESSFUL - {customer_id}")
    return response.json()
