#!./venv/bin/python

# -*- coding: utf-8 -*-

import os
import sys
import argparse


possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir))
                                                

# 
# if os.path.exists(os.path.join(possible_topdir,
#                                'app1',
#                                '__init__.py')):
apppath = (os.path.join(possible_topdir,
                               'tokenleaderclient',
                               'tokenleaderclient'))
#    sys.path.insert(0, apppath)

sys.path.insert(0, apppath)

#print(sys.path)
# from tokenleader.app1.adminops import  admin_functions as af
# from tokenleader.app1.catalog import  catalog_functions as cf

from tokenleaderclient.configs.config_handler import Configs
from tokenleaderclient.client.client  import Client
auth_config = Configs()
c = Client(auth_config)

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument( '--authuser', action = "store", dest = "authuser", required = False,)
parent_parser.add_argument('--authpwd', action = "store", dest = "authpwd", required = False)


subparser = parent_parser.add_subparsers()

token_parser = subparser.add_parser('gettoken', parents=[parent_parser], help="Get a token from the tokenleader server ,"
                                    " configure {} and generate the auth file using tlconfig command before "
                                    "getting a token".format(auth_config.config_file))

token_parser = subparser.add_parser('verify', help='verify  a token' )
token_parser.add_argument('-t', '--token', 
                  action = "store", dest = "token",
                  required = True,
                  help = "verify and retrieve users role and work context from the token "
                        " ensure you have obtained the public key from the tokenleader server"
                        "and put it in tl_public_key section of {}".format(auth_config.config_file)
                  )

list_parser = subparser.add_parser('list', help='list entity: org,ou,dept,wfc,role,user ' )
list_parser.add_argument('-e', '--entity', choices=['org', 'ou', 'dept', 'wfc', 'role', 'user' ])
list_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = False,
                  help = "Name of the entitiy , type 'all' as name while listing ",
                  )

delete_parser = subparser.add_parser('delete', help='delete entity: org,ou,dept,wfc,role,user')
delete_parser.add_argument('entity', choices=['org', 'ou', 'dept', 'wfc', 'role', 'user' ])
delete_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = True,
                  help = "Name of the entitiy , type 'all' as name while listing ",
                  )

add_parser = subparser.add_parser('add', help='add entity for all except except user: org,ou,dept,wfc,role')
add_parser.add_argument('entity', choices=['org', 'ou', 'dept', 'role' ])
add_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = True,
                  help = "Name of the entitiy , type 'all' as name while listing ",
                  )

add_parser.add_argument('--orgtype' , action = "store", dest = "orgtype",
                  required = False,
                  help = "internal or external org , to be used while registtering org ",
                  default = "internal")

addwfc_parser = subparser.add_parser('addwfc', help='add a wfc , work function context ')
addwfc_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = True,
                  help = "Name of the wfc simple string ,",
                  )
addwfc_parser.add_argument('--wfcorg' , action = "store", dest = "wfcorg",
                  required = True,
                  help = "org  name linked with the wfc , to be used while registtering wfc ",
                  ) 
addwfc_parser.add_argument('--wfcou' , action = "store", dest = "wfcou",
                  required = True,
                  help = "org  unit name linked with the wfc , to be used while registtering wfc ",
                  ) 
addwfc_parser.add_argument('--wfcdept' , action = "store", dest = "wfcdept",
                  required = True,
                  help = "dept name linked with the wfc , to be used while registtering wfc ",
                  ) 

adduser_parser = subparser.add_parser('adduser', help='Add User')
adduser_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = True,
                  help = "Name of the user",
                  )
adduser_parser.add_argument('--password' , action = "store", dest = "password",
                  required = True,
                  help = "password for the user ",
                  )
adduser_parser.add_argument('--emailid' , action = "store", dest = "emailid",
                  required = True,
                  help = "email id of  the user ",
                  )
