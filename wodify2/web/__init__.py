from collections import OrderedDict
import json

from flask import Flask
from flask import request
from flask import render_template

from wodify2.settings import DEBUG
from wodify2.utils import connect_db, dict_factory


app = Flask(__name__)

def get_athlete_by_uuid(uuid):
    """Returns back single athlete
    as 2-tuple (id, name)

    :returns: Athlete
    :rtype: tuple
    """
    db = connect_db()

    sql_query = """
        SELECT id, name
        FROM athlete
        WHERE athlete.id = ?;"""
    cur = db.execute(sql_query, [uuid])

    return cur.fetchall()[0] 


def get_athlete(name):
    """Returns back single athlete
    as 2-tuple (id, name)

    :returns: Athlete
    :rtype: tuple
    """
    db = connect_db()

    sql_query = """
        SELECT id, name
        FROM athlete
        WHERE athlete.name = ?;"""
    cur = db.execute(sql_query, [name])

    return cur.fetchall()[0]

def get_athletes():
    """Returns a list of 2-tuple (id, name)
    athletes.

    :returns: Athlete
    :rtype: tuple
    """
    db = connect_db()

    sql_query = """
        SELECT id, name
        FROM athlete
        ORDER BY athlete.name;"""
    cur = db.execute(sql_query)

    return cur.fetchall()

def search_athletes(text):
    """Returns a list of 2-tuple (id, name)
    athletes.

    :returns: Athlete
    :rtype: dict
    """
    db = connect_db()
    db.row_factory = dict_factory

    sql_query = """
        SELECT id, name
        FROM athlete
        WHERE name LIKE ?
        ORDER BY athlete.name;"""
    cur = db.execute(sql_query, ['%{}%'.format(text)])

    return cur.fetchall()

def get_athlete_data(uuid):
    """Takes UUID and returns athlete
    max weights associated with UUID.

    :returns: List of data points
    :rtype: dict
    """
    db = connect_db()
    # db.row_factory = dict_factory

    sql_query = """
        SELECT weight.name, MAX(record.max_weight) as max_weight
        FROM weight, record  
        WHERE weight.id = record.weight_id AND 
        record.athlete_id = ? 
        GROUP BY record.weight_id
        ORDER BY weight.name;"""
    cur = db.execute(sql_query, [uuid])

    return cur.fetchall()

def get_max_weights(athlete):
    """Return back a list of 2-tuple
    (weight_name, weight_amount)

    :returns: list of max weights
    :rtype: list
    """
    db = connect_db()

    sql_query = """
        SELECT weight.name, MAX(record.max_weight) 
        FROM weight, record  
        WHERE weight.id = record.weight_id AND 
        record.athlete_id = ? 
        GROUP BY record.weight_id
        ORDER BY weight.name;"""
    cur = db.execute(sql_query, [athlete[0]])

    return cur.fetchall()


@app.route("/")
def homepage():
    athletes = get_athletes()

    charts = []
    for athlete in athletes:

        max_weights = get_max_weights(athlete)

        max_weight_names = []
        max_weight_values = []
        for name, value in max_weights:

            if 'misfit' in name.lower():
                continue

            if 'metcon' in name.lower():
                continue

            try:
                max_weight_names.append('{}'.format(name))
                max_weight_values.append('{}'.format(value))
            except UnicodeEncodeError:
                continue  # on to the next one

        charts.append({
            'athlete_id': athlete[0],
            'athlete_name': athlete[1],
            'max_weight_names': max_weight_names,
            'max_weight_values': max_weight_values})

    return render_template('index.html', charts=charts)


@app.route('/v1/athlete/<text>/')
def athlete(text):
    results = search_athletes(text)
    return unicode(results)

@app.route('/v1/athlete/data/')
def athlete_data():

    uuids = request.args.get('uuids').split(',')

    results = []
    for uuid in uuids:
        data = get_athlete_data(uuid)

        results.append({
            'name': get_athlete_by_uuid(uuid)[1],
            'weight_names': [d[0] for d in data],
            'weights': [d[1] for d in data]
        })

    all_names = []
    for data in results:
        for name in data['weight_names']:
            all_names.append(name)

    all_names = sorted(set(all_names))

    for weight_idx, weight_name in enumerate(all_names):
        for result_idx, data in enumerate(results):

            # If the athlete does not have the weight
            # Then append it in the appropriate spot
            if weight_name not in data['weight_names']:
                results[result_idx]['weights'].insert(weight_idx, 0)

    series = []
    for result in results:
        series.append({
            'name': result['name'],
            'data': result['weights']
            })

    return json.dumps({
        'categories': all_names,
        'series': series
    })

@app.route("/compare/")
def compare():
    athletes = get_athletes()
    return render_template('compare.html', athletes=athletes)

@app.route("/vs/<name1>/<name2>/")
def vs(name1, name2):
    a1 = {'name': 'Will Holtkamp'}
    a2 = {'name': 'Justin Fleming'}

    a1['weights'] = dict(get_max_weights(get_athlete(a1['name'])))
    a2['weights'] = dict(get_max_weights(get_athlete(a2['name'])))

    list_of_keys_to_pop = []
    for key in a1['weights'].iterkeys():
        try:
            str(key)
        except UnicodeEncodeError:
            list_of_keys_to_pop.append(key)

    for key in a2['weights'].iterkeys():
        try:
            str(key)
        except UnicodeEncodeError:
            list_of_keys_to_pop.append(key)

    for key in list_of_keys_to_pop:
        a1['weights'].pop(key, None)
        a2['weights'].pop(key, None)


    a1['weights'] = dict([(str(k), v) for k, v in a1['weights'].iteritems()])
    a2['weights'] = dict([(str(k), v) for k, v in a2['weights'].iteritems()])

    for weight_name in a1['weights'].iterkeys():
        if weight_name not in a2['weights'].keys():
            a2['weights'][weight_name] = 0

    for weight_name in a2['weights'].iterkeys():
        if weight_name not in a1['weights'].keys():
            a1['weights'][weight_name] = 0

    print 'a1', a1['weights']
    print 'a2', a2['weights']

    a1['weights'] = OrderedDict(sorted(a1['weights'].items()))
    a2['weights'] = OrderedDict(sorted(a2['weights'].items()))


    return render_template(
        'vs.html',
        athlete1=a1,
        athlete2=a2)


if __name__ == "__main__":
    app.run(debug=DEBUG)
