from midaxusers.models import db, User, UserAttributes, UserLogin, PasswordNeedsResetError, ManagerTypesEnum, domain_separator
from flask import Flask, jsonify, make_response, abort, request, current_app, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import types, and_, or_
from sqlalchemy.orm.session import Session
from collections import namedtuple
import sys

auth = HTTPBasicAuth()
api = Blueprint('api', __name__, url_prefix='/api/v1.0')

def verify_domain_rights(loggeduser, targetuser = None, targetdomain = None):
    if loggeduser.domain == '*':
        return True
    
    if targetdomain is None:   
        if targetuser is None:
           abort(404)

        if targetuser.domain is None:
            abort(404)        

        targetdomain = targetuser.domain

    targetdomain = targetdomain.casefold()

    userdomainlevels = loggeduser.domain.split(domain_separator)
    targetdomainlevels  = targetdomain.split(domain_separator)
    zipped_tuples = zip(userdomainlevels, targetdomainlevels)
    for user_element, target_element in zipped_tuples:
        if user_element != target_element:
            abort(403)
            
    if len(userdomainlevels) > len(targetdomainlevels):
        abort(403)

    return True

def verify_user_manage_rights(loggeduser, targetuser = None, targetdomain = None, self_update_force_allowed = False):
    if loggeduser != None and loggeduser == targetuser and self_update_force_allowed == True:
        return True

    if loggeduser.user_manage_rights == ManagerTypesEnum.none:
        abort(403)

    if loggeduser.domain == '*':
        return True

    if targetdomain is None:   
        if targetuser is None:
           abort(404)

        if targetuser.domain is None:
            abort(404)        

        targetdomain = targetuser.domain

    targetdomain = targetdomain.casefold()

    userdomainlevels = loggeduser.domain.split(domain_separator)
    targetdomainlevels  = targetdomain.split(domain_separator)
    zipped_tuples = zip(userdomainlevels, targetdomainlevels)
    for user_element, target_element in zipped_tuples:
        if user_element != target_element:
            abort(403)
            
    if len(userdomainlevels) > len(targetdomainlevels):
        abort(403)

    if len(userdomainlevels) == len(targetdomainlevels) and loggeduser.user_manage_rights == ManagerTypesEnum.subdomain:
        abort(403)

    return True

@api.route('/', methods=['GET'])
@api.route('/index', methods=['GET'])
@api.route('/user/attributes', methods=['GET'])
@api.route('/user', methods=['GET'])
@auth.login_required
def index():
    return get_user(uuid = request.loggeduser.uuid)

@api.route('/users/<string:uuid>', methods=['GET'])
@api.route('/users/<string:uuid>/attributes', methods=['GET'])
@auth.login_required
def get_user(uuid):    
    try:
        user = User.search(uuid)
    except:
        abort(404)
    
    return jsonify(user.serialize()), 200

@api.route('/domain/users/inactive', methods=['GET'])
@auth.login_required
def get_current_domain_users_inactive():
    return get_domain_users_inactive(request.loggeduser.domain)

@api.route('/domains/<string:domain>/users/inactive', methods=['GET'])
@auth.login_required
def get_domain_users_inactive(domain):
    return get_domain_users_int(domain, active = False)

@api.route('/domain/users', methods=['GET'])
@auth.login_required
def get_current_domain_users():
    return get_domain_users(request.loggeduser.domain)

@api.route('/domains/<string:domain>/users', methods=['GET'])
@auth.login_required
def get_domain_users(domain):
    return get_domain_users_int(domain, active = True)


@api.route('/domains/<string:domain>/users', methods=['GET'])
@auth.login_required
def get_domain_users_int(domain, active = True):
    loggeduser = request.loggeduser      

    verify_domain_rights(loggeduser, targetdomain = domain)    

    domainlevels = domain.split(domain_separator)
    current_domain_depth = ''    
        
    current_domain_depth = domainlevels[0]    

    if current_domain_depth == '*':
        current_domain_depth = ''
        
    for domainlevel in domainlevels[1:]: 
        if domainlevel is not None and len(domainlevel) > 0:
            current_domain_depth += '^{}'.format(domainlevel)
        
    current_domain_depth += '%'      

    users = User.query.filter(User.domain.like(current_domain_depth)).filter_by(active = active)

    if users is not None:
        return jsonify([e.serialize() for e in users])

    abort(404)

   

