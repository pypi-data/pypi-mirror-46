from flask import Blueprint,  jsonify
from tokenleaderclient.rbac import enforcer

bp1 = Blueprint('bp1', __name__)

@bp1.route('/ep3', methods=['GET', 'POST'])
@enforcer.enforce_access_rule_with_token('service1:first_api:rulename1')                                           
def ep3(wfc=None):
    resp = {'message': 'Catch me if you can'}
    return jsonify(resp)



