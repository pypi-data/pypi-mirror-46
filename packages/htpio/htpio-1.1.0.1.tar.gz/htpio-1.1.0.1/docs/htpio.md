# Module `htpio` {#htpio}

*** Hardware Test Platform (HTP) Remote I/O Classes and Modules. ***

HTPIO is an executable package, which allows the user to test or use some of its library functionality from the command line.

*Set value using telnet:*

```
htpio -p telnet set --host 192.168.199.31 --pin 14 --val 1
```

*Get value using socket:*
```
htpio -p socket get --host 192.168.199.31 --pin 14
```

*Lock/Unlock pin:*
```
htpio -p telnet lock --host 192.168.199.31 --pin 14
htpio -p socket unlock --host 192.168.199.31 --pin 14
```


    
## Sub-modules

* [htpio.bridge](#htpio.bridge)
* [htpio.decorators](#htpio.decorators)
* [htpio.socketio](#htpio.socketio)
* [htpio.telnetio](#htpio.telnetio)






    
# Module `htpio.bridge` {#htpio.bridge}

This module provides the connection between the client application and the remote i/o implementation. It separates use from implementation and might be useful when implementing user interfaces.

*** Example *** :

```
import time
import htpio.bridge as bridge
import htpio.telnetio as telnetio
import htpio.socketio as socketio

device = telnetio.RaspberryPi('192.168.199.31')
gpio = bridge.RemoteAccess(device)

gpio.lock(14)
gpio.configure(14, telnetio.RaspberryPi.OUTPUT)

gpio.set(14, 1)
time.sleep(1)
gpio.set(14, 0)

gpio.unlock(14)
gpio.deconfigure(14)
gpio.logout()

device = socketio.RaspberryPi('192.168.199.31')
gpio = bridge.RemoteAccess(device)

gpio.lock(15)
gpio.configure(15, socketio.RaspberryPi.OUTPUT)

gpio.set(15, 1)
time.sleep(1)
gpio.set(15, 0)

gpio.unlock(15)
gpio.deconfigure(15)
gpio.logout()

```





    
## Classes


    
### Class `Device` {#htpio.bridge.Device}



> `class Device(*args, **kwargs)`


Define the implementor's interface from the bridge pattern. This interface
provides homogeneous interface for all remote I/O libraries.

Typically the implementor interface provides only primitive operations,
and abstraction defines higher-level operations based on these primitives.



    
#### Descendants

* [htpio.socketio.RaspberryPi](#htpio.socketio.RaspberryPi)
* [htpio.telnetio.RaspberryPi](#htpio.telnetio.RaspberryPi)


    
#### Class variables


    
##### Variable `INPUT` {#htpio.bridge.Device.INPUT}

Pin input mode

    
##### Variable `OUTPUT` {#htpio.bridge.Device.OUTPUT}

Pin output mode




    
#### Methods


    
##### Method `configure` {#htpio.bridge.Device.configure}



    
> `def configure(self, pin, direction)`


Abstract method

    
##### Method `deconfigure` {#htpio.bridge.Device.deconfigure}



    
> `def deconfigure(self, pin)`


Abstract method

    
##### Method `get` {#htpio.bridge.Device.get}



    
> `def get(self, pin)`


Abstract method

    
##### Method `isconfigured` {#htpio.bridge.Device.isconfigured}



    
> `def isconfigured(self, pin)`


Abstract method

    
##### Method `islocked` {#htpio.bridge.Device.islocked}



    
> `def islocked(self, pin)`


Abstract method

    
##### Method `lock` {#htpio.bridge.Device.lock}



    
> `def lock(self, pin)`


Abstract method

    
##### Method `login` {#htpio.bridge.Device.login}



    
> `def login(self)`


Abstract method

    
##### Method `logout` {#htpio.bridge.Device.logout}



    
> `def logout(self)`


Abstract method

    
##### Method `reset` {#htpio.bridge.Device.reset}



    
> `def reset(self, pin)`


Abstract method

    
##### Method `set` {#htpio.bridge.Device.set}



    
> `def set(self, pin, value)`


Abstract method

    
##### Method `unlock` {#htpio.bridge.Device.unlock}



    
> `def unlock(self, pin)`


Abstract method

    
### Class `RemoteAccess` {#htpio.bridge.RemoteAccess}



> `class RemoteAccess(protocol_api)`


Define the abstraction's interface from the bridge pattern used by the
client application.

Typically the implementor interface provides only primitive operations,
and abstraction defines higher-level operations based on these primitives.







    
#### Methods


    
##### Method `configure` {#htpio.bridge.RemoteAccess.configure}



    
> `def configure(self, pin, direction)`


Configure pin with direction if it is free

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.configure(14, led.OUTPUT)
led.set(14, 1)
...
```

    
##### Method `deconfigure` {#htpio.bridge.RemoteAccess.deconfigure}



    
> `def deconfigure(self, pin)`


Deconfigure pin if it belongs to my session

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.deconfigure(14)
...
```

    
##### Method `get` {#htpio.bridge.RemoteAccess.get}



    
> `def get(self, pin)`


Get pin value

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.configure(14, led.OUTPUT)
led.set(14, 1)
print(led.get(14))
...
```

    
##### Method `isconfigured` {#htpio.bridge.RemoteAccess.isconfigured}



    
> `def isconfigured(self, pin)`


Check if pin is configured

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.isconfigured(14)
...
```

    
##### Method `islocked` {#htpio.bridge.RemoteAccess.islocked}



    
> `def islocked(self, pin)`


Check if pin is locked by another process

*** Example: ***
```python
from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.lock(14)
if led.islocked(14):
    print("LED is locked!!!")
led.logout()
...
```

    
##### Method `lock` {#htpio.bridge.RemoteAccess.lock}



    
> `def lock(self, pin)`


Lock pin if it is not used

*** Example: ***
```python
from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.lock(14)
...
```

    
##### Method `login` {#htpio.bridge.RemoteAccess.login}



    
> `def login(self)`


Registers to remote device

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.login()
...
```

    
##### Method `logout` {#htpio.bridge.RemoteAccess.logout}



    
> `def logout(self)`


Unregisters from remote device

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.logout()
...
```

    
##### Method `reset` {#htpio.bridge.RemoteAccess.reset}



    
> `def reset(self, pin)`


Remove pin lock forcefully

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.lock(14)
print(led.islocked(14))
led.reset(14)
print(led.islocked(14))
...
```

    
##### Method `set` {#htpio.bridge.RemoteAccess.set}



    
> `def set(self, pin, value)`


Write value to pin

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.configure(14, led.OUTPUT)
led.set(14, 1)
print(led.get(14))
...
```

    
##### Method `unlock` {#htpio.bridge.RemoteAccess.unlock}



    
> `def unlock(self, pin)`


Unlock pin if it belongs to my session

***Example***:
```python

from htpio.bridge import RemoteAccess
from htpio import telnetio, socketio

remoteio = socketio.RaspberryPi('192.168.199.31')
led = RemoteAccess(remoteio)
led.unlock(14)
...
```



    
# Module `htpio.decorators` {#htpio.decorators}

This module implement various decorators such as function calls and exception logging. Decorators are used to implement additional functionality to a method or function without changing its name.

Currently the following decorators are implemented :

 + @countcalls                - Counts the number of function calls
 + @logger(filename)          - Logs function exceptions to a give file

*** Example: ***

```python

    from htpio.decorators import Countcalls, Logger

    @Countcalls
    def f():
        pass

    count = 0
    for i in range(100):
        count = i + 1
        f()

    print(f.count(), count)
```

```python
    @Countcalls
    @Logger(LOGFILE)
    def f():
        return 1 / 0

    # Function under test
    raised = False
    try:
        f()
    except:
        raised = True
        logger.log.info("Number of calls==[{0}]".format(f.count()))
```





    
## Classes


    
### Class `Countcalls` {#htpio.decorators.Countcalls}



> `class Countcalls(f)`


Decorator that keeps track of the number of times a function is called.
<https://wiki.python.org/moin/PythonDecoratorLibrary>

***Example***:

```python
from htpio.decorators import Countcalls

@Countcalls
def f():
    pass

@Countcalls
def g():
    pass

count = 0
for i in range(100):
    count = i + 1
    f()
    g()

print(f.count())  # Number of calls for funciton f
print(g.count())  # Number of calls for function g
print(Countcalls.counts()) # Dump number of calls for f and g
```




    
#### Class variables


    
##### Variable `instances` {#htpio.decorators.Countcalls.instances}

Stores the function names and number of calls



    
#### Static methods


    
##### `Method counts` {#htpio.decorators.Countcalls.counts}



    
> `def counts()`


Return a dictionary for all registered functions is keys and the
number of function calls as values.


    
#### Methods


    
##### Method `count` {#htpio.decorators.Countcalls.count}



    
> `def count(self)`


Return the number of times the function was called.

    
### Class `Logger` {#htpio.decorators.Logger}



> `class Logger(logfile)`


Decorator that logs exceptions into a given file.

*** Example: ***

```python
from htpio.decorators import Logger

@Logger('c:\test.log')
def f():
    return 1 / 0

### Function under test
raised = False
try:
    f()
except:
    raised = True
    logger.log.info("Number of calls==[{0}]".format(f.count()))
```




    
#### Class variables


    
##### Variable `log` {#htpio.decorators.Logger.log}

Instance of a logging object

    
##### Variable `logfile` {#htpio.decorators.Logger.logfile}

Log file use to store the logs






    
# Module `htpio.socketio` {#htpio.socketio}

This is a socket i/o control module wrapping the python pigpio client. PIGPIO is a client/server library using sockets for remote control of the general purpose input outputs(GPIO).


*** Example: ***

```python

import htpio.socketio as socketio

r = socketio.RaspberryPi(host = '192.168.199.31',
                         port = 8888)

try:
    r.lock(14)
except:
    r.logout()
    raise

r.configure(14, socketio.RaspberryPi.OUTPUT)
r.set(14, 1)

print(r.get(14))

r.unlock(14)
r.deconfigure(14)
```





    
## Classes


    
### Class `CannotConnectToTarget` {#htpio.socketio.CannotConnectToTarget}



> `class CannotConnectToTarget(*args, **kwargs)`


Raised the object cannot connect to the specified [target:socket]


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `PinLockedByOtherProcess` {#htpio.socketio.PinLockedByOtherProcess}



> `class PinLockedByOtherProcess(lock_owner=None, my_session=None)`


Raised when the gpio pin is used by other process from the same class.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `RaspberryPi` {#htpio.socketio.RaspberryPi}



> `class RaspberryPi(host=None, port=8888)`


This class allows users to connect and control the GPIO
on a Raspberry remotely by using and extending the pigpio library.

#### Configuration

Enable Remote GPIO

    sudo raspi-config
    Menu : Interfacing Options -> Remote GPIO

Enable pigpiod to start on boot

    sudo systemctl enable pigpiod


#### Class attributes

    LOCK_DIR        : Location of lock files (ramdisk)
    MAX_GPIO        : Maximum number of gpio locks ( from 0 .. MAX)
    INPUT           : GPIO is digital input
    OUTPUT          : GPIO is digital output
    EOF             : End of file


#### Instance attributes

    host            : ip v4 address
    port            : port (from 0 to 65535)

#### Public methods

    islocked(gpio)              : Check if the gpio is locked
    lock(gpio)                  : Locks the gpio
    unlock(gpio)                : Unlocks the gpio
    isconfigured(gpio)          : Checks if the gpio is configured
    configure(gpio, direction)  : Configures the gpio with direction
    deconfigure(gpio)           : Restores the default configuration
    get(gpio)                   : Reads the gpio status
    set(gpio, value)            : Writes new value to gpio
    login()                     : Registers to the remote system
    logout()                    : Unregisters from the remote system
    reset()                     : Deletes all configuration data

#### Constructor

When called with host address, the constructor creates
a telnet connection and performs automatic login. The default port is 8888

```python
import htpio.socketio as socketio

t = socketio.RaspberryPi('192.168.199.31')
```


    
#### Ancestors (in MRO)

* [pigpio.pi](#pigpio.pi)
* [htpio.bridge.Device](#htpio.bridge.Device)



    
#### Class variables


    
##### Variable `EOF` {#htpio.socketio.RaspberryPi.EOF}

Symbol for end of transmission

    
##### Variable `LOCKDIR` {#htpio.socketio.RaspberryPi.LOCKDIR}

Lock files directory

    
##### Variable `MAX_GPIO` {#htpio.socketio.RaspberryPi.MAX_GPIO}

Maximum number of GPIOs




    
#### Methods


    
##### Method `configure` {#htpio.socketio.RaspberryPi.configure}



    
> `def configure(self, pin, direction)`


Configures the gpio for input or output operation.

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')

led.configure(14, socketio.RaspberryPi.OUTPUT)
...
```

    
##### Method `deconfigure` {#htpio.socketio.RaspberryPi.deconfigure}



    
> `def deconfigure(self, pin)`


Removes the gpio configuration.

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')

led.deconfigure(14)
...
```

    
##### Method `get` {#htpio.socketio.RaspberryPi.get}



    
> `def get(self, pin)`


Reads the value of the gpio.

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')

led.get(14)
...
```

    
##### Method `isconfigured` {#htpio.socketio.RaspberryPi.isconfigured}



    
> `def isconfigured(self, pin)`


Check if gpio is configured by comparing the current direction
configuration with the default one (INPUT).

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')

led.configure(14, socketio.RaspberryPi.OUTPUT)
if led.isconfigured(14):
    print("LED is configured!!!")
...
```

    
##### Method `islocked` {#htpio.socketio.RaspberryPi.islocked}



    
> `def islocked(self, pin)`


Opens the gpio lock file and checks it size. If the size is more than
zero then the gpio is considered to be locked by another process.

*** Example: ***
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')
led.lock(14)
if led.islocked(14) :
    print("LED is locked!!!")
...
```

    
##### Method `lock` {#htpio.socketio.RaspberryPi.lock}



    
> `def lock(self, pin)`


Lock the given pin by creating a lock file and writing the current
session id into it.

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')
led.lock(14)
...
```

    
##### Method `login` {#htpio.socketio.RaspberryPi.login}



    
> `def login(self)`


Registers device for use with target device by checking for
an established connection and creating all gpio lock files.

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi()
led.host = '192.168.199.31'
led.port = 8888
led.login()
...
```

    
##### Method `logout` {#htpio.socketio.RaspberryPi.logout}



    
> `def logout(self)`


Unregisters device from remote device.

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')

led.logout()

...
```

    
##### Method `reset` {#htpio.socketio.RaspberryPi.reset}



    
> `def reset(self, pin)`


Deletes the content of all generated lock files.

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')

led.reset(14)

...
```

    
##### Method `set` {#htpio.socketio.RaspberryPi.set}



    
> `def set(self, pin, value)`


Writes the value to the gpio.

*** Example: ***
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')

led.configure(14, socketio.RaspberryPi.OUTPUT)
led.set(14, 1)
...
```

    
##### Method `unlock` {#htpio.socketio.RaspberryPi.unlock}



    
> `def unlock(self, pin)`


Unlock the pin by truncating the size of the lock file to zero.

***Example***:
```python
import htpio.socketio as socketio

led = socketio.RaspberryPi('192.168.199.31')
led.unlock(14)
...
```



    
# Module `htpio.telnetio` {#htpio.telnetio}

This is a telnet client i/o control module.
Telnet is a client/server text-oriented communication protocol using a virtual terminal connection and operates over TCP. It provides a command-line interface to the operating system on a remote host.

*** Example: ***

```python

import htpio.telnetio as telnetio

r = telnetio.RaspberryPi(host = '192.168.199.31',
                         port = 23,
                         user = 'pi',
                         password = 'raspberry')

try:
    r.lock(14)
except:
    r.logout()
    raise

r.configure(14, telnetio.RaspberryPi.OUTPUT)
r.set(14, 1)

print(r.get(14))

r.unlock(14)
r.deconfigure(14)

```





    
## Classes


    
### Class `CannotCreateLockDirectory` {#htpio.telnetio.CannotCreateLockDirectory}



> `class CannotCreateLockDirectory(*args, **kwargs)`


Raised when the lockfolder cannot be created.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `CannotMountRamDisk` {#htpio.telnetio.CannotMountRamDisk}



> `class CannotMountRamDisk(*args, **kwargs)`


Raised when the ram disk cannot be mapped to the lock folder


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `InvalidLoginDetails` {#htpio.telnetio.InvalidLoginDetails}



> `class InvalidLoginDetails(*args, **kwargs)`


Raised when user or password provided not valid


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `PinLockedByOtherProcess` {#htpio.telnetio.PinLockedByOtherProcess}



> `class PinLockedByOtherProcess(lock_owner=None, my_session=None)`


Raised when the gpio pin is used by other process from the same class.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `RaspberryPi` {#htpio.telnetio.RaspberryPi}



> `class RaspberryPi(host=None, port=23, user='htp', password='sokotnar', login_prompt='login:', password_prompt='Password:', shell_prompt='$', timeout=20)`


RaspberryPi telnet remote i/o access class.

This class provides basic funcitonality for controlling the GPIO by
using a remote telnet session and sending commands to the operating system.

#### Configuration

The user should be part of the sudo and gpio group and the visudo file
should be configured for no password prompt when using the sudo. This is
accomplished by executing the following commands :

```
sudo adduser htp
sudo usermod -a -G gpio htp                
sudo usermod -a -G sudo htp

sudo visudo                
    (add line) htp     ALL=(ALL) NOPASSWD: ALL            
    (add line) %gpio   ALL=(ALL) NOPASSWD: ALL

```

#### Class attributes

    LOCK_DIR         Location of lock files (ramdisk)
    MAX_GPIO         Maximum number of gpio locks ( from 0 .. MAX)
    INPUT            GPIO is digital input
    OUTPUT           GPIO is digital output
    EOF              End of file


#### Instance attributes

    host            : ip v4 address
    port            : port (from 0 to 65535)
    user            : user
    password        : user password
    login_prompt    : token to detect when login is expected
    password_prompt : token to detect when password is expected
    shell_prompt    : token to detect return after command execution
    timeout         : timeout time in case of connectivity problems

#### Public methods

    islocked(gpio)              : Check if the gpio is locked
    lock(gpio)                  : Locks the gpio
    unlock(gpio)                : Unlocks the gpio
    isconfigured(gpio)          : Checks if the gpio is configured
    configure(gpio, direction)  : Configures the gpio with direction
    deconfigure(gpio)           : Restores the default configuration
    get(gpio)                   : Reads the gpio status
    set(gpio, value)            : Writes new value to gpio
    login()                     : Registers to the remote system
    logout()                    : Unregisters from the remote system
    reset()                     : Deletes all configuration data

#### Constructor

When called with host address, the constructor creates
a telnet connection and performs automatic login:

```python
import htpio.telnetio as telnetio

t = telnetio.RaspberryPi('192.168.199.31')
```

When called without host address, the constructor creates
an unconnected instance. In this case the object might be
configured by using the instance attributes:

```python
import htpio.telnetio as telnetio

t = telnetio.RaspberryPi()

t.host = '192.168.199.31'
t.port = 23
t.user = 'user'
t.password = 'password'
t.login_prompt = 'login:'
t.password_prompt = 'Password:'
t.shell_prompt = '$'
t.timeout = 20
```

After the configuration above the user is required to use the
following statements:

```python
t.open(host, port)
t.login()
```


    
#### Ancestors (in MRO)

* [telnetlib.Telnet](#telnetlib.Telnet)
* [htpio.bridge.Device](#htpio.bridge.Device)



    
#### Class variables


    
##### Variable `EOF` {#htpio.telnetio.RaspberryPi.EOF}

Character used to mark end of line transmission

    
##### Variable `LOCKDIR` {#htpio.telnetio.RaspberryPi.LOCKDIR}

Directory containing the lock files

    
##### Variable `MAX_GPIO` {#htpio.telnetio.RaspberryPi.MAX_GPIO}

Maximum number of gpio lock files

    
##### Variable `RAMDISK` {#htpio.telnetio.RaspberryPi.RAMDISK}

Label for the ramdisk mounted on the lock directory




    
#### Methods


    
##### Method `configure` {#htpio.telnetio.RaspberryPi.configure}



    
> `def configure(self, pin, direction)`


Create the sysfs virtual folder for gpio manipulation.

*** Shell : ***
```shell
echo 14 | tee /sys/class/gpio/export
```

***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')

led.configure(14, telnetio.RaspberryPi.OUTPUT)
...
```

    
##### Method `deconfigure` {#htpio.telnetio.RaspberryPi.deconfigure}



    
> `def deconfigure(self, pin)`


Delete the sysfs virtual folder for pin manipulation.

*** Shell : ***
```
echo 14 | tee /sys/class/gpio/unexport
```

***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')

led.deconfigure(14)
...
```

    
##### Method `get` {#htpio.telnetio.RaspberryPi.get}



    
> `def get(self, pin)`


Gets the current status of the given pin by reading the system file.

*** Shell : ***
```shell
cat /sys/class/gpio/gpio14/value
```

***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')

led.get(14)
...
```

    
##### Method `isconfigured` {#htpio.telnetio.RaspberryPi.isconfigured}



    
> `def isconfigured(self, pin)`


This function checks if the sysfs folder /sys/class/gpio/gpioNN exists.

***Shell:***
```shell
find /sys/class/gpio -name gpio14
```

***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')

led.configure(14, telnetio.RaspberryPi.OUTPUT)
if led.isconfigured(14):
    print("LED is configured!!!")
...
```

    
##### Method `islocked` {#htpio.telnetio.RaspberryPi.islocked}



    
> `def islocked(self, pin)`


Check if pin is already locked by an object of this class and returns
the identification number of the locking process.

*** Shell: ***
```
sudo cat /tmp/htp/locks/gpio14
```

*** Example: ***
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')
led.lock(14)
if led.islocked(14) :
    print("LED is locked!!!")
...
```

    
##### Method `lock` {#htpio.telnetio.RaspberryPi.lock}



    
> `def lock(self, pin)`


Throws an exception <b>PinLockedByOtherProcess</b> or opens the gpio
lock file and writes the session id in it.

***Shell***:
```shell
echo 1921681993055555 | sudo tee /tmp/htp/gpio14
```

***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')
led.lock(14)
...
```

    
##### Method `login` {#htpio.telnetio.RaspberryPi.login}



    
> `def login(self)`


Performs an automatic login to the remote system using the supplied
user and password as instance properties.

!!! Use only when creating an unconnected instance !!!


***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi()
led.host = '192.168.199.31'
led.port = 23
led.user = 'htpio'
led.password = 'sokotnar'

led.open(host, port)
led.login()

...
```

    
##### Method `logout` {#htpio.telnetio.RaspberryPi.logout}



    
> `def logout(self)`


Closes the connection to the target.

***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')

led.logout()

...
```

    
##### Method `reset` {#htpio.telnetio.RaspberryPi.reset}



    
> `def reset(self, pin)`


Deletes lock file for pin.

***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')

led.reset(14)

...
```

    
##### Method `set` {#htpio.telnetio.RaspberryPi.set}



    
> `def set(self, pin, value)`


Sets the current value of the given pin by using the system file.

*** Shell: ***
```
echo 1 | sudo tee /sys/class/gpio/gpio14
```


*** Example: ***
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')

led.configure(14, telnetio.RaspberryPi.OUTPUT)
led.set(14, 1)
...
```

    
##### Method `unlock` {#htpio.telnetio.RaspberryPi.unlock}



    
> `def unlock(self, pin)`


Unlocks the gpio by deleting the content of the lock file.

***Shell***:
```shell
sudo truncate --size=0 /tmp/htp/locks/gpio14
```

***Example***:
```python
import htpio.telnetio as telnetio

led = telnetio.RaspberryPi('192.168.199.31')
led.unlock(14)
...
```


-----
Generated by *pdoc* 0.6.1 (<https://pdoc3.github.io>).
