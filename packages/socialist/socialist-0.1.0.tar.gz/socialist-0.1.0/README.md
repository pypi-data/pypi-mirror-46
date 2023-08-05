# SociaList - Tool based on Social Engineering

SociaList is an open-source tool dedicated to the creation of password lists based on information 
collected through social engineering.

What is social engineering?
---------------------------

Social engineering is the term used for a broad range of malicious activities accomplished through human interactions. It uses psychological manipulation to trick users into making security mistakes or giving away sensitive information.

Attacks happen in one or more steps. A perpetrator first investigates the intended victim to gather necessary background information, such as potential points of entry and weak security protocols, needed to proceed with the attack. Then, the attacker moves to gain the victim’s trust and provide stimuli for subsequent actions that break security practices, such as revealing sensitive information or granting access to critical resources. What makes social engineering especially dangerous is that it relies on human error, rather than vulnerabilities in software and operating systems. Mistakes made by legitimate users are much less predictable, making them harder to identify and thwart than a malware-based intrusion.

For more information about social engineering attacks check [social engineering attacks].

Requirements
-------------------
  - python 3
  - tqdm
  - phonenumbers
  - validate_email
  - py3dns
  
Installation
-------------

**Linux**

 ```
 apt-get install python3-pip
 git clone https://github.com/OverwatchHeir/SociaList.git
 cd SociaList
 python3 -m pip install -r requirements.txt
 ```
 
**MacOS**
 ```
 brew install python3
 brew install pip
 git clone https://github.com/OverwatchHeir/SociaList.git
 cd SociaList
 python3 -m pip install -r requirements.txt
 ```
 **Windows**
 
 Download python 3 and pip from [python webpage] and then: 
 ```
 git clone https://github.com/OverwatchHeir/SociaList.git
 cd SociaList
 python3 -m pip install -r requirements.txt
 ```
 **Alternative**
 
 Using the traditional installation from **pip** or **easy_install**
 ```
 easy_install3 -U pip # you have to install python3-setuptools , update pip
 pip3 install tqdm
 pip3 install phonenumbers
 pip3 install validate_email
 pip3 install py3dns
 pip3 install socialist
 socialist # installed successfully
 ```
Usage
---------

**Run**

```$ python3 socialist.py [-h] -o OUTPUT [-c COMBINATIONS]```

At the beginning of the execution of this script, you will be asked for a series of personal information about which you intend to create the list of passwords. From the personal data entered by keyboard, combinations and permutations will be made according to those entered in the arguments.
 
**Options**
```
optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        path to output wordlist
  -c COMBINATIONS, --combinations COMBINATIONS
                        maximum number of words combinations -- default 2
```

Contributing
---------------

For bug reports or enhancements, please open an [issue] here.

[social engineering attacks]: https://www.incapsula.com/web-application-security/social-engineering-attack.html
[issue]: https://github.com/OverwatchHeir/SociaList/issues
[python webpage]: https://www.python.org/


