import os
from boto3.session import Session
from sense_core import config, log_error
from sense_file.decorate import delete_db_logs, upload_db_logs


class S3File(object):

    def __init__(self, label, region_name='cn-north-1', log_write=False):
        session = Session(aws_access_key_id=config(label, 'key'), aws_secret_access_key=config(label, 'secret'),
                          region_name=region_name)
        self.server = session.resource('s3')
        self.bucket_map = {}
        self.log_write = log_write

    def __file_key_format(self, file_name):
        file_list = file_name.split('.')
        file_type = file_list[-1]
        file_list[-1] = file_type.lower()
        return '.'.join(file_list)

    def __get_bucket(self, bucket_name):
        if bucket_name not in self.bucket_map:
            self.bucket_map[bucket_name] = self.server.Bucket(bucket_name)
        return self.bucket_map[bucket_name]

    def file_exists(self, file_name, bucket_name):
        bucket = self.__get_bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=file_name):
            if obj.key == file_name:
                return True
        return False

    def download(self, file_name, aim_path, bucket_name):
        file_name = self.__file_key_format(file_name)
        if not self.file_exists(file_name, bucket_name):
            return False
        try:
            self.server.Object(bucket_name, file_name).download_file(aim_path)
        except Exception as e:
            log_error('file {} down from s3 {} error,msg: {}'.format(file_name, bucket_name, e.__str__()))
            return False
        return os.path.exists(aim_path), file_name

    @upload_db_logs
    def upload(self, file_name, origin_path, bucket_name):
        file_name = self.__file_key_format(file_name)
        try:
            obj = self.server.Object(bucket_name, file_name)
            obj.upload_file(origin_path)
        except Exception as e:
            print(e)
            log_error('file {} upload from s3 {} error,msg: {}'.format(file_name, bucket_name, e.__str__()))
            return False
        return self.file_exists(file_name, bucket_name), file_name

    @delete_db_logs
    def delete_file(self, file_name, bucket_name):
        file_name = self.__file_key_format(file_name)
        try:
            file_obj = self.server.Object(bucket_name, file_name)
            res = file_obj.delete()
        except Exception as e:
            print(e)
            log_error('file {} delete from s3 {} error,msg: {}'.format(file_name, bucket_name, e.__str__()))
            return False
        return res['DeleteMarker'], file_name


if __name__ == '__main__':
    file_path = '/Users/liuguangbin/Documents/test.PDF'
    s3_file = S3File('aws')
    # x = s3_file.file_exists('000b9ccb-76d7-5421-997d-e3b8413479a2', 'sdai-pdfs')
    # print(x)
    print(s3_file.download('000b9ccb-76d7-5421-997d-e3b8413479a2.PDF', '/Users/liuguangbin/Documents/ex.pdf', 'sdai-pdfs'))
    # print(s3_file.upload('000b9ccb-76d7-5421-997d-e3b8413479a2.PDF', file_path, 'sdai-pdfs'))
    # print(s3_file.delete_file('000b9ccb-76d7-5421-997d-e3b8413479a2.PDF', 'sdai-pdfs'))
    # s3_file.delete_file('2016/2016-12/2016-12-31/test.pdf', 'sdai-pdfs')