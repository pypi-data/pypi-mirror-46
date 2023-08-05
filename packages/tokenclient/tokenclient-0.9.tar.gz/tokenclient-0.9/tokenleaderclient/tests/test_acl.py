import unittest
# from flask import Flask
from flask_testing import TestCase
import json
from  tokenleaderclient import flaskapp
from tokenleaderclient.rbac.enforcer import Enforcer
from tokenleaderclient.client.client import Client
from tokenleaderclient.tests.base_tests import  conf, conf_from_manual_input

role_acl_map_file='tokenleaderclient/tests/testdata/role_to_acl_map.yml'

TLClient = Client(conf) 
enforcer = Enforcer(TLClient, role_acl_map_file=role_acl_map_file)



app = flaskapp.create_app()



sample_token = {"message":"Token has been successfully decrypted",
                          "payload":{"exp":1548487022,
                                     "iat":1548483422,
                                     "sub":{"email":"user1@itc.in",
                                            "id":1,
                                            "roles": ["role1",],
                                            "username":"user1",
                                            "wfc": {
                                                    "department": "dept1",
                                                    "id": 1,
                                                    "name": "wfc1",
                                                    "org": "org1",
                                                    "orgunit": "ou1"
                                                  }
                                            }
                                     },
                          "status":"Verification Successful"}

admin_token = {"message":"Token has been successfully decrypted",
                          "payload":{"exp":1548487022,
                                     "iat":1548483422,
                                     "sub":{"email":"admin@itc.in",
                                            "id":1,
                                            "roles": ["admin",],
                                            "username":"admin",
                                            "wfc": {
                                                    "department": "dept1",
                                                    "id": 1,
                                                    "name": "wfc1",
                                                    "org": "org1",
                                                    "orgunit": "ou1"
                                                  }
                                            }
                                     },
                          "status":"Verification Successful"}


sample_token_role_as_list_nonexisting = {"message":"Token has been successfully decrypted",
                          "payload":{"exp":1548487022,
                                     "iat":1548483422,
                                     "sub":{"email":"test_user1@itc.in",
                                            "id":1,
                                            "roles": ["test_role_1", "test_role_2"],
                                            "username":"test_user1",
                                            "wfc": {
                                                    "department": "dept1",
                                                    "id": 1,
                                                    "name": "wfc1",
                                                    "org": "org1",
                                                    "orgunit": "ou1"
                                                  }
                                            }
                                     },
                          "status":"Verification Successful"}

sample_token_role_as_list_valid_role = {"message":"Token has been successfully decrypted",
                          "payload":{"exp":1548487022,
                                     "iat":1548483422,
                                     "sub":{"email":"test_user1@itc.in",
                                            "id":1,
                                            "roles": ["role1", "role2"],
                                            "username":"test_user1",
                                            "wfc": {
                                                    "department": "dept1",
                                                    "id": 1,
                                                    "name": "wfc1",
                                                    "org": "org1",
                                                    "orgunit": "ou1"
                                                  }
                                            }
                                     },
                          "status":"Verification Successful"}


TLClient_from_user_input = Client(conf_from_manual_input)        
enforcer_user_input = Enforcer(TLClient_from_user_input, role_acl_map_file=role_acl_map_file,
                            test_token=admin_token)  
           


class TestAcl(TestCase):
    def create_app(self):       
        return app  
