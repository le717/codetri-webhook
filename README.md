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

The app operates on two pieces: Services and Hooks. Services are Python classes that know how to interact with the website
they are written for and perform the user-defined commands. Hooks are configuration files. They specify a Service to use
and provide the information needed to properly respond to the fired webhook. On application start, the created Hooks
are enumerated over and an endpoint for each Hook is created.

So, if your app is running at `http://127.0.0.1:5000` and you have a Hook named `sample.json`, a `POST`-only endpoint will be created
at `http://127.0.0.1:5000/sample`. You then set that url in the appropriate website's webhook configuration.

Because of this architecture, a Service can be written for practically any website,
and there can be any number of Hooks defined that use a single Service, but with Hook having their own tasks.

## Creating a service/hook

For working examples, sample Services and Hooks are available in the `samples/` directory.

1. TODO: Write this section

## Required Secrets

- Flask secret key (`SECRET_KEY`)
- HTTP bind port (`BIND_PORT`)

## Development

1. Install Python 3.11+ and [Poetry](https://python-poetry.org/) 1.2.0+
1. If you want to use a pre-configured debug launch, also install VS Code
1. Launch the service using the provided VS Code launch configuration
1. Create required secret keys in `./secrets`
1. Run `poetry install`

## Deploy

1. Ensure Python 3.10+ and `pip` are installed on the server
1. Ensure running the `python` command executes Python 3.10,
   installing [python-is-python3](https://packages.ubuntu.com/jammy/python-is-python3) if necessary
1. Ensure the [`virtualenv`](https://pypi.org/project/virtualenv/) Python package is installed
1. Ensure a reverse proxy through Apache, nginx, Caddy, or the like is set up
1. Create required secret keys in `./secrets`
1. Run `. ./install.sh` to create the app virtualenv and install the app
1. Run `./start.sh` to start the service
    - The app will bind on `http://127.0.0.1:6000`
    - To change the port, change the the HTTP bind port secret value

## License

2019, 2021-2024 Caleb

[MIT](LICENSE)
