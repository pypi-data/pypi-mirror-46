
New feature and major changes 

ver 1.5
--------------------------

Client was ignoring the user supplied passowrd in config and falling back to encrypted password stored as serect
This bug has been sloved

ver 1.4 
---------------------------------
api for add , delete , all entities 
 

ver 1.3
-------------------------------------------
request_id , time_stamp and client_address  is included in wfc . 


ver 1.2
----------------------------------------------
Enforcer can now be instanciated with test_token and role_acl_map_file


enforcer = Enforcer(TLClient, role_acl_map_file=role_acl_map_file,
                            test_token=sample_token_role_as_list_valid_role)

This will enable  all the actual  rest api to be tested with test enforcer without  running tokenleader 

ver 1.1 
----------------------
username and email made available to api route functions through enforcer. function now can extract it from the manadatory 
wfc param 

ver 1.0
-----------------
more api routes for listing objects 

tokenleader list -e <object name e.g user, org, ou , role  etc. > 

ver 0.71 
-------------------------

1. Before the client instanciation , we need a auth_config instance 
2. user name and password can be passed to auth_config=Configs() instance wither form the  config file  
   or  as a parameter of auth_config=Configs(tlusr , tlpwd)
3. tl_user and tl_url configuration is moved to client_configs.yml  file  since there is no need to keep these files
   as secret along with the encrypted password file
   


tokenleaderclient
=================================

Pyhton  client  - reads  users credentials from the /etc/tokenleader/client_configs.yml . 
The user name and password can be also provided as input  while initializing the Client class.

When it is from file , the encrypted password is generested by  a cli utility named
tokenleader-auth -p <password>


the client has the folowing operations :  

-- tokenleader-auth  cli utility for storing uers credential in local disk with password encryption  (normally users home directory)

-- get token from token leader , including the catalog information 

-- verify the token and  retrieve users role and  wfc( work function context)

-- provides an role based access control enforcer which can be bind to a flask api route  



 
Installation:
=================================================================
create a venv :   in your home diectory $ 

		virtualenv -p python3 venv

		source venv/bin/activate

		pip install tokenleaderclient  

Configuration
===================================================


The configuration file is divided into two files . 
/etc/tlclient/general_configs.yml which holds the non secret configs  about the client and looks as
        
        sudo vi /etc/tokenleader/client_configs.yml

		user_auth_info_from: file # OSENV or file
		user_auth_info_file_location: tokenleaderclient/tests/testdata/test_settings.ini
		fernet_key_file: tokenleaderclient/tests/testdata/farnetkeys
		tl_public_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCYV9y94je6Z9N0iarh0xNrE3IFGrdktV2TLfI5h60hfd9yO7L9BZtd94/r2L6VGFSwT/dhBR//CwkIuue3RW23nbm2OIYsmsijBSHtm1/2tw/0g0UbbneM9vFt9ciCjdq3W4VY8I6iQ7s7v98qrtRxhqLc/rH2MmfERhQaMQPaSnMaB59R46xCtCnsJ+OoZs5XhGOJXJz8YKuCw4gUs4soRMb7+k7F4wADseoYuwtVLoEmSC+ikbmPZNWOY18HxNrSVJOvMH2sCoewY6/GgS/5s1zlWBwV/F0UvmKoCTf0KcNHcdzXbeDU9/PkGU/uItRYVfXIWYJVQZBveu7BYJDR bhujay@DESKTOP-DTA1VEB
		tl_user: user1
		tl_url: http://localhost:5001
		ssl_verify: False

