import datetime
import logging
import os
import time
import uuid
import json
import boto3
from io import StringIO


class SequenceTokenDoesNotExist(Exception): pass
class PutLogEventError(Exception): pass


class CloudLoggerObject:
    def __init__(self, format, name, **kwargs):
        self.name = name
        self.format = format
        self.kwargs = kwargs
        aws_access_key_id = os.environ.get(
            'CLOUD_LOGGER_ACCESS_KEY_ID').strip()
        aws_secret_access_key = os.environ.get(
            'CLOUD_LOGGER_SECRET_ACCESS_KEY').strip()
        self.client = boto3.client('logs',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)


class CloudLogger:
    def __init__(self, logger_obj):
        self.logger_obj = logger_obj

    def build_put_params(self, log_streams, log_stream_name, message):
        params = dict(
            logGroupName=self.logger_obj.name,
            logStreamName=log_stream_name,
            logEvents=[{
                'timestamp': int(time.time()) * 1000,
                'message': message
            }],
        )
        try:
            s_token = log_streams['logStreams'][0]['uploadSequenceToken']
            params['sequenceToken'] = s_token
        except:
            raise Exception('Invalid sequenceToken')
        return params

    def get_log_streams(self, log_stream_name):
        return self.logger_obj.client.describe_log_streams(
            logGroupName=self.logger_obj.name,
            logStreamNamePrefix=log_stream_name,
            limit=1)


class CloudHandler(logging.StreamHandler):
    level = logging.DEBUG

    def __init__(self, logger_obj):
        super().__init__()
        logging.StreamHandler.__init__(self)
        self.logger_obj = logger_obj
        self.setFormatter(logging.Formatter(logger_obj.format))
        client = self.logger_obj.client
        groups = ['DEBUG','WARNING','ERROR','CRITICAL','FATAL']
        for group in groups:
            try:
                client.create_log_stream(
                    logGroupName=self.logger_obj.name, logStreamName=group)
            except Exception as e:
                continue

    def build_put_params(self, log_streams, log_stream_name, message):
        params = dict(
            logGroupName=self.logger_obj.name,
            logStreamName=log_stream_name,
            logEvents=[{
                'timestamp': int(time.time()) * 1000,
                'message': message
            }],
        )

        try:
            s_token = log_streams['logStreams'][0]['uploadSequenceToken']
            params['sequenceToken'] = s_token
            return params
        except:
            return params

    def get_log_streams(self, log_stream_name):
        return self.logger_obj.client.describe_log_streams(
            logGroupName=self.logger_obj.name,
            logStreamNamePrefix=log_stream_name,
            limit=1)

    def put_log_event(self,log_stream_name,msg):
        self.logger_obj.client.put_log_events(**self.build_put_params(
        self.get_log_streams(log_stream_name), log_stream_name, msg))

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            log_stream_name = record.levelname
            log_streams = self.get_log_streams(log_stream_name)
            self.flush()
            try:
                self.put_log_event(log_stream_name,msg)
            except Exception as e2:
                print(f'PutLogEventError: {e2}')
        except Exception as e:
            self.handleError(record)
        




