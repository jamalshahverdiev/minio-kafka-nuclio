import ssl
from minio import Minio
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
# Create client with access key and secret key with specific region.
client = Minio(
    "192.168.184.41:9001",
    access_key="nuclio_user",
    secret_key="nucl10p244w0rd",
    secure=False,
    region="us-west-1",
)
def get_minio_obj(filename):
    result = client.fget_object("nuclioevents", filename, filename)

