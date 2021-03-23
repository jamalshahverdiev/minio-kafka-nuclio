import ssl
from urllib.request import urlopen
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
#events = client.listen_bucket_notification(
# "nuclioevents",
# prefix="event-catch/",
# events=["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
#)
#for event in events:
# print(event)
#buckets = client.list_buckets()
#for bucket in buckets:
# print(bucket.name, bucket.creation_date)
## Upload data.
result = client.fput_object("nuclioevents", "remote_name.pdf", "./local_example.pdf",)
print(result)
# Download data of an object.
#result = client.fget_object("nuclioevents", "remote_name.pdf", "./local_example.pdf")
#print(result)

