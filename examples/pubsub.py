import functions_framework
import base64

from cloudevents.http import CloudEvent
from google.cloud import pubsub_v1

# example https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/functions/v2/pubsub/main.py
@functions_framework.cloud_event
def my_cloudevent_function(cloud_event: CloudEvent) -> None:
    """13818704876485087
    result of print(cloud_event.data)
    {
        'message': {
            'data': 'RnJpZW5k', 
            'messageId': '13819338076642563', 
            'message_id': '13819338076642563', 
            'publishTime': '2025-01-29T10:41:27.485Z', 
            'publish_time': '2025-01-29T10:41:27.485Z'
        }, 
        'subscription': 'projects/optimap-438115/subscriptions/eventarc-asia-northeast3-function-946247-sub-225'
    }

    참고
    https://cloud.google.com/docs/overview?hl=en -> base64 encoding = aHR0cHM6Ly9jbG91ZC5nb29nbGUuY29tL2RvY3Mvb3ZlcnZpZXdcP2hsXD1lbg==
    aHR0cHM6Ly9jbG91ZC5nb29nbGUuY29tL2RvY3Mvb3ZlcnZpZXdcP2hsXD1lbg== -> base64 decoding = https://cloud.google.com/docs/overview\?hl\=en
    escape sequence 처리 필수
    """
    decoded = base64.b64decode(cloud_event.data["message"]["data"])
    data = decoded.decode()
    print(data)
    print(cloud_event.data)
    if data == "finish":
        return

    # create topic
    # https://cloud.google.com/pubsub/docs/publisher?hl=ko
    # https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library?hl=ko
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(
        project="optimap-438115",
        topic="functions2-topic",
    )
    data_str = "finish"
    # when you publish a message, the client returns a future
    publish_future = publisher.publish(
        topic_path, 
        data_str.encode("utf-8"), # byte string by utf8, 자동으로 base64로 인코딩
        origin="python-sample", username="gcp"
    )
    print(publish_future.result()) # topic id를 출력함
    print(f"Published messages with error handler to {topic_path}.")

    """
    log result
    LEVEL    NAME      EXECUTION_ID  TIME_UTC                 LOG
         function  PzFVCOGT9SXV  2025-01-29 12:18:26.213  {'message': {'attributes': {'origin': 'python-sample', 'username': 'gcp'}, 'data': 'ZmluaXNo', 'messageId': '13819686650430781', 'message_id': '13819686650430781', 'publishTime': '2025-01-29T12:18:23.024Z', 'publish_time': '2025-01-29T12:18:23.024Z'}, 'subscription': 'projects/optimap-438115/subscriptions/eventarc-asia-northeast3-function-993034-sub-174'}
         function  PzFVCOGT9SXV  2025-01-29 12:18:26.213  finish
I        function                2025-01-29 12:18:26.209
         function  YjeLm1PbeHLf  2025-01-29 12:18:23.029  Published messages with error handler to projects/optimap-438115/topics/functions2-topic.
         function  YjeLm1PbeHLf  2025-01-29 12:18:23.029  13819686650430781
         function  YjeLm1PbeHLf  2025-01-29 12:18:22.846  {'message': {'data': 'aHR0cHM6Ly9jbG91ZC5nb29nbGUuY29tL2RvY3Mvb3ZlcnZpZXdcP2hsXD1lbg==', 'messageId': '13820202978517900', 'message_id': '13820202978517900', 'publishTime': '2025-01-29T12:18:19.47Z', 'publish_time': '2025-01-29T12:18:19.47Z'}, 'subscription': 'projects/optimap-438115/subscriptions/eventarc-asia-northeast3-function-993034-sub-174'}
         function  YjeLm1PbeHLf  2025-01-29 12:18:22.846  https://cloud.google.com/docs/overview\?hl\=en
I        function                2025-01-29 12:18:22.821
I        function                2025-01-29 12:08:12.380  Default STARTUP TCP probe succeeded after 1 attempt for container "worker" on port 8080.
         function                2025-01-29 12:08:08.302  13818704876485087
         function                2025-01-29 12:08:08.302  /workspace/main.py:232: SyntaxWarning: invalid escape sequence '\?'
    """