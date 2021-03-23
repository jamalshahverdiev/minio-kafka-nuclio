# ZooKeeper and Kafka cluster with Ansible.
### Prerequisites:
You have the following tool installed on DevOps computer:
   - [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html "Ansible install page")

## In order to have a working environment please follow the sequence shown below:
  - [x] Download needed roles
  - [x] Deploy roles for ZooKeeper and Kafka cluster
### Download needed roles
```bash
$ ansible-galaxy install sleighzy.kafka
$ ansible-galaxy install sleighzy.zookeeper
```
**Note**: Bu default roles will be installed `~/.ansible/roles` path.
### Deploy roles for ZooKeeper and Kafka cluster
#### Prepare `zookeeper-deploy.yml`, `kafka-deploy.yml` and `hosts` (`hosts` inventory file will be used by `ansible.cfg` file) files,
```bash
➜ cat zookeeper-deploy.yml
---
- hosts: zookeeper-nodes
  roles:
    - sleighzy.zookeeper
...
```
```bash
➜ cat kafka-deploy.yml
---
- hosts: kafka-nodes
  roles:
    - sleighzy.kafka
...
```
```bash
➜ cat hosts
[control]
controller ansible_connection=local

[zookeeper-nodes]
kafka1 ansible_ssh_user=root ansible_ssh_pass='freebsd' ansible_ssh_port=22 zookeeper_id=1
kafka2 ansible_ssh_user=root ansible_ssh_pass='freebsd' ansible_ssh_port=22 zookeeper_id=2
kafka3 ansible_ssh_user=root ansible_ssh_pass='freebsd' ansible_ssh_port=22 zookeeper_id=3

[zookeeper-nodes:vars]
somevar=somevalue


[kafka-nodes]
kafka1 ansible_ssh_user=root ansible_ssh_pass='freebsd' ansible_ssh_port=22 kafka_broker_id=1 kafka_listener_hostname=kafka1
kafka2 ansible_ssh_user=root ansible_ssh_pass='freebsd' ansible_ssh_port=22 kafka_broker_id=2 kafka_listener_hostname=kafka2
kafka3 ansible_ssh_user=root ansible_ssh_pass='freebsd' ansible_ssh_port=22 kafka_broker_id=3 kafka_listener_hostname=kafka3

[kafka-nodes:vars]
somevar=somevalue
```

**Note:** Don't forget add `syn-cloud` hostnames and IP addresses to the `/etc/hosts` file and add the right password to the `vaultpass.txt` file to decrypt inventory file and start deploy. 

#### Deploy ZooKeeper and Kafka:
```bash
$ ansible-playbook zookeeper-deploy.yml
$ ansible-playbook kafka-deploy.yml
```
#### To check Zookeper nodes execute the following command on each of nodes to find which one is follower and leader:
```bash
$ echo srvr | nc 127.0.0.1 2181
```

#### Kafka role will unify each kafka node `borker.id` in the `/etc/kafka/server.properties` file. Log files placed in the `/var/lib/kafka/logs` folder. To troubleshoot we can comment needed keys inside of `/var/lib/kafka/logs/meta.properties` file for each of the nodes.

#### Execute the following command in one of the nodes to create Kafka Topic:
```bash
$ /opt/kafka/bin/kafka-topics.sh --create --zookeeper 192.168.184.71:2181 --replication-factor 3 --partitions 1 --topic nuclioevents
Created topic nuclioevents.
```
#### Look at the replicated topic:
```bash
$ /opt/kafka/bin/kafka-topics.sh --describe --zookeeper 192.168.184.71:2181 --topic nuclioevents
Topic: nuclioevents     PartitionCount: 1       ReplicationFactor: 3    Configs:
        Topic: nuclioevents     Partition: 0    Leader: 2       Replicas: 2,1,3 Isr: 2,1,3
```
##### From one of the nodes send some messages to the created topic:
```bash
$ /opt/kafka/bin/kafka-console-producer.sh --broker-list 192.168.184.71:9092 --topic nuclioevents
>test tessage
>^C
```

#### From another node get this messages from topic:
```bash
$ /opt/kafka/bin/kafka-console-consumer.sh --topic nuclioevents --from-beginning --bootstrap-server 192.168.184.72:9092
test tessage
```

#### Create consumer group with name `nuclio-consumer-group` for the topic `nuclio`:
```bash
$ /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 192.168.184.72:9092 --topic nuclioevents --consumer-property group.id=nuclio-consumer-group
^CProcessed a total of 0 messages
```

#### List consumer groups:
```bash
$ /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server 192.168.184.72:9092 --describe --group nuclio-consumer-group
Consumer group 'nuclio-consumer-group' has no active members.
GROUP                 TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID     HOST            CLIENT-ID
nuclio-consumer-group nuclioevents    0          1               1               0               -               -               -
```