you may need the  public key from tokenleader server or use the default one which works with the 
defualt docker bhujay/tokenleader:1.8 

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDENN9QYdy6RUEJUsOcGECj+7uvyhHlNaZqVN5YcP/MCxBIEoWD3ewu1bQxqW/xC938gHXGZ7NWncv+u9IADwmVYBD8/hYUWJFOKFOKtt8+ZcAFamAz6qGAmKFUnThZ5C/n1PAwS8L03aj62NfxXTjgpohcKRn3Pq9SW7TNgeApn3RSkGoydKJOqo8GeNnKuDxJMHhkR663pLtYH+VOvE/TzethQn64Xc1/HL02o6HRsCWtI0UXev2RLMsVa/wP0k2ItUi7YnmZPyL6ATfeiHIRrRmfDsidqUA6eNZ+fsdw6dO6H0TGggeYd+d8I14PBTx6zYwL+QIEiqNBxP6nIdMp bhujay@DESKTOP-DTA1VEB

public-key:10.174.112.143
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCrcbPLYZemD/nGgx7oGdstVplCunKLscapN7AKomxLCM5eJOltxoI9r2tsX9rOuiCoSrstg71FHzUby4wcPLQERPFB5bN/otAjQpRjvLM3OL3S4ZEPpBnN6FKK1U5QLh5nF/sVCw70Xa63SDWeliCAL3uAvrqZM4iMHahg1Ze2AzJCnapgOdKy9eVMQ4Ergx7MYZhkFrGILp0ZT4GIqLZvWQyDErq1wE6F2eLY0rhR3PtiNMC4Hai/jXlk5f9jvizo7Lpwx6rSRPQVNkleicsMOBHQqnAYqh69VXdCppKkLtA02+lEwGL0rS/1l3y45Mc03NWuzxuRaI6QaSHzhQm7 ubuntu@tokenleader

users authentiaction information . The file is generated using  an cli   
------------------------------------------------------------------------------

		tokenleader-auth  -p user1 

the file , /home/bhujay/tlclient/user_settings.ini , thus generated will looks like this :    

		[DEFAULT]  		
		tl_password = gAAAAABcYnpRqet_VEucowJrE0lM1RQh2j5E-_Al4j8hm8vJaMvfj2nk7yb3zQo95lBFDoDR_CeoHVRY3QBFFG-p9Ga4bkJKBw==

note that the  original password has been encrypted before  saving in the file. if the keyfile is lost or the 
password is forgotten   the  file has to be deleted and recreated. Accordingly the users password in the 
tokenleader server also to be changed. 



CLI utilities 
====================================================================
using user name and password from config file 

		tokenleader  gettoken 
		
or username and password can be supplied  theough the CLI 

		gettoken  --authuser user1 --authpwd user1
		
Other CLI operaions 

		tokenleader  verify -t <paste the toen here>
		tokenleader  list user
 
 
Python client 
======================================================================================
From python shell it works as follows:

        from tokenleaderclient.configs.config_handler import Configs    
		from  tokenleaderclient.client.client import Client 
		
		
this will read  the credentials from configurations file. Will be used for CLI. 
 
		auth_config = Configs()  	
		
the user name and password will be  taken from the input  but rest of the settings will be from config files.  
This will be used for browser based login  

		auth_config = Configs(tlusr='user1', tlpwd='user1') 
		
Inititialize the client with auth_config
	 
		c = Client(auth_config)
		c.get_token()

{'service_catalog': 
                    {'tokenleader': 
                                   {'endpoint_url_admin': None, 
                                   'endpoint_url_external': None, 
                                   'name': 'tokenleader', 
                                   'endpoint_url_internal': 'localhost:5001', 
                                   'id': 1}, 
                    'linkInventory': {'endpoint_url_admin': None, 
                    'endpoint_url_external': 'https://192.168.111.141:5004', 
                    'name': 'linkInventory', 
                    'endpoint_url_internal': 'https://192.168.111.141:5004', 
                    'id': 2}}, 
'status': 'success', 
'message': 'success', 
'auth_token': 'AA'}
		
