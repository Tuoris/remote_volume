from flask import Flask, render_template, request, jsonify
from volume_control import Volume

app = Flask(__name__)
volume = Volume()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/info', methods=['GET'])
def get_level():
    level = volume.get_volume_level()
    muted = volume.get_mute()
    return jsonify({'level': level, 'muted': muted})


@app.route('/change_level', methods=['POST'])
def change_level():
    json = request.get_json()
    level = int(json['level'])
    volume.set_volume_level(level)
    return jsonify({'success': True})


@app.route('/mute', methods=['POST'])
def mute_speaker():
    json = request.get_json()
    mute = json['mute']
    if mute:
        volume.mute()
    else:
        volume.un_mute()
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
