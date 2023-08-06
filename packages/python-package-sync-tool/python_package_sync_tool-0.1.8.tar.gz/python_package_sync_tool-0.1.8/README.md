## PythonPackageSyncTool

PythonPackageSyncTool is a Python utility to "fix" requirements.txt.

It is used to make manipulation on requirements.txt that is produces by 'pip freeze'

### Getting Help


### QuickStart
```bash
pip3 install python-package-sync-tool
```

##
```bash
cd /opt/anaconda3/lib/python3.7/site-packages/alexber/reqsync/data/
```
Note: This is Path where you're actually install my utility, it can be different in your machine.

If you use venv it will look something like:

```bash
cd /opt/MyProject/venv/Lib/site-packages/alexber/reqsync
```
##


Alternatively you can create sctipt file for yourself, named, say, driver.py:

```python3
#!/usr/bin/python3

import alexber.reqsync.app as app

if __name__ == "__main__":
   app.main()
```

Than create file config.yml near your script (see data/config.yml) or provide all parameter using command line
argruments. Use ':' in places where you should naturally write '==' (see explanation below).

Parammeters 'source' and 'destination' are required. You should also provide (requirements) file for 'source'.

'mutual_exclusion' has default value True.



##
Now, type

```bash
python3 -m alexber.reqsync.data --add=some_new_package:1.0.0
```

or if you're using script (driver.py) go the directory with the script and type
```bash
./driver.py --add=some_new_package:1.0.0
```
This will run quick check whether package is not in remove list. If it is, the utility will fail. You can override this
beahivor by supplying `--mutual_exclusion=False`. 

Then, this will add some_new_package with version 1.0.0 to the requirements-dest.txt

Note:

Semicolomn and not equal sign is used here due to Python limitaion of usage of equal sign in the value in the command line.

You can specified multiple packages using comma delimiter.

You can specifiy path to your config file using `--config_file`.

It can be absolute or relative. If you're running using script (driver.py), that it can be relative to the directory 
whether you put your script. If you're running as the module (`python3 -m`), it can be relative to 
`/opt/anaconda3/lib/python3.7/site-packages/alexber/reqsync/data/` (exact path can be different, see above).  

##
You can supplied multiply packages by using comma:


```bash
python3 -m alexber.reqsync.data --add=some_new_package:1.0.0,another_new_package:2.0.0
```

or if you're using script (driver.py) go the directory with the script and type
```bash
./driver.py --add=some_new_package:1.0.0,another_new_package:2.0.0
```



### Installing from source
```bash
python3 -m pip install . # only installs "required"
```
```bash
python3 -m pip install .[test] # installs dependencies for tests
```
##

From the directory with setup.py
```bash
python3 setup.py test #run all tests
```
```bash
pytest
```



## Requirements


PythonPackageSyncTool requires the following modules.

* Python 3.7+

* PyYAML==5.1