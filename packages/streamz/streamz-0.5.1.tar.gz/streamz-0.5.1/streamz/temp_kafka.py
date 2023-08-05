from streamz import Stream
import pandas as pd
import hvplot.streamz
import panel

s = Stream.from_textfile("/private/var/log/m_agent.log", from_end=True)
last = s.sliding_window(n=15).map(
    pd.DataFrame).to_dataframe(example=pd.DataFrame(['oi']))
layout = panel.Row([last.hvplot(kind="table")])
layout.show()
s.start()


def get_message_batch(kafka_params, topic, partition, low, high, timeout=None):
    """Fetch a batch of kafka messages in given topic/partition

    This will block until messages are available, or timeout is reached.
    """
    import confluent_kafka as ck
    t0 = time.time()
    consumer = ck.Consumer(kafka_params)
    tp = ck.TopicPartition(topic, partition, low)
    consumer.assign([tp])
    out = []
    try:
        while True:
            msg = consumer.poll(0.01)
            if msg:
                v = msg.value()
                if v and msg.error() is None:
                    off = msg.offset()
                    if high >= off:
                        out.append(v)
                    if high <= off:
                        break
            if timeout is not None and time.time() - t0 > timeout:
                break
    finally:
        pass
    return out


