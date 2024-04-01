from flask import Flask,request, jsonify
import requests

app = Flask(__name__)

BEARER_TOKEN = "t-g2053qn7XJGGVSRVPSPCFWPKRRZYE4WGWZDZ7U7A"

@app.route('/base' , methods=['POST'])
def hello_world():
    request_data = request.json  # This holds your JSON data
    print(request_data)

    if 'challenge' in request_data:
        return jsonify({"challenge": request_data['challenge']}), 200

    # Use jsonify to return the data in JSON format
    # The URL of the webhook
    url = 'https://webhooks.workato.com/webhooks/rest/7f8bae3d-560e-4cbd-9a56-44241fc466b0/test_base'

    # The payload you want to send
    payload = {
        "email": "junyu.wang@bytedance.com",
        "subject": "receive a sheet update",
        "content": "content: {}".format(request_data)
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

@app.route('/sheet/creation' , methods=['POST'])
def manage_sheet():
    # Step 1: Create Sheet
    create_response = create_sheet()
    print("create_response", create_response)

    if create_response['code'] != 0:
        return jsonify({"error": "Failed to create sheet"}), 500
    spreadsheet_token = create_response['data']['spreadsheet']['spreadsheet_token']
    spreadsheet_url = create_response['data']['spreadsheet']['url']

    # Step 2: Subscribe to Sheet
    subscribe_response = subscribe_sheet(spreadsheet_token)
    if subscribe_response.get('code', 1) != 0:  # Assuming a non-zero code is an error
        return jsonify({"error": "Failed to subscribe to sheet"}), 500

    print("subscribe_response", subscribe_response)

    # Step 3: Get Sheet Info
    sheet_info_response = get_sheet_info(spreadsheet_token)
    if sheet_info_response['code'] != 0:
        return jsonify({"error": "Failed to get sheet info"}), 500

    print("sheet_info_response", sheet_info_response)
    sheet_id = sheet_info_response['data']['sheets'][0]['sheet_id']

    return jsonify({"message": "Sheet created successfully {}".format(spreadsheet_url),
                    "spreadsheet_token":  spreadsheet_token,
                    "sheet_id": sheet_id}), 200


@app.route('/sheet/update' , methods=['POST'])
def sheet_update():
    request_data = request.json  # This holds your JSON data
    print(request_data)

    spreadsheet_token = request_data['spreadsheet_token']
    sheet_id = request_data['sheet_id']
    values = [["===", "https://www.xxx.com/"], ["Hello", "https://www.xxx.com/"],
              ["World", "https://www.xxx.com/"], ["===", "https://www.xxx.com/"]]

    if 'gmail' in request_data:
        values = [["Gmail", "{}".format(request_data['gmail'])]]


    # Step 4: Update Sheet

    update_response = update_sheet(spreadsheet_token, sheet_id, values)
    if update_response.get('code', 1) != 0:
        return jsonify({"error": "Failed to update sheet"}), 500

    print("update_response", update_response)

    return jsonify({"message": "Sheet created and updated successfully {}"}), 200

def create_sheet():
    url = "https://open.larksuite.com/open-apis/sheets/v3/spreadsheets"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"title": "title"}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def subscribe_sheet(spreadsheet_token):
    url = f"https://open.larksuite.com/open-apis/drive/v1/files/{spreadsheet_token}/subscribe?file_type=sheet"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, headers=headers)
    return response.json()

def get_sheet_info(spreadsheet_token):
    url = f"https://open.larksuite.com/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/query"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",}
    response = requests.get(url, headers=headers)
    return response.json()

def update_sheet(spreadsheet_token, sheet_id, values):
    url = f"https://open.larksuite.com/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"valueRange": {"range": f"{sheet_id}!A1:B4", "values": values}}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
