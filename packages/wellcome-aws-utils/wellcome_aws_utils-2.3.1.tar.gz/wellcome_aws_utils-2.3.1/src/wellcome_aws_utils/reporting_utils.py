#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
get records from VHS, apply the transformation to them, and shove them into
an elasticsearch index
"""
import json
import boto3
import certifi
from attr import attrs, attrib
from elasticsearch import Elasticsearch
from wellcome_aws_utils.lambda_utils import log_on_error


def get_es_credentials():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="eu-west-1"
    )
    get_secret_value_response = client.get_secret_value(
        SecretId="prod/Elasticsearch/ReportingCredentials"
    )
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)


def dict_to_location(d):
    return ObjectLocation(**d)


@attrs
class ObjectLocation(object):
    namespace = attrib()
    key = attrib()


@attrs
class HybridRecord(object):
    id = attrib()
    version = attrib()
    location = attrib(converter=dict_to_location)


@attrs
class ElasticsearchRecord(object):
    id = attrib()
    doc = attrib()


def extract_sns_messages_from_event(event):
    keys_to_keep = ['id', 'version', 'location']

    for record in event["Records"]:
        full_message = json.loads(record["Sns"]["Message"])
        stripped_message = {
            k: v for k, v in full_message.items() if k in keys_to_keep
        }
        yield stripped_message


def get_s3_objects_from_messages(s3, messages):
    for message in messages:
        hybrid_record = HybridRecord(**message)
        s3_object = s3.get_object(
            Bucket=hybrid_record.location.namespace,
            Key=hybrid_record.location.key
        )
        yield hybrid_record.id, s3_object


def unpack_json_from_s3_objects(s3_objects):
    for hybrid_record_id, s3_object in s3_objects:
        record = s3_object["Body"].read().decode("utf-8")
        yield hybrid_record_id, json.loads(record)


def transform_data_for_es(data, transform):
    for hybrid_record_id, data_dict in data:
        yield ElasticsearchRecord(
            id=hybrid_record_id,
            doc=transform(data_dict)
        )


@log_on_error
def process_messages(
    event, transform, index, s3_client=None, es_client=None, credentials=None
):
    s3_client = s3_client or boto3.client("s3")

    if es_client:
        pass

    elif credentials and not es_client:
        es_client = Elasticsearch(
            hosts=credentials["url"],
            use_ssl=True,
            ca_certs=certifi.where(),
            http_auth=(credentials['username'], credentials['password'])
        )

    else:
        raise ValueError(
            'process_messages needs an elasticsearch client or a set of '
            'credentials to create one'
        )

    _process_messages(event, transform, index, s3_client, es_client)


def _process_messages(event, transform, index, s3_client, es_client):
    messages = extract_sns_messages_from_event(event)
    s3_objects = get_s3_objects_from_messages(s3_client, messages)
    data = unpack_json_from_s3_objects(s3_objects)
    es_records_to_send = transform_data_for_es(data, transform)

    for record in es_records_to_send:
        es_client.index(
            index=index,
            doc_type="_doc",
            id=record.id,
            body=record.doc
        )
