import requests
from pprint import pprint
import yaml


def get_json_from_post_request(documents_to_classify, api_suffix):
    api_url = base_url + api_suffix
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(api_url, headers=headers, json=documents_to_classify)
    return response.json()


def get_language(documents_to_classify):
    return get_json_from_post_request(documents_to_classify, "languages")


def get_sentiment(documents_to_classify):
    return get_json_from_post_request(documents_to_classify, "sentiment")


def get_key_phrases(documents_to_classify):
    return get_json_from_post_request(documents_to_classify, "keyPhrases")


if __name__ == "__main__":
    global subscription_key
    global base_url
    with open('settings.yaml', 'r') as f:
        data = yaml.load(f)
    subscription_key = data['azure-subscriptionkey']
    base_url = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/"

    documentsLanguage = {'documents': [
        {'id': '1', 'text': 'This is a document written in English.'},
        {'id': '2', 'text': 'Este es un document escrito en Español.'},
        {'id': '3', 'text': '这是一个用中文写的文件'}]}

    documentsSentiment = {'documents': [
        {'id': '1', 'language': 'en',
         'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
        {'id': '2', 'language': 'en',
         'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},
        {'id': '3', 'language': 'es',
         'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},
        {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}]}

    documentsKeyPhrases = {'documents': [{'id': '1', 'text': 'This is a document written in English.'},
                                         {'id': '2', 'text': 'Este es un document escrito en Español.'},
                                         {'id': '3', 'text': '这是一个用中文写的文件'}]}

    languages = get_language(documentsLanguage)
    sentiment = get_sentiment(documentsSentiment)
    key_phrases = get_key_phrases(documentsKeyPhrases)

    pprint(languages)
    pprint(sentiment)
    pprint(key_phrases)

