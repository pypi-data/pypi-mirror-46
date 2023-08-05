Overview
========

Using this tool you'll be able to provision your board: real or virtual one.

Install `v-bootstrap` tool:
========

Before the installation procedure we assume that Python2.7|3.x installed on your system.

In order to install `v-bootstrap` please issue the following command:

```bash
# sudo pip install v-bootstrap
```

in case of Windows:
```bash
# pip install v-bootstrap
```

The `v-bootstrap` commands and arguments:
========

```bash
# v-bootstrap --help
usage: v-bootstrap [-h] [--register-host REGISTER_HOST]
             [--register-port REGISTER_PORT] [--cert CERT] [-u USER]
             [-p PASSWORD]
             {board,virt-board} ...

The board provisioning tool

optional arguments:
  -h, --help            show this help message and exit
  --register-host REGISTER_HOST
                        Host address to register. Default: aoscloud.io
  --register-port REGISTER_PORT
                        Port to register. Default: 10000
  --cert CERT           Certificate file. Default:
                        /home/user/.v_bootstrap/security/oem-client.pem
  -u USER, --user USER  Specifies the user to log in as on the remote board.
  -p PASSWORD, --password PASSWORD
                        User password.

Commands:
    board               Launch a board provisioning procedure.
    virt-board          Launch a virtual board provisioning procedure.

Run 'v-bootstrap COMMAND --help' for more information on a command.

```

`v-bootstrap virt-board` arguments:
-------
```bash
# v-bootstrap virt-board --help
usage: v-bootstrap virt-board [-h] --host HOST [--port PORT]

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  Virtual board host name or IP. Default: 127.0.0.1
  --port PORT  Virtual board port. Default: 2222

```

Steps to provision a board:
==========

We assume that a virtual board is installed and ready for provisioning.

Generate a key pair
----------

In order to start it is necessary to generate a key pair.
Using the commands below to do this:

* install package

```bash
# sudo pip install generate-keys
```

* generate

the output directory (depends on your platform) needs to be the following:
* linux - `/home/<current-user-name>/.v_bootstrap/security/`
* macOS - `/Users/<current-user-name>/.v_bootstrap/security/`
* Windows - `C:/Users/<current-user-name>/.v_bootstrap/security/`

example for linux:

```bash
# generate_keys -o /home/<current-user-name>/.v_bootstrap/security/
-----BEGIN PUBLIC KEY-----
.............
-----END PUBLIC KEY-----

```  

Issue and download your certificate using a public key that was generated before.
---------
Go to the OEM dashboard and past your public key to the pop-up.

* go to `https://aoscloud.io/oem/dashboard`
* click the "Issue certificate" button
* add your public key to the pop-up window and click the button 

Then in the user home directory **put/copy** the `oem-client.pem` certificate to the `.v_bootstrap/security/` location.

as example for linux:
```
/home/<current-user-name>/.v_bootstrap/security/oem-client.pem
```


In case of virtual board issue the following command:
---------

```bash
# v-bootstrap virt-board
Starting the provision procedure ... find the whole log info in /home/<current-user-name>/.v_bootstrap/log/bootstrap.log
Obtaining hardware ID ...
Generating security keys ...
Registering the board ...
Configuring the board ...
Vehicle with VIN:YV1SW58D3623123 has registered successfully.

```

To provision a real board please issue the following command:
---------

```bash
# v-bootstrap board
Unplug device before continue [Y/n]: 
Please plug-in device. Waiting for ...
/dev/ttyUSB0 - FT232R USB UART device detected. Continue: [Y/n]: 
Please, switch on your device 
  using the button near the sticker 'StarterKit'
  and wait for 5 seconds, then press 'y'
 [Y/n]: 
Starting the provision procedure ... find the whole log info in /home/<current-user-name>/.v_bootstrap/log/bootstrap.log
waiting for device ready (this may take a while) ...
waiting for device ready (this may take a while) ...
Obtaining hardware ID ...
HW ID=f888221bc323f9174d7745cc5c377d23
Generating security keys ...
Registering the board ...
waiting for device ready (this may take a while) ...
Configuring the board ...
Vehicle with VIN:YV1SW58D6567007 has registered successfully.
```
