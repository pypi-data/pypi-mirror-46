# Gitlabracadabra

🧹 GitLabracadabra 🧙

:alembic: Adds some magic to GitLab :crystal\_ball:

GitLab'racadabra is a way to configure a [GitLab](https://gitlab.com/) instance
from a YAML configuration, using the [API](https://docs.gitlab.com/ce/api/README.html).

It is able to create GitLab's groups, projects and users (more is coming...)

It is based on [Python GitLab](https://github.com/python-gitlab/python-gitlab).

## Installation

### Using pip

```
pip install gitlabracadabra
```

### Using docker image

There are also [Docker/OCI images](https://gitlab.com/gitlabracadabra/gitlabracadabra/container_registry).

Example usage:
```shell
sudo docker run -ti \
  -v "$HOME/.python-gitlab.cfg:/home/gitlabracadabra/.python-gitlab.cfg:ro" \
  -v "$PWD/gitlabracadabra.yml:/tmp/app/gitlabracadabra.yml:ro" \
  registry.gitlab.com/gitlabracadabra/gitlabracadabra:0.1.0 \
  --verbose --dry-run
```

### From source

Local installation (in `$HOME/.local`):
```shell
# On Debian >= 10 (buster) or Ubuntu >= 19.04
sudo apt install python3-jsonschema python3-gitlab python3-yaml python3-coverage python3-vcr
# On others
pip install -r requirements.txt

# Build, install and test
python3 setup.py build
python3 setup.py install --user
# python3 setup.py test
~/.local/bin/gitlabracadabra --verbose --dry-run
```

## Configuration

GitLabracadabra uses the same configuration file as Python GitLab CLI to store
connection parameters.

Example `~/.python-gitlab.cfg`:
```ini
[global]
default = gitlab

[gitlab]
url = https://gitlab.com
private_token = T0K3N
```

More information in [Python GitLab documentation](https://python-gitlab.readthedocs.io/en/stable/cli.html#configuration).

## Action file(s)

GitLabracadabra *actions* are configured with a YAML file.

See [GitLabracadabra's own action file](https://gitlab.com/gitlabracadabra/gitlabracadabra/blob/master/gitlabracadabra.yml).
