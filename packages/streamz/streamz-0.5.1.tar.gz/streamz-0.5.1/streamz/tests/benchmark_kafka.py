import confluent_kafka as ck
from streamz.tests.test_kafka import launch_kafka
import time
from streamz import Stream

cid = launch_kafka()
conf = {'bootstrap.servers': 'localhost:9092'}
cconf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'testing'}

ck.Producer(conf)
producer = ck.Producer(conf)
topic = 'mytest'

n_parts = 1
n_msg = 100_000

for i in range(n_msg):
    producer.produce(topic, value=b'%i' % i, partition=i % n_parts)
    if i % 1000 == 0:
        producer.flush()

consumer = ck.Consumer(cconf)
tp = ck.TopicPartition(topic, 0, 0)

t0 = time.time()
msg = consumer.poll(0)
while msg and msg.value():
    keep = msg
    msg = consumer.poll(0)
print('direct', time.time() - t0)

print('batched', time.time())
stream = Stream.from_kafka_batched(topic, cconf, npartitions=n_parts,
                                   poll_interval=0.1)
stream.map(lambda batch: (any(
    int(msg) >= n_msg-1 for msg in batch), time.time())).sink(print)
stream.start()


# import dask.distributed
# client = dask.distributed.Client(processes=False)
#
# print('dask start', time.time())
# stream = Stream.from_kafka_batched(topic, cconf, npartitions=n_parts, dask=True)
# stream.map(lambda batch: (any(
#     int(msg) >= n_msg-1 for msg in batch), time.time())).gather().sink(print)
# stream.start()