@api.route('/users/', methods=['POST'])
@auth.login_required
def create_user():
    loggeduser = request.loggeduser
    
    verify_user_manage_rights(loggeduser, targetdomain = request.json['domain'])    

    try:
        newuser = User(namedtuple("User", request.json.keys())(*request.json.values()))
    except Exception as e:        
        print(str(e), file=sys.stderr)
        abort(400)

    try:
        db.session.add(newuser)
        db.session.commit()
    except Exception as e:        
        print(str(e), file=sys.stderr)
        return jsonify({'error': "Duplicate user"}), 409

    return jsonify(newuser.serialize()), 201

@api.route('/users/<string:uuid>', methods=['PUT'])
@auth.login_required
def update_user(uuid):    
    try:
        targetuser = User.search(uuid)
    except:
        abort(404)

    verify_user_manage_rights(request.loggeduser, targetuser = targetuser)  

    #this allows domain changing as well so we need to check the new domain too if present
    try:
        verify_user_manage_rights(request.loggeduser, targetdomain = request.json['domain'])  
    except KeyError:
        pass 

    try:
        targetuser.update_from_named_tuple(namedtuple("User", request.json.keys())(*request.json.values()))
        db.session.commit()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return jsonify({'error': "Cannot update user"}), 400
    
    return jsonify(targetuser.serialize()), 200


@api.route('/users/<string:uuid>/logins', methods=['POST'])
@auth.login_required
def change_user_logins(uuid):
    try:
        loggeduser = request.loggeduser
        targetuser = User.search(uuid)
    except Exception as e:
        print(str(e), file=sys.stderr)
        abort(404)

    verify_user_manage_rights(loggeduser, targetuser = targetuser, self_update_force_allowed = True)    

    
    try:                   
        for key, value in request.json.items():
            value['login_type'] = key
            if value['login_key'] is None or len(value['login_key']) == 0:
                targetuser.logins.pop(key, None)
            else:
                a_login = targetuser.logins.get(key, None)
                if a_login is None:
                    a_login = UserLogin()
                    
                a_login.update_from_dict(value)
                targetuser.logins[key] = a_login
        
        db.session.commit()
    except Exception as e:
        print(str(e), file=sys.stderr)
        abort(400)

    return jsonify({'result' : 'Logins Updated'}), 200


@api.route('/user/password', methods=['POST'])
def reset_password():
    try:
        verify_pw_internal(request.authorization.username, request.authorization.password)
    except PasswordNeedsResetError as exc:
        request.loggeduser = exc.user
    except Exception as e:
        print(str(e), file=sys.stderr)
        abort(401)    

    try:
        request.loggeduser.logins[request.login_type].password = request.json['password']
        request.loggeduser.logins[request.login_type].force_password_change = False    
        db.session.commit()
    except:
        abort(400)

    return jsonify({'result' : 'Password Reset'}), 200


@api.route('/users/<string:uuid>/deactivate', methods=['POST'])
@auth.login_required
def deactivate_user(uuid):
    try:
        targetuser = User.search(uuid)
    except Exception as e:
        print(str(e), file=sys.stderr)
        abort(404)

    verify_user_manage_rights(request.loggeduser, targetuser = targetuser, self_update_force_allowed = True)
    
    try:  
        targetuser.active = False          
        db.session.commit()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return jsonify({'error': "Cannot deactivate user"}), 409

    return jsonify({'status': "SUCCESS"}), 200





#need to be the last routes
@api.route("/<path:missing>", methods=['PUT', 'PATCH', 'DELETE'])
@auth.login_required
def method_not_allowed_on_unknown_path(missing):
    abort(405)

@api.route("/<path:missing>")
@auth.login_required
def path_did_not_match(missing):
    abort(404)


@auth.verify_password
def verify_pw(username, password):
    try:
        return verify_pw_internal(username, password)
    except PasswordNeedsResetError:
        abort(423)
    except Exception as e:   
        print(str(e), file=sys.stderr)
        return False
        

def verify_pw_internal(username, password):
    if username is None or password is None:
        return False
    try:
        request.login_type = request.headers['Login-Type']
    except KeyError:
        request.login_type = 'WEBSITE'
    
    request.loggeduser = UserLogin.get_user({'login_type': request.login_type, 'login_key': username, 'password': password}, check_password=True)
    
    return True


@api.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@api.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Access forbidden for user'}), 403)

@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@api.errorhandler(423)
def locked(error):
    return make_response(jsonify({'error': 'User has been locked, change password.'}), 423)

@api.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@auth.error_handler
def unauthorized_auth():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

