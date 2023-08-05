

# Private config class
class __Config:

    def __init__(self):
        self.project = 'YOUR_PROJECT'
        self.topic = 'YOUR_TRIGGER_TOPIC'
        self.subscription = 'YOUR_SUB_NAME'
        self.subscription_project = 'YOUR_SUB_PROJECT'
        self.api_key = 'YOUR_API_KEY'
        self.gcp_conn_name = 'GCP_CONN'
        self.logging_topic = 'YOUR_LOG_TOPIC'


config = __Config()
