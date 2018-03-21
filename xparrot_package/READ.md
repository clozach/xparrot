# Generic CLI App

Based on [this tutorial](https://medium.com/@trstringer/the-easy-and-nice-way-to-do-cli-apps-in-python-5d9964dc950d)

* `__init__.py`: Tells python that the dir contains a package. Runs this code first, if not empty.
* `__main__.py`: Main entry point for CLI app (as dictated by `setup.py`)
  * Minimal implementation to "show it works":
    ```python
    import sys
    from .classmodule import MyClass
    from .funcmodule import my_function
    def main():
        print('in main')
        args = sys.argv[1:]
        print('count of args :: {}'.format(len(args)))
        for arg in args:
            print('passed argument :: {}'.format(arg))
        my_function('hello world')
        my_object = MyClass('Thomas')
        my_object.say_name()
    if __name__ == '__main__':
        main()
    ```
* `classmodule.py`: Demonstrates importing a class from a module:
  ```python
  class MyClass():
    def __init__(self, name):
        self.name = name
    def say_name(self):
        print('name is {}'.format(self.name))
  ```
* `funcmodule.py`: Demonstrates importing a single function from a module:
  ```python
  def my_function(text_to_display):
    print('text from my_function :: {}'.format(text_to_display))
  ```
* `setup.py`: Tells python how the app's held together:

  ```python
  from setuptools import setup

  setup(
    name = 'pycli',
    version = '0.1.0',
    packages = ['pycli'],
    entry_points = {
        'console_scripts': [
            'pycli = pycli.__main__:main' # Change left-of-`=` to change the entry_point name
        ]
    })
  ```

What I've done so far is identical, aside the fact that I'm using `cliapp` as the package and root folder names.

Oh, and I just discovered `docopt`, which blows argparse out of the water! Srsly.

Note, if using pip per the tutorial, use `-e` ('editable') for development mode.

Also consider: [`clint`](https://pypi.python.org/pypi/clint/) (from this [list](http://docs.python-guide.org/en/latest/scenarios/cli/)). From what I can tell by skimming, Cliff and Cement are too heavy. `docopt` _seems_ like the way to go for generating args from the help docs themselves. `docopts` should do the trick for parsing. And `clint` could make output fancier…?

Well, at any rate, let's start with a test of docopt by editing `__main__.py` to look like this:

```python
"""Naval Fate.

Usage:
  xParrot list
  xParrot sayHi <name>
  xParrot (-h | --help)
  xParrot --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt


def main():
    arguments = docopt(__doc__, version='cliapp 0.0.1')

    print(arguments)


if __name__ == '__main__':
    main()
```

Which yields:

```
$ cliapp list
{'--help': False,
 '--version': False,
 '<name>': None,
 'list': True,
 'sayHi': False}
$ cliapp sayHi foo
{'--help': False,
 '--version': False,
 '<name>': 'foo',
 'list': False,
 'sayHi': True}
```

````
## Remaking XParrot

As of this writing, it's now `xParrot list`, and it works…if you paste the AirTable API key into `__main__.py`…which isn't really ideal. So now I'm adding a new arg, as well as a new ENV option: AIRTABLE_API_KEY

Question: do breakpoints work when xParrot's run from the built-in VSCode terminal? (Answer: apparently not the way I've got things configured! ☹️)

Note that I've got this in my `fish` functions, thus allowing me to replace all calls to xparrot with `xp <command>`, minus the api key:

```fish
function xp
    set -g -x AIRTABLE_API_KEY 'insert_your_key_to_api_here'
    xparrot $argv -k $AIRTABLE_API_KEY
end
````
