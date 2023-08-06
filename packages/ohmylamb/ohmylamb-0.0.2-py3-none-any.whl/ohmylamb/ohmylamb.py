#!/usr/bin/env python
import sys
import boto3
import base64
import configparser
import json
import snowflake.connector as sf
import pandas as pd
from botocore.exceptions import ClientError

#####################################################################
# AWS
#####################################################################


#####################################################################
# Secret Manager
#####################################################################
session = boto3.session.Session()

def aws_secret_manager_get_client(region_name):
    if len(region_name) == 0:
        region_name = "us-east-1"
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    return client


def aws_secret_manager_get_secret(secret_name, region_name):
    client = aws_secret_manager_get_client(region_name)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(
            f"Error while fetching secret: {secret_name} from AWS secret manager. Error: {e.response['Error']['Code']}")
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])

#####################################################################
# S3
#####################################################################

# Get file from aws s3
def download_file_from_s3(bucket, key, local_file_path):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).download_file(key, local_file_path)


# Put file to aws s3
def upload_file_to_s3(bucket, key, local_file_path):
    s3 = boto3.client('s3')
    s3.upload_file(local_file_path, bucket, key)


#####################################################################
# Configration
#####################################################################

config = configparser.ConfigParser()

try:
    config.read('app.ini')
except Exception as e:
    print(f"Error while reading app.ini file. Error: {e.response['Error']['Code']}")

appTeam = config['app']['team']
appName = config['app']['name']
appEnv = config['app']['env']
try:
    appConfigRegion = config['app']['configRegion']
except:
    print("No region defined. Will use default")
    appConfigRegion = ""
appConfigRegion = appConfigRegion if len(appConfigRegion) == 0 else ""
appConfAWSSecretName = f"{appTeam}/{appEnv}/{appName}"


def get_app_configuration():
    return get_secret_map(appConfAWSSecretName)


def get_resource_conf(resource_name):
    key = f"{appTeam}/{appEnv}/{resource_name}"
    return get_secret_map(key)


def get_secret_map(key):
    try:
        j = aws_secret_manager_get_secret(key, appConfigRegion)
        k = json.loads(j)
        return None, k
    except Exception as e:
        print(f"Error while getting config for secretName: {key}. Error: {e}")
        return e, {}


class AppConfValue(object):
    def __init__(self, resource_name):
        self.resource = get_secret_map(resource_name)

    def __call__(self, *args, **kwargs):
        return self.resource


class CofigFromFile(object):

    def __init__(self, file_name):
        print(file_name)
        self.conf = configparser.ConfigParser()
        self.conf.read(file_name)

    def __call__(self, f,*args, **kwargs):
        def wrapper(*args, **kwargs):
            argL = list(args)
            segment = argL[0]
            keyword = argL[1]
            return self.conf[segment][keyword]
        return wrapper

#####################################################################
# SnowFlake
#####################################################################


class SnowFlakeCredential:
    def __init__(self, props, dbName):
        self.url = props["url"]
        self.username = props["username"]
        self.password = props["password"]
        self.account = props["account"]
        self.account_region = props["account_region"]
        d = props[f"{dbName.lower()}_warehouse_db_schema"].split(":::")
        self.warehouse, self.db, self.schema = d[0], d[1], d[2]


# Create snowflake currsor
cursors = {}


def get_cursor(snowFlakeCredential):
    print(f"{snowFlakeCredential.username} {snowFlakeCredential.password}  {snowFlakeCredential.account}")
    ctx = sf.connect(
        user=snowFlakeCredential.username,
        password=snowFlakeCredential.password,
        account=f"{snowFlakeCredential.account}.{snowFlakeCredential.account_region}"
    )
    cs = ctx.cursor()
    w = f"USE warehouse {snowFlakeCredential.warehouse}"
    d = f"USE {snowFlakeCredential.db}.{snowFlakeCredential.schema}"
    cs.execute(w)
    cs.execute(d)
    return cs


def create_cursor(dbName):
    error, snowflakeProps = get_resource_conf("snowflake")
    if error is not None:
        print(f"Error while getting Snowflake props. Error {error}")
        exit(1)
    snowFlakeCredential = SnowFlakeCredential(snowflakeProps, dbName)
    cs = get_cursor(snowFlakeCredential)
    cursors[dbName] = cs
    return cs


def get_cursor_for_db(dbName):
    return cursors[dbName] if dbName in cursors else create_cursor(dbName)


def query_to_df(dbName, query):
    cs = get_cursor_for_db(dbName)
    cur = cs.execute(query)
    return pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])


#####################################################################
# SNS Services
#####################################################################
class SMSNotifier(object):
    def __init__(self, l):
        self.l = l
        self.client = boto3.client("sns")

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            msg = f(*args, **kwargs)
            for x in self.l: self.client.publish(PhoneNumber=x, Message=msg)

        return wrapper


class GroupSMSNotifier(object):
    def __init__(self, groupName):
        self.groupName = groupName
        self.client = boto3.client("sns")

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            msg = f(*args, **kwargs)
            for x in self.l: self.client.publish(PhoneNumber=x, Message=msg)

        return wrapper


#####################################################################
# Lambda Entry Wrappers
#####################################################################


class s3EventHandler(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, event, context):
        for record in event['Records']:
            bucketName = record['s3']['bucket']['name']
            keyName = record['s3']['object']['key']
            k = keyName.replace("/", "-")
            f = f"/tmp/{bucketName}-{k}"
            download_file_from_s3(bucketName, keyName, f)
            self.f(bucketName, keyName)


class cronJob(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, event, context):
        self.f()
