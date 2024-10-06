# Heat Island API

## Project Overview

The **Heat Island API** is a Flask-based web service designed to process environmental data related to various geographical locations. It analyzes factors such as temperature, green space distance, street distance, and shadow presence to provide insights into urban heat island effects.

## Project Structure

- **`src/app.py`**: Initializes the Flask application and registers blueprints.
- **`src/routes/process.py`**: Defines the `/process` endpoint to handle POST requests.
- **`src/config.py`**: Contains configuration settings for the application.
- **`src/wsgi.py`**: Entry point for WSGI servers like Gunicorn.
- **`requirements.txt`**: Lists Python dependencies.
- **`tests/`**: Directory containing unit tests for the application.

## How It Works

1. **Initialization**: The Flask application is initialized in `src/app.py`, where configurations are loaded, and blueprints are registered.
2. **Endpoint Handling**: The `/process` endpoint defined in `src/routes/process.py` accepts POST requests with JSON payloads containing environmental data.
3. **Data Processing**: Upon receiving a request, the API validates the input, processes each location's data (e.g., adjusting temperature based on green distance), and optionally sends the processed data to an external backend.
4. **Response**: The API responds with the processed data and a success message or appropriate error messages if issues arise. Data is posted to Heat Island App (https://github.com/vojcc/heat-islands).

## Creating a POST Request

To interact with the Heat Island API, you can create POST requests using tools like `curl` or **Postman**. Below are instructions and examples for both methods.

### Using `curl`

**Sample Successful Request:**

```bash
curl -X POST http://156.17.72.58:5000/process \
     -H "Content-Type: application/json" \
     -d '{
            "session_id": "321",
            "places": [
                {
                    "latitude": 51.11997701375166,
                    "longitude": 17.02961325645447,
                    "temperature": 20,
                    "greenDistance": 0.2,
                    "streetDistance": 0.3,
                    "shadow": false,
                    "isChanged": true
                },
                {
                    "latitude": 51.119983748152215,
                    "longitude": 17.029838562011722,
                    "temperature": 23,
                    "greenDistance": 0.2,
                    "isChanged": false
                },
                {
                    "latitude": 51.11995681054406,
                    "longitude": 17.03011751174927,
                    "temperature": 20,
                    "greenDistance": 0.2,
                    "shadow": false,
                    "isChanged": true
                }
            ]
        }'
```
**Sample bash script with request:**
``` bash
bash upload.sh
```

**Note**: message.json is a sample data input.