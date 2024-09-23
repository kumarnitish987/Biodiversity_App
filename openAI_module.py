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
        return convert_into_json(text)
    
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

def convert_into_json(text):
    data = {
        "Introduction": "",
        "Plants": [],
        "Trees": [],
        "Spices": []
    }

    sections = re.split(r'\n\n(?=\w+:)', text.strip())
    intro_text = sections.pop(0)  # The initial text part before sections
    introduction_start = intro_text.find("Introduction:") + len("Introduction: ")
    introduction = intro_text[introduction_start:].strip()

    data["Introduction"] = introduction

    plants_section = text.split("Plants:")[1].split("Trees:")[0]
    data["Plants"] = extract_items(plants_section)

    trees_section = text.split("Trees:")[1].split("Spices:")[0]
    data["Trees"] = extract_items(trees_section)

    spices_section = text.split("Spices:")[1]
    data["Spices"] = extract_items(spices_section)

    return data

def extract_items(section):
    items = re.split(r'\n\n+', section.strip())
    result = []
    for item in items:
        items_split = re.split(r'\n(?=\d+\.)', item.strip())
        for item in items_split:
            lines = item.split(": ", 1)
            if len(lines) > 1:
                name = lines[0].strip().split(". ")[1]  # Get the name
                maintenance = lines[1].strip()  # Get the maintenance information
                result.append({"Name": name, "Maintenance": maintenance})
    return result
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
            #if len(title_line) > 1:
                #item_info["Maintenance"] = title_line[1].strip()  # Extract the maintenance details if present

            # Step 5: Extract maintenance details if present
            #for line in item_lines[1:]:
                #if "Maintenance:" in line:
                    #maintenance_info = line.split("Maintenance:")[1].strip()
                    #item_info["Maintenance"] = maintenance_info
            
            # Add the processed item to the corresponding section
            result[section_title].append(item_info)
    
    return result