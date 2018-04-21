import requests


class TextAnalyzerAzure:

    __base_url = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/"
    __headers = ""

    def __init__(self, subscriptionkey):
        self.__headers = {"Ocp-Apim-Subscription-Key": subscriptionkey}

    def send_post_request(self, document_to_analyze, api_suffix):
        api_url = self.__base_url + api_suffix
        response = requests.post(api_url, headers=self.__headers, json=document_to_analyze)
        return response.json()

    def get_language(self, documents_to_analyze):
        return self.send_post_request(documents_to_analyze, "languages")

    def get_sentiment(self, documents_to_analyze):
        return self.send_post_request(documents_to_analyze, "sentiment")

    def get_key_phrases(self, documents_to_analyze):
        return self.send_post_request(documents_to_analyze, "keyPhrases")

    @staticmethod
    def get_documents_with_language(list_of_text_to_analyze, language):
        json_objects = []
        index = 1
        for text in list_of_text_to_analyze:
            json_objects.append({'language': language, 'id': str(index), 'text': text})
            index += 1
        return {'documents': json_objects}

    @staticmethod
    def get_documents(list_of_text_to_analyze):
        json_objects = []
        index = 1
        for text in list_of_text_to_analyze:
            json_objects.append({'id': str(index), 'text': text})
            index += 1
        return {'documents': json_objects}
