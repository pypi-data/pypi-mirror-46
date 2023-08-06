# Easy Readme
> Always looking up markdown syntax when you start a new project?  Get a good looking barebones README.md in seconds with one command.
## Installing package
```sh
python easy_readme/setup.py install
```
## Start a new project and use
```sh
mkdir new-project
cd new-project
easy-readme
```
Answer a few quick questions
```sh
? What's the name of your project?  Gitcoin
? What's a brief description of your project?  Blockchain and version control, what's not to love?
```
You've got yourself a beautiful start for a README.md

    cat README.md
    # Gitcoin
    > Blockchain and version control, what's not to love?
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
    ```

Create a git repo and start working on the important stuff!
```
git init
git add .
git commit -m "Add readme; initial commit"
```
## Development Setup
```sh
docker-compose run app bash
```
## Running Tests
```sh
docker-compose run app bash
python -m unittest discover
```
