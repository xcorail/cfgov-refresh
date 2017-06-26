from __future__ import absolute_import, unicode_literals

import json
import os
import sqlite3

from math import acos, cos, radians, sin
from six import print_


def distance_in_miles(lat1_radians, lng1_radians, lat2_radians, lng2_radians):
    """Estimate distance in miles between two points in radians.

    Uses simplified algorithm to determine proximity based on latitude and
    longitude, described at https://stackoverflow.com/q/1916953.
    """
    earth_radius_in_miles = 3959

    return earth_radius_in_miles * acos(
        cos(lat1_radians) *
        cos(lat2_radians) *
        cos(lng2_radians - lng1_radians) +
        sin(lat1_radians) *
        sin(lat2_radians)
    )


def get_db_connection():
    connection = sqlite3.connect(':memory:')
    connection.create_function('distance_in_miles', 4, distance_in_miles)

    return connection


def fill_db(connection, counselors):
    def prepare_counselors(counselors):
        for counselor in counselors:
            yield (
                radians(float(counselor['agc_ADDR_LATITUDE'])),
                radians(float(counselor['agc_ADDR_LONGITUDE'])),
                json.dumps(counselor)
            )

    create_sql = """
CREATE TABLE counselors (
    latitude_radians REAL,
    longitude_radians REAL,
    json TEXT
)
"""

    insert_sql = """
INSERT INTO
    counselors(latitude_radians, longitude_radians, json)
VALUES (?, ?, ?)
"""

    connection.execute(create_sql)
    connection.executemany(insert_sql, prepare_counselors(counselors))


def query_db(connection, latitude_radians, longitude_radians):
    sql = """
SELECT
    json,
    distance_in_miles(latitude_radians, longitude_radians, ?, ?) AS distance
FROM
    counselors
ORDER BY distance ASC
LIMIT 10
    """

    response = connection.execute(sql, (latitude_radians, longitude_radians))

    results = []
    for row in response:
        result = json.loads(row[0])
        result['distance'] = row[1]
        results.append(result)

    return results


def generate_counselor_json(counselors, zipcodes, target):
    connection = get_db_connection()
    fill_db(connection, counselors)

    print_('generating JSON into', target, flush=True)

    for zipcode, (latitude_degrees, longitude_degrees) in zipcodes.items():
        counselors = query_db(
            connection,
            radians(latitude_degrees),
            radians(longitude_degrees)
        )

        zipcode_data = {
            'zip': {
                'zipcode': zipcode,
                'lat': latitude_degrees,
                'lng': longitude_degrees,
            },
            'counseling_agencies': counselors,
        }

        json_filename = os.path.join(target, '{}.json'.format(zipcode))

        with open(json_filename, 'w') as f:
            f.write(json.dumps(zipcode_data))