import requests, os, subprocess, json

sample_data = json.load(open('sample_app_data.json'))

if __name__ == '__main__':
    print(sample_data)
