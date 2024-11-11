import time
from typing import List
import requests
import yaml
from urllib.parse import urlparse
import sys

class FetchRequest:
    def __init__(self,headers={},method="GET",name='',url='',body={}):
        self.headers = headers
        self.method = method
        self.name = name
        self.url = url
        self.body = body
    
    def set_headers(self,headers: dict):
        self.headers = headers
    
    def set_method(self,method: str):
        self.method = method
    
    def set_name(self,name: str):
        self.name = name
    
    def set_url(self, url: str):
        self.url = url
    
    def set_body(self,body: str):
        self.body = body
    
    #testing purposes
    def to_string(self)-> str:
        res = f'NAME: {self.name}\n'
        res += f'URL: {self.url} \n'
        res+= f'METHOD: {self.method}\n'
        res+= f'HEADERS: {str(self.headers)} \n'
        res += f'BODY: {self.body} \n'
        return res

#takes in file path for input yaml file, writes to 
def open_yaml_input_file(file_path: str) -> List[FetchRequest]:
    compiled_requests = []
    with open(file_path) as file:
        try:
            input_data = yaml.safe_load(file)
            for endpoint in input_data:
                #print('e:',endpoint)
                cur_fetch = FetchRequest()
                if 'name' in endpoint:
                    cur_fetch.set_name(endpoint['name'])
                else:
                    #invalid endpoint because name is required
                    continue

                if 'url' in endpoint:
                    cur_fetch.set_url(endpoint['url'])
                else:
                    #invalid endpoint because url is required
                    continue
                
                if 'method' in endpoint:
                    cur_fetch.set_method(endpoint['method'])
                
                if 'headers' in endpoint:
                    cur_fetch.set_headers(endpoint['headers'])

                if 'body' in endpoint:
                    cur_fetch.set_body(endpoint['body'])

                compiled_requests.append(cur_fetch)

            return compiled_requests
        except yaml.YAMLError as e:
            print("Error with yaml input file:",e)

#takes in fetch request object and returns True/False on whether it suceeded or not
#True - UP
#False - DOWN
def make_request(data: FetchRequest)-> bool:
    response = requests.request(data.method, data.url, headers=data.headers, data=data.body)

    #status code needs to be between 200-299 and response latency needs to be less than 500ms 
    if response.status_code >= 200 and response.status_code <=299 and (response.elapsed.total_seconds() * 1000) < 500:
        return True
    return False


def loop_request_list(health_check_list: List[FetchRequest]):
    percentage_tracker = {} #'url_domain' : (UP count,total_iterations)
    while True:
        for endpoint in health_check_list:
            result = make_request(endpoint)

            url_domain = urlparse(endpoint.url).netloc
            if url_domain not in percentage_tracker:
                percentage_tracker[url_domain] = (0,0)

            if result:
                percentage_tracker[url_domain] = (percentage_tracker[url_domain][0]+1,percentage_tracker[url_domain][1]+1)
            else:
                percentage_tracker[url_domain] = (percentage_tracker[url_domain][0],percentage_tracker[url_domain][1]+1)

        for url_domain,values in percentage_tracker.items():
            availability_percentage_calc = round(100 *(values[0] / values[1]))
            print(f'{url_domain} has {availability_percentage_calc}% availability percentage')

        time.sleep(15)
    

if __name__=="__main__":
    args = sys.argv
    if len(args) > 2:
        print('Invalid yaml input file. Required to include path to yaml input file. Example: python main.py /path/to/input.yaml')
    input_file = args[1]
    #TODO add user input for input yaml file
    health_check_list = open_yaml_input_file(input_file)
    if not health_check_list:
        print("Error parsing yaml input or yaml input is empty.")
    else:
        loop_request_list(health_check_list)


'''
Edgecases:
- user wants to input multiple yaml files to monitor

'''