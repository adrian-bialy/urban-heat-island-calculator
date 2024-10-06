import requests

def send_to_external_backend(url, output_data):
    try:
        response = requests.post(url, json=output_data)
        if response.status_code == 200:
            return True, response.text
        else:
            return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)
