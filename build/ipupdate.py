import sys
import os
import json
from INWX.Domrobot import ApiClient, ApiType

username = os.environ['INWX_USER']
password = os.environ['INWX_PASS']
records_json = os.environ['RECORDS']
recordContent = sys.argv[1]

if(len(sys.argv) != 2):
    print("usage:", sys.argv[0], "IP")
    print("example:", sys.argv[0], "dead:beef::1")
    exit()

if(len(username) < 1):
    print("Environment variable INWX_USER not set. exit!")
    exit()

if(len(password) < 1):
    print("Environment variable INWX_PASS not set. exit!")
    exit()

if(len(records_json) < 1):
    print("Environment variable RECORDS not set. exit!")
    exit()

records = json.loads(records_json)

api_client = ApiClient(api_url=ApiClient.API_LIVE_URL, api_type=ApiType.JSON_RPC, debug_mode=True)

login_result = api_client.login(username, password)

if login_result['code'] == 1000:

    for recordLine in records:
        domain = recordLine["domain"]
        recordName = recordLine["record"]
        recordType = 'AAAA'

        list_record_result = api_client.call_api(api_method='nameserver.info', method_params={'domain': domain, 'name': recordName, 'type': recordType})

        if list_record_result['code'] == 1000:
            dns_record = list_record_result['resData']['record'][0]
            dns_record_id = dns_record['id']
            dns_record_content = dns_record['content']

            if dns_record_content != recordContent:
                print("would update now:", {'id': dns_record_id, 'content': recordContent})
                update_record_result = api_client.call_api(api_method='nameserver.updateRecord', method_params={'id': dns_record_id, 'content': recordContent})

                if update_record_result['code'] == 1000:
                    print('Record update successfully')
                else:
                    raise Exception('Api error while updating the record. Code: ' + str(update_record_result['code'])
                                    + '  Message: ' + update_record_result['msg'])
            else:
                print("nothing to do!")
        else:
            raise Exception('Api error while getting the DNS record. Code: ' + str(update_record_result['code'])
                            + '  Message: ' + update_record_result['msg'])

    api_client.logout()
else:
    raise Exception('Api login error. Code: ' + str(login_result['code']) + '  Message: ' + login_result['msg'])
