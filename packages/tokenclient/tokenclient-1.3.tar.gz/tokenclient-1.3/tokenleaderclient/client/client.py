import requests
import json
import jwt



class Client():

    emailid = ''
    domain = ''
    otp = ''
    def __init__(self , auth_config):
        # print(dir(auth_config))
        '''
        auth_config is  tokenleaderclient.configs.config_handler.Configs object
        initialized by the user of the client
        '''
        if auth_config.tl_user:
            # print('username found')
            self.tl_username = auth_config.tl_user
#        auth_config.decrypt_password()
        if auth_config.tl_password:
            # print('password found')
            self.tl_password = auth_config.tl_password
        if auth_config.domain:
            self.domain = auth_config.domain
        if auth_config.tl_email:
            # print('email login')
            self.emailid = auth_config.tl_email
        if auth_config.otp:
            # print('login with otp')
            self.otp = auth_config.otp
        self.tl_url = auth_config.tl_url
        self.ssl_verify = auth_config.ssl_verify
        self.tokenleader_public_key = auth_config.tl_public_key

    def get_token(self, username=None, otp=None):
        api_route = '/token/gettoken'
        service_endpoint = self.tl_url + api_route
        #print(service_endpoint)
        # print(username)
        # print(otp)
        headers={'content-type':'application/json'}
        if username is not None and otp is not None:
            self.data=json.dumps(dict(username=username, otp=otp))
        elif username is None and otp is not None:
            e = {'error': 'please enter username and otp, incase you are external user'}
            return e
        elif username is not None and otp is None:
            e = {'error': 'please enter username and otp, incase you are external user'}
            return e
        else:
            # print('getting into else part')
            if self.domain and self.otp:
                self.data=json.dumps(dict(username=self.tl_username, password=self.tl_password, domain=self.domain, otp=self.otp))
            elif self.domain:
                self.data=json.dumps(dict(username=self.tl_username, password=self.tl_password, domain=self.domain))
            elif self.otp and not self.emailid:
                self.data=json.dumps(dict(username=self.tl_username, password=self.tl_password, otp=self.otp))
            elif self.emailid and self.otp:
                self.data=json.dumps(dict(email=self.emailid, otp=self.otp))
            # if self.tl_username and self.tl_password and not self.domain and not self.otp:
            else:
                self.data=json.dumps(dict(username=self.tl_username, password=self.tl_password))
        # print(self.data)
        try:
            r = requests.post(service_endpoint, self.data, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}
        # print(r_dict)
        return r_dict

    def verify_token_from_tl(self,token,):
        api_route = '/token/verify_token'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}
        try:
            r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}
    #     print(r.content)
    #     print(type(r.content))

        return r_dict

    def verify_token(self, token):
        #print(self.tokenleader_public_key)
        payload = self._decrypt_n_verify_token(token, self.tokenleader_public_key)
        if payload == "Signature expired. Please log in again." :
            status = "Signature expired"
            message = "Signature expired. Please log in and get a fresh token and send it for reverify."
        elif payload == "Invalid token. Please log in again.":
            status = "Invalid token"
            message = "Invalid token. obtain a valid token and send it for verifiaction"
        elif payload == "did you configured the correct public key in the client_config file":
            status = " Invalid public key , can not decrypt  token"
            message = status
        elif not isinstance(payload, dict):
            status = "could not verify token"
            message = status

        else:
            status = "Verification Successful"
            message = "Token has been successfully decrypted"

        responseObject = {
                            'status': status,
                            'message': message,
                            'payload': payload}
#         print(responseObject)
        return responseObject

    def _decrypt_n_verify_token(self, auth_token, pub_key):
        try:
            payload = jwt.decode(
                auth_token,
                pub_key,
                algorithm=['RS512']
            )

            return payload
    #
        except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'
        except ValueError as e:
               return 'did you configured the correct public key in the client_config file'
        except Exception as e:
            return "could not decrypt the token for error {}".format(e)


    def list_users(self, username, otp=None):
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/list/users'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}
        try:
            r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}

