from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from mkdocs.config import load_config
from mkdocs.commands.build import build
from apps import about
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        mkdocs_path = os.path.dirname(about.__file__)
        filename = os.path.join(mkdocs_path, 'mkdocs.yml')
        self.generate_config(mkdocs_path, filename)
        self.build(filename)

    def build(self, config_filename):
        mkdocs_config = load_config(config_file=config_filename)
        build(mkdocs_config)

    def generate_config(self, mkdocs_path, filename):
        rendered = render_to_string('mkdocs.yml', {
            'mkdocs_dir': mkdocs_path,
        })

        with open(filename, 'w'):
            # Clean file
            pass

        with open(filename, 'w') as config_file:
            config_file.write(rendered)
