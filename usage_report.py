import requests, os, sys, subprocess, json, argparse, typing

sample_data = json.load(open('sample_object.json'))

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
            if space_name not in res:
                request_url = api_url + '/v3/spaces/' + space_guid
                space_response = requests.get(request_url, headers=header).json()
                quota_guid = space_response['relationships']['quota']['data']['guid']
                quota_url = api_url + '/v3/space_quotas/' + quota_guid
                quota_response = requests.get(quota_url, headers=header).json()
                total_memory = quota_response['apps']['total_memory_in_mb']
                res.append({'space': space_name, 'total_mem': total_memory, 'mem_used': memory_used, 'mem_unused': memory_unused})
            else:
                d = next((sp for sp in res if sp['space'] == space_name), None)
                if memory_used != '' and memory_unused != '':
                    d['mem_used'] += memory_used
                    d['mem_unused'] += memory_unused

    return res 



if __name__ == '__main__':
    foundation = input('Please enter the foundation: ')
    if foundation not in foundations:
        print('Foundation must be one of ' + str(foundations))
        sys.exit(2)
    api_url = 'https://' + input('Please enter the API url: ')
    get_space_memory_allocation(foundation, api_url, cf_token)