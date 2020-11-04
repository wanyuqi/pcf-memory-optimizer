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
            org, space_name = obj['org'], obj['space']
            space_guid, memory_used, memory_unused = obj['space_guid'], obj['memory_used_p'], obj['memory_unused_mb']
            if '-DEV' in space_name or '-TST' in space_name or '-UAT' in space_name or '-PROD' in space_name:
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
                            res.append({'org': org, 'space': space_name, 'total_mem': total_memory, 'mem_used': 0.0, 'mem_unused': memory_unused})
                        else: 
                            res.append({'org': org, 'space': space_name, 'total_mem': total_memory, 'mem_used': 0.0, 'mem_unused': 0.0})
                    else:
                        res.append({'org': org, 'space': space_name, 'total_mem': total_memory, 'mem_used': memory_used, 'mem_unused': memory_unused})
                else:
                    if memory_used != '' and memory_unused != '':
                        existing_space['mem_used'] += memory_used
                        existing_space['mem_unused'] += memory_unused

            # buffer time for PCF API
            time.sleep(0.3)    

    return res 


if __name__ == '__main__':
    cf_token = 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vdWFhLnN5cy5jYWMucGNmLm1hbnVsaWZlLmNvbS90b2tlbl9rZXlzIiwia2lkIjoia2V5LTEiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI2ZTllNGMxMDQ2NzY0MDllOWQyZGVlNTRjOTQ2NWUxOCIsInN1YiI6ImQ2ZGYwMWMzLWU4YTAtNDA0OC05MzU4LWEwZGU1NzdiYzcwZiIsInNjb3BlIjpbIm9wZW5pZCIsInJvdXRpbmcucm91dGVyX2dyb3Vwcy53cml0ZSIsIm5ldHdvcmsud3JpdGUiLCJzY2ltLnJlYWQiLCJjbG91ZF9jb250cm9sbGVyLmFkbWluIiwidWFhLnVzZXIiLCJyb3V0aW5nLnJvdXRlcl9ncm91cHMucmVhZCIsImNsb3VkX2NvbnRyb2xsZXIucmVhZCIsInBhc3N3b3JkLndyaXRlIiwiY2xvdWRfY29udHJvbGxlci53cml0ZSIsIm5ldHdvcmsuYWRtaW4iLCJkb3BwbGVyLmZpcmVob3NlIiwic2NpbS53cml0ZSJdLCJjbGllbnRfaWQiOiJjZiIsImNpZCI6ImNmIiwiYXpwIjoiY2YiLCJncmFudF90eXBlIjoicGFzc3dvcmQiLCJ1c2VyX2lkIjoiZDZkZjAxYzMtZThhMC00MDQ4LTkzNTgtYTBkZTU3N2JjNzBmIiwib3JpZ2luIjoidWFhIiwidXNlcl9uYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluIiwiYXV0aF90aW1lIjoxNjA0NTE2MjE1LCJyZXZfc2lnIjoiNDVkZjEzMTciLCJpYXQiOjE2MDQ1MTYyMjAsImV4cCI6MTYwNDUyMzQyMCwiaXNzIjoiaHR0cHM6Ly91YWEuc3lzLmNhYy5wY2YubWFudWxpZmUuY29tL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbImNsb3VkX2NvbnRyb2xsZXIiLCJzY2ltIiwicGFzc3dvcmQiLCJjZiIsInVhYSIsIm9wZW5pZCIsImRvcHBsZXIiLCJuZXR3b3JrIiwicm91dGluZy5yb3V0ZXJfZ3JvdXBzIl19.mCsI0vHWq4T30AMbMlgAvXL2nuv8qf2FG_ulwCSXpzmUqNwATQ8idGMRRVVGYwObiwvuMm767dEzSiQqq6tE251KHf8ojaWvGzJu1Q1eSzEoNra8jDxrshWqUoSVXQTUIAwPWSjgQ0bvKdgcgumR1RJ3JVRGa99tx43w-g3pPwtHqtwl-BHbWbsMMK_4tdJnm2ggicIGasGw4qrqBEri7CLG4gkoGK0jFu2VmV293aK3EvjCkX2BKiN-M0WmfM_yq8SSKfAPGiC8lgcOp73mw_Awi2VIR8GEJah-iC3KRvj7tKZlTZcopAO7-ZIPlmquXttu1bcRbSMoLcHdse1PYw'
    foundation = input('Please enter the foundation: ')
    if foundation not in foundations:
        print('Foundation must be one of ' + str(foundations))
        sys.exit(2)
    api_url = 'https://' + input('Please enter the API url: ')
    ret = get_space_memory_allocation(foundation, api_url, cf_token)
    with open('memory_usage_output.json', 'w') as fout:
        json.dump(ret, fout)