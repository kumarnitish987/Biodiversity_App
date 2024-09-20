from flask import Flask, jsonify
from environment_details import  get_gps_info,  get_current_environment_conditions
from openAI_module import azure_chat_openai


app = Flask(__name__)

@app.route('/getPlantSuggestions', methods=['GET'])
def get_environment_Conditions():
    try:
        # image_path = "C:\\Users\\kumarnitish\\Desktop\\Hackathon\\DSCN0010.jpg"  # Replace with your image path
        # lat, lon = get_gps_info(image_path)
        # environment_Conditions = get_current_environment_conditions(lat, lon)
        response = azure_chat_openai()
        return jsonify(response)
    except Exception as e:
        raise e 


if __name__ == '__main__':
    app.run(debug=True)
