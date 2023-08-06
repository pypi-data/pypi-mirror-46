import os
import requests
import json
import jwt

# from tokenleaderclient.client.client import Client as tlClient
from micros2client.configs.config_handler import Configs as MSConfig

# must_have_keys_in_yml_for_ms1c = {
#                                   'url_type',
#                                   'ssl_enabled',
#                                   'ssl_verify'                            
#                                  }   

service_name = 'micros2'
conf_file='/etc/tokenleader/client_configs.yml'

must_have_keys_in_yml = {}   

conf = MSConfig(service_name, conf_file=conf_file, must_have_keys_in_yml= must_have_keys_in_yml)

micros2_yml = conf.yml.get(service_name)


class MSClient():   
    '''
    First initialize an instance of tokenleader client and  pass it to MSCclient 
    as its parameter
    '''
    
    def __init__(self, tlClient ):       
        
        self.tlClient = tlClient
        self.url_type = micros2_yml.get('url_type')
        self.ssl_enabled = micros2_yml.get('ssl_verify')
        self.ssl_verify = micros2_yml.get('ssl_verify')
#         self.url_to_connect = self.get_url_to_connect()
#         
            
    def get_service_ep_n_auth_header(self, api_route, service_name=service_name):
        ''' url to connect method was not caturing the exception when service enfpoint
        construction fails for non availability of tokenleader. Also there  call to 
        tokenleader used to be  twice. This code will correct the above issues but need to 
        be tested'''       
        url_to_connect = None
        try:
            all_data_token = self.tlClient.get_token()
            auth_token = all_data_token.get('auth_token')
            headers_v={'X-Auth-Token': auth_token}
            catalogue = all_data_token.get('service_catalog')            
            api_route = api_route            
        #print(catalogue)
            if catalogue.get(service_name):
                #print(catalogue.get(service_name))
                url_to_connect = catalogue[service_name][self.url_type]
                service_endpoint_v = url_to_connect + api_route
            else:
                msg = ("{} is not found in the service catalogue, ask the administrator"
                       " to register it in tokenleader".format(service_name))
                print(msg)
        except:
            print("could not retrieve service_catalog from token leader," 
                  " is token leaader service running ?"
                  " is tokenleader reachable from this server/container ??")
        return service_endpoint_v,  headers_v
    
    
    def handle_response(self, return_response):
        try:
            r_dict = json.loads(return_response.content.decode())
        except Exception as e:
            r_dict = {"Content returned by the server is not json serializable"
                    " checking the server log  might  help. "
                    " the text returned by the server is {}".format(
                        return_response.text)}
        return r_dict
        
        
    def post_request(self , api_route, data):        
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        headers.update({'content-type':'application/json'})
        try:  
            r = requests.post(service_ep, 
                             headers=headers, 
                             data = json.dumps(data),                             
                            verify=self.ssl_verify)
            r_dict = self.handle_response(r)               
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}    #     
            print(r_dict)
#         print(r)  # for displaying from the cli  print in cli parser
        return r_dict
    
    
    def put_request(self , api_route, data):        
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        headers.update({'content-type':'application/json'})
        try:  
            r = requests.put(service_ep, 
                             headers=headers, 
                             data = json.dumps(data),                             
                            verify=self.ssl_verify)
            r_dict = self.handle_response(r)                
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}    #     
            print(r_dict)
        return r_dict
    
    
    def delete_request(self, api_route ):
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        try:  
            r = requests.delete(service_ep, headers=headers, verify=self.ssl_verify)            
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}
        r_dict = self.handle_response(r) 
        return r_dict
    
    
    def get_request(self, api_route):
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        try:  
            r = requests.get(service_ep, headers=headers, verify=self.ssl_verify)            
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}
        r_dict = self.handle_response(r) 
        return r_dict
    
    
    def file_request_put(self, api_route, filepath):
            service_endpoint, headers = self.get_service_ep_n_auth_header(api_route)
            print(service_endpoint, headers)
            files = {'file': ( os.path.basename(filepath), 
                              open(filepath, 'rb'), 
                              'application/vnd.ms-excel', 
                              {'Expires': '0'})}
            try:              
                r = requests.put(service_endpoint, headers=headers, 
                                 files=files, verify=self.ssl_verify)
                r_dict = self.handle_response(r)               
            except Exception as e:
                r_dict = {'error': 'could not connect to server , the error is {}'.format(e)} 
            
            return r_dict
        
    def file_request_post(self, api_route, filepath):
            service_endpoint, headers = self.get_service_ep_n_auth_header(api_route)
            print(service_endpoint, headers)
            files = {'file': ( os.path.basename(filepath), 
                              open(filepath, 'rb'), 
                              'application/vnd.ms-excel', 
                              {'Expires': '0'})}
            try:              
                r = requests.post(service_endpoint, headers=headers, 
                                 files=files, verify=self.ssl_verify)
                r_dict = self.handle_response(r)               
            except Exception as e:
                r_dict = {'error': 'could not connect to server , the error is {}'.format(e)} 
            
            return r_dict
    
    
    def save_tesprec(self, listdata):
        r_dict = self.post_request('/save_tesprec', listdata )
        return r_dict
    
      
    def display(self, invno):
        api_route = '/display/{}'.format(
            invno)
        r_dict = self.get_request(api_route)
        return r_dict
        
    
    def list_invoices(self, field_name, field_value, level):        
        api_route = '/list/{}/{}/{}'.format(
            field_name, field_value, level)
        r_dict = self.get_request(api_route)       
        return r_dict 
        
    
    def delete_invoices(self, inv_num):        
        api_route = '/delete/{}'.format(inv_num)        
        r_dict = self.delete_request(api_route)
        return r_dict
