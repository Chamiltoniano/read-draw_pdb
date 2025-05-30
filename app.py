from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        lines = file.read().decode('utf-8').splitlines()
        return jsonify(lines)
    return jsonify([])

if __name__ == '__main__':
    app.run()
