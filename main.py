from flask import Flask,request, jsonify
import requests

app = Flask(__name__)

@app.route('/base')
def hello_world():
    request_data = request.json  # This holds your JSON data
    print(request_data)
    data = {"message": "Hello, World!", "status": "success"}
    print('Hello, World!')
    # Use jsonify to return the data in JSON format
    # The URL of the webhook
    url = 'https://webhooks.workato.com/webhooks/rest/7f8bae3d-560e-4cbd-9a56-44241fc466b0/base'

    # The payload you want to send
    payload = {
        "email": "junyu.wang@bytedance.com",
        "subject": "subject",
        "content": "content"
    }

    # Additional headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return jsonify({"message": "Webhook sent successfully"}), 200
    else:
        return jsonify({"message": "Failed to send webhook", "status_code": response.status_code}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