{'message': 'success', 'status': 'success', 'auth_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJpYXQiOjE1NDk5NjcxODAsImV4cCI6MTU0OTk3MDc4MCwic3ViIjp7IndmYyI6eyJvcmd1bml0Ijoib3UxIiwibmFtZSI6IndmYzEiLCJkZXBhcnRtZW50IjoiZGVwdDEiLCJpZCI6MSwib3JnIjoib3JnMSJ9LCJlbWFpbCI6InVzZXIxIiwiaWQiOjEsInVzZXJuYW1lIjoidXNlcjEiLCJyb2xlcyI6WyJyb2xlMSJdfX0.gzW0GlgR9qiNLZbR-upuzgHMw5rOm2luV-EnHZwlOSJ-0kJnHsiiT5Wk-HZaqMGZd0YJxA1e9GMroHixtj7WJsbLLjhgqQ5H1ZprCkA9um6-vdkwAFVduWIqIN7S6LbsE036bN7y4cdgVhuJAKoiV1KyxOU1-Hxid5l3inL0Hx2aDUrZ3InzFKBw7Mll86xWdfkpHSdyVjVuayKQMvH2IdT3N15k4O2tSwV3t6UhG6MO0ngHFt3LFR471QWGzJ8UyRzqyqbheuk5vwPk684MfRclCtKx33LWAMf-HXQgVA2py_NzmEiY1ROsKmZqpbIO9YKIO_aFCmzB7DQSI8dcYg', 'service_catalog': {'tokenleader': {'endpoint_url_external': 'localhost:5001', 'endpoint_url_admin': None, 'id': 2, 'endpoint_url_internal': None, 'name': 'tokenleader'}, 'micros1': {'endpoint_url_external': 'localhost:5002', 'endpoint_url_admin': None, 'id': 1, 'endpoint_url_internal': None, 'name': 'micros1'}}}
		
		c.verify_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJpYXQiOjE1NDk5NjcxODAsImV4cCI6MTU0OTk3MDc4MCwic3ViIjp7IndmYyI6eyJvcmd1bml0Ijoib3UxIiwibmFtZSI6IndmYzEiLCJkZXBhcnRtZW50IjoiZGVwdDEiLCJpZCI6MSwib3JnIjoib3JnMSJ9LCJlbWFpbCI6InVzZXIxIiwiaWQiOjEsInVzZXJuYW1lIjoidXNlcjEiLCJyb2xlcyI6WyJyb2xlMSJdfX0.gzW0GlgR9qiNLZbR-upuzgHMw5rOm2luV-EnHZwlOSJ-0kJnHsiiT5Wk-HZaqMGZd0YJxA1e9GMroHixtj7WJsbLLjhgqQ5H1ZprCkA9um6-vdkwAFVduWIqIN7S6LbsE036bN7y4cdgVhuJAKoiV1KyxOU1-Hxid5l3inL0Hx2aDUrZ3InzFKBw7Mll86xWdfkpHSdyVjVuayKQMvH2IdT3N15k4O2tSwV3t6UhG6MO0ngHFt3LFR471QWGzJ8UyRzqyqbheuk5vwPk684MfRclCtKx33LWAMf-HXQgVA2py_NzmEiY1ROsKmZqpbIO9YKIO_aFCmzB7DQSI8dcYg')
		
{'payload': {'iat': 1549967180, 
             'exp': 1549970780, 
             'sub': {'username': 'user1', 
                     'roles': ['role1'], 
                     'id': 1, 
                     'email': 'user1', 
                      'wfc': {'orgunit': 'ou1', 
                              'id': 1, 
                              'org': 'org1', 
                              'department': 'dept1', 
                              'name': 'wfc1'}}}, 
 'message': 'Token has been successfully decrypted', 
 'status': 'Verification Successful'}
		


