from flask import request, jsonify, Blueprint
from app.predictor import Predictor
predictor = Predictor()
print(predictor)
bp = Blueprint('blueprint', __name__, template_folder='templates')


@bp.route("/", methods=["GET"])
def index():
    return jsonify(message="Hello World!"), 200


@bp.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        prediction = predictor.predict(request)
        return prediction
    else:
        return '''<form method="POST">
                  Song Lyrics: <textarea name="lyrics" row=500 columns=1000 style="width: 800px; height: 500px;"></textarea>
                  <input type="submit" value="Submit"><br>
              </form>'''
        # return jsonify(message="Hello World!"), 200
        # return render_template('index.html')
