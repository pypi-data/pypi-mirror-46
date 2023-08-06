import os
from PyInquirer import prompt

from .answers_to_markdown import answers_to_markdown
from .defaults import get_default_project_name


def generate_readme():
    try:
        os.stat('README.md')
    except FileNotFoundError:
        pass
    else:
        text = input('A README.md file already exists. '
                     'Do you want to overwrite? [Y/n]')
        if text != 'Y':
            return

    questions = [
        {
            'type': 'input',
            'name': 'project_name',
            'message': "What's the name of your project?",
            'default': get_default_project_name(os.getcwd()),
        },
        {
            'type': 'input',
            'name': 'description',
            'message': "What's a brief description of your project?",
            'default': 'TODO',
        },
    ]

    answers = prompt(questions)

    markdown = answers_to_markdown(answers)

    with open('README.md', 'w') as filehandle:
        filehandle.write(f'{markdown}\n')
