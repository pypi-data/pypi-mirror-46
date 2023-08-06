from subprocess import Popen, PIPE, STDOUT
import pkg_resources


class ReindeerComponent:
    def __init__(self, name, deer_type):
        self.name = name
        self.deer_type = deer_type
        self.input_nodes = list()
        self.output_nodes = list()

    def connect_with_successor(self, output_node):
        self.set_output_node(output_node)
        output_node.set_input_node(self)

    def connect_with_predecessor(self, input_node):
        self.set_input_node(input_node)
        input_node.set_output_node(self)

    def set_output_node(self, output_node):
        self.output_nodes.append(output_node)

    def set_input_node(self, input_node):
        self.input_nodes.append(input_node)

    def get_input_nodes(self):
        return ''.join(' :' + node.name for node in self.input_nodes)

    def get_output_nodes(self):
        return ''.join(' :' + node.name for node in self.output_nodes)

    def get_string_head(self):
        head = ':{0} \n' \
               '\t a \t deer:{1}'.format(self.name, self.deer_type)
        if self.input_nodes:
            head += ' ;\n \t fcage:hasInput \t ({0})'.format(self.get_input_nodes())
        return head

    def get_string_footer(self):
        footer = ''
        if self.output_nodes:
            footer += ' ;\n \t fcage:hasOutput \t ({0}) .\n'.format(self.get_output_nodes())
        return footer


def connect_nodes(predecessors, successors):
    predecessors.connect_with_successor(successors)


class FileModelReader(ReindeerComponent):
    def __init__(self, name, path):
        super().__init__(name, 'FileModelReader')
        self.path = path

    def __str__(self):
        if len(self.input_nodes) is 0 and len(self.output_nodes) is 1:
            return self.get_string_head() + ' ;\n  \t deer:fromPath \t "{0}"'.format(
                self.path) + self.get_string_footer()
        else:
            pass


class WebModelReader(ReindeerComponent):
    def __init__(self, name, uri):
        super().__init__(name, 'FileModelReader')
        self.uri = uri

    def __str__(self):
        if len(self.input_nodes) is 0 and len(self.output_nodes) is 1:
            return self.get_string_head() + ' ;\n  \t deer:fromUri \t "{0}"'.format(self.uri) + self.get_string_footer()
        else:
            pass


def create_model_reader(name: str, path: str = None, uri: str = None) -> ReindeerComponent:
    if path and not uri:
        return FileModelReader(name, path)
    elif uri and not path:
        return WebModelReader(name, uri)


class MergeOperator(ReindeerComponent):
    def __init__(self, name):
        super().__init__(name, 'MergeEnrichmentOperator')

    def __str__(self):
        if len(self.input_nodes) is 2 and len(self.output_nodes) is 1:
            return self.get_string_head() + self.get_string_footer()
        else:
            pass


def create_merge_operator(name: str, predecessor_1: ReindeerComponent,
                          predecessor_2: ReindeerComponent) -> MergeOperator:
    operator = MergeOperator(name)
    operator.connect_with_predecessor(predecessor_1)
    operator.connect_with_predecessor(predecessor_2)
    return operator


class CloneOperator(ReindeerComponent):
    def __init__(self, name):
        super().__init__(name, 'CloneEnrichmentOperator')

    def __str__(self):
        if len(self.input_nodes) is 1 and len(self.output_nodes) > 1:
            return self.get_string_head() + self.get_string_footer()
        else:
            pass


def create_clone_operator(name: str, predecessor: ReindeerComponent) -> CloneOperator:
    operator = CloneOperator(name)
    operator.connect_with_predecessor(predecessor)
    return operator


