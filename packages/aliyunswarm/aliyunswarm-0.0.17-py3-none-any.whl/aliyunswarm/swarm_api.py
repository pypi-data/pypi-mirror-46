import sys
from .common import *
from .config import *
from .http_api import *

class SwarmApi():
    http_api = None

    def __init__(self, swarm_url, ca_pem, cert_pem, key_pem):
        self.http_api = HttpApi(swarm_url, ca_pem, cert_pem, key_pem)

    #######################################
    #
    # application api
    #
    #######################################
    @auto_handle_http_response
    def create_application(self, template, application_name, description='', version='1.0', environment=None, latest_image=False):
        data = {
                "name": application_name,
                "description": description,
                "template": template,
                "version": version,
                "environment": environment,
                "latest_image": latest_image
            }
        path = PROJECTS_API_PATH
        return self.http_api.send_post_request(path, headers=JSON_HEADERS, data=data)

    @auto_handle_http_response
    def query_applications(self, application_name=None, services=False, containers=False):
        params = {
            'services': services,
            'containers': containers,
        }
        if application_name:
            params['q'] = application_name
        path = PROJECTS_API_PATH
        return self.http_api.send_get_request(path, params=params)


    @auto_handle_http_response
    def stop_application(self, application_name, timeout=10):
        path = PROJECTS_API_PATH + application_name + '/stop' + '?t=' + str(timeout)
        return self.http_api.send_post_request(path)


    @auto_handle_http_response
    def start_application(self, application_name):
        path = PROJECTS_API_PATH + application_name + '/start'
        return self.http_api.send_post_request(path)


    @auto_handle_http_response
    def kill_application(self, application_name):
        path = PROJECTS_API_PATH + application_name + '/kill'
        return self.http_api.send_post_request(path)


    @auto_handle_http_response
    def delete_application(self, application_name, force='true', volume='true'):
        params = {
            'force': force,
            'volume': volume
        }
        path = PROJECTS_API_PATH + application_name
        return self.http_api.send_delete_request(path, params)


    @auto_handle_http_response
    def redeploy_application(self, application_name):
        path = PROJECTS_API_PATH + application_name + '/redeploy'
        return self.http_api.send_post_request(path)


    @auto_handle_http_response
    def update_application(self, template, application_name, description='', version='1.0', environment=None, latest_image=False):
        data = {
                "name": application_name,
                "description": description,
                "template": template,
                "version": version,
                "environment": environment,
                "latest_image": latest_image
            }
        path = PROJECTS_API_PATH + application_name + '/update'
        return self.http_api.send_post_request(path, headers=JSON_HEADERS, data=data)


    #######################################
    #
    # service api
    #
    #######################################
    @staticmethod
    def build_service_id(project_name, service_name):
        return project_name + '_' + service_name


    @auto_handle_http_response
    def query_services(self, service_name, containers=True):
        params = {
            'q': service_name,
            'containers': containers,
        }
        path = SERVICES_API_PATH
        return self.http_api.send_get_request(path, params)


    @auto_handle_http_response
    def query_service(self, project_name, service_name):
        service_id = self.build_service_id(project_name, service_name)
        path = SERVICES_API_PATH + service_id
        return self.http_api.send_get_request(path)


    @auto_handle_http_response
    def start_service(self, project_name, service_name):
        service_id = self.build_service_id(project_name, service_name)
        path = SERVICES_API_PATH + service_id + '/start'
        return self.http_api.send_post_request(path)


    @auto_handle_http_response
    def stop_service(self, project_name, service_name, timeout=10):
        service_id = self.build_service_id(project_name, service_name)
        path = SERVICES_API_PATH + service_id + '/stop'
        params = {
            'timeout': timeout
        }
        return self.http_api.send_post_request(path, params=params)


    @auto_handle_http_response
    def kill_service(self, project_name, service_name, signal=2):
        service_id = self.build_service_id(project_name, service_name)
        path = SERVICES_API_PATH + service_id + '/'
        params = {
            'signal': signal
        }
        return self.http_api.send_post_request(path, params=params)
