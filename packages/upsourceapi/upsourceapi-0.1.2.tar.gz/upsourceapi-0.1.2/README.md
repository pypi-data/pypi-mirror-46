# Upsource API

A Python client library for accessing [Upsource APIs](https://upsource.jetbrains.com/~api_doc/index.html). These client library are not complete and are in developing mode.

### Index

1. [Install](#install)
2. [Usage](#usage)

## Install

You can run Upsource API through Docker:
```bash
docker run -it --rm vanyaland/upsourceapi --help
```
Build by your own:
```bash
docker build -t upsourceapi .
docker run -it --rm upsourceapi --help
```

or install it using the [Python package manager](https://github.com/pypa/pip):

```bash
pip install .
```

## Usage

### Command line usage

In this section we cover in detail each of the commands implemented in upsourceapi.

```bash
upsourceapi --help
```

### Commands

- [Get all projects](#get-all-projects) - returns the list of all short project infos.
- [Create project](#create-a-project) - creates a project.
- [Find projects](#find-projects) - returns the list of projects matching a given search criteria.

#### Get all projects

With this command you can the list of all short project infos.

- `--base-url`: Base URL of the Upsource API.
- `--auth-token`: Upsource authorization token, provide it to see private projects. `optional`

Example:

```bash
upsourceapi get-all-projects \
  --base-url "https://example.com/~rpc" \
  --auth-token "AUTH_TOKEN"
```

#### Create a project

You **must** have configured your SSH previously.

With this command you can create upsource project.

- `--base-url`: Base URL of the Upsource API.
- `--auth-token`: Upsource authorization token. To see private projects.
- `--project-name`: Name for the new Upsource project.
- `--project-url`: The URL to the repo, e.g. ssh://git@example.com/example-repo.git.
- `--ssh-key`: Private SSH key in OpenSSH format.
- `--ssh-key-passphrase`: SSH key passphrase.
- `--sync-token`: Anonymous access to the GitLab/GitHub API is forbidden. Please provide an OAuth 2.0 token (recommended) or a personal access token, which we'll use to read data from GitLab/GitHub. Write requests will be performed on behalf of each individual Upsource user.

Example:

```bash
upsourceapi create-project \
  --auth-token "AUTH_TOKEN" \
  --base-url "https://example.com/~rpc" \
  --project-name "example-project" \
  --project-url "ssh://git@example.com/example-project.git" \
  --ssh-key "$(cat ~/.ssh/id_rsa)" \
  --ssh-key-passphrase "ssh-key-passphrase" \
  --sync-token "OAuth 2.0 token"
```

#### Find projects

With this command you can get the list of projects matching a given search criteria.

- `--base-url`: Base URL of the Upsource API.
- `--auth-token`: Upsource authorization token, provide it to see private projects. `optional`
- `--pattern`: Search query, e.g. part of the name.
- `--limit`: Number of projects to return.

Example:

```bash
docker run -it --rm upsourceapi find-projects \
  --base-url "https://example.com/~rpc" \
  --auth-token "AUTH_TOKEN" \
  --pattern "query" \
  --limit 10
```
