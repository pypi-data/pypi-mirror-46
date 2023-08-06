import json
import requests
import uuid

class PersonalizerClient:

    subscription_key = ''
    personalizer_endpoint = ''
    headers = ''

    def __init__(self, subscription_key, personalizer_endpoint):
        self.subscription_key = subscription_key
        self.personalizer_endpoint = personalizer_endpoint
        self.headers = {'Ocp-Apim-Subscription-Key' : subscription_key, 'Content-Type': 'application/json'}

    def create_event_id(self):
        eventid = uuid.uuid4().hex
        return eventid
    
    def create_empty_rank_request(self):
        request = {
            'contextFeatures': [
            ],
            'actions': [
            ],
            'excludedActions': [
            ],
            'eventId': '',
            'deferActivation': False
        }
        return request
    
    def create_empty_reward_request(self):
        request = {
            "value": 0
        }
        return request

    def rank(self, event_id, rank_request):
        rank_request['eventId'] = event_id
        personalizer_rank_url = self.personalizer_endpoint + "/personalizer/v1.0/rank"
        response = requests.post(personalizer_rank_url, headers = self.headers, params = None, json = rank_request)
        return response
    
    def reward(self, event_id, reward_request):
        personalizer_reward_url = self.personalizer_endpoint + "/personalizer/v1.0/events/{}/reward"
        response = requests.post(personalizer_reward_url.format(event_id), headers = self.headers, params= None, json = reward_request)
        return response

    def reset_model(self):
        personalizer_reset_model_url = self.personalizer_endpoint + "/personalizer/v1.0/model"
        response = requests.delete(personalizer_reset_model_url, headers = self.headers, params = None)
        return response
        