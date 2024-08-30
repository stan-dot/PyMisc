from bluesky_stomp.messaging import MessageContext, MessagingTemplate
from bluesky_stomp.models import Broker, MessageQueue, MessageTopic

# from here https://pypi.org/project/bluesky-stomp/

# Assumes you have an unauthenticated broker such as ActiveMQ running on localhost:61613
template = MessagingTemplate.for_broker(Broker(host="localhost", port=61613))

try:
    # Connect to the broker
    template.connect()

    # Send a message to a queue and a topic
    template.send(MessageQueue(name="my-queue"), {"foo": 1, "bar": 2})
    template.send(MessageTopic(name="my-topic"), {"foo": 1, "bar": 2})

    # Subscribe to messages on a topic, print all messages received,
    # assumes there is another service to post messages to the topic
    def on_message(message: str, context: MessageContext) -> None:
        print(message)

    template.subscribe(MessageTopic(name="my-other-topic"), on_message)

    # Send a message and wait for a reply, assumes there is another service
    # to post the reply
    reply_future = template.send_and_receive(
        MessageQueue(name="my-queue"), {"foo": 1, "bar": 2}
    )
    print(reply_future.result(timeout=5.0))
finally:
    # Disconnect at the end
    template.disconnect()
