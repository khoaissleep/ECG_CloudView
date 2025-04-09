from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ecg_data = []

@app.route('/')
def index():
    return render_template('index.html', ecg_data=ecg_data)

@app.route('/update_data', methods=['POST'])
def update_data():
    global ecg_data
    data = request.json
    ecg_data = data.get("data", [])
    return jsonify({"status": "success"}), 200

@app.route('/get_data')
def get_data():
    global ecg_data
    return jsonify({"data": ecg_data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
