from .doc import DocAst
from .bash import helpers, tree, minimize


class Parser(object):

  def __init__(self, script, params):
    self.script = script
    self.settings = ParserSettings(script, params)
    self.doc_ast = DocAst(self.settings, script.doc.value)

  @property
  def patched_script(self):
    return self.script.insert_parser(str(self), self.settings.refresh_command)

  def __str__(self):
    nodes = [node for node in self.doc_ast.nodes if node is not self.doc_ast.root_node]
    ast_helper_names = set([n.helper_name for n in nodes])
    ast_helper_fns = list(filter(lambda h: h.name in ast_helper_names, [
      tree.Command(self.settings),
      tree.Either(self.settings),
      tree.OneOrMore(self.settings),
      tree.Optional(self.settings),
      tree.Required(self.settings),
      tree.Switch(self.settings),
      tree.Value(self.settings),
    ]))
    helper_fns = [
      helpers.ParseShorts(self.settings),
      helpers.ParseLong(self.settings),
      helpers.Error(self.settings, usage_section=self.doc_ast.usage_section),
      helpers.Main(self.settings, root_node=self.doc_ast.root_node, leaf_nodes=self.doc_ast.leaf_nodes),
    ]
    if len(self.doc_ast.leaf_nodes) > 0:
      helper_fns.append(helpers.Defaults(self.settings, leaf_nodes=self.doc_ast.leaf_nodes))
    parser_str = '\n'.join(map(str, nodes + ast_helper_fns + helper_fns))
    if self.settings.minimize:
      parser_str = minimize(parser_str, self.settings.max_line_length)
    return parser_str + '\n'


class ParserSettings(object):

  def __init__(self, script, docopt_params):
    self.script = script
    self.docopt_params = docopt_params

  @property
  def name_prefix(self):
    return self.docopt_params['--prefix']

  @property
  def add_doc_check(self):
    return not self.docopt_params['--no-doc-check']

  @property
  def options_first(self):
    return self.docopt_params['--options-first']

  @property
  def add_help(self):
    return not self.docopt_params['--no-help']

  @property
  def add_version(self):
    if self.docopt_params['--no-version']:
      return False
    return self.script.version.present

  @property
  def add_teardown(self):
    return not self.docopt_params['--no-teardown']

  @property
  def minimize(self):
    return not self.docopt_params['--no-minimize']

  @property
  def max_line_length(self):
    return int(self.docopt_params['--line-length'])

  @property
  def refresh_command(self):
    command = 'docopt.sh'
    if self.docopt_params['--debug']:
      command += ' --debug'
    if self.docopt_params['--prefix'] != '':
      command += ' --prefix=' + self.docopt_params['--prefix']
    if self.docopt_params['SCRIPT'] is not None:
      command += ' ' + self.docopt_params['SCRIPT']
    return command
