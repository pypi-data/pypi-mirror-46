from argparse import ArgumentParser


class BaseCommand:
    def create_parser(self):
        parser = ArgumentParser()
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        pass

    def run_from_argv(self, argv):
        parser = self.create_parser()
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        self.execute(*args, **cmd_options)

    def execute(self, *args, **kwargs):
        self.handle(*args, **kwargs)

    def handle(self, *args, **kwargs):
        raise NotImplementedError('Method handle must be implementer.')
