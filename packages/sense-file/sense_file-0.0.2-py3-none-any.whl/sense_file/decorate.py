import datetime
from sense_core import get_db_factory, DBACTION


def upload_db_logs(function):
    def inner(self, file_name, origin_path, bucket_name):
        _success, key = function(self, file_name, origin_path, bucket_name)
        if _success:
            db_factory = get_db_factory('mysql_file')
            _now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db_factory.findKeySql(DBACTION.REPLACE, table='file_sheet', data={'key': key, 'bucket_name': bucket_name,
                                                                              'create_time': _now, 'modify_time': _now,
                                                                              'status': 1})
        return _success
    return inner


def delete_db_logs(function):
    def inner(self, file_name, bucket_name):
        _success, key = function(self, file_name, bucket_name)
        if _success:
            db_factory = get_db_factory('mysql_file')
            _now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db_factory.findKeySql(DBACTION.DELETE_BY_ATTR, table='file_sheet', params={'key': key})
        return _success, key
    return inner