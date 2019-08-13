from flask import request, jsonify, Blueprint


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
        return jsonify(message="Hello World!"), 200
        # return render_template('index.html')
