import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import re

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

def azure_chat_openai(latitude, longitude, temperature, precipitation):     
    
    try:
        client = AzureOpenAI(
            azure_endpoint = OPENAI_API_BASE, 
            api_key=OPENAI_API_KEY,  
            api_version=OPENAI_API_VERSION
            )
        
        prompt = get_prompt()
        types = 'Plants,Trees,Spices,Succulents'
        formatted_prompt = format_prompt(prompt, latitude, longitude, str(temperature)+'C', str(precipitation)+'mm')

        # Create the request to the Azure OpenAI model
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": formatted_prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            model=OPENAI_ENGINE
        )
        
        # Extract and return the model's response
        text = response.choices[0].message.content
        return recursive_split(text)
    
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
    
def format_prompt(template, latitude, longitude, temperature, precipitation):
    # Use the format method to replace placeholders
    return template.format(latitude=latitude, longitude=longitude, temperature=temperature, precipitation=precipitation)


def recursive_split(text):
    result = {}
    
    # Step 1: Split the text into main categories (Plants, Trees, Spices, Succulents)
    sections = re.split(r'\n\n(?=\w+:)', text.strip())  # Matches "\n\n" followed by a section heading
    intro_text = sections.pop(0)  # The initial text part before sections

    result["Introduction"] = intro_text.strip()

    # Step 2: Process each section
    for section in sections:
        section_title, items = section.split(":\n", 1)  # Split the section title (Plants, Trees, etc.) from the content
        section_title = section_title.strip()
        result[section_title] = []
        
        # Step 3: Extract individual items (plants, trees, etc.)
        items_split = re.split(r'\n(?=\d+\.)', items.strip())  # Matches lines starting with numbered items like "1."
        
        for item in items_split:
            item_lines = item.split("\n")  # Split individual items by newlines
            item_info = {}
            
            # Step 4: Extract item name and description
            title_line = item_lines[0].split(" - ")
            item_info["Name"] = title_line[0].split(". ")[1].strip()  # Extract the item name
            if len(title_line) > 1:
                item_info["Scientific Name"] = title_line[1].strip()  # Extract the scientific name if present

            # Step 5: Extract maintenance details if present
            for line in item_lines[1:]:
                if "Maintenance:" in line:
                    maintenance_info = line.split("Maintenance:")[1].strip()
                    item_info["Maintenance"] = maintenance_info
            
            # Add the processed item to the corresponding section
            result[section_title].append(item_info)
    
    return result