from pprint import pprint

import yaml

from api.textanalyzer_azure import TextAnalyzerAzure
from api.textanalyzer_watson import TextAnalyzerWatson
from textextraction.extract_frompdf import extract_text

if __name__ == '__main__':
    with open('settings.yaml', 'r') as f:
        credentials = yaml.load(f)

    azure = TextAnalyzerAzure(credentials["azure-subscriptionkey"])
    watson = TextAnalyzerWatson(credentials["ibm-username"], credentials["ibm-password"], "2017-02-27")

    files = ['../../exampleData/Unternehmensbefragung/Unternehmensbefragung-2001-kurz.pdf',
             '../../exampleData/Unternehmensbefragung/Unternehmensbefragung-2002-kurz.pdf',
             '../../exampleData/Unternehmensbefragung/Unternehmensbefragung-2003-2004-kurz.pdf',
             '../../exampleData/Unternehmensbefragung/Unternehmensbefragung-2005-kurz.pdf',
             '../../exampleData/Unternehmensbefragung/Unternehmensbefragung-2006-kurz-D.pdf',
             '../../exampleData/Unternehmensbefragung/Unternehmensbefragung-2008-Kurz-Deutsch.pdf']

    texts = []
    print("Start extracting text from pdf files...")
    for file in files:
        texts.append(extract_text(file).replace("-\n",""))
    print("Finished extracting text from pdf files!")

    document = azure.get_documents(texts)
    response = azure.get_language(document)
    pprint(response)








