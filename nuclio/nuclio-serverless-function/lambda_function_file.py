import os
import json
import rand_string.rand_string as rand
from testlib import debug_log
from get_minio import get_minio_obj
def handler_function_name(context, event):
    context.logger.info(debug_log(str(event.body)))
    data = json.loads(event.body)
    if data["EventName"]  == "s3:ObjectCreated:Put":
        filename = data["Key"].split("/")[1]
        get_minio_obj(filename)
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            context.logger.info(debug_log(f))
    return context.Response(body='Test, from nuclio 2 :] ' + rand.RandString("alphanumerical", 15),
                            headers={},
                            content_type='text/plain',
                            status_code=200)



