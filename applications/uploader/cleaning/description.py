from interfaces.openai_client import OpenAIClient
from applications.uploader.data_models import OutputCleanDescription
from interfaces.scraper_db.pages.service import get_inferred_description, set_inferred_description
from hashlib import md5



def build_formatted_description_prompt(raw_data):
    with open('applications/uploader/cleaning/prompts/formatted_description.txt', 'r') as file:
        prompt = file.read()
    return prompt.replace('<<raw_data>>', str(raw_data))



def clean_description(description: str|None, url: str) -> str:
    if not description:
        return description
    
    inferred_description = get_inferred_description(url)
    description_hash = md5(description.encode()).hexdigest()
    if inferred_description and inferred_description.get('original_description_hash') == description_hash:
        return inferred_description.get('description')
    
    client = OpenAIClient()
    response = client.openai_stuctured_request(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that cleans and formats descriptions of boats from a website."},
            {"role": "user", "content": build_formatted_description_prompt(description)}
        ],
        response_format=OutputCleanDescription,
        model='gpt-4.1-nano'
    )

    set_inferred_description(url, response['description'], description_hash)

    return response['description']




