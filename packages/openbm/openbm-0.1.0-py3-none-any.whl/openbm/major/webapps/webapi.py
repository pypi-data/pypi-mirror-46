from pyramid.view import view_config
from pyramid.events import ContextFound
# ApplicationCreated
from pyramid.events import subscriber
# from webapps.exceptions import RequestError
# from datetime import datetime
# from openbm.plugins import dataset_auth
from pyramid.httpexceptions import (HTTPException,
                                    HTTPCreated,
                                    HTTPMovedPermanently,
                                    HTTPUnauthorized,
                                    # HTTPNotFound,
                                    HTTPInternalServerError,
                                    exception_response
                                    )
# from pyramid.view import forbidden_view_config
# from pyramid.security import forget
# import faulthandler
from .resources import (UserList,
                        User,
                        Group,
                        Node,
                        NodeList,
                        ScheduleList,
                        Schedule,
                        JobList,
                        Job,
                        JobSetList,
                        JobSet,
                        # Groups,
                        # Calendars,
                        Cluster
                        )


@subscriber(ContextFound)
def mysubscriber(event):
    if event.request.path_info == '/cluster':
        return True
    follower = event.request.scheduler('find_leader')
    if follower:
        raise HTTPMovedPermanently(location='http://' +
                                            ':'.join(map(str, follower)) +
                                            event.request.path_info)


# @view_config(name='auth', request_method='POST',
#             request_param=('userid', 'passwd'))
# def login(request):
#    """Returns Hello in JSON."""
#    userid = request.POST['userid']
#    passwd = request.POST['passwd']
#    if request.registry.auth.check_credentials(userid, passwd):
#        groups = request.registry.auth.user_groups(userid)
#        return request.create_jwt_token(userid, groups=groups)
#    else:
#        raise HTTPUnauthorized()


# Context UserList


@view_config(context=UserList, request_method='GET',
             permission='admin_user')
def view_userlist(request):
    return {'status': 'success',
            'data': request.context.get_list()}


# Context User


@view_config(context=User, request_method='GET', permission='view_user')
def view_user(request):
    return {'status': 'success',
            'data': request.context.get_user()}


@view_config(context=User, request_method='PUT', request_param=('password',),
             permission='admin_user')
def create_user(request):
    request.context.add_user(**request.POST)
    raise HTTPCreated('user created')


@view_config(context=User, request_method='DELETE', permission='admin_user')
def delete_user(request):
    request.context.delete_user()
    return {'status': 'success', 'data': request.context.delete_user()}


# Context Group


@view_config(context=Group, request_method='GET',
             permission='view_group')
def view_group(request):
    return {'status': 'success',
            'data': request.context.get_group()}


@view_config(context=Group, request_param=('description',),
             request_method='PUT', permission='create_group')
def create_group(request):
    request.context.create_group(request.POST['description'])
    raise HTTPCreated('group created')


@view_config(context=Group, request_method='DELETE', permission='create_group')
def delete_group(request):
    request.context.delete_group()


# Context NodeList


@view_config(context=NodeList, request_method='GET',
             permission='view_node')
def view_nodelist(request):
    return {'status': 'success',
            'data': [dict(node) for node in request.context.get_list()]}


# Context Node


@view_config(context=Node, request_method='PATCH',
             request_param=('inits',), permission='config_node')
def modify_node(request):
    return {'status': 'success',
            'data': request.context.modify_node(int(request.POST['inits']))}


# Context JobSetList


@view_config(context=JobSetList, request_method='GET',
             permission='view_jobset')
def view_jobsetlist(request):
    request.context.get_list()


# Context JobSet


@view_config(context=JobSet, request_method='GET',
             permission='view_jobset')
def view_jobset(request):
    request.context.get_jobset()


@view_config(context=JobSet, request_method='PUT',
             request_param=('starttime', 'endtime', 'totalslots'),
             permission='config_jobset')
