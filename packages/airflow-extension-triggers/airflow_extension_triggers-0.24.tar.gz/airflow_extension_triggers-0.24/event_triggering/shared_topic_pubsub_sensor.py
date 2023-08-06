from airflow.utils.decorators import apply_defaults
from airflow.contrib.sensors.pubsub_sensor import PubSubPullSensor
from airflow.contrib.hooks.gcp_pubsub_hook import PubSubHook
from airflow.contrib.operators.pubsub_operator import (
    PubSubTopicCreateOperator, PubSubSubscriptionCreateOperator,
    PubSubPublishOperator, PubSubTopicDeleteOperator,
    PubSubSubscriptionDeleteOperator
)

# A pubsub pull sensor that can be set to listen for a specific message from a central pubsub topic.
# Different instances of the sensor can be set to listen for different
# messages.
class SharedTopicPubSubPullSensor(PubSubPullSensor):

    @apply_defaults
    def __init__(
            self,
            project,
            trigger_msg,
            subscription,
            max_messages=100000,
            return_immediately=True,
            ack_messages=True,
            gcp_conn_id='google_cloud_default',
            delegate_to=None,
            poke_interval=60,
            timeout=180,
            *args,
            **kwargs):

        super(SharedTopicPubSubPullSensor, self).__init__(poke_interval=poke_interval,timeout=timeout,*args, **kwargs)

        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.project = project
        self.subscription = subscription
        self.max_messages = max_messages
        self.return_immediately = return_immediately
        self.ack_messages = ack_messages
        self._messages = None
        self.trigger_msg = trigger_msg

    def poke(self, context):
        self.log.info("poking...")
        hook = PubSubHook(gcp_conn_id=self.gcp_conn_id,
                          delegate_to=self.delegate_to)
        self.log.info("pulling messages...")
        self._messages = hook.pull(
            self.project, self.subscription, self.max_messages,
            self.return_immediately)
        if self._messages and self.ack_messages:
            self.log.info("found a message")
            # Check each pulled message and see if it contains the trigger
            # message the sensor is waiting for. If it does then add the
            # message ackId to an array.
            for mes in self._messages:
                for k, v in mes.iteritems():
                    self.log.info("key: " + str(k))
                    self.log.info("value: " + str(v))
            ack_ids = [m['ackId'] for m in self._messages if m.get('ackId')
                       and m.get('attributes') and m['attributes'].get('trigger_msg')
                       and m['attributes']['trigger_msg'] == self.trigger_msg]
            if len(ack_ids) > 0:
                self.log.info("found trigger message.  Acknowledging message")
                hook.acknowledge(self.project, self.subscription, ack_ids)
                return [msg for msg in self._messages if msg.get(
                    'ackId') and msg['ackId'] in ack_ids]


class SharedTopicSubscriptionTaskSet:

    def __init__(self, config, dag, trigger_msg):
        self.config = config
        self.dag = dag
        self.trigger_msg = trigger_msg

    @property
    def create_task(self):
        return PubSubSubscriptionCreateOperator(
            task_id='create_subscription', topic_project=self.config.project,
            subscription=self.config.subscription, topic=self.config.topic,
            subscription_project=self.config.subscription_project,
            dag=self.dag)

    @property
    def sensor_task(self):
        return SharedTopicPubSubPullSensor(
            task_id='success_sensor',
            project=self.config.project,
            trigger_msg=self.trigger_msg,
            subscription=self.config.subscription,
            max_messages=2,
            ack_messages=True,
            dag=self.dag)

    @property
    def delete_task(self):
        return PubSubSubscriptionDeleteOperator(
            task_id='delete_subscription',
            project=self.config.project,
            subscription=self.config.subscription,
            dag=self.dag)
