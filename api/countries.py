from flask import jsonify, Blueprint, request
from helpers import login_required
from db import Repository

api = Blueprint('api', __name__)

db = Repository()


@api.route('/corps/<query>', methods=['GET'])
@api.route('/corps/', methods=['GET'])
@login_required
def corps(user, query=""):
    return jsonify(
        [c for c in db.get_companies_names_like(
            query,
            request.args.get('limit', 0),
            request.args.get('skip', 0),
        )]
    )


@api.route('/corps/esgscore/<tci>', methods=['GET'])
@login_required
def esgs(user, tci):
    return jsonify(
        db.get_company_by_ric(tci)
    )
