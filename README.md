# CodeTri-Webhook

> A small webhook responder

## Background

For years, I have roughly followed the [Git Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
for my projects and have even used it at work. I find it to be simple and logical. Because of this workflow, I have long wished to
make use of [GitHub Webhooks](https://developer.github.com/webhooks/) to automatically deploy projects, particularly web apps.
However, I didn't want to set it up individually in each application, and I didn't want to go through the trouble of setting up a third-party CI,
such as [Travis CI](https://travis-ci.org/), to securely interact with my server. That's when I had an idea, birthing this project.

Basically, what lives here is a webhook responder, AKA a cross between a CI task runner and microservice. After configuring it for your project
and setting up the webhook, you can basically run any commands you want once the webhook is fired, including deploying code and rebooting your app.

## Operation

The app operates on on two pieces: Services and Hooks. Services are Python [dataclasses](https://docs.python.org/3/library/dataclasses.html)
that know how to interact with the website they are written for and perform the user-defined commands. Hooks are like configuration files.
They specify a Service to use and provide the information needed to properly repsond to the fired webhook. On application start, the created Hooks
are enumerated over and an endpoint for each Hook is created. So if your app is running on `http://127.0.0.1:5000` and you have a Hook named `sample.json`, a `POST`-only endpoint will be created
at `http://127.0.0.1:5000/sample`. You then set that url in the appropriate website's webhook configuration.

Because of this architecture, a Service can be written for practically any website, and there can be any number of Hooks defined that use a single Service,
but with Hook having their own tasks. For more details and a working example, a sample Service and Hook are available.

## Required Secrets

- Flask secret key (`SECRET_KEY`)

## Development

1. Install Python 3.10+ [Poetry](https://python-poetry.org/) 1.1.0+, and VS Code
1. Create required secret keys (default: `./secrets` or environment)
1. Run `poetry install`
1. Launch the service using the provided VS Code launch configuration

## Deploy

1. Ensure Python 3.10+ and `pip` are installed on the server
1. Ensure running the `python` command executes Python 3.10,
   installing [python-is-python3](https://packages.ubuntu.com/jammy/python-is-python3) if necessary
1. Ensure the [`virtualenv`](https://pypi.org/project/virtualenv/) Python package is installed
1. Run `. ./install.sh` to create the app virtualenv and install the app.

6. Run `chmod u+x ./run-supervisord.sh && chmod u+x ./run-app.sh`
7. Run `./run-supervisord.sh` to start the service


## License

2019, 2021-2022 Caleb

[MIT](LICENSE)
