import importlib

from fabric.api import task, runs_once
from fabric.task_utils import _Dict
from fabric import state, main as fab_main

from .settings import SETTINGS


local_task = runs_once(task)()


def load_components_tasks() -> None:
    for component in SETTINGS['components']:
        try:
            tasks = importlib.import_module('{}.tasks'.format(component))
            commands = state.commands
            parts = getattr(tasks, 'NAMESPACE', component.split('.')[-1])
            for part in parts.split('.'):
                commands = commands.setdefault(part, _Dict())

            _, new_style, classic, _ = fab_main.load_tasks_from_module(tasks)
            tasks = new_style if state.env.new_style_tasks else classic

            commands.update(tasks)
            del tasks
        except ImportError:
            pass
