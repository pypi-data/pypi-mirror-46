# dictmentor

[![PyPI version](https://badge.fury.io/py/dictmentor.svg)](https://badge.fury.io/py/dictmentor)
[![Build Status](https://travis-ci.org/HazardDede/dictmentor.svg?branch=master)](https://travis-ci.org/HazardDede/dictmentor)
[![Coverage Status](https://coveralls.io/repos/github/HazardDede/dictmentor/badge.svg?branch=master)](https://coveralls.io/github/HazardDede/dictmentor?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


A python utility framework to augment dictionaries

1\.  [Installation](#installation)  
2\.  [Getting started](#gettingstarted)  
3\.  [Extensions](#extensions)  
3.1\.  [Variables](#variables)  
3.2\.  [Environment](#environment)  
3.3\.  [ExternalResource](#externalresource)  
3.4\.  [ExternalYamlResource](#externalyamlresource)  

<a name="installation"></a>

## 1\. Installation

Installation is straightforward via pip:

```bash
pip install dictmentor
```

<a name="gettingstarted"></a>

## 2\. Getting started

Using `dictmentor` is simple. Just create an instance of `DictMentor` and bind some extensions to it. The extensions
do the hard work augmenting the dictionary. `DictMentor` does not have any extensions that are enabled by default. This
is because some extensions need some additional arguments passed that control their behaviour. If you bind no extensions
on your own and augment a dictionary, it will actually do nothing and return the dictionary as it is.

**Example usage:**

```python
import os
from dictmentor import DictMentor, extensions as ext, utils


base_path = os.path.dirname(__file__)
dm = DictMentor(
    ext.Environment(),
    ext.ExternalResource(base_path=base_path),
    ext.ExternalYamlResource(base_path=base_path)
)

yml = """
products:
    - external: item1.yaml
    - external: item2.yaml
home_directory: "{{env::HOME}}"
extraction_sql: "{{external::products.sql}}"
"""

with utils.modified_environ(HOME="/home/pi"):
    res = dm.load_yaml(yml)

from pprint import pprint
pprint(res)

# Result:
# {'extraction_sql': '-- Contents of products.sql\nSELECT *\nFROM products\n;',
#  'home_directory': '/home/pi',
#  'products': [{'item1': {'price': 50, 'stock': 100}},
#               {'item2': {'price': 99, 'stock': 10}}]}

```

For a list of provided extensions please see the chapter Extensions. You can easily write your own extensions as well.
Please see existing extensions for a how-to.


<a name="extensions"></a>

## 3\. Extensions

<a name="variables"></a>

### 3.1\. Variables

Augment the given dictionary by resolving pre-defined variables on the fly

Example

```python
# Import DictMentor and extensions
import dictmentor.extensions as ext
from dictmentor import DictMentor, utils

yml = """
statements:
  my_env: "{{var::my_env}}"
  home: "{{var::home}}"
  unknown: "{{var::unknown}}"
  combined: "{{var::my_env}}@{{var::home}}"
"""

var_ext = ext.Variables(
    my_env='development',
    home="/home/pi",
)
result = DictMentor().bind(var_ext).load_yaml(yml)

from pprint import pprint
pprint(result)

# Result:
# {'statements': {'combined': 'development@/home/pi',
#                 'home': '/home/pi',
#                 'my_env': 'development',
#                 'unknown': 'none'}}

```

<a name="environment"></a>

### 3.2\. Environment

Augment the given dictionary by resolving environment variables on the fly

Example

```python
# Import DictMentor and extensions
import dictmentor.extensions as ext
from dictmentor import DictMentor, utils

yml = """
statements:
  my_env: "{{env::MY_ENV}}"
  home: "{{env::HOME}}"
  unknown: "{{env::UNKNOWN}}"
  with_default: "{{env::UNKNOWN:=the_default}}"
"""

# Make sure that MY_ENV is set and that UNKNOWN is unset
with utils.modified_environ("UNKNOWN", MY_ENV='development'):
    result = DictMentor().bind(ext.Environment()).load_yaml(yml)

from pprint import pprint
pprint(result)

# Result:
# {'statements': {'home': '/home/pi',
#                 'my_env': 'development',
#                 'unknown': 'none'
#                 'with_default': 'the_default'}}

```

<a name="externalresource"></a>

### 3.3\. ExternalResource

Augment the given dictionary by resolving files on disk (whether absolute or relative) and integrating their content.
If the path to the file is specified in a relative manner you should pass a `base_path` to the `ExternalResource`
instance when instantiating it. Otherwise the current working directory will be assumed.

Example

```sql
-- Contents of all.sql
SELECT *
FROM foo
;
```

```sql
-- Contents of single.sql
SELECT *
FROM foo
WHERE id = {placeholder}
;
```

```python
# Import DictMentor and extensions
import dictmentor.extensions as ext
from dictmentor import DictMentor

import os
base_path = os.path.dirname(__file__)

yml = """
statements:
  all: "{{external::all.sql}}"
  single: "{{external::single.sql}}"
"""

result = DictMentor().bind(ext.ExternalResource(base_path)).load_yaml(yml)

from pprint import pprint
pprint(result)

# Result:
# {'statements': {'all': '-- Contents of all.sql\nSELECT *\nFROM foo\n;',
#                 'single': '-- Contents of single.sql\nSELECT *\nFROM foo\nWHERE id = {placeholder}\n;'}}

```

<a name="externalyamlresource"></a>

### 3.4\. ExternalYamlResource

Augment the given dictionary by resolving by yaml file on disk (whether absolute or relative) and integrating
its content (as a dictionary) as the current node. The yaml's contents will be augmented as well.

If the path to the file is specified in a relative manner you should pass a `base_path` to the `ExternalYamlResource`
instance when instantiating it. Otherwise the current working directory will be assumed.

Example

```yaml
# Contents of inner.yaml
inner:
  item1:
  item2:
  external: item3.yaml
```

```yaml
# Contents of item3.yaml
item2:
  price: 50  # You may also update nodes from the parent node
item3:
  price: 100
  count: 5
  sold: 200
```

```python
# Import DictMentor and extensions
import dictmentor.extensions as ext
from dictmentor import DictMentor

import os
base_path = os.path.dirname(__file__)

yml = """
statements:
  external: "inner.yaml"
"""

result = DictMentor().bind(ext.ExternalYamlResource(base_path=base_path)).load_yaml(yml)

from pprint import pprint
pprint(result)

# Result:
# {'statements': {'inner': {'item1': None,
#                           'item2': {'price': 50},
#                           'item3': {'count': 5, 'price': 100, 'sold': 200}}}}

```
