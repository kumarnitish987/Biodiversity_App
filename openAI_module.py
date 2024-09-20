import os
import openai
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# load configuration from environment variables
try:
    OPENAI_API_BASE = os.environ['openai_api_base']
    OPENAI_API_VERSION = os.environ['openai_api_version']
    OPENAI_ENGINE = os.environ['openai_engine']
    OPENAI_API_KEY = os.environ['openai_api_key']
    OPENAI_API_TYPE = os.environ['openai_api_type']
except KeyError as e:
    raise e

def azure_chat_openai():    
    # Set up OpenAI environment variables for the Azure OpenAI service
    # openai.api_type = OPENAI_API_TYPE
    # openai.api_key = OPENAI_API_KEY
    # openai.api_base = OPENAI_API_BASE
    # openai.api_version = OPENAI_API_VERSION
    
    try:
        client = AzureOpenAI(
            azure_endpoint = OPENAI_API_BASE, 
            api_key=OPENAI_API_KEY,  
            api_version=OPENAI_API_VERSION
            )
        # Create the request to the Azure OpenAI model
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": get_prompt()}
            ],
            temperature=0.7,
            max_tokens=1000,
            model=OPENAI_ENGINE
        )
        
        # Extract and return the model's response
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error during OpenAI request: {e}")
        return e
    
def get_prompt():
    try:
        with open('prompt_file.txt', 'r') as file:
            prompt = file.read()
            return prompt
    except Exception as e:
        raise e


