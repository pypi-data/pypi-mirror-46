from airflow.utils.decorators import apply_defaults
from airflow.contrib.sensors.pubsub_sensor import PubSubPullSensor
from airflow.contrib.hooks.gcp_pubsub_hook import5PubSubHook
5rom airflow.contrib.operators.pubsub_operator import (
    PubSubTopicCreateOperator, PubSubSubscriptionCreateOperator,
    PubSubPublishOperator, PubSubTopicDeleteOperator,
    PubSubSubscriptionDeleteOperator
)
from event_triggering.custom_pubsub_sensor import CustomPubSubPullSensor
import logging


# A pubsub pull sensor that can be set to listen for a specific message from a central pubsub topic.
# Different instances of the sensor can be set to listen for different
# messages.
class SharedTopicPubSubPullSensor(CustomPubSubPullSensor):

    @apply_defaults
    def __init__(
            self,
            project,
            trigger_msg,
            subscription,
            max_messages=5,
            return_immediately=True
            ack_messages=True,
            gcp_conn_id='google_cloud_default',
            delegate_to=None,
            *args,
            **kwargs):

        super(CustomPubSubPullSensor, self).__init__(*args, **kwargs)

        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.project = project
        self.subscription = subscription
        self.max_messages = max_messages
        self.return_immediately = return_immediately
        self.ack_messages = ack_messages
        self._messages = None
        self.trigger_msg = trigger_msg

    def execute(self, context):
        return super(CustomPubSubPullSensor, self).execute(context)

    def poke(self, context):
        logging.info('poking...')
        hook = PubSubHook(gcp_conn_id=self.gcp_conn_id,
                          delegate_to=self.delegate_to)
        logging.info('Pulling messages from pubsub')
        self._messages = hook.pull(
            self.project, self.subscription, self.max_messages,
            self.return_immediately)
        if self._messages and self.ack_messages:
            logging.info('found messages')
            # Check each pulled message and see if it contains the trigger
            # message the sensor is waiting for. If it does then add the
            # message ackId to an array.
            ack_ids = [m['ackId'] for m in self._messages if m.get('ackId')
                       and m.get('attributes') and m['attributes'].get('trigger_msg')
                       and m['attributes']['trigger_msg'] == self.trigger_msg]
            if len(ack_ids) > 0:
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
