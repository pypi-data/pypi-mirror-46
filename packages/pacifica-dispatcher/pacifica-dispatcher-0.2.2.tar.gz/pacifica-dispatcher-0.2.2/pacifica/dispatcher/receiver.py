#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/receiver.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Receiver module.

Contains a factory returning a receiver class that can create
PeeWee models and CherryPy endpoints.
"""
import datetime
import json
import sys
import traceback
import typing
import uuid
import functools
from contextlib import contextmanager

import celery
import cherrypy
import peewee

from .router import RouteNotFoundRouterError, Router

# pylint: disable=too-many-statements
# this is not too many statements it's all wrapped up in the class.


def create_peewee_model(passed_db: peewee.Database) -> object:
    """Factory creating a receiver class."""
    @contextmanager
    def closed_db_context(ctxt_db=passed_db):
        """Context to refresh db connection."""
        try:
            if not ctxt_db.is_closed():
                ctxt_db.close()
            ctxt_db.connect()
            yield ctxt_db
        finally:
            ctxt_db.close()

    def refresh_database(func):
        """Decorator to bind and wrap models to databases."""
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with closed_db_context():
                return func(*args, **kwargs)
        return inner

    class ReceiveTaskModel(peewee.Model):
        """
        Receiver task model class.

        This class is the primary interface class wrapping up
        creating PeeWee models, handling CherryPy rest
        interfaces and Celery backend workers.
        """

        uuid = peewee.UUIDField(default=uuid.uuid4, index=True, primary_key=True)

        event_type = peewee.CharField(index=True, null=True)
        event_type_version = peewee.CharField(index=True, null=True)
        cloud_events_version = peewee.CharField(index=True, null=True)
        source = peewee.CharField(index=True, null=True)
        event_id = peewee.CharField(index=True, null=True)
        event_time = peewee.CharField(index=True, null=True)
        schema_url = peewee.CharField(index=True, null=True)
        content_type = peewee.CharField(index=True, null=True)

        event_data = peewee.TextField()
        data = peewee.TextField()

        task_id = peewee.UUIDField(index=True, unique=True)
        task_application_name = peewee.CharField(index=True)
        task_name = peewee.CharField(index=True)
        task_status = peewee.CharField(index=True)

        exc_type = peewee.CharField(null=True)
        exc_value = peewee.CharField(null=True)
        exc_traceback = peewee.TextField()

        created = peewee.DateTimeField(default=datetime.datetime.now, index=True)
        updated = peewee.DateTimeField(default=datetime.datetime.now, index=True)
        deleted = peewee.DateTimeField(index=True, null=True)

        # pylint: disable=too-few-public-methods
        class Meta:
            """Meta class connecting the database."""

            database = passed_db
        # pylint: enable=too-few-public-methods

        @classmethod
        def create_celery_app(cls, router: Router, name: str, receive_task_name: str,
                              *args, **kwargs) -> celery.Celery:
            """
            Create the Celery app.

            Creates the Celery tasks and app to process events to
            backend workers.
            """
            celery_app = celery.Celery(name, *args, **kwargs)

            celery_app.conf.worker_redirect_stdouts = False

            # pylint: disable=unused-variable
            @celery_app.task(bind=True, ignore_result=True, name=receive_task_name)
            def receive_task(self, event_data: typing.Dict[str, typing.Any]) -> None:
                """Primary Celery task entrypoint."""
                inst = cls(**{
                    'event_type': event_data.get('eventType', None),
                    'event_type_version': event_data.get('eventTypeVersion', None),
                    'source': event_data.get('source', None),
                    'event_id': event_data.get('eventID', None),
                    'event_time': event_data.get('eventTime', None),
                    'schema_url': event_data.get('schemaURL', None),
                    'content_type': event_data.get('contentType', None),

                    'event_data': json.dumps(event_data),
                    'data': json.dumps(event_data.get('data', None)),

                    'task_id': self.request.id,
                    'task_application_name': name,
                    'task_name': receive_task_name,
                    'task_status': '202 Accepted',

                    'exc_type': None,
                    'exc_value': None,
                    'exc_traceback': '',
                })
                with closed_db_context():
                    inst.save(force_insert=True)

                try:
                    route = router.match_first_or_raise(event_data)
                except RouteNotFoundRouterError as exc:
                    inst.task_status = '422 Unprocessable Entity'
                    inst.exc_type = 'RouteNotFoundRouterError'
                    inst.exc_value = str(exc)
                    with closed_db_context():
                        inst.save()
                else:
                    inst.task_status = '102 Processing'
                    with closed_db_context():
                        inst.save()

                    try:
                        route(event_data)
                    # pylint: disable=broad-except
                    except Exception:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        inst.exc_type = exc_type.__name__
                        inst.exc_value = str(exc_value)
                        inst.exc_traceback = traceback.format_tb(exc_traceback)

                        inst.task_status = '500 Internal Server Error'
                        with closed_db_context():
                            inst.save()
                    # pylint: enable=broad-except
                    else:
                        inst.task_status = '200 OK'
                        with closed_db_context():
                            inst.save()
            return celery_app

        @classmethod
        def create_cherrypy_app(cls, receive_task: celery.Task) -> cherrypy.Application:
            """
            Create the CherryPy application root object.

            This creates a set of CherryPy objects to be mounted in a
            server.
            """
            # pylint: disable=too-few-public-methods
            class Get:
                """Get class for grabbing info about an event."""

                exposed = True

                # pylint: disable=invalid-name
                @staticmethod
                @refresh_database
                @cherrypy.tools.json_out()
                def GET(task_id: str):
                    """Get REST method entrypoint."""
                    try:
                        inst = cls.get(task_id=uuid.UUID(task_id))
                    except peewee.DoesNotExist:
                        raise cherrypy.HTTPError('404', 'Not Found')
                    except ValueError:
                        raise cherrypy.HTTPError('422', 'Unprocessable Entity')

                    return {
                        'eventType': inst.event_type,
                        'eventTypeVersion': inst.event_type_version,
                        'source': inst.source,
                        'eventID': inst.event_id,
                        'eventTime': inst.event_time,
                        'schemaURL': inst.schema_url,
                        'contentType': inst.content_type,
                        'eventData': inst.event_data,
                        'data': inst.data,
                        'taskID': str(inst.task_id),
                        'taskStatus': inst.task_status,
                        'taskApplicationName': inst.task_application_name,
                        'taskName': inst.task_name,
                        'exceptionType': inst.exc_type,
                        'exceptionValue': inst.exc_value,
                        'exceptionTraceback': inst.exc_traceback,
                        'created': str(inst.created) if inst.created is not None else None,
                        'updated': str(inst.updated) if inst.updated is not None else None,
                        'deleted': str(inst.deleted) if inst.deleted is not None else None,
                    }
                # pylint: enable=invalid-name

            class Receive:
                """Receive entrypoint for new cloud events."""

                exposed = True

                # pylint: disable=invalid-name
                @staticmethod
                @refresh_database
                @cherrypy.tools.json_in()
                @cherrypy.tools.json_out()
                def POST() -> bytes:
                    """Primary REST endpoint for receiving cloud events."""
                    return receive_task.delay(cherrypy.request.json).id
                # pylint: enable=invalid-name

            class Status:
                """Status of a specific cloud event."""

                exposed = True

                # pylint: disable=invalid-name
                @staticmethod
                @refresh_database
                @cherrypy.tools.json_out()
                def GET(task_id: str):
                    """Get REST entrypoint for specific UUID."""
                    try:
                        inst = cls.get(task_id=uuid.UUID(task_id))
                    except peewee.DoesNotExist:
                        raise cherrypy.HTTPError('404', 'Not Found')
                    except ValueError:
                        raise cherrypy.HTTPError('422', 'Unprocessable Entity')
                    return inst.task_status
                # pylint: enable=invalid-name

            class Root:
                """CherryPy root object."""

                exposed = True
                get = Get()
                receive = Receive()
                status = Status()

                # pylint: disable=invalid-name
                @staticmethod
                @refresh_database
                @cherrypy.tools.json_out()
                def GET():
                    """Main root get method for some introspection."""
                    return list(map(lambda inst: {
                        # 'eventType': inst.event_type,
                        # 'eventTypeVersion': inst.event_type_version,
                        # 'source': inst.source,
                        # 'eventID': inst.event_id,
                        # 'eventTime': inst.event_time,
                        # 'schemaURL': inst.schema_url,
                        # 'contentType': inst.content_type,
                        # 'eventData': inst.event_data,
                        # 'data': inst.data,
                        'taskID': str(inst.task_id),
                        # 'taskStatus': inst.task_status,
                        # 'taskApplicationName': inst.task_application_name,
                        # 'taskName': inst.task_name,
                        # 'exceptionType': inst.exc_type,
                        # 'exceptionValue': inst.exc_value,
                        # 'exceptionTraceback': inst.exc_traceback,
                        'created': str(inst.created) if inst.created is not None else None,
                        'updated': str(inst.updated) if inst.updated is not None else None,
                        'deleted': str(inst.deleted) if inst.deleted is not None else None,
                    }, cls.select(*[
                        # cls.event_type,
                        # cls.event_type_version,
                        # cls.source,
                        # cls.event_id,
                        # cls.event_time,
                        # cls.schema_url,
                        # cls.content_type,
                        # cls.event_data,
                        # cls.data,
                        cls.task_id,
                        # cls.task_application_name,
                        # cls.task_name,
                        # cls.task_status,
                        # cls.exc_type,
                        # cls.exc_value,
                        # cls.exc_traceback,
                        cls.created,
                        cls.updated,
                        cls.deleted,
                    ]).order_by(*[
                        cls.created.desc(),
                    ])))
                # pylint: enable=invalid-name
            # pylint: enable=too-few-public-methods

            def error_page_default(**kwargs: typing.Dict[str, typing.Any]) -> bytes:
                """Error page when something goes wrong."""
                cherrypy.response.headers['Content-Type'] = 'application/json'
                return bytes(json.dumps(kwargs), 'utf-8')

            application = cherrypy.Application(Root(), '/', config={
                '/': {
                    'error_page.default': error_page_default,
                    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                },
            })

            return application

    return ReceiveTaskModel


__all__ = ('create_peewee_model', )
