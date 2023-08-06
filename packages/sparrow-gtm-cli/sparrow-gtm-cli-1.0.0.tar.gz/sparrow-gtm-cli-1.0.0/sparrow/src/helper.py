from colorama import Fore


def extract_info(src: list or dict, what="trigger", ids=True) -> list:
    """
    extract_info extracts variables and tags ids recursively from dict
    extract_info can operate on list or nested lists as well

    :param ids:
    :param src: accepts lists or dict
    :param what: accepts 3 options trigger, tag and variable default to trigger
    :return: list: output a list of unique ids
    """
    i = []
    o = []

    if type(src) is dict:
        t = 'tagId' if ids else 'name'
        tr = 'firingTriggerId' if ids else 'name'
        v = 'variableId' if ids else 'name'
        if what == "tag":
            for tag in src.get('containerVersion').get('tag'):
                if tag.get(t):
                    i.append(tag[t])
        elif what == "trigger":
            for tag in src.get('containerVersion').get('tag'):
                if tag.get(tr):
                    i.append(tag[tr])
        elif what == "variable":
            for variable in src.get('containerVersion').get('variable'):
                if variable.get(v):
                    i.append(variable[v])

    else:
        i = src

    def deep_extract(ls):
        if type(ls) is list:
            for ids in ls:
                if not o.__contains__(ids):
                    deep_extract(ids)
        else:
            if not o.__contains__(ls):
                o.append(ls)

        return o

    for tr in i:
        deep_extract(tr)

    return o


def info(src: dict):
    if not src.get('containerVersion'):
        err = "sparrow error: {}GTM configuration file is not valid {}"
        print(err.format(Fore.RED, Fore.RESET))
        exit(1)
    else:
        tags = len(extract_info(src, what='tag'))
        triggers = len(extract_info(src, what='trigger'))
        variables = len(extract_info(src, what='variable'))
        output = f"""
-----------------------------------------------------------
|                   General container info                |
-----------------------------------------------------------

Export-time:                {src['exportTime']}
Name:                       {src['containerVersion']['container']['name']}
Domain:                     {src['containerVersion']['container']['domainName']}
Public-id:                  {src['containerVersion']['container']['publicId']}
Container-id:               {src['containerVersion']['container']['containerId']}
Context:                    {src['containerVersion']['container']['usageContext']}
#Tags:                      {tags}
#Triggers:                  {triggers}
#Variables:                 {variables}

    """
        return output


def general_help(gray=False):
    if not gray:
        general_cli_help = """
Usage: sparrow [globals] <command> 

Globals:
  -v, --version                                 output the version number
  -h, --help                                    output usage information

Commands:
  extract <file.json> <input.json>              extract configuration file from source
  info <file.json>                              print information about the container


Examples

sparrow extract configuration.json target.json
    output -> output.json should be created in the current working directory

sparrow info configuration.json
    output -> Container related info

"""
        return general_cli_help
    else:
        general_cli_help = """
Usage: sparrow [globals] <command> 

Globals:
  -v, --version                                 output the version number
  -h, --help                                    output usage information

Commands:
  extract <file.json> <input.json> [flags]      extract configuration file from source
  info <file.json>                              print information about the container
  

Examples

sparrow extract configuration.json target.json
    output -> output.json should be created in the current working directory

sparrow info configuration.json
    output -> Container related info

        """
        return general_cli_help


def command_not_found(cmd):
    err = f"""sparrow command not found {cmd}\n"""
    return err
