import json

from flask import Blueprint, url_for, jsonify, request
from geoalchemy2.functions import ST_AsGeoJSON, ST_Intersects

from gis import app, db
from gis.models import ZipCode

api = Blueprint(__name__, "api", url_prefix="/api")

# @api.errorhandler(Exception)
# def api_error(e):
#     response = jsonify({'error': e.__class__.__name__, 'message': str(e)})
#     response.status_code = 500
#     return response

@api.route("/")
def index():
    return jsonify({
        'locate': url_for(".locate"),
        'which': url_for(".which")
    })


@api.route("/locate")
def locate():
    zips = request.args.getlist("zips[]")
    print(len(zips), zips)
    data = db.session.query(
        ZipCode.zip_code,
        ZipCode.lat,
        ZipCode.lng,
        ST_AsGeoJSON(ZipCode.geometry).label('geo')
    ).filter(
        ZipCode.zip_code.in_(zips)
    ).all()

    return json.dumps({
        'zips': [dict(zip_code=z.zip_code, lat=z.lat, lng=z.lng, geo=json.loads(z.geo)) for z in data]
    })


@api.route("/which")
def which():
    lat, lon = request.args.get('lat', None), request.args.get('lng', None)
    if not lat and lon:
        raise ValueError("lat and lon are required")

    codes = db.session.query(
        ZipCode.zip_code,
        ZipCode.lat,
        ZipCode.lng,
        ST_AsGeoJSON(ZipCode.geometry).label('geo')
    ).filter(
        ST_Intersects(
            db.func.ST_SetSRID(
                db.func.ST_MakePoint(float(lon), float(lat)), 4326
            ),
            ZipCode.geometry
        )
    ).all()

    return json.dumps({
        'zips': [dict(zip_code=z.zip_code, lat=z.lat, lng=z.lng, geo=json.loads(z.geo)) for z in codes]
    })


app.register_blueprint(api)
