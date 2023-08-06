# Another Python Terminal Logger

Here it is: another python terminal logger---apytl.

# Installation

I've attempted to make this easy. If this is the first time you're installing 
the package, all you should need to do is `cd` to the source directory (i.e., 
the one containing `setup.py`) and run:

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

This command will attempt to delete every entry in `.installed_files.txt`, so 
use with caution.

To reinstall, simply run the `build` and `install` commands mentioned at the 
beginning of the section.
