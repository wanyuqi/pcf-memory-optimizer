import requests, os, sys, subprocess, json, argparse, typing

sample_data = json.load(open('sample_app_data.json'))

foundations = [] 
for app in sample_data:
    fd = app['foundation']
    if fd not in foundations:
        foundations.append(fd)

report = []

def get_space_memory_allocation(foundation: str, api_url: str, cf_token: str):
    header = {'Authorization': f'bearer {cf_token}'}
    for obj in sample_data:
        if obj['foundation'] == foundation:
            space_guid, space_name = obj['space_guid'], obj['space']
            if space_name not in report:
                report.append({'space' : space_name})
            request_url = api_url + '/v3/spaces/' + space_guid
            response = requests.get(request_url, headers=header).json()
            quota_guid = response['relationships']['quota']['data']['guid']


if __name__ == '__main__':
    cf_token = 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vdWFhLnN5cy5jYWMucHJldmlldy5wY2YubWFudWxpZmUuY29tL3Rva2VuX2tleXMiLCJraWQiOiJrZXktMSIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1M2FjNmY5NTZhMTg0NGNmODcxZWEzNzcxZTJmMGFjYyIsInN1YiI6ImI4ZDFlYmMwLTAyYzctNDkxYS04YTlhLWJjMTIyODVjODY2NSIsInNjb3BlIjpbIm9wZW5pZCIsInJvdXRpbmcucm91dGVyX2dyb3Vwcy53cml0ZSIsIm5ldHdvcmsud3JpdGUiLCJzY2ltLnJlYWQiLCJjbG91ZF9jb250cm9sbGVyLmFkbWluIiwidWFhLnVzZXIiLCJyb3V0aW5nLnJvdXRlcl9ncm91cHMucmVhZCIsImNsb3VkX2NvbnRyb2xsZXIucmVhZCIsInBhc3N3b3JkLndyaXRlIiwiY2xvdWRfY29udHJvbGxlci53cml0ZSIsIm5ldHdvcmsuYWRtaW4iLCJkb3BwbGVyLmZpcmVob3NlIiwic2NpbS53cml0ZSJdLCJjbGllbnRfaWQiOiJjZiIsImNpZCI6ImNmIiwiYXpwIjoiY2YiLCJncmFudF90eXBlIjoicGFzc3dvcmQiLCJ1c2VyX2lkIjoiYjhkMWViYzAtMDJjNy00OTFhLThhOWEtYmMxMjI4NWM4NjY1Iiwib3JpZ2luIjoidWFhIiwidXNlcl9uYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluIiwiYXV0aF90aW1lIjoxNjA0MzM2OTcxLCJyZXZfc2lnIjoiOGI5MGQ2YWMiLCJpYXQiOjE2MDQzMzkxMDMsImV4cCI6MTYwNDM0NjMwMywiaXNzIjoiaHR0cHM6Ly91YWEuc3lzLmNhYy5wcmV2aWV3LnBjZi5tYW51bGlmZS5jb20vb2F1dGgvdG9rZW4iLCJ6aWQiOiJ1YWEiLCJhdWQiOlsiY2xvdWRfY29udHJvbGxlciIsInNjaW0iLCJwYXNzd29yZCIsImNmIiwidWFhIiwib3BlbmlkIiwiZG9wcGxlciIsIm5ldHdvcmsiLCJyb3V0aW5nLnJvdXRlcl9ncm91cHMiXX0.Z6vcInyvt3hvNyEsxT9VFRpDVwMNzgMRGbM30Q4uUDR8AeK0i38vfayqEOWVq5KjHCsRnnTAryo_li10Hu-D5TTmfJ95nPYcugn427KhYyhHESkRT__4ffEf1x-xx7FpXOMMk_4DUBMbsAHk6PMjD6zycKXCjPu7YDsLuzmCtFx-fKwAHd_MPQEHSyOBQTHx0L5vwx_guO3e-rlPcj9s-T4sp3qZBRRAgZxGN422cH_vrnDwFW0gNS_EUk8Ns7uzdFxoSwwhzoskRS6T_zPBCweiBCREmEycHb7Y12M2b7_bJYvVKjGz567sa-F2CX0Hcrg1Jx2vHavmQSAlcgPIhA'
    foundation = input('Please enter the foundation: ')
    if foundation not in foundations:
        print('Foundation must be one of ' + str(foundations))
        sys.exit(2)
    api_url = 'https://' + input('Please enter the API url: ')
    get_space_memory_allocation(foundation, api_url, cf_token)