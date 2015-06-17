from geoalchemy2 import Geometry

from gis import db


class ZipCode(db.Model):
    id = db.Column('gid', db.Integer(), primary_key=True)
    zip_code = db.Column('zcta5ce10', db.String(5))
    geoid10 = db.Column('geoid10', db.String(5))
    fips_class = db.Column('classfp10', db.String(2))  # B5 - 2010 Census FIPS class code
    mtfcc10 = db.Column('mtfcc10', db.String(5))  # G6350 - MAF/TIGER feature class code (G5040)
    funcstat10 = db.Column('funcstat10', db.String(1))  # S - 2010 Census functional status
    aland10 = db.Column('aland10', db.Integer())  # 63411475
    awater10 = db.Column('awater10', db.Integer())  # 157689
    lat = db.Column('intptlat10', db.String())  # +41.3183010
    lng = db.Column('intptlon10', db.String())  # -083.6174935
    geometry = db.Column('geom', Geometry("MULTIPOLYGON"))


__all__ = ['ZipCode']
