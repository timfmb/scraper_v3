from interfaces.openai_client import OpenAIClient
from applications.uploader.data_models import OutputCleanDescription
from interfaces.scraper_db.pages.service import get_inferred_description, set_inferred_description
from hashlib import md5
from logging_config import get_logger

logger = get_logger(__name__)


def build_formatted_description_prompt(raw_data):
    with open('applications/uploader/cleaning/prompts/formatted_description.txt', 'r') as file:
        prompt = file.read()
    return prompt.replace('<<raw_data>>', str(raw_data))


def clean_description(description: str|None, url: str) -> str:
    """
    Clean and format boat description with improved caching logic.
    
    Issues fixed:
    1. Added input validation and normalization
    2. Improved error handling
    3. Enhanced logging for debugging
    4. Better cache verification
    """
    # Input validation
    if not description or not isinstance(description, str):
        logger.debug(f"No description provided for URL: {url}")
        return description
    
    # Normalize description (strip whitespace, handle encoding)
    normalized_description = description.strip()
    if not normalized_description:
        logger.debug(f"Empty description after normalization for URL: {url}")
        return description
    
    # Generate hash for normalized description
    description_hash = md5(normalized_description.encode('utf-8')).hexdigest()
    logger.debug(f"Generated hash {description_hash} for URL: {url}")
    
    # Try to get cached result
    try:
        inferred_description = get_inferred_description(url)
        logger.debug(f"Retrieved cached data for URL {url}: {inferred_description}")
        
        if inferred_description and isinstance(inferred_description, dict):
            cached_hash = inferred_description.get('original_description_hash')
            cached_result = inferred_description.get('description')
            
            if cached_hash == description_hash and cached_result:
                logger.info(f'Using cached description for URL: {url}')
                return cached_result
            else:
                logger.debug(f"Cache miss - hash mismatch or missing result. Cached hash: {cached_hash}, Current hash: {description_hash}")
        else:
            logger.debug(f"No valid cached data found for URL: {url}")
            
    except Exception as e:
        logger.error(f"Error retrieving cached description for URL {url}: {e}")
    
    # Generate new description using OpenAI
    logger.info(f'Generating new inferred description for URL: {url}')
    try:
        client = OpenAIClient()
        response = client.openai_stuctured_request(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that cleans and formats descriptions of boats from a website."},
                {"role": "user", "content": build_formatted_description_prompt(normalized_description)}
            ],
            response_format=OutputCleanDescription,
            model='gpt-4.1-mini'
        )
        
        if not response or 'description' not in response:
            logger.error(f"Invalid response from OpenAI for URL: {url}")
            return description
        
        new_description = response['description']
        
        # Cache the result with error handling
        try:
            set_inferred_description(url, new_description, description_hash)
            logger.debug(f"Cached new description for URL: {url}")
        except Exception as e:
            logger.error(f"Error caching description for URL {url}: {e}")
        
        return new_description
        
    except Exception as e:
        logger.error(f"Error generating description for URL {url}: {e}")
        return description




