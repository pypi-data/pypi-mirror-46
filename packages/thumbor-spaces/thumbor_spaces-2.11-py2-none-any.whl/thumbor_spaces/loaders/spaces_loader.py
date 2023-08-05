from os import fstat
from datetime import datetime
from os.path import join, exists, abspath

from six.moves.urllib.parse import unquote
from tornado.concurrent import return_future

from . import http_loader

from thumbor.loaders import LoaderResult


@return_future
def load(context, path, callback):
    logger.debug("INSIDE SPACES LOADER")
    logger.debug(path)
    logger.debug(context.request.url)
    if 'https://'+context.config.SPACES_ENDPOINT+'.digitaloceanspaces.com/storage/' not in context.request.url: 
        http_loader.load(context, path, callback)
    else
        key = get_key_name(context, context.request.url)
        buff = BytesIO()
        session = boto3.session.Session()
        client = session.resource('s3',
                                    region_name=context.config.SPACES_REGION,
                                    endpoint_url='https://'+context.config.SPACES_ENDPOINT+'.digitaloceanspaces.com',
                                    aws_access_key_id=context.config.SPACES_KEY,
                                    aws_secret_access_key=context.config.SPACES_SECRET)
        try:
            objkey = client.Bucket(context.config.SPACES_BUCKET).Object(key)
            objkey.download_fileobj(buff)
            result = LoaderResult()
            result.successful = True
            result.buffer = buff
            result.metadata = objkey.get_metadata("Metadata")
            result.metadata.pop('Body')
            logger.debug(result.metadata)
            callback(result)
        except:
            callback(None)
        callback(None)

def get_key_name(context, path):
    path_segments = path.lstrip('/').split("/")
    key = re.sub('[^0-9a-zA-Z]+', '_', path_segments[0])
    key = '/'.join([context.config.SPACES_LOADER_FOLDER, key, path_segments[-1:][0]])
    return key