for RBAC configure  /etc/tokenleader/role_to_acl_map.yml
============================================================================================
	
      sudo mkdir /etc/tokenleader 
      sudo vi /etc/tokenleader/role_to_acl_map.yml
	 
	  maintain atleast one role and one entry in the follwoing format 
	 
		- name: role1
		  allow:
		  - tokenleader.adminops.adminops_restapi.list_users		  
		  
		- name: role2
		  allow:
		  - service1.third_api.rulename3
		  - service1.fourthapi_api.rulename4

		from tokenleaderclient.rbac.enforcer import Enforcer
		enforcer = Enforcer(c)
		
Here c is the instance of  Client() , the tokenleadercliet which we have initialized in the previous
example of python client.  

Now @enforcer.enforce_access_rule_with_token('rulename1') is avilable within any flask application  
where tokenleader client is installed.   



=============================================================================================================


the detial of the RBAC is as follows:  
 ==============================================================================================
 
 How role based access control (RBAC) enforcing is done   
=======================================================

An enforcer  decorator function named @authclient.enforce_access_rule_with_token(rule_name) does   
the job.  Every api route shoukd bind this enforcer decorator with a rule name. The list of rules  
are deifned in the etc/tokenleader/role_to_aclmap.yml file  in the format of:  
 
		"serviename:api_route_name:access_method_name"    
		
 		  e.g. micros1:firstapi:read_all_entries  


How authentication works  
===========================
a. Any requests coming to a flask applications api endpoint  url should carry a   
   "X-Auth-Token": "<JWT token>" in its header.   
   
   The enforcer rejects the request if the header does not carry the token.  
    
   Typical  request from cli is :  
   
		curl -H  "X-Auth-Token:<paste toekn here>"  http://localhost:5000/ep3  
   
needless to say , before putting this request , one has to get a token from the tokkenleader by issuing
requests such as :  

		curl -X POST -d '{"username": "admin", "password": "admin"}'  \
		-H "Content-Type: Application/json"  localhost:5001/token/gettoken  

or using the tokeneader client as shown below 	
		

Before this request the user should be registered in the tokenleader service by the admin of tokeleader server.

 For authorization , the enforcer decorator to be used by each microservice .  
 A sample microsdervice with this decoraator has been shown here . Any api route which is bind 
 with this decorator will retrieve role and wfc(work function context) from the tokenleader service.   
 The role will be used by the decorator to compare with the local acl map yml file for allowing or denying the  
 access to api route url. 
 The wfc will be passed to the api route function for later usage by the function for database query filtering. 
 The api route function must have a keyword argument 'wfc'  for the enforcer decorator to work.  


b. the token then is verified by the token leader client and decryption is done.
   if the status is sucessful the autheticaation is treated as success  otherwise 
   authentication failure messsage is returned.
   list of roles are  retrieved from the  decrypted token  
   token leader new version has been designed to multiple role to a single user   


c. How  from the role authorization to the api route is done
===================================================================

once users role is known , for admin role all checks are bypassed but for other roles  
a search is performed in /etc/tokenleaderclient/role_to_acl_map.yml to check if agianst the role
there is an entry for the api access method. The yml file entry is as below:
- name: role1
  allow:
  - service1:first_api:rulename1
  - service1:second_api:rulename2
  
- name: role2
  allow:
  - service1:third_api:rulename3
  - service1:fourthapi_api:rulename4
  
 
For the programmer , when a new api route is introduced it is much easier to create new  aceess control 
by making an entry in the srole_to_acl_map.yml instated of database operation

every time the api  call is made , the enforcer decorator reload the role_to_acl_map.yml  making it possible to 
make online changes to the yml file by the operator . 

For each role  assigned to user  the  check is done in iterative way  and if the rule is found  for any of the role 
authorization is allowed.


Future
==============
- consistency checking between two yml file and the actual  api route to be done 
- as the role map size grows , caching to be improved for faster retrival of role map
- in the token leader currently role is directly entered in users table , the role table  to be segregarted 
- to be mapped with user through foreign key

