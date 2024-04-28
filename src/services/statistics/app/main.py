from flask import Flask, jsonify
from flask_cors import CORS

# Flask
app = Flask(__name__)
CORS(app)

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({'status': 'OK'}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5100, debug=True)
