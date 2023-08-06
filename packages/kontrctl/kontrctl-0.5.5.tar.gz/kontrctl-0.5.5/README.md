# Kontrctl - Kontr portal CLI client

`kontrctl` - Kontr Portal management CLI Tool


## Setup

There are multiple variants how to install and run the `kontrctl`.


### Install from pypi registry

The best way to install the `kontrctl` is using the `pip`.

```bash
pip install kontrctl
```

### Install from source

For development purposes clone the repository and install dependencies using the pipenv

```bash
git clone https://gitlab.fi.muni.cz/grp-kontr2/kontrctl
pipenv install
```

Update `kontr-api` (optional)

```bash
pipenv update kontr-api
pipenv shell
```

## Run the `kontrctl`

```
kontrctl --help
```

## Development run

Run the development version

```bash
python -m kontrctl.cli --help
```

## First run setup

Before using the `kontrctl` to manage the portal and submit, you need to set remote

```bash
kontrctl remotes add default https://kontr.fi.muni.cz
kontrctl remotes select default
kontrctl login  # Provide username and password
```

### Remotes

Remote sets location and default params for the kontr instance

```bash
kontrctl remotes --help
kontrctl remotes list
kontrctl remotes add <name> <url>
kontrctl remotes rm <name>
kontrctl remotes read <name>
kontrctl remotes select <name>
kontrctl remotes deselect <name> # Not implemented
```

### Auth

Authentication commands

#### Login

```bash
kontrctl login
kontrctl --help
```

#### Logout


```bash
kontrctl logout
kontrctl logout --help
```

### Users

Users resources management

```bash
kontrctl users --help
kontrctl users list
kontrctl users read <name>
kontrctl users delete <name>
```

### Courses:
Courses resources management

```bash
kontrctl courses --help
kontrctl courses list
kontrctl courses read <name>
kontrctl courses delete <name>
kontrctl courses select <name>
kontrctl courses deselect
```

### Components:
Components resources management

```bash
kontrctl components --help
kontrctl components list
kontrctl components read <name>
kontrctl components delete <name>
```

### Projects:
Projects resources management

```bash
kontrctl projects --help
kontrctl projects list
kontrctl projects read <name>
kontrctl projects delete <name>
kontrctl projects select <name>
kontrctl projects deselect

# if selected course not provided:
kontrctl projects list -c <course_name>
```

### Submit
Create new submission

```bash
kontrctl submit --help
kontrctl submit -c <course> -p <project> -t git -u <repo_url> -D <subdir>

# Example:
kontrctl submit -c TestCourse1 -p HW01 -t git -u "https://github.com/pestanko/example-repo" -D <subdir>
```

## Contributing

Take a look at [General Contribution Guide](https://gitlab.fi.muni.cz/grp-kontr2/kontr-documentation/blob/master/contributing/GeneralContributionGuide.adoc).
