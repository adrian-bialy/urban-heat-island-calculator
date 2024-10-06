from flask import Blueprint, request, jsonify, current_app
import logging
import uuid  # For generating a unique session_id
from ..services.external_api import send_to_external_backend

process_bp = Blueprint('process_bp', __name__)

@process_bp.route('/process', methods=['POST'])
def process_points():
    # Log the receipt of a new request
    current_app.logger.info(f"Received request from {request.remote_addr}")

    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            current_app.logger.warning(
                f"Invalid input from {request.remote_addr}: Expected a JSON object with 'places' key."
            )
            return jsonify({'error': 'Invalid input, expected a JSON object with "places" key'}), 400

        points_list = data.get('places')
        if points_list is None or not isinstance(points_list, list):
            current_app.logger.warning(
                f"Invalid 'places' data from {request.remote_addr}."
            )
            return jsonify({'error': 'Missing or invalid "places" key in input'}), 400

        processed_points = []

        for point in points_list:
            latitude = point.get('latitude')
            longitude = point.get('longitude')
            temperature = point.get('temperature')
            green_distance = point.get('greenDistance', 0)
            street_distance = point.get('streetDistance', 0)  # Optional with default 0
            shadow = point.get('shadow')  # Optional, not used in calculation
            is_changed = point.get('isChanged', False)

            # Validate required inputs
            if latitude is None or longitude is None or temperature is None:
                current_app.logger.warning(
                    f"Missing latitude, longitude, or temperature in point from {request.remote_addr}."
                )
                return jsonify({'error': 'Missing latitude, longitude, or temperature in point'}), 400

            # Process only if isChanged is true
            if is_changed:
                # Perform calculations
                temp_change = 0

                # Apply greenDistance factor (0 to -5 degrees)
                if 0 <= green_distance <= 1:
                    temp_change += (-green_distance * 5)
                else:
                    current_app.logger.warning(
                        f"Invalid greenDistance value from {request.remote_addr}: {green_distance}"
                    )
                    return jsonify({'error': 'greenDistance must be between 0 and 1'}), 400

                # Apply streetDistance factor if provided
                if street_distance is not None:
                    if 0 <= street_distance <= 1:
                        temp_change += (street_distance * 5)
                    else:
                        current_app.logger.warning(
                            f"Invalid streetDistance value from {request.remote_addr}: {street_distance}"
                        )
                        return jsonify({'error': 'streetDistance must be between 0 and 1'}), 400

                # Update temperature
                temperature += temp_change

            # Append the point to the processed_points list
            processed_points.append({
                'latitude': latitude,
                'longitude': longitude,
                'temperature': temperature
            })

        session_id = str(uuid.uuid4())

        # Prepare the output data
        output_data = {
            'session_id': session_id,
            'places': processed_points
        }

        # Check the configuration flag
        if current_app.config.get('SEND_TO_EXTERNAL_API', False):
            # Send data to the external backend
            external_backend_url = current_app.config['EXTERNAL_BACKEND_URL']
            success, response_text = send_to_external_backend(external_backend_url, output_data)

            if success:
                current_app.logger.info(f"Data sent to external API for session_id {session_id}")
                return jsonify({'message': 'Data sent to external API successfully'}), 200
            else:
                current_app.logger.error(
                    f"Failed to send data to external API for session_id {session_id}: {response_text}"
                )
                return jsonify({'error': 'Failed to update external backend', 'details': response_text}), 500
        else:
            # Return the output data to the user
            current_app.logger.info(f"Processed request successfully for session_id {session_id}")
            return jsonify(output_data), 200

    except Exception as e:
        current_app.logger.exception(f"Exception occurred while processing request from {request.remote_addr}")
        return jsonify({'error': 'Internal server error'}), 500
