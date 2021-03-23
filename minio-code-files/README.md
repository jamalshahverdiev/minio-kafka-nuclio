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
