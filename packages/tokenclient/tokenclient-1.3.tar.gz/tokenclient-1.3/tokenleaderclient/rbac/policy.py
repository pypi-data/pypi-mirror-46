import yaml


def parse_yml(file):
    with open(file, 'r') as f:
        try:
            parsed = yaml.safe_load(f)
        except yaml.YAMLError as e:            
            raise ValueError(six.text_type(e))
        return parsed or {}

def load_service_access_policy(service_access_policy_file='acl/service_access_policy.yml'):
    return parse_yml(service_access_policy_file)

def load_role_to_acl_map(role_to_acl_map_file='acl/role_to_acl_map.yml'):
    return parse_yml(role_to_acl_map_file)
    
    
    