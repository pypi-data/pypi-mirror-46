# Sparrow
Sparrow is a simple cli tool to extract user-defined tags from a GTM container json file and generate a new configuration file with all related tags informations.



  ### Installation
  ```bash
  pip install sparrow-gtm-cli
  ```
_sparrow should be now installed and ready to be used from the command line._

#### Usage
```
sparrow [globals] <command>
```

#### global flags
  > -v [--version] output the version number of sparrow

  > -h [--help] output the help section of sparrow

#### command
> **extract** extract specific tags with all related info from configuration file and generate a new config file that can be imported back to a GTM container.

> **info** display info about a container.

---
#### Quick  Usage
```
sparrow extract <config.json> <target.json>
```
  > config.json: GTM container configuration file.

  > target.json: a valid json format file listing tags to be extracted from the config file.

  > output: generate a new configuration file **output.json**

::*target.json:: file format must be a valid json file with the below structure.

```json
{
  "keys": [
    "<tag-name-goes-here>",
    "<tag-name-goes-here>",
  ]
}
```

---
```
sparrow info <config.json>
```
  > config.json: A valid GTM container configuration json file.
  
  > output: output related container info (#variables, #tags, #triggers).