adduser_parser.add_argument('--rolenames' , action = "store", dest = "rolenames",
                  required = True,
                  help = "comma separed names of roles which were already registered in the role db.\
                   there should not be any space beteween the role names. \
                   examaple  , --rolenames role1,role2,role3 " 
                  )  
adduser_parser.add_argument('--wfc' , action = "store", dest = "wfc",
                  required = True,
                  help = "wfc or work function context name " 
                  ) 

addservice_parser = subparser.add_parser('addservice', help='add a service in the service catalog')
addservice_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = True,
                  help = "Name of the microservice",
                  )
# addservice_parser.add_argument('--password' , action = "store", dest = "password",
#                   required = False,
#                   help = "service account name password, this password will \
#                   be used for intra service communication",
#                   ) 
addservice_parser.add_argument('--urlext' , action = "store", dest = "urlext",
                  required = False,
                  help = "url of the service endpoint , that is avilable to all users ",
                  ) 
addservice_parser.add_argument('--urlint' , action = "store", dest = "urlint",
                  required = True,
                  help = "url of the service endpoint , that is used for service to service \
                  communication and is not avilable to all users. This is useful when service network and \
                  user network is different",
                  )
addservice_parser.add_argument('--urladmin' , action = "store", dest = "urladmin",
                  required = False,
                  help = "url of the service endpoint , that is used for admin activities. \
                  This is useful to segregte the admin network from user and service network",
                  ) 


deletservice_parser = subparser.add_parser('deletservice', help='delete a service from service catalog')
deletservice_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = True,
                  help = "Name of the microservice",
                  )

listservice_parser = subparser.add_parser('listservice', help='List a service from service catalog')
listservice_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = True,
                  help = "Name of the microservice",
                  )






try:                    
    options = parent_parser.parse_args()  
except:
    #print usage help when no argument is provided
    parent_parser.print_help(sys.stderr)    
    sys.exit(1)

def main():     
  
    if len(sys.argv)==1:
        # display help message when no args are passed.
        parent_parser.print_help()
        sys.exit(1)   
   
    #print(sys.argv)
    if options.authuser and options.authpwd:        
        auth_config = Configs(tlusr=options.authuser, tlpwd=options.authpwd)       
        print("initializing client  using the user name and password supplied from CLI")
    else:
         auth_config = Configs()
         
    c = Client(auth_config)
    
    if  sys.argv[1] == 'gettoken':
        print(c.get_token())
        
    if  sys.argv[1] == 'verify':
        print(c.verify_token(options.token))
    
    if  sys.argv[1] == 'list':
        if options.entity == 'user':
         if options.name:
            print(c.list_user_byname(options.name))
         else:
            print(c.list_users())
                
    if  sys.argv[1] == 'list':
        if options.entity == 'dept':
         if options.name:
            print(c.list_dept_byname(options.name))
         else:
            print(c.list_dept()) 
            
    if  sys.argv[1] == 'list':
        if options.entity == 'org':
         if options.name:
           print(c.list_org_byname(options.name))
         else:
           print(c.list_org())

    if  sys.argv[1] == 'list':
        if options.entity == 'role':
          if options.name:
            print(c.list_role_byname(options.name))
          else:
            print(c.list_role())

    if  sys.argv[1] == 'list':
        if options.entity == 'ou':
          if options.name:
            print(c.list_ou_byname(options.name))
          else:
            print(c.list_ou())
            
    if  sys.argv[1] == 'adduser':
        r = c.add_user()
        print(r)
            
                    
            
    if  sys.argv[1] == 'add':
        
        if options.entity == 'org':      
            af.register_org(options.name)
               
        
        if options.entity == 'ou':      
            r = c.add_orgunit(options.name)
        print(r)
                
                
        if options.entity == 'dept':      
            af.register_dept(options.name)
          
                
        if options.entity == 'role':
            af.register_role(options.name)
    
if __name__ == '__main__':
    main()
    
'''
/mnt/c/mydev/microservice-tsp-billing/tokenleader$ ./tokenadmin.sh  -h    to get help
'''
    
    
