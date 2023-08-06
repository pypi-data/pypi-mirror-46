# Jskit

## Introduction
- A personal tool kit

## Installtion

```
pip install Jskit
```

- Upgrade form python3.5 to 3.6 in server

```
# sudo apt-get install software-properties-common

sudo add-apt-repository ppa:jonathonf/python-3.6 
sudo apt-get update 
sudo apt-get install python3.6
```

- Point pip to python3.6

```
sudo apt install python3-pip
python3.6 -m pip install --upgrade pip
sudo pip install --upgrade pip

sudo rm /usr/bin/python3
sudo ln -s /usr/bin/python3.6 /usr/bin/python3
PATH=/usr/bin:$PATH

```

- Upload

```
python setup.py sdist
twine upload dist/
```

## NOTE
- Since tkinter have some problems with the threading, it will cause infinite loop promblem and tkinter is needed in pyautogui of pymessagebox, so we can use gedit to become the copy content getter 

<del>
- Install tkinter to ensure pymessagebox works fine

```
sudo apt-get install python3-tk
```
</del>