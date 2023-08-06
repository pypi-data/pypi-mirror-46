# -*- coding: utf-8 -*-

"""
azkaban_cli.api

This module provides a set of requests for the Azkaban API
"""

import logging
import os

def upload_request(session, host, session_id, project, zip_path):
    """Upload request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param str project: Project name on Azkaban
    :param str zip_path: Local path from zip that will be uploaded
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    zip_file = open(zip_path, 'rb')
    zip_name = os.path.basename(zip_path)

    response = session.post(
        host + '/manager',
        data={
            u'session.id': session_id,
            u'ajax': u'upload',
            u'project': project
        },
        files={
            u'file': (zip_name, zip_file, 'application/zip'),
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response

def login_request(session, host, user, password):
    """Login request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str user: The user name
    :param str password: The user password
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.post(
        host,
        data={
            u'action': u'login',
            u'username': user,
            u'password': password
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response

def schedule_request(session, host, session_id, project, flow, cron, **execution_options):
    r"""Schedule request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param str project: Project name that contains the flow that will be scheduled on Azkaban
    :param str flow: Flow name to be scheduled on Azkaban
    :param str cron: Cron expression in quartz format used to schedule
    :param \*\*execution_options: Optional parameters to execution
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    data = {
        u'session.id': session_id,
        u'ajax': u'scheduleCronFlow',
        u'projectName': project,
        u'flow': flow,
        u'cronExpression': cron
    }
    data.update(execution_options)

    logging.debug("Request data: \n%s", data)

    response = session.post(
        host + '/schedule',
        data=data
    )

    logging.debug("Response: \n%s", response.text)

    return response

def fetch_flows_request(session, host, session_id, project):
    """Fetch flows of a project request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param str project: Project name whose flows will be fetched on Azkaban
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.get(
        host + '/manager',
        params={
            u'session.id': session_id,
            u'ajax': 'fetchprojectflows',
            u'project': project
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response

def fetch_schedule_request(session, host, session_id, project_id, flow):
    """Fetch flow of a project request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param str project_id: Project ID whose flow schedule will be fetched on Azkaban
    :param str flow: Flow name whose schedule will be fetched on Azkaban
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.get(
        host + '/schedule',
        params={
            u'session.id': session_id,
            u'ajax': 'fetchSchedule',
            u'projectId': project_id,
            u'flowId': flow
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response

def unschedule_request(session, host, session_id, schedule_id):
    r"""Unschedule request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param str schedule_id: Schedule id of the flow that will be unscheduled on Azkaban
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    data = {
        u'session.id': session_id,
        u'action': u'removeSched',
        u'scheduleId': schedule_id
    }

    logging.debug("Request data: \n%s", data)

    response = session.post(
        host + '/schedule',
        data=data
    )

    logging.debug("Response: \n%s", response.text)

    return response

#TODO: Add optional parameters
def execute_request(session, host, session_id, project, flow):
    """Execute request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :param str project: Project name that contains the flow that will be executed on Azkaban
    :param str flow: Flow name to be executed on Azkaban
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.get(
        host + '/executor',
        params={
            u'session.id': session_id,
            u'ajax': 'executeFlow',
            u'project': project,
            u'flow': flow
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response

def create_request(session, host, session_id, project, description):
    """Create a Project request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str session_id: An id that the user should have when is logged in
    :param str project: Project name to be created on Azkaban
    :param str description: The description for the project
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.post(
        host + '/manager',
        data={
            u'session.id': session_id,
            u'action': u'create',
            u'name': project,
            u'description': description
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response

def delete_request(session, host, session_id, project):
    """Delete a Project request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str session_id: An id that the user should have when is logged in
    :param str project: Project name to be deleted on Azkaban:return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.get(
        host + '/manager',
        params={
            u'session.id': session_id,
            u'delete': 'true',
            u'project': project
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response

def fetch_projects_request(session, host, session_id):
    """Fetch all projects request for the Azkaban API

    :param session: A session for creating the request
    :type session: requests.Session
    :param str host: Hostname where the request should go
    :param str session_id: An id that the user should have when is logged in
    :return: The response from the request made
    :rtype: requests.Response
    :raises requests.exceptions.ConnectionError: if cannot connect to host
    """

    response = session.get(
        host + '/index?all',
        params={
            u'session.id': session_id
        }
    )

    logging.debug("Response: \n%s", response.text)

    return response
