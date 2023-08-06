import json
import csv
import numpy as np
from rdflib import Graph, URIRef, Literal


def csv2ttl(input_path, output_path):
    graph = Graph()
    with open(input_path, 'r') as f:
        csv_data = np.array([row for row in csv.reader(f, delimiter=',')])
        csv_topic = csv_data[0, 0].replace(' ', '_') + '/'
        csv_predicats = csv_data[0, 1:]
        csv_subjects = csv_data[1:, 0]
        csv_objects = csv_data[1:, 1:]
        for row in range(len(csv_subjects)):
            if 'http:' in csv_subjects[row]:
                rdf_subject = URIRef(csv_subjects[row])
            else:
                if 'http:' in csv_topic:
                    rdf_subject = URIRef(csv_topic + csv_subjects[row].replace(' ', '_'))
                else:
                    rdf_subject = URIRef('http://row.org/' + csv_topic + csv_subjects[row].replace(' ', '_'))
            for column in range(len(csv_predicats)):
                if csv_objects[row, column].lower() not in ['none', 'null', 'na']:
                    if 'http:' in csv_objects[row, column]:
                        rdf_object = URIRef(csv_objects[row, column])
                    else:
                        rdf_object = Literal(csv_objects[row, column])
                    if 'http:' in csv_predicats[column]:
                        rdf_predicate = URIRef(csv_predicats[column])
                    else:
                        if 'http:' in csv_topic:
                            rdf_predicate = URIRef(csv_topic + csv_predicats[column].replace(' ', '_'))
                        else:
                            rdf_predicate = URIRef('http://column.org/' + csv_topic + csv_predicats[column].replace(' ', '_'))
                    graph.add((rdf_subject, rdf_predicate, rdf_object))
    graph.serialize(output_path, format='turtle')


def json2csv(input_path, output_path):
    json_data = load_json(input_path)
    columns = extract_columns(json_data)
    save_as_csv(json_data, columns, output_path)


# Helper Functions
def load_json(path):
    with open(path, 'r') as f:
        json_file = f.read()
        return json.loads(json_file)


def extract_columns(json_data):
    columns = set()
    for json_obj in json_data:
        for key in json_obj.keys():
            columns.add(key)
    return list(columns)


def save_as_csv(json_data, columns, output_path):
    with open(output_path, 'w', newline='') as out_file:
        csv_w = csv.writer(out_file)
        csv_w.writerow(columns)

        for json_obj in json_data:
            row = ['NULL' for column in columns]
            for key in json_obj.keys():
                i = columns.index(key)
                if key == '@id':
                    row[i] = json_obj[key]
                else:
                    if '@value' in json_obj[key][0].keys():
                        row[i] = json_obj[key][0]['@value']
                    else:
                        row[i] = json_obj[key][0]['@id']
            csv_w.writerow(row)
