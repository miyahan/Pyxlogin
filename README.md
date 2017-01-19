Python Telnet Client
---

## Requirement

- Python 3.5 or leater


## Dependencies

- PIP/pexpect


## How to install

`pip3 install -U git+https://github.com/miyahan/pyxlogin.git`


## Usage

### Python script

```python
# Telnet to Cisco router
from pyclogin import CiscoLogin
pl = CiscoLogin('10.0.0.1', usename='admin', password='passpass', use_telnet=Tue)
pl.login()
print(pl.execute('show version'))
print(pl.execute('show ip int brief'))
```

```python
# SSH to Linux server
from pyllogin import LinuxLogin
pl = LinuxLogin('10.0.0.2', usename='root', password='admin123', encode='euc-jp')
pl.login()
print(pl.execute('ls -l'))
```

### Command line

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