d. Work Function Context for further granular control of who can see what based on users work function
====================================================================================================
   Work function context for the user is also retrived from the token leader.
   The wfc is  passed to the api route function for later usage by 
   the function for database query filtering. 
   The api route function must have a keyword argument 'wfc'  for the enforcer decorator to work.
   
   Example :  
 
	    @bp1.route('/test1', methods=[ 'POST'])
		@authclient.enforce_access_rule_with_token(<'rulename'> )
		def acl_enforcer_func_for_test(wfc=None):
		'''
		the rule name in this case should be :
		'pkgname.modulename.classname.acl_enforcer_func_for_test'
		for each api route functions the parameter wfc must be present
		'''
		    msg = ("enforcer decorator working ok with wfc org = {},"
		            "orgunit={}, dept={}".format(wfc.org, wfc.orgunit, wfc.department))
		    print("requestid: {}, date: {}, client_address:{}".format(
        						wfc.request_id,  wfc.time_stamp, wfc.client_address))
		  
		    return msg
	  
In the above example, the decorator  impose aceess control on the route /test1 . 

role name for the user  is retrived from the token leader , compared with the rule to acl map yml file 
(/etc/tokenleaderclient/role_acl_map_file.yml) which is maintained locally in the server where the service is running .

the role_to_acl_map file maps the  api route function names to and looks like :
- name: role1
  allow:
  - pkgname.modulename1.acl_enforcer_func_for_test
  - pkg1.module1.acl_enforcer_func_for_test
 
 check the sample data  and test cases  inside the tokenleaderclient for better understanding.
 tokenleader server ( this repo) it self uses  the tokenleader client for enforcing the rbac for 
 many api routes , for example adding users , listing users etc. Check the 
 tokenleader/app1/adminops/adminops_restapi.py file to get a better understanding or mail me
 your query at bhujay.bhatta@yahoo.com

decorator alos retrived work function context for the  user from tokenleader and passed it to 
original route function acl_enforcer_func_for_test .   The route function mandatorily to have a 
parameter called wfc as argument for the wfc , to get the value from the decorator.

now within the acl_enforcer_func_for_test  funtion  , wfc attributes like org, orgunit and department is used
to display a message. They actually  to be used for database query filtering so that based on the work function
user is able to view only relevant information.
		

Tests
==============================================
git clone the repo and then run from the pkg  folder

        python -m unittest  discover tokenleaderclient.tests
        
		python -m unittest tokenleaderclient.tests.unittests.test_acl.TestAcl  
		python -m unittest tokenleaderclient.tests.unittests.test_acl_enforcer_decorator.TestAclEnforcer  

This one need tokenleader server to be running  

		python -m unittest tokenleaderclient.tests.unittests.test_integration_tests.BaseTestCase



change log 
======================

ver 0.70
----------------
public key reading from id_rsa.pub disabled since it is picked up from yml

ver 0.69
-----------------------

1. all configs are in /etc/tokenleader
2. tlclient command changed to tokenleader
3. tlconfig command changed to tokenleader-auth

ver 0.64
-----------------

1. bug - tlclient command  breaking code resloved 

ver 0.63
-----------------

1. check for  presense of required  keys in /etc/tlclient/general_configs.yml   
2. ssl_verify: False corrently this should be always False, cert verification can be introduced later based on reqirement.  
3. ability to connect on https   when the  tokenleader url is https  in user_settings.ini   



TODO:
-----------------

1) integrate rbac inside the client - Done
2) make the client an installable pkg  - Done
3) extend user creation/ catalog creation  etc. as part of the client  
4) develop client for micros1  - which will make it easier to understand how  other microservice  should be developed keeping token leader in mind.  Target one week.


if expired token , should read the users credentials from file and get a fresh token
returns verification result  - may not be required 

token admin operation for user and role registration , org, dept and other db opertaions - done from servers cli 

should support https and certificates
python-pkg with cli facility for getting token
it should be a dependency  pkg to other microservices
other microsrrvies should be able to import and use it  - Done



