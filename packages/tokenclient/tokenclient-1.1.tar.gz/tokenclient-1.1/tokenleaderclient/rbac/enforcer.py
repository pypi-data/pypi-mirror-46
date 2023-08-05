import flask
from flask import request, make_response
import requests
import json
import functools

from tokenleaderclient.rbac.policy import load_service_access_policy 
from tokenleaderclient.rbac.policy import load_role_to_acl_map
from tokenleaderclient.rbac.wfc import WorkFuncContext
from  tokenleaderclient.client.client import Client 

#TODO:  This file should be read from  configuration settings 

WFC = WorkFuncContext()
role_acl_map_file='/etc/tokenleader/role_to_acl_map.yml'

class Enforcer():   
    
    def __init__(self, tl_client, 
                 role_acl_map_file='/etc/tokenleader/role_to_acl_map.yml' ,
                 test_token=None):
        
        self.tl_client = tl_client
        self.role_acl_map_file = role_acl_map_file
        self.test_token = test_token

    def get_token_only(self):
        r_dict = self.tl_client.get_token()            
        if r_dict['status'] == 'success': 
            token_received = r_dict['auth_token'] 
    #         print('got the token as : {}'.format(token_received))
        else:
              token_received = r_dict['status']
        return token_received   # we need to handle auth faliure 


    def verify_token(self, token):
        r_dict = self.tl_client.verify_token(token)
        return r_dict


    def extract_token_data_from_api_request(self):
        
        token_verification_result = {}
        
        if not self.test_token: 
            auth_token = flask.request.headers.get('X-Auth-Token')
            if not auth_token :
                #flask.abort(404)
                msg = ("This end point  need authentication, 'X-Auth-Token' "
                       "key is not present in the  request header \n")
                token_verification_result['message'] = msg
                token_verification_result['status'] = "Token verification failed"
                
            else:
                #auth_token = fdata['auth_token']
                token_verification_result = self.verify_token(auth_token) 
        else:
            if isinstance(self.test_token, dict):
                token_verification_result =   self.test_token
            else: 
                token_verification_result['message']  = 'invalid token type' 
                token_verification_result['status'] = "Token verification failed"
              
        return  token_verification_result    
       

    def compare_role_in_token_with_acl_map(self, user_role_in_token, rule_name):
        role_to_acl_map_list = load_role_to_acl_map(self.role_acl_map_file)
    #     print(role_to_acl_map_list)
        found_role_acl_map = []
        for role_acl_map in role_to_acl_map_list:        
            if  (role_acl_map.get('name') == user_role_in_token
                 and rule_name in role_acl_map.get('allow') ):            
                found_role_acl_map.append(True)
            else:
                found_role_acl_map.append(False)    
    #     print(found_role_acl_map)           
        if  True in found_role_acl_map :                                                    
            print('authorization success for rule: {}, role: {}'.format(
                user_role_in_token, rule_name))
            return True
        else:
            msg = ('role:  {} does not have permission for rule:  {}'.format(
                        user_role_in_token, rule_name)) 
            print(msg)
    #         print(role_to_acl_map_list)
            return False   
    
    
    def extract_roles_from_verified_token_n_compare_acl_map(self, rule_name):
        token_verification_result = self.extract_token_data_from_api_request()
        #print(token_verification_result)
        if token_verification_result['status'] == 'Verification Successful' :                   
            username = token_verification_result['payload'].get('sub').get('username')
            email = token_verification_result['payload'].get('sub').get('email')
            wcf_from_token = token_verification_result['payload'].get('sub').get('wfc')
            roles_in_token = token_verification_result['payload'].get('sub').get('roles')
            print("user has following roles: {}".format(roles_in_token))
            status_list_of_rule_check = []
            for user_role_in_token in roles_in_token:
                # don't compare  roles in yml file  when the role name from token is admin
                if user_role_in_token == 'admin':
                      status_list_of_rule_check.append(True)
                else:      
                    compare_status = self.compare_role_in_token_with_acl_map(user_role_in_token, 
                                                       rule_name)
                    #print(compare_status)            
                    status_list_of_rule_check.append(compare_status)            
            #print(status_list_of_rule_check)    
            if True in status_list_of_rule_check:
                return True, username, email, wcf_from_token, token_verification_result['message']
            else:
                return False, username, email, wcf_from_token, token_verification_result['message']  
        else:
            return False, False, False, False, token_verification_result['message'] 
                


    def enforce_access_rule_with_token(self, rule_name):
        '''
        the original function  where you will apply this enforcer decorator 
        must have a mandatory wfc  as its argument
        '''
        def decorator(f):  
            @functools.wraps(f)
            def wrapper_function(*args, **kws):
                role_exists_in_acl, username, email, wcf_from_token, msg = \
                self.extract_roles_from_verified_token_n_compare_acl_map(rule_name)
                #print(role_exists_in_acl, wcf_from_token)
                if wcf_from_token:
                    WFC.setcontext(username, email, wcf_from_token)
                    #print(WFC.org)
                    kws['wfc'] = WFC                    
                if role_exists_in_acl:
                    
                        return f(*args, **kws)
                else:
                    msg = ("this endpoint is restricted , authenticaton or authorization failed \n"
                           "possible reasons: \n  1.access configuration in role_acl_map.yml \n"
                           "2. missing public key  in the client config file ")
                    print(msg)
                    return json.dumps({'message': msg})
                                
            return wrapper_function
        return decorator






