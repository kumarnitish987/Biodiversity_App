from flask import Flask, jsonify, request
from environment_details import  get_gps_info,  get_current_environment_conditions
from openAI_module import azure_chat_openai
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/getPlantSuggestions', methods=['POST'])
def get_plants_suggestions():
    try:
        req_body = request.json        
        temperature, precipitation = get_current_environment_conditions(req_body["lat"], req_body["lon"])
        response = azure_chat_openai(req_body["lat"], req_body["lon"], temperature, precipitation)
        return jsonify(response)
    except Exception as e:
        raise e 
    
@app.route('/getPlantSuggestionsUsingPicture', methods=['POST'])
def get_plants_suggestions_by_image():

    UPLOAD_FOLDER = 'uploads/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    try:
        file = request.files['file'] 
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        lat, lon = get_gps_info(file_path)
        temperature, precipitation = get_current_environment_conditions(lat, lon)
        response = azure_chat_openai(lat, lon, temperature, precipitation)

        if os.path.exists(file_path):
            os.remove(file_path)
            
        return jsonify(response)
    except Exception as e:
        raise e 


if __name__ == '__main__':
    app.run(debug=True)
