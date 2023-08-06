# Another Python Terminal Logger

Here it is: another python terminal logger---apytl.

This implementation uses only the standard Python library and supports unicode 
emojis. If you've ever wanted a progress bar that fills with piles of poop, 
eggplants, or extended middle fingers, then you're in the right place.

# Installation
## `pip`
I've attempted to make this easy. You should be able to use `pip` to install the 
package by running:

```console
pip install apytl
```

Right now the package is only released for Python >=3.5. If `pip` complains 
about not finding a version, you can either try upgrading Python, or build from 
source.

## Building from source
You may install from source by either downloading the files from PyPI 
[(here)](https://pypi.org/project/apytl/#files) or cloning the git repository:

```console
git clone https://github.com/anadolski/apytl.git
```

If this is the first time you're installing the package, all you should need to 
do is `cd` to the source directory (i.e., the one containing `setup.py`) and 
run:

```console
python setup.py build
python setup.py install --user --record ./.installed_files.txt
```

If you re-clone the repo (or `git pull` or otherwise update the source code), 
you will need to reinstall to take advantage of all the fun new features. And 
bugs. Let's not forget those bugs. To reinstall---again, from the source 
directory---run:

```console
rm $(cat ./.installed_files.txt)
```

(Note: This command will attempt to delete every entry in 
`.installed_files.txt`, so use with caution. Ensure there isn't anything 
important hiding in that file.)

To reinstall, simply run the `build` and `install` commands mentioned at the 
beginning of the section.

# Use
You can use the progress bar for iteration tracking. All the function needs to 
know is the total number of iterations in the loop, and the iteration that it 
currently on. Just drop the `apytl.drawbar()` function inside your loop and pass 
it those parameters. Here's a minimal example:

```python
import time
import apytl

total_iterations = 50
wait = 0.1

for index, value in enumerate(range(total_iterations)):
    # Your code goes here, then we draw the progress bar
    apytl.drawbar(value, total_iterations)
    time.sleep(wait)
```

But you probably want emojis, so do this instead:

```python
import time
import apytl

total_iterations = 50
wait = 0.1

for index, value in enumerate(range(total_iterations)):
    # Your code goes here, then we draw the progress bar
    apytl.drawbar(value, total_iterations, fill='poop')
    time.sleep(wait)
```

Ta-da! Poop all over your terminal (assuming your terminal emulator, display 
manager, and font combinations support it).

`drawbar()` accepts some customization options; see the docstring for complete 
details. Here are a couple highlights:
 * `fill`: takes arbitrary single-character alphanumeric input, or an arbitrary 
   Python-formatted unicode emoji (of the form `\\UXXXXXXXX` or `\\uXXXX`), or 
   one of a few preset options listed in the docstring.
 * `barsize`: takes an integer and sets the size of the filling region.

# Development
This package is an alpha release and under active development. That means that I 
fix bugs and create new ones approximately whenever I feel like it.

The `master` branch is the most stable version of the package, with primary 
development happening on `dev`.

Pull requests and issue tickets are both welcomed and encouraged. Please put 
specific emoji requests into issue tickets (for now).
