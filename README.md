# Instructions for setting up NAO SDK on the Ubuntu VMs on the lab PCs
The lab PCs should already have the SDK installed (try "wsl --install"); if there is an error or the Ubuntu shell does not launch, then follow the fresh installation instructions directly below. Otherwise, if installation looks clean, skip straight to the teleoperation section.

## setting up NAOqi 2.8 SDK on Ubuntu 24.04 WSL instance
```wsl —install```
	set username and password
	hilab1: gatechhilab1
	hilab2: gatechhilab2
```python3 —version```
```nano ~/.bashrc```
write ```alias python="python3" ```
	ctrl+X
	select Y
```source ~/.bashrc```
```python —version```
```sudo apt-get update```
```sudo apt-get install python3-pip```
```sudo apt-get install cmake```
```sudo apt-get install python3-venv```
```mkdir nao```
```cd nao```
```python3 -m venv nao_venv```
```source nao_venv/bin/activate``` (to exit: ```deactivate```)
```python3 -m pip install qi```

## loading Ubuntu 24.04 WSL instance (if WSL instance is already installed)
```wsl —install```

# Teleoperating the NAO
The NAO uses the qi framework as the primary API for programming the NAO. The qi framework supports Python 3. (It used to be called naoqi, but that framework has been deprecated since it supported Python 2.x only.) To learn how the API works, visit [the Aldebaran NAOqi v2.8 docs](http://doc.aldebaran.com/2-8/dev/libqi/api/python/index.html#py-api-index) for general information on using the qi framework to program NAO. 

Of particular interest to the teleoperator is the [Python qi API framework](http://doc.aldebaran.com/2-8/dev/libqi/api/python/index.html#py-api-index) page, the [qi.Application](http://doc.aldebaran.com/2-8/dev/libqi/api/python/application.html) page, and the [ALDialog](http://doc.aldebaran.com/2-8/naoqi/interaction/dialog/aldialog-api.html#aldialog-api) module page.

```teleop_test.py``` contains the skeleton for a basic NAO program. When run, NAO will verbalize scripted utterances (lines 11-13) with its default gestures, which can be reprogrammed using the ALMotion APIs. The program will run until the operator manually quits (ctrl+C) the program in the terminal.

First, download this repository onto the lab PC. Then, navigate to this repository through the Ubuntu VM terminal. 

To run the test Python script on NAO, use the following command:

```python3 <filepath/teleop_test.py> --qi-url=tcp://<robot's IP address>:<port>```

where ```<filepath/teleop_test.py>``` is the file path to the script (likely "~/nao/nao-game-bridge/teleop_test.py"), ```<robot's IP address>``` is the IP address of the NAO in the 192.168.XX.XX format (IP address can be gained from pressing NAO's chest button once while it's fully booted), and ```<port>``` is the port the robot is listening on (most of the time, it's port **9559** – don't worry about how ports work, it's mostly for client-server communication with server.py).