#     
#     def test_role1_success_compare_role_in_token_with_admin_role(self):
#         true_result = authclient.compare_role_in_token_with_acl_map(
#             'admin', 'service1:first_api:rulename1',
#             role_acl_map_file=role_acl_map_file)
#        
#         self.assertTrue(true_result)  

    def test_token_ops_from_class(self):
        t = enforcer.get_token_only()        
        v = enforcer.verify_token(t)
        #print(v)
        self.assertTrue(v.get('status') == 'Verification Successful')
        
    def test_extract_token_data_from_api_request_with_verified_token(self):       
        enforcer = Enforcer(TLClient, role_acl_map_file=role_acl_map_file,
                            test_token=sample_token)

        result = enforcer.extract_token_data_from_api_request()
        #print(result)
        self.assertTrue(result == sample_token)
        
                
    def test_role1_success_compare_role_in_token_with_acl_map(self):
        true_result = enforcer.compare_role_in_token_with_acl_map(
            'role1', 'service1:first_api:rulename1')
       
        self.assertTrue(true_result)
        
    def test_role2_success_compare_role_in_token_with_acl_map(self):
        true_result = enforcer.compare_role_in_token_with_acl_map(
            'role2', 'service1:third_api:rulename3')
       
        self.assertTrue(true_result)
    
    def test_role4_success_with_rule1_compare_role_in_token_with_acl_map(self):
        true_result = enforcer.compare_role_in_token_with_acl_map(
            'role4', 'service1:first_api:rulename1')
       
        self.assertTrue(true_result)
    
    def test_role4_success_with_rule7_compare_role_in_token_with_acl_map(self):
        true_result = enforcer.compare_role_in_token_with_acl_map(
            'role4', 'service1:7api_api:rulename7')
       
        self.assertTrue(true_result)
        
    def test_role4_success_with_rule4_compare_role_in_token_with_acl_map(self):
        true_result = enforcer.compare_role_in_token_with_acl_map(
            'role4', 'service1:fourthapi_api:rulename4')
       
        self.assertTrue(true_result)
        
    
    def test_rule_mismatch_compare_role_in_token_with_acl_map(self):        
        false_result = enforcer.compare_role_in_token_with_acl_map(
            'rule1', 'rule_mismatched')
                
        self.assertFalse(false_result)
        
        
    def test_role_mismatch_compare_role_in_token_with_acl_map(self):        
        false_result = enforcer.compare_role_in_token_with_acl_map(
            'rule_mismatched', 'service1:first_api:rulename1')
                
        self.assertFalse(false_result)    
   
        
    def test_extract_roles_from_verified_token_n_compare_acl_map_invalid_role(self):        
        enforcer = Enforcer(TLClient, role_acl_map_file=role_acl_map_file,
                            test_token=sample_token_role_as_list_nonexisting)
        result_false, _,_,_,_ = enforcer.extract_roles_from_verified_token_n_compare_acl_map(
            'service1:first_api:rulename1')
        self.assertFalse(result_false)
    
    
    def test_extract_roles_from_verified_token_n_compare_acl_map_valid_role(self):        
        enforcer = Enforcer(TLClient, role_acl_map_file=role_acl_map_file,
                            test_token=sample_token_role_as_list_valid_role)
        result_true, _, _, wfc, _ = enforcer.extract_roles_from_verified_token_n_compare_acl_map(
            'service1:first_api:rulename1')
        #print(result_true)
        self.assertEqual(result_true, True)
        
        self.assertEqual(wfc, {'id': 1, 
                               'org': 'org1',
                               'department': 'dept1',
                               'orgunit': 'ou1', 
                               'name': 'wfc1'})
        
        
    def test_extract_roles_from_verified_token_n_compare_acl_map_admin_role(self):                    
        enforcer = Enforcer(TLClient, role_acl_map_file=role_acl_map_file,
                            test_token=admin_token)
        result_true, _, _, wfc, _  = enforcer.extract_roles_from_verified_token_n_compare_acl_map(
            'service1:first_api:rulename1')
        print(result_true)
        self.assertEqual(result_true, True)
        
        
    
    def test_extract_roles_from_verified_token_n_compare_acl_map_admin_role_manual_input(self):    
        
        result_true, _, _,  wfc, _  = enforcer_user_input.extract_roles_from_verified_token_n_compare_acl_map(
            'service1:first_api:rulename1')
        print(result_true)
        self.assertEqual(result_true, True)
        
        
    
        
                   
    
    

