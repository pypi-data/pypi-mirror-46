from reindeer.converdeer import json2csv, csv2ttl
from subprocess import Popen, PIPE, STDOUT
from rdflib import Graph

deer_jar_file_path = './deer-cli/deer-cli-2.0.1.jar'


def enriche(input_files: list, output_file, operator: str):
    """
    Enriches a given csv-dataset with information from linked data.
    :param input_files: a list with one or more input-files in csv format. The first column will be interpreted as the
    subjects. The first row is interpreted as predicates, while all the other cells are interpreted as objects.
    :param output_file: a path where the output csv should be stored.
    :param operator: A string that determines which script is executed.
    """
    all_csv2ttl(input_files)
    run_deer(operator)
    deer2csv(output_file)


def all_csv2ttl(input_files: list):
    for i in range(len(input_files)):
        csv2ttl(input_files[i], './temp/in' + str(i) + '.ttl')


def run_deer(script):
    script_file = operators[script]
    p = Popen(['java', '-jar', deer_jar_file_path, script_file], stdout=PIPE, stderr=STDOUT)
    for line in p.stdout:
        print(line)


def deer2csv(output_file):
    g = Graph()
    g.parse('./temp/out.ttl', format='n3')
    g.serialize(destination='./temp/out.json', format='json-ld', indent=4)
    json2csv('./temp/out.json', output_file)


operators = {
    'merge': './deer_scripts/deer_merge_script.ttl',
    'ner_merge': './deer_scripts/deer_ner_merge_script.ttl',
    'filter': './deer_scripts//deer_filter_script.ttl'
}
