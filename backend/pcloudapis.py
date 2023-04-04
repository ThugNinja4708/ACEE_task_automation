import json
import requests
import logging
logging.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S")

session = requests.Session()

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'eyJraWQiOiJSbENXRENCQ2NRbGdtTGVPcDlCcnMwV2VPQTluS1ZHZUNFTnJFQWJaeGlvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoianNKUENXcGhkSjlGUmRQb0RRNWdodyIsInN1YiI6ImI3MjUwZWE0LTZmMzAtNDliOC1iZWRlLTYwYTQ0M2EzMDg2NyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9kVkdSY2RLUTFfY3liZXJhcmstaWRlbnRpdHkiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZFZHUmNkS1ExIiwiY29nbml0bzp1c2VybmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5X3JrYW50aGFAY3liZXJhcmsuY29tIiwibm9uY2UiOiJyRUNicm5HUWhRTzJtRy1rR1M0bnpORm9NVVJ6cjRZN3l1NjMyTGxCa1VoNGZ3RXhQN3FjV3RKelgwV282SUhaMUt6WmtaSGpwLVBPajdYMnNZTXlINjBHcmRfOWw1Ukh3X1ZkblJqLXBqdENmV3UwcG8xV3lQYWJmb0draXBpSF9yU3M3dDhha0hXUWZQTHVOeTdfWmRxdjhBdHNZaXVGSjlNT0dIX21NWm8iLCJhdWQiOiI2cXFucGxvNWJjZmFraDRjamZwOGhtb3RucCIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6InJrYW50aGFAY3liZXJhcmsuY29tIiwicHJvdmlkZXJOYW1lIjoiY3liZXJhcmstaWRlbnRpdHkiLCJwcm92aWRlclR5cGUiOiJTQU1MIiwiaXNzdWVyIjoiaHR0cHM6XC9cL2FhZTQyMjIubXkuaWRhcHRpdmUuYXBwXC8xNzZjNDA5Yi0wNTRhLTQ4ZjQtOWRjMi1jOWU3MjM4ZDhkOWEiLCJwcmltYXJ5IjoidHJ1ZSIsImRhdGVDcmVhdGVkIjoiMTY3Mjg0MzMwMDQzNSJ9XSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2ODA1OTM3MDEsImN1c3RvbTpVU0VSX0dST1VQUyI6InBDbG91ZENvbnNvbGVPcHNQUkQiLCJleHAiOjE2ODA2MDgxMDEsImlhdCI6MTY4MDU5MzcwMn0.TDjMeFmnOEltyY9eA14RcfQjMaEa7zm2uU6ku4WJJ8c7HxPmN6MeO9lGqtO6POEBZcSHeZAdiYwOutCF_agdq4RoMysUhTVAIiKr3mAQP-NRO3cOHP4nt9tXgfValBd7Y-nVsrcANA5APnZNsKlsRsK-9GeY20og71pXpFfBYNN29TQwEp_wUCIlJR-dYHFQIam3TtlYXu5L_Gcy6WDGLeAFoOldZJoHnT-Agvb-S5-4CibO8AKEHruIl5r6o-sB8E0SoVGQitjEnJr_c2RtAEDjH24v4woyCd9YTZmJraYXakoKv4LKxiqBead_SGc7TL8s019Yu1QtvioCXYK-GQ',
}

CONSOLE_URL = 'https://console.privilegecloud.cyberark.com/'



def get_public_ips(customer_id):
    url = f'{CONSOLE_URL}/tenants/v1/{customer_id}'
    try:
        response = requests.get(url, headers=HEADERS)
    except Exception as e:
        raise Exception(f"Could not get the tenant - {customer_id}")
    else:
        customer_public_ips = response.get('customerPublicIPs', [])
        logging.info(f"Retrieved public IPs of - {customer_id}")
        return customer_public_ips

def update_public_ips(customer_id: str(), ips_to_add: list()):
    url = f"{CONSOLE_URL}tenants/v1/{customer_id}/config"
    try:
        current_ips = get_public_ips(customer_id)
        updated_ips = current_ips + ips_to_add
        payload = json.dumps({"customerPublicIPs": updated_ips})
        try:
            response = requests.patch(url, headers=HEADERS, data=payload)
        except Exception as err:
            raise Exception(f"Could not update public IPs of - {customer_id}")
    except Exception as err:
        logging.error(err)
    else:
        logging.info(f"Retrieved public IPs of - {customer_id}")
        return response.json()


   
    # try:
    #     update_public_ips
    # except Exception as err:
    #      logging.error(err.)

# def update_public_ips(customer_id: str(), ips_to_add: list()):
#     try:

#         current_ips = get_public_ips(customer_id)
#         updated_ips = current_ips + ips_to_add

#         logging.info(f"UPDATE_PUBLIC_IPS MSG: Retrieve public IPs SUCCESSFUL - {customer_id}")

#     except (Exception) as err:
#         logging.error(f'UPDATE_PUBLIC_IPS failed to fetch public ips of customer ID {customer_id}-{err}')
#         return {'err': f"Error occured while retrieving public IPs - {err}"}

#     url = f"{CONSOLE_URL}tenants/v1/{customer_id}/config"
#     payload = json.dumps({"customerPublicIPs": updated_ips})

#     try:
#         response = session.patch(url, headers=HEADERS, data=payload)
#         # response.raise_for_status()
#     except (Exception) as err:
#         logging.error(f'UPDATE_PUBLIC_IPS Msg: Failed to update public Ips - {err}')
#         return {'err': f"Error occured while updating public IPs"}

#     logging.info(f"UPDATE_PUBLIC_IPS MSG: Public Ips Update SUCCESSFUL for Customer - {customer_id}")
#     return response.json()









def get_task_status(customer_id):
    url = f'{CONSOLE_URL}tenants/v1/tasks?mainObjectId={customer_id}'
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
        headers = HEADERS
        headers.pop('Content-Type')
        print ("############",headers,url)
        response = session.post(url, headers=headers,data=payload, files=files)
        # response.raise_for_status()

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
        # print("fileName: " , fileName)
        # print("path: " , path + "\\" + file_name)
        files.append(('files', (fileName, open(
            path + "\\" + file_name, 'rb'), 'application/octet-stream')))
    headers = HEADERS
    headers.pop('Content-Type')
    url = f"{CONSOLE_URL}files/v1/installCertificate/{customer_id}"
    files = [('files', (file_name[file_name.index("_")+1:], open(f"database_files/{file_name}", 'rb'), 'application/octet-stream')) for file_name in ldap_files]

    try:
        response = session.post(url, headers=HEADERS,data=payload, files=files)

    except (Exception) as err:
        logging.error(f"INSTALL_LDAP_CERTS MSG: POST API call failed with error - {err}")
        return {'err': "install_LDAP_certs failed with error - {err}"}

    logging.info(f"INSTALL_LDAP_CERTS MSG: SUCCESSFUL - {customer_id}")
    return response.json()
