from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    data = {"message": "Hello, World!", "status": "success"}
    # Use jsonify to return the data in JSON format
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
