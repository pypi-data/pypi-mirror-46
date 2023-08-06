def answers_to_markdown(answers):
    project_name = answers['project_name']
    description = answers['description']
    todo_placeholders = '''
## Development Setup
```sh
#TODO
```
## Running Tests
```sh
#TODO
```
## Deployment
```sh
#TODO
```'''
    return f'# {project_name}\n> {description}{todo_placeholders}'
