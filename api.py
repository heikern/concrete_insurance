# from urllib.request import Request
# from flask import request, jsonify
# import flask

import flask
from flask import request, jsonify
from flask_cors import CORS
from joblib import dump, load
from pathlib import Path
from scipy.stats import norm

curr_dir = Path.cwd()
parent_dir = curr_dir.parents[0]
output_data_dir = parent_dir / "machine_learning_model"
model_path = output_data_dir / "model.joblib"

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcom to Concrete Concrete!!</h1>"


@app.route('/get_quote', methods = ['GET'])
def get_strength():
    if 'wcr' in request.args and 'acr' in request.args:
        wcr = float(request.args["wcr"])
        acr = float(request.args["acr"])
        long = float(request.args["long"])
        lat = float(request.args["lat"])
        req_strength = float(request.args["req_strength"])
        pour_revenue = float(request.args["pour_revenue"])
        
        pour_star = request.args["pour_star"]

        pour_star_multipliers = [1.2,1,0.99,0.97,0.96]
        pour_star_coeff = pour_star_multipliers[int(pour_star)]

        clf = load(model_path)
        mean_strength = float(clf.predict([[wcr,acr,long,lat]]))
        # internal hardcoded parameter
        sigma = 0.1
        margin = 1.1
        cdf = norm.cdf(x=req_strength, loc=mean_strength, scale=sigma)

        premium = pour_revenue * margin * cdf * pour_star_coeff


        output = {
            "pof": cdf,
            "pour_revenue" : pour_revenue,
            "margin": margin,
            "pour_star_coeff": pour_star_coeff,
            "mean_strength": mean_strength,
            "variance_strength" : sigma*sigma,
            "premium": premium
        }
        return jsonify(output)
        # return output
    else:
        return "gimmie something to work with"

app.run()


# http://127.0.0.1:5000/get_quote?wcr=0.45&acr=4.4&long=30&lat=50&&output=json