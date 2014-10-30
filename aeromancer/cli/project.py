import logging
import os

from aeromancer.db.models import *
from aeromancer import project

from cliff.command import Command
from cliff.lister import Lister


class Add(Command):
    "(Re)register a project to be scanned"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Add, self).get_parser(prog_name)
        parser.add_argument(
            'project',
            nargs='+',
            default=[],
            help=('project directory names under the project root, '
                  'for example: "stackforge/aeromancer"'),
        )
        return parser

    def take_action(self, parsed_args):
        session = self.app.get_db_session()
        for project_name in parsed_args.project:
            project_path = os.path.join(self.app.options.repo_root, project_name)
            proj_obj = project.add_or_update(session, project_name, project_path)
        session.commit()


class List(Lister):
    """Show the registered projects"""

    def take_action(self, parsed_args):
        session = self.app.get_db_session()
        query = session.query(Project).order_by(Project.name)
        return (('Name', 'Path'),
                ((p.name, p.path) for p in query.all()))


class Remove(Command):
    "Remove a project from the database"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Remove, self).get_parser(prog_name)
        parser.add_argument(
            'project',
            nargs='+',
            default=[],
            help=('project directory names under the project root, '
                  'for example: "stackforge/aeromancer"'),
        )
        return parser

    def take_action(self, parsed_args):
        session = self.app.get_db_session()
        for project_name in parsed_args.project:
            project.remove(session, project_name)
        session.commit()
