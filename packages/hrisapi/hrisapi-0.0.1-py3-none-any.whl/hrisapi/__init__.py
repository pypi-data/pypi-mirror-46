from basescript import BaseScript
from tornadoql.tornadoql import TornadoQL

from . import schema

class HRISAPIScript(BaseScript):
    DESC = 'Human Resource Information Systems API'

    def run(self):
        pass

    def cmd_schema(self):
        _schema = schema.make_schema()
        print(_schema)

    def cmd_runserver(self):
        _schema = schema.make_schema()
        TornadoQL.start(_schema)

    def define_args(self, parser):
        pass

    def define_subcommands(self, subcommands):
        super().define_subcommands(subcommands)

        schema_cmd = subcommands.add_parser('schema',
            help='Show the Schema')
        schema_cmd.set_defaults(func=self.cmd_schema)

        runserver_cmd = subcommands.add_parser('runserver',
            help='Run server')
        runserver_cmd.add_argument('--port', type=int, default=8888)
        runserver_cmd.set_defaults(func=self.cmd_runserver)

def main():
    HRISAPIScript().start()

if __name__ == '__main__':
    main()
