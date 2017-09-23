Python Telnet Client
===

## Requirement

- Python 3.6 or leater


## Dependencies

- PyPI/pexpect


## How to install

### Using PIP

* `pip install -U git+https://github.com/miyahan/pyxlogin.git` (or use SSH)

### Using setup.py

* `git clone git@github.com:miyahan/Pyxlogin.git` (or use HTTPS)
* `python setup.py install`


## Usage

### via Python script

```python
# Telnet to Cisco router
from pyxlogin.cisco_login import CiscoLogin
pl = CiscoLogin('10.0.0.1', usename='admin', password='passpass', use_telnet=Tue)
pl.login()
print(pl.execute('show version'))
print(pl.execute('show ip int brief'))
```

```python
# SSH to Linux server
from pyxlogin.linux_login import LinuxLogin
pl = LinuxLogin('10.0.0.2', usename='root', password='admin123', encode='euc-jp')
pl.login()
print(pl.execute('ls -l'))
```

### via command line

```shell
# Telnet to Cisco router
python3 cisco_login.py 10.0.0.1 -u admin -v passpass -c "show version" "show ip int brief" -T
```

```shell
# SSH to Linux server
python3 linux_login.py 10.0.0.2 -u root -v admin123 -c "ls -l" -E euc-jp
```


## License

MIT