#       print(r_dict)  # for displaying from the cli  print in cli parser
        return r_dict

    def list_org(self, username, otp=None):
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/list/org'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}
        try:
            r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())
        except Exception as e:
        	r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}

        return r_dict

    def list_wfc(self, username, otp=None):
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/list/wfc'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}
        r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def list_dept(self, username, otp=None):
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/list/dept'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}
        r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def list_role(self, username, otp=None):
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/list/role'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}
        r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def list_ou(self, username, otp=None):
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/list/ou'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}
        r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def add_orgunit(self, data, username, otp=None):
        '''
        data = {"ouname": "ou5",}
        '''
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/add/ou'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.post(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def add_dept(self, data, username, otp=None):
        '''
        data = {"deptname": "dept5",}
        '''
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/add/dept'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.post(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def add_org(self, data, username, otp=None):
        '''
        data = {"oname": "org5",}
        '''
        if otp is not None:
            token = self.get_token(username, otp).get('auth_token')
        else:
            token = self.get_token().get('auth_token')
        api_route = '/add/org'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.post(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def add_role(self, data, username, otp=None):
        '''
        data = {"rolename": "role5",}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/add/role'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.post(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def add_user(self, data, username, otp=None):
        '''
        data = {"username": "user5", "email": "user5", "password": "user5", "wfc": "wfc1", "roles": ["role1"]}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/add/user'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.post(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def add_wfc(self, data, username, otp=None):
        '''
        data_must_contain = ['fname', 'orgname', 'ou_name', 'dept_name']
        data = {"fname": "wfc6", "orgname": "org1", "ou_name": "ou1", "dept_name": "dept1"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/add/wfc'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.post(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def delete_user(self, data, username, otp=None):
        '''
        data = {"username": "user5"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/delete/user'
        service_endpoint = self.tl_url + api_route
        print(service_endpoint)
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.delete(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def delete_org(self, data, username, otp=None):
        '''
        data = {"oname": "org5"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/delete/org'
        service_endpoint = self.tl_url + api_route
        print(service_endpoint)
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.delete(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def delete_ou(self, data, username, otp=None):
        '''
        data = {"ouname": "ou5"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/delete/ou'
        service_endpoint = self.tl_url + api_route
        print(service_endpoint)
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.delete(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def delete_dept(self, data, username, otp=None):
        '''
        data = {"deptname": "dept5"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/delete/dept'
        service_endpoint = self.tl_url + api_route
        print(service_endpoint)
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.delete(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def delete_role(self, data, username, otp=None):
        '''
        data = {"rolename": "role5"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/delete/role'
        service_endpoint = self.tl_url + api_route
        print(service_endpoint)
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.delete(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def delete_wfc(self, data, username, otp=None):
        '''
        data = {"wfcname": "wfc5"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/delete/wfc'
        service_endpoint = self.tl_url + api_route
        print(service_endpoint)
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.delete(service_endpoint,
                          headers=headers,
                          data=json.dumpsdata,
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def add_service(self, data, username, otp=None):
        '''
        data_must_contain = ['name', 'urlint', 'urlext','urladmin']
        data = {"name": "testservice", "urlint": "http//:localhost:5005", "urlext": "http//:localhost:5005", "urladmin": "http//:localhost:5005"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/add/service'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.post(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict

    def delete_service(self, data, username, otp=None):
        '''
        data = {"name": "testservice"}
        '''
        if otp is not None:             
            token = self.get_token(username, otp).get('auth_token')         
        else:             
            token = self.get_token().get('auth_token')
        api_route = '/delete/service'
        service_endpoint = self.tl_url + api_route
        print(service_endpoint)
        headers={'X-Auth-Token': token, 'content-type':'application/json' }
        r = requests.delete(service_endpoint,
                          headers=headers,
                          data=json.dumps(data),
                          verify=self.ssl_verify)
        r_dict = json.loads(r.content.decode())
        return r_dict