class FilterOperator(ReindeerComponent):
    def __init__(self, name, selector):
        super().__init__(name, 'FilterEnrichmentOperator')
        self.selector = selector

    @staticmethod
    def get_selector_script(selector):
        selector_script = ";\n\t deer:selector"
        i = 0
        for pred, obj in selector:
            if i is 0:
                selector_script += "\t\t [ deer:{0} {1} ]".format(pred, obj)
                i += 1
            else:
                selector_script += "\n\t\t\t[ deer:{0} {1} ]".format(pred, obj)
                i += 1
            if i is len(selector):
                pass
            else:
                selector_script += " ,"
        return selector_script

    def __str__(self):
        if len(self.input_nodes) is 1 and len(self.output_nodes) is 1:
            return self.get_string_head() + self.get_selector_script(self.selector) + self.get_string_footer()
        else:
            pass


def create_filter_operator(name: str, selectors, predecessor: ReindeerComponent) -> FilterOperator:
    operator = FilterOperator(name, selectors)
    operator.connect_with_predecessor(predecessor)
    return operator


class FileModelWriter(ReindeerComponent):
    def __init__(self, name, output_path, output_format):
        super().__init__(name, 'FileModelWriter')
        self.output_path = output_path
        self.output_format = output_format

    def __str__(self):
        if len(self.input_nodes) is 1 and len(self.output_nodes) is 0:
            return self.get_string_head() + ' ;\n \t deer:outputFile \t "{0}" ;\n' \
                                            '\t deer:outputFormat \t "{1}" .'.format(self.output_path,
                                                                                     self.output_format)
        else:
            pass


def create_model_writer(name: str, output_path: str, output_format: str,
                        predecessor: ReindeerComponent) -> FileModelWriter:
    operator = FileModelWriter(name, output_path, output_format)
    operator.connect_with_predecessor(predecessor)
    return operator


def generate_script(last_node, path):
    in_script = set()

    def get_predecessors(node):
        if node.input_nodes is None:
            if node not in in_script:
                in_script.add(node)
                return '\n\n' + str(node)
            else:
                return None
        else:
            helper = ''
            for predecessor in node.input_nodes:
                helper += get_predecessors(predecessor)
            if node not in in_script:
                in_script.add(node)
                return helper + '\n\n' + str(node)
            else:
                return helper

    prefix_str = '@base <http://example.org/random> .\n\
@prefix : <urn:example:demo/> .\n\
@prefix fcage: <http://w3id.org/fcage/> .\n\
@prefix deer: <http://w3id.org/deer/> .\n\
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . \n\
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .'
    deer_str = get_predecessors(last_node)
    script_str = prefix_str + deer_str
    with open(path, "w") as s:
        s.write(script_str)


def run_deer_script(path):
    resource_package = __name__
    resource_path = '/'.join(('deer-cli', 'deer-cli-2.0.1.jar'))
    deer_jar_file_path = pkg_resources.resource_stream(resource_package, resource_path)
    # deer_jar_file_path = './reindeer/deer-cli/deer-cli-2.0.1.jar'
    p = Popen(['java', '-jar', deer_jar_file_path.name, path], stdout=PIPE, stderr=STDOUT)
    for line in p.stdout:
        print(line)


class DeerFlow:
    @staticmethod
    def reader(name: str, path: str = None, uri: str = None) -> ReindeerComponent:
        return create_model_reader(name, path=path, uri=uri)

    @staticmethod
    def merge(name: str, predecessor_1: ReindeerComponent, predecessor_2: ReindeerComponent) -> MergeOperator:
        return create_merge_operator(name, predecessor_1, predecessor_2)

    @staticmethod
    def clone(name: str, predecessor: ReindeerComponent) -> CloneOperator:
        return create_clone_operator(name, predecessor)

    @staticmethod
    def filter(name: str, selectors, predecessor: ReindeerComponent) -> FilterOperator:
        return create_filter_operator(name, selectors, predecessor)

    @staticmethod
    def writer(name: str, output_path: str, output_format: str, predecessor: ReindeerComponent) -> FileModelWriter:
        return create_model_writer(name, output_path, output_format, predecessor)

    @staticmethod
    def play(last_node, path="./temp/script.ttl"):
        generate_script(last_node, path)
        run_deer_script(path)
