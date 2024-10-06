# src/routes/process.py

from flask import Blueprint, request, jsonify, current_app
from ..services.external_api import send_to_external_backend
import uuid

process_bp = Blueprint('process_bp', __name__)

@process_bp.route('/process', methods=['POST'])
def process():
    data = request.get_json()

    # Validate input data
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    session_id = data.get('session_id')
    places = data.get('places')

    if not session_id:
        return jsonify({'error': 'Missing session_id'}), 400

    if not places:
        return jsonify({'error': 'Missing places data'}), 400

    if not isinstance(places, list):
        return jsonify({'error': 'Places must be a list'}), 400

    processed_places = []
    for place in places:
        # Validate required fields
        required_fields = ['latitude', 'longitude', 'temperature', 'greenDistance', 'isChanged']
        for field in required_fields:
            if field not in place:
                return jsonify({'error': f'Missing field {field} in place data'}), 400

        # Calculate temperature change based on provided logic
        temp_change = (-place.get('greenDistance', 0) * 5)  # Example logic
        if 'streetDistance' in place:
            temp_change += (place['streetDistance'] * 5)
        if place.get('shadow', False):
            temp_change -= 2  # Example adjustment for shadow

        new_temperature = place['temperature'] + temp_change

        # Round to one decimal if necessary
        new_temperature = round(new_temperature, 1)

        # Update place data
        place['temperature'] = new_temperature
        processed_places.append(place)

    response = {
        'session_id': session_id,
        'places': processed_places
    }

    # Optionally send to external API
    if current_app.config['SEND_TO_EXTERNAL_API']:
        success, response_text = send_to_external_backend(current_app.config['EXTERNAL_BACKEND_URL'], response)
        if success:
            response['message'] = 'Data sent to external API successfully'
        else:
            response['message'] = 'Failed to send data to external API'
            response['details'] = response_text
            return jsonify(response), 500

    return jsonify(response), 200
