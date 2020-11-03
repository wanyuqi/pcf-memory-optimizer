import requests, os, sys, subprocess, json, argparse, typing, time

sample_data = json.load(open('sample_app_data.json'))

foundations = [] 
for app in sample_data:
    fd = app['foundation']
    if fd not in foundations:
        foundations.append(fd)

def get_space_memory_allocation(foundation: str, api_url: str, cf_token: str):
    res = []
    header = {'Authorization': f'bearer {cf_token}'}
    for obj in sample_data:
        if obj['foundation'] == foundation:
            space_guid, space_name, memory_used, memory_unused = obj['space_guid'], obj['space'], obj['memory_used_p'], obj['memory_unused_mb']
            if '-DEV' in space_name or '-TST' in space_name:
                existing_space = next((sp for sp in res if sp['space'] == space_name), None)
                if existing_space is None:
                    request_url = api_url + '/v3/spaces/' + space_guid
                    print(request_url)
                    space_response = requests.get(request_url, headers=header).json()
                    quota_guid = space_response['relationships']['quota']['data']['guid']
                    quota_url = api_url + '/v3/space_quotas/' + quota_guid
                    print(quota_url)
                    quota_response = requests.get(quota_url, headers=header).json()
                    total_memory = quota_response['apps']['total_memory_in_mb']
                    if memory_used == '':
                        if memory_unused != '': 
                            res.append({'space': space_name, 'total_mem': total_memory, 'mem_used': 0.0, 'mem_unused': memory_unused})
                        else: 
                            res.append({'space': space_name, 'total_mem': total_memory, 'mem_used': 0.0, 'mem_unused': 0.0})
                    else:
                        res.append({'space': space_name, 'total_mem': total_memory, 'mem_used': memory_used, 'mem_unused': memory_unused})
                else:
                    if memory_used != '' and memory_unused != '':
                        existing_space['mem_used'] += memory_used
                        existing_space['mem_unused'] += memory_unused

            # buffer time for PCF API
            time.sleep(0.5)    

    return res 



if __name__ == '__main__':
    cf_token = ''
    foundation = input('Please enter the foundation: ')
    if foundation not in foundations:
        print('Foundation must be one of ' + str(foundations))
        sys.exit(2)
    api_url = 'https://' + input('Please enter the API url: ')
    ret = get_space_memory_allocation(foundation, api_url, cf_token)
    with open('memory_usage_output.json', 'w') as fout:
        json.dump(ret, fout)