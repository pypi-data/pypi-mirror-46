# hush-push

## Installation

`pip install --user hush-push`

## Usage
```
usage: hush [-h] [--version] [--execute] [--overwrite] [--verbose]
            [--remote-endpoint REMOTE_ENDPOINT]

Hello world

optional arguments:
  -h, --help            show this help message and exit
  --version             show the current version
  --execute, -e         create the specified configuration parameters
  --overwrite, -o       force put the configuration parameters even if they
                        already exist
  --verbose, -v         enable verbose logging
  --remote-endpoint REMOTE_ENDPOINT, -r REMOTE_ENDPOINT
                        specify remote endpoint
```

## Pre-requisites
You need to specify which configuration file to use by setting the environment variable `AWS_CONFIG_FILE` to the absolute path of your configuration file.

## Directory structure

The directory structure need to be organized in folders at the root of your project. The first folder name should be equal to the profile name specified in the configuration file to use for the call. If your config looks like this:
```ini
[profile accProfile]
role_arn = arn:aws:iam::000000000000:role/ROLE
region = eu-west-1
source_profile = default
```
You must put your configuration parameters in the following structure under the directory `secrets/`:
```
<project-root>:
  secrets/
    accProfile/
      parameterName
```

If the `parameterName` is a folder structure, the configuration parameter name will be a concatenated version of those. If the folder structure looks like this:
```
<project-root>:
  secrets/
    accProfile/
      eu-west-1/
        staging/
          remoteEndpoint
```
the parameter name will look like this: `/eu-west-1/staging/remoteEndpoint` with the value of the parameter set to the content of the file `remoteEndpoint`

## Development

To build the dist: `python3 setup.py sdist bdist_wheel` and answer "no" to the question if it's a production release. To upload the created dist run `python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*` and sign in with your username and password.