from interfaces.openai_client import OpenAIClient
from .models import Output
from markdownify import markdownify


class FeatureExtractor:
    def __init__(self):
        self.client = OpenAIClient()

    def build_prompt(self, html_data):
        markdown_data = markdownify(html_data)
        with open('applications/data_extractor/feature_extraction/prompts/feature_extraction_prompt.txt', 'r') as file:
            prompt = file.read()

        prompt = prompt.format(raw_data=markdown_data)
        return prompt
    

    def build_messages(self, prompt):
        return [
            {"role": "system", "content": "You are an AI assistant that extracts structured data from boat listings. Your task is to parse the raw data and return a JSON object that strictly matches the given schema"},
            {"role": "user", "content": prompt}
        ]


    def extract_features(self, html_data):
        prompt = self.build_prompt(html_data)
        messages = self.build_messages(prompt)
        features = self.client.openai_stuctured_request(messages, Output)
        return features
