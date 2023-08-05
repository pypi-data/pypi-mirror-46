# MergeTB Python Client

This repo contains

## Python3 client library for merge

This can be used for building Python based tools that interact with Merge, or for talking to Merge through Python in a Jupyter notebook. There are some special routines that are Jupyter aware that make working a Jupyter environment nicer.

## CLI application

The CLI application is named `mergetb` and is installed from `mergetb/mergetb_cli.py` into the $PATH during installation.

called merge.py. To use, you need to first login to the authentication server and get a client token. This token will be stashed in a local file and referenced in subseqeuent calls to the API. 

Usage:
```
usage: mergetb [-h] [-l LOGIN] [-p PASSWORD] [-P TOKEN_PATH] [-a API] [-u URL]
               [-L {none,all,debug,info,warning,error,critical}]
               subject verb ...

Command line interface to the mergetb API. To login, run with -l user@address. This
will create and store a temporary authorization token in the given token-path.

Run with optional and then "[subject verb] ...". To see help for an individual
commands run: "[subject] help" "[subject verb] help" Valid commands are:

api get path
experiments delete pid eid
experiments history pid eid
experiments info pid eid
experiments list pid
experiments new pid eid desc
experiments push pid eid path
experiments realize pid eid name hsh
materialization delete pid eid rid name
materialization info pid eid rid name
materialization list pid eid rid
projects delete pid
projects info pid
projects list
projects new pid desc
realization accept pid eid name
realization delete pid eid name
realization info pid eid name
realization list pid eid
realization materialize pid eid rid name
realization reject pid eid name
sites delete name
sites list
sites new name fqdn model
system status
users list

positional arguments:
  subject               The thing to view or modify.
  verb                  The action to apply to the subject.
  args                  variable number of possibly optional arguments.

optional arguments:
  -h, --help            show this help message and exit
  -l LOGIN, --login LOGIN
                        Login the given username by getting and stashing a client side token for that user.
  -p PASSWORD, --password PASSWORD
                        Use the password given when executing a --login. If not given, it will be prompted for.
  -P TOKEN_PATH, --token-path TOKEN_PATH
                        Path to read or write the API access token to or from. If not given, ~/.merge/cli_token will be used.
  -a API, --api API     If given, use the address for the merge API. Defaults to api.mergetb.net
  -u URL, --url URL     The API path to read
  -L {none,all,debug,info,warning,error,critical}, --loglevel {none,all,debug,info,warning,error,critical}
                        The level at which to log. Must be one of none, debug, info, warning, error, or critical. Default is none. (This is mostly used for debugging.)
```

To get bash tab completion for mergetb, generate and install the bash completion configuration file (after library installation) like so:

```shell
> ./bin/gen_bash_completions.py  > /tmp/mergetb
> sudo cp /tmp/mergetb /etc/bash_completion.d
```

Example usage:
```
> mergetb -l murphy@ceftb.net
Password: ******
>
> mergetb projects list
[
{
    "description": "Murphy's personal project",
        "id": 1,
        "name": "murphy"
},
{
    "description": "Murphy's research group project",
    "id": 2,
    "name": "kong"
}
]
> mergetb -u projects/murphy
{
    "description": "Murphy's personal project",
    "id": 1,
    "name": "murphy"
}
```

NOTE: If using in the LWDE context, you need to set the environment MERGE_API_CERT to the LWDE api service's cert. Or use the `-c` option.

```
export MERGE_API_CERT=/home/glawler/go/src/gitlab.com/mergetb/prototypes/lwde/api_cert.pem
```

Even then, the script will display a warning as the LWDE certificate does not use a subject alt name. And you need to alias the CN in the certificate to the ip address of the api container.

``` 
echo 172.20.0.25 portal.ceftb.net >> /etc/hosts
```

## Testing

The python-cli supports pytest unit testing. To run the tests, run pytest in the root directory.

```
python3 -m pytest
```

The test framework assumes a few things about the state of the system though. There must be two existing and active users: `murphy` and `maisie`. The
`murphy` account will be used for most unittests (create project, destroy projects, etc). The `maisie` account will be used to test project membership.

It also assumes the `MERGE_API_CERT` environment variable is set to the full path of the API's full cert chain file. 
