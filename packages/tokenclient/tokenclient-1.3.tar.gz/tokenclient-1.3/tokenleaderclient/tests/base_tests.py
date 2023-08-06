import os
import unittest
from tokenleaderclient.configs.config_handler import Configs
from tokenleaderclient.client.client import Client
from setuptools.command.setopt import config_file

settings_file = 'tokenleaderclient/tests/testdata/test_general_configs.yml'
pwd_file = 'tokenleaderclient/tests/testdata/test_settings.ini'
tl_user = 'user1'
tl_pwd = 'user1'
tl_url  =  'http://localhost:5001'

conf = Configs(config_file=settings_file)
conf_from_manual_input = Configs(config_file=settings_file , tlusr=tl_user , tlpwd=tl_pwd )
TLClient = Client(conf)  
TLClient_Param=Client(conf_from_manual_input)
   


class TestConfigs(unittest.TestCase):
    
    def test_generate_auth_file_with_encrypted_pwd(self):
        if os.path.exists(pwd_file):
            os.remove(pwd_file)
        conf.generate_user_auth_file(tl_pwd)
        self.assertTrue(os.path.exists(pwd_file))
        
    def test_generate_auth_file_with_encrypted_pwd_as_param(self):
        if os.path.exists(pwd_file):
            os.remove(pwd_file)
        conf_from_manual_input.generate_user_auth_file(tl_pwd)
        self.assertTrue(os.path.exists(pwd_file))
        
    def test_get_user_auth_info(self):
        conf.decrypt_password()
        self.assertTrue((conf.tl_password , conf.tl_user, conf.tl_url) == (tl_pwd, tl_user, tl_url))
        
    
    def test_client_has_got_the_encrypted_n_param_passwords(self):
        self.assertTrue(TLClient.tl_password == tl_pwd)
        self.assertTrue(TLClient_Param.tl_password == tl_pwd)   
    
    def test_conf_and_client_same_password(self):
        srijib_conf = Configs(tlusr='srijib' , tlpwd='srijib3131441')
        srijib_TLClient = Client(srijib_conf)
        self.assertTrue(srijib_TLClient.tl_username == srijib_conf.tl_user)
        self.assertTrue(srijib_TLClient.tl_password == srijib_conf.tl_password)
        
         
    def test_get_token_method(self):        
        TLClient = Client(conf)            
        r1 = TLClient.get_token()
        print(r1)   
        self.assertTrue(isinstance(r1, dict))        
        self.assertTrue('auth_token'  in r1)   
        
    
    def test_get_token_method_with_manual_user_input(self):        
        TLClient = Client(conf_from_manual_input)                 
        r1 = TLClient.get_token()
        print(r1)   
        self.assertTrue(isinstance(r1, dict))        
        self.assertTrue('service_catalog' in r1)   
    
     
    
    def test_verify_token_local(self):
        TLClient = Client(conf) 
        r = TLClient.get_token()
        print(r)
        token = r['auth_token']
        r1 = TLClient.verify_token(token)
        self.assertTrue(r1['status'] == 'Verification Successful')        
        self.assertTrue(isinstance(r1.get('payload').get('sub'), dict))
        
    
    def test_verify_token_local_manaul_user(self):
        TLClient = Client(conf_from_manual_input) 
        r = TLClient.get_token()
        print(r)
        token = r['auth_token']
        r1 = TLClient.verify_token(token)
        self.assertTrue(r1['status'] == 'Verification Successful')        
        self.assertTrue(isinstance(r1.get('payload').get('sub'), dict))
    
