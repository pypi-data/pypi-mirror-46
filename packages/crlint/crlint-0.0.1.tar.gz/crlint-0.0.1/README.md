# About:

Copyright linter

# Copytights format:
* Python code copyrights:
```
# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Denis Kazak <denis.kazak@celadon.ae>
```
* JavaScript code copyrights:
```
// Copyright (c) 2019 Celadon Development LLC, All rights reserved.
// Author Denis Kazak <denis.kazak@celadon.ae>
```

# How to use:
* Install crlint package:
```$ python3 setup.py install```
*  Go to project directory and put `.crlintrc` in it. Config must have such format:
```
        [ignore]
        patterns=*.json, *.txt
```
* Run crlint command in working directory:
```$ crlint```

# Integration with CI:
* Generate and copy [pipeline ssh key](https://confluence.atlassian.com/bitbucket/use-ssh-keys-in-bitbucket-pipelines-847452940.html) and send it to mainteiner of this repo
* Add such step in your `bitbucket-pipelines.yml`:
```
pipelines:
  default:
    - step:
        name: lint copyrights
        image: python:3.7.2
        script:
          - git clone git@bitbucket.org:celadonteam/crtool.git
          - cd crtool
          - python setup.py install
          - cd .. && rm -rf crtool
          - crlint
```
