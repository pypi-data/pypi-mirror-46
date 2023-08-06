import datetime
import logging
import os
import time
import uuid
import json
import boto3
from io import StringIO


class CloudLoggerObject:
    def __init__(self, format, logger_obj, name, **kwargs):
        self.name = name
        self.format = format
        self.logger_obj = logger_obj
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
        formatter = logging.Formatter(logger_obj.format)
        self.setFormatter(formatter)
        self.create_log_group_and_streams()

    def create_log_group_and_streams(self):
        try:
            self.logger_obj.create_log_stream(
                logGroupName=self.logger_obj.name, logStreamName='DEBUG')
            self.logger_obj.create_log_stream(
                logGroupName=self.logger_obj.name, logStreamName='ERROR')
            self.logger_obj.create_log_stream(
                logGroupName=self.logger_obj.name, logStreamName='WARN')
            self.logger_obj.create_log_stream(
                logGroupName=self.logger_obj.name, logStreamName='CRITICAL')

            self.logger_obj.create_log_stream(
                logGroupName=self.logger_obj.name, logStreamName='FATAL')
            self.logger_obj.create_log_group(
                logGroupName=name, tags={'app': self.logger_obj.name})
        except Exception as e:
            pass

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

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            log_stream_name = record.levelname
            self.logger_obj.client.put_log_events(**self.build_put_params(
                self.get_log_streams(log_stream_name), log_stream_name, msg))
            self.flush()
        except Exception:
            self.handleError(record)