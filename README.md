# soliloquy-server

Back-end for the [soliloquy](https://github.com/Shampooing/soliloquy-client) client.

**Warning: at the present day, no authentication is performed on incoming http requests, which makes this server unsuitable for use over any public network. It is currently configured to only listen to requests coming from localhost (you may change this setting at your own risks), as the intended usage is for the server to run alongside the soliloquy client (ie on the same machine). Support for use over the network will (hopefully) come at a later stage.**

Installation
============

python >= 3.6 is required. You can get it [here](https://www.python.org/) or using your preferred package manager.

1. Clone this repo and `cd` into it:

```bash
git clone https://github.com/Shampooing/soliloquy-server .
cd soliloquy-server
```

2. (_optional_) Create and activate a dedicated python virtual environment to store the required packages we are about to install. For example, to create and activate a 'soliloquy' virtual env under a folder 'venv' in the current directory:

```bash
python -m venv venv/soliloquy
source venv/soliloquy/bin/activate
```

3. Install the project's dependencies:

```bash
pip install -r requirements.txt
```

4. (_optional_) It is recommended to replace the django key that comes in this repo with a new one, although as long as the server only listens to requests from localhost, it doesn't really matter. The thorough user may generate a random key using `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` and replace the `SECRET_KEY` under `src/settings.py` with the printed value.


Usage
=====

The following starts the server on port 8000 of the local host:

```bash
python src/manage.py runserver 0.0.0.0:8000
```

You can then check that the server is running by visiting http://127.0.0.1:8000.