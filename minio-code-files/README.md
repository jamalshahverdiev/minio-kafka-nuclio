#### Download Minio binary files to the all servers:
```bash
$ wget https://dl.min.io/server/minio/release/linux-amd64/minio && chmod +x minio && mv minio /usr/sbin/
$ wget https://dl.min.io/client/mc/release/linux-amd64/mc && chmod +x mc && mv mc /usr/sbin/
```

#### To install 4 linux servers and copy rightly named service files to the `/etc/systemd/system/minio.service` file then execute the following command.
```bash
$ systemctl enable minio --now
```

##### Add minio host on the server to use mc command:
```bash
$ mc config host add minio http://192.168.184.41:9001 superadmin M1n10Suer2dm1np244 --api s3v4
mc: Configuration written to `/root/.mc/config.json`. Please update your access credentials.
mc: Successfully created `/root/.mc/share`.
mc: Initialized share uploads `/root/.mc/share/uploads.json` file.
mc: Initialized share downloads `/root/.mc/share/downloads.json` file.
Added `minio` successfully.
```

#### `nuclio.policy` is policy file and will be used to apply to the user to restrict access only of the `niclioevents` bucket.

- [MinIO bucket notification guide](https://docs.min.io/docs/minio-bucket-notification-guide.html)
- [MinIO Python client API reference](https://docs.min.io/docs/python-client-api-reference.html)

#### Check minio notification supported endpoints list (We will configure kafka):
```bash
$ mc admin config get minio | grep notify
notify_webhook        publish bucket notifications to webhook endpoints
notify_amqp           publish bucket notifications to AMQP endpoints
notify_kafka          publish bucket notifications to Kafka endpoints
notify_mqtt           publish bucket notifications to MQTT endpoints
notify_nats           publish bucket notifications to NATS endpoints
notify_nsq            publish bucket notifications to NSQ endpoints
notify_mysql          publish bucket notifications to MySQL databases
notify_postgres       publish bucket notifications to Postgres databases
notify_elasticsearch  publish bucket notifications to Elasticsearch endpoints
notify_redis          publish bucket notifications to Redis datastores
```

#### Execute the following command in all minio nodes to activate kafka notification and restart minio service:
```bash
$ mc admin config set minio notify_kafka:1 tls_skip_verify="off"  queue_dir="" queue_limit="0" sasl="off" sasl_password="" sasl_username="" tls_client_auth="0" tls="off" client_tls_cert="" client_tls_key="" brokers="192.168.184.71:9092,192.168.184.72:9092,192.168.184.73:9092" topic="nuclioevents" version=""
Successfully applied new settings.
Please restart your server 'mc admin service restart minio'.
$ mc admin service restart minio
```

#### Create new bucket with name `nuclioevents`:
```bash
$ mc mb minio/nuclioevents
Bucket created successfully `minio/nuclioevents`.
```

#### Activate event sending to the kafka nodes for `nuclioevents` bucket if somebody upload any file with `.pdf` extension:
```bash
$ mc event add minio/nuclioevents arn:minio:sqs::1:kafka --suffix .pdf
Successfully added arn:minio:sqs::1:kafka
```

#### Look at the configured event list for `nuclioevents` bucket which will send to the kafka nodes:
```bash
$ mc event list minio/nuclioevents
arn:minio:sqs::1:kafka   s3:ObjectCreated:*,s3:ObjectRemoved:*,s3:ObjectAccessed:*   Filter: suffix=".pdf"
```

**Note:** Delete all events in the `nucliolambdas` bucket. Activate only `put` based events for the `pdf` type documents on the `nucliolambdas` bucket:
```bash
$ mc event remove minio/nucliolambdas --force
$ mc event add nucliostore/nucliolambdas/ arn:minio:sqs::1:kafka -p --event put --suffix .pdf
```

#### Apply `nuclio.policy` file to create new policy with name `nuclio_policy` which will be applied to the `nuclioevents` bucket:
```bash
$ mc admin policy add minio nuclio_policy nuclio.policy --debug
Added policy `nuclio_policy` successfully.
```

#### Create user with name `nuclio_user` and password `nucl1op244w0rd`:
```bash
$ mc admin user add minio nuclio_user nucl10p244w0rd
Added user `nuclio_user` successfully.
```

#### Apply `nuclio.policy` to the user `nuclio_user`:
```bash
$ mc admin policy set minio nuclio_policy user=nuclio_user
Policy `nuclio_policy` is set on user `nuclio_user`
```

#### Look at the users list:
```bash
$ mc admin user list minio
enabled    nuclio_user           nuclio_policy
```

#### Add nuclio credentials like as the `nucliostore` to the `mc` configuration:
```bash
$ mc config host add nucliostore http://192.168.184.41:9001 nuclio_user nucl10p244w0rd --api s3v4
Added `nucliostore` successfully.
```

#### List all buckets in the `nucliostore`:
```bash
$ mc ls nucliostore
[2021-03-23 05:18:01 CDT]     0B nuclioevents/
```

#### Copy content of the current folder content recursively to the bucket with name `nuclioevents`:
```bash
$ mc cp --recursive . nucliostore/nuclioevents
```

#### Delete all files inside of the bucket `nuclioevents` recursively:
```bash
$ mc rm --recursive --force nucliostore/nuclioevents
```

#### List content of the bucket `nuclioevents`:
```bash
$ mc ls nucliostore/nuclioevents/
```

