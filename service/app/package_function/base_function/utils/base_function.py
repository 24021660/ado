from app.package_function import mydb,redis_client
from bson.json_util import dumps
from bson import ObjectId
import json,os


def data_query(table_name,query):
    chart_config_table = mydb[table_name]
    res = json.loads(dumps(chart_config_table.find(query)))
    return res


def data_del(table_name,query):
    chart_config_table = mydb[table_name]
    chart_config_table.delete_one(query)

def data_update(table_name,query,commit_data):
    chart_config_table = mydb[table_name]
    chart_config_table.update_one(query, {'$set': commit_data})

def data_commit(table_name,commit_data):
    chart_config_table = mydb[table_name]
    if commit_data['edit_class'] == 'add':
        chart_config_table.insert_one(commit_data)
    elif commit_data['edit_class'] == 'edit':
        query = {'_id': ObjectId(commit_data['_id']['$oid'])}
        del commit_data['_id']
        chart_config_table.update_one(query, {'$set': commit_data})

def redis_commit_hash(redis_key,hash_key,hash_value):
    redis_client.hset(redis_key,hash_key,hash_value)

def redis_commit_list(redis_key,redis_value):
    redis_client.rpush(redis_key, redis_value)

def file_folder_exist(path):
    return os.path.exists(path)