def add_jobset(request):
    request.context.add_jobset(request.POST['starttime'],
                               request.POST['endtime'],
                               request.POST['totalslots'],
                               request.POST['timezone'])
    return HTTPCreated(json_body={'status': 'success', 'data': 'jobset added'})


@view_config(context=JobSet, request_method='PATCH',
             permission='config_jobset')
def modify_jobset(request):
    return {'status': 'success',
            'data': request.context.modify_jobset(request.POST)}


@view_config(context=JobSet, request_method='DELETE',
             permission='config_jobset')
def delete_jobset(request):
    return {'status': 'success',
            'data': request.context.delete_jobset()}


# Context ScheduleList


@view_config(context=ScheduleList, request_method='GET',
             request_param=('query',), permission='view_schedule')
def view_schedulelist(request):
    return {'status': 'success',
            'data': (request.registry.settings['timezone'],
                     request.context.get_list(request.GET['query']))}


# Context Schedule

@view_config(context=Schedule, name='details', request_method='GET',
             permission='view_schedule')
def view_details(request):
    return request.context.details()


@view_config(context=Schedule, name='abort', request_method='PUT',
             permission='view_schedule')
def view_abort(request):
    return request.context.abort()


@view_config(context=Schedule, name='source', request_method='GET',
             permission='view_schedule')
def view_source(request):
    return {'status': 'success', 'data': request.context.source()}


# Context JobList


@view_config(context=JobList, request_method='GET', permission='view_job')
def view_jobs(request):
    return {'status': 'success',
            'data': request.context.get_jobs()}


@view_config(context=JobList, request_method='POST',
             permission='config_job')
def add_job(request):
    jobspec = request.POST['jobspec']
    request.context.add_job(jobspec)
    return HTTPCreated(json_body={'status': 'success', 'data': 'job added'})


@view_config(context=JobList, request_method='POST',
             request_param=('validate'), permission='config_job')
def validate_job(request):
    jobspec = request.POST['jobspec']
    request.context.validate_job(jobspec)


@view_config(context=JobList, request_method='PUT', permission='config_job')
def modify_job(request):
    jobspec = request.POST['jobspec']
    request.context.add_job(jobspec, replace=True)
    return {'status': 'success', 'data': 'job modified'}

# Context Job


@view_config(context=Job, request_method='GET', permission='view_job')
def view_job(request):
    return {'status': 'success', 'data': request.context.get_job()['spec']}


@view_config(context=Job, request_method='DELETE', permission='config_job')
def delete_job(request):
    return {'status': 'success', 'data': request.context.delete_job()}


@view_config(context=Job, name='schedule', request_method='POST',
             permission='config_job')
def add_schedule(request):
    jobid = request.context.add_schedule(request.POST.get('schedule'))
    return HTTPCreated(json_body={'status': 'success', 'data': jobid})


@view_config(context=Job, name='refresh_schedule', request_method='PUT',
             permission='config_job')
def refresh_schedule(request):
    return {'status': 'success', 'data': request.context.refresh_schedule()}

# Context Cluster


@view_config(context=Cluster, request_method='GET',
             permission='view_cluster')
def cluster_info(request):
    # get_leader()
    return request.scheduler('cluster_status')


@view_config(context=HTTPException)
def error_view(exc, request):
    """Map any RequestError as the correct HTTPError exception"""
    if exc.code == 403 and request.authenticated_userid is None:
        exc = HTTPUnauthorized()
    if type(exc.detail) is list or type(exc.detail) is dict:
        message = exc.detail
    elif exc.detail:
        message = exc.detail.__str__()
    else:
        message = exc.explanation
    if exc.code <= 399:
        json_body = {'status': 'success', 'code': exc.code,
                     'data': message}
    else:
        json_body = {'status': 'error', 'code': exc.code,
                     'message': message}
    return exception_response(exc.code, json_body=json_body)


@view_config(context=Exception)
def exception_view(exc, request):
    raise HTTPInternalServerError()
