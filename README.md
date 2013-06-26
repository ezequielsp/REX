## REX

REX: regular expressions explorer tool, is a small utility to test and work with regular expressions in Python
Nothing big or fancy here, a tool with a basic web interface to test your Python regular expression without having to run your code.

## Python version

REX runs with Python 2.7 and higher, because I use the argparse module.

## Dependencies

You will need to have cherrypy 3 installed.
The web interface is based on Ext-JS. You will have to download it and copy it in the "www/extjs" directory.

## How to use

```
usage: REX [-h] [-d] [-p SERVER_PORT]

REX: Small utility to test and work with regular expressions in Python

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           specify that REX will run in debug mode
  -p SERVER_PORT, --port SERVER_PORT
                        specify the TCP port on which REX will listen to
```

## Sreenshot

![REX screenshot](/www/resources/images/rex.png)