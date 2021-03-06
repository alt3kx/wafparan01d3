# Quick WAF "paranoid" Doctor Evaluation 

<h1 align="center">
  <a href="https://github.com/alt3kx/wafparanoid/"><img src="https://user-images.githubusercontent.com/3140111/142735562-7f223d9c-0da0-485c-9d06-e256ee7bdabd.png" alt="wafparano1d3" width="500" height="500"></a>
  <br>
  WAFPARAN01D3
</h1>
<p align="center">
  <b>The Web Application Firewall Paranoia Level Test Tool.</b>
  <br>
  <b>
    &mdash; From <a href="https://alt3kx.github.io">alt3kx.github.io</a>
  </b>
</p>
<p align="center">
  <a href="https://docs.python.org/3/download.html">
    <img src="https://img.shields.io/badge/Python-3.x/2.x-green.svg">
  </a>
  <a href="https://github.com/alt3kx/wafparan01d3/releases">
    <img src="https://img.shields.io/badge/Version-v1.1%20(stable)-blue.svg">
  </a>
  <a href="https://github.com/alt3kx/wafparan01d3/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-GNU%20General%20v3.0-orange">
  </a> 

</p>

### Introduction to Paranoia Levels 

In essence, the Paranoia Level (PL) allows you to define how aggressive the Core Rule Set is. </br>
Reference: https://coreruleset.org/20211028/working-with-paranoia-levels/

### How it works 

- The `wafparan01d3.py` python3 script takes malicious requests using encoded payloads placed in different parts of HTTP requests based on GET parameters, The results of the evaluation are recorded in the report debug file `wafparan01d3.log` created on your machine. 
- Observe the behavior and response for each WAF paranoia level setting different attacks or payloads by using the default config level.
- The PoC below provide de basic installation and configuration from scratch and re-use byself the current WAF deployed by settting a basic "Mock" and simulate the backend.
- The default payloads avaiable was called `mysql_gosecure.txt` based on the research "A Scientific Notation Bug in MySQL left AWS WAF Clients Vulnerable to SQL Injection" from gosecure available here https://www.gosecure.net/blog/2021/10/19/a-scientific-notation-bug-in-mysql-left-aws-waf-clients-vulnerable-to-sql-injection/ evaluating our WAFs using modsecurity in their different levels of paranoia either in a default configuration or by disabling different rules / IDs in a staggered and quick way.

<p align="center"><img src="https://user-images.githubusercontent.com/3140111/142755697-50db1851-5c28-4ccd-a94d-4bbb4a26a90c.png"></p>

### Approach

- `Pentesters`: GreyBox scope with limited access to WAF Linux box using a "shell" with privileges to start/reload and edit WAF Apache config files on DEV/STG/TEST enviroments sending diferent payloads.</br>
- `Secutity Officers`: Take the best decision to apply the level of WAF paranoia for each solution in your organization. </br>
- `Blueteamers`: Rule enforcement, best alerting , less false positive results in your organization. </br>
- `Integrators`: Perform a depper troubheshooting and define the adequate level of WAF paranoia quickly customizing rules or creating virtual patches. </br>

### Proof of Concept: Based on Ubuntu 20.04.3 and OWASP Core Rule Set (CRS) v3.3.2 
Reference: https://www.inmotionhosting.com/support/server/apache/install-modsecurity-apache-module/ </br>

#### Initial installation 
1. Update software repos: </br>
```
$ sudo apt update -y && sudo apt dist-upgrade -y
```
2. Install Essentials: </br>
```
$ sudo apt-get install build-essential -y
```
3. Install apache2 for ubuntu (if it is not installed): </br>
```
$ sudo apt-get install apache2 -y
```
4. Download and install the ModSecurity Apache module: </br>
```
$ sudo apt install libapache2-mod-security2 -y
```
5. Install curl for ubuntu (if it is not installed): </br>
```
$ sudo apt-get install curl vim gridsite-clients net-tools -y
```
6. Restart the Apache service: </br>
```
$ sudo systemctl restart apache2
```
7. Ensure the installed software version is at least 2.9.x: </br>
```
$ sudo apt-cache show libapache2-mod-security2
```
![install](https://user-images.githubusercontent.com/3140111/142753216-8e03966a-64b6-4076-afa8-1677a43241bf.png)

#### Configure ModSecurity 
1. Copy and rename the file: </br>
```
$ sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
```
Next, change the ModSecurity detection mode. First, move into the `cd /etc/modsecurity` folder </br>
2. Edit the ModSecurity configuration file with vi, vim, emacs, or nano. </br>
```
$ sudo vim /etc/modsecurity/modsecurity.conf
```
3. Near the top of the file, you???ll see `SecRuleEngine DetectionOnly`. Change `DetectionOnly` to `On`. </br>

  Original value: `SecRuleEngine DetectionOnly` </br>
  New value: `SecRuleEngine On` </br>
  
![modsec](https://user-images.githubusercontent.com/3140111/142753438-1b9d687b-e6fd-4b80-b172-46e4f59e4916.png)

4. Save changes. </br>
5. Restart Apache: </br>
```
$ sudo systemctl restart apache2
```
#### Download OWASP Core Rule Set 
1. Download the latest CRS from CoreRuleSet.org/installation </br>
```
$ cd ~
$ wget https://github.com/coreruleset/coreruleset/archive/refs/tags/v3.3.2.zip
```
2. Verify the checksum, be sure match of public available here: https://coreruleset.org/installation/ </br>
```
$ sha1sum v3.3.2.zip && echo ProvidedChecksum
88f336ba32a89922cade11a4b8e986f2e46a97cf  v3.3.2.zip
ProvidedChecksum 
```
![checksum](https://user-images.githubusercontent.com/3140111/142753669-85f62be6-edf8-4244-be51-8ac8b7c22ebd.png)

3. Uncompress the zip file. </br>
```
$ unzip v3.3.2.zip
```
4. Move the CRS setup file from the new directory into your ModSecurity directory:  </br>
```
$ sudo mv coreruleset-3.3.2/crs-setup.conf.example /etc/modsecurity/crs/crs-setup.conf
```
- (Optional but recommended) Move the rules directory from the new directory to your ModSecurity directory:  </br>
```
$ sudo mv coreruleset-3.3.2/rules/ /etc/modsecurity/crs/
```
5. Edit your Apache security2.conf file to ensure it???ll load ModSecurity rules:  </br>
```
$ sudo vim /etc/apache2/mods-enabled/security2.conf
```
```    
<IfModule security2_module>
        # Default Debian dir for modsecurity's persistent data
        SecDataDir /var/cache/modsecurity

        # Include all the *.conf files in /etc/modsecurity.
        # Keeping your local configuration in that directory
        # will allow for an easy upgrade of THIS file and
        # make your life easier
        IncludeOptional /etc/modsecurity/crs-setup.conf
        IncludeOptional /etc/modsecurity/rules/*.conf

        # Include OWASP ModSecurity CRS rules if installed
        #IncludeOptional /usr/share/modsecurity-crs/*.load
</IfModule>

```
![secmodule](https://user-images.githubusercontent.com/3140111/142803377-1463b5f9-0532-497e-9134-52e7f52a2555.png)

6. Ensure both the default ModSecurity and new CRS configuration files are listed. The first line conf file path may already be included. 
The second file path should be wherever you moved the /rules directory.  </br>
7. Edit /etc/apache2/apache2.conf  </br>
```
$ sudo vim /etc/apache2/apache2.conf
```
Copy & Paste the following code and save it. </br>
```     
# Include list of ports to listen on
Include ports.conf

Include /etc/modsecurity/modsecurity.conf
Include /etc/modsecurity/crs/crs-setup.conf
Include /etc/modsecurity/crs/rules/*.conf
```
![ports](https://user-images.githubusercontent.com/3140111/142803549-079b5c29-bb07-442e-9137-9abd8a16ce90.png)

#### Apache Load Modules Rewrite & Proxy
1. Copy the following modules. Enable Proxy and Rewrite module.  </br>
``` 
$ cd /etc/apache2
$ sudo cp mods-available/proxy_http.load mods-enabled
$ sudo cp mods-available/proxy.load mods-enabled/
$ sudo cp mods-available/rewrite.load mods-enabled/
```
2. Restart Apache </br>
```
$ sudo systemctl restart apache2
```
#### Add Virtualhosts for testing "Mocks"
1. Add ports, edit `/etc/apache2/ports.conf` </br>
```
$ sudo vim /etc/apache2/ports.conf
```
Copy & Paste the following code and save it. </br>
```
# If you just change the port or add more ports here, you will likely also
# have to change the VirtualHost statement in
# /etc/apache2/sites-enabled/000-default.conf

Listen 8080
Listen 18080

<IfModule ssl_module>
        Listen 443
</IfModule>

<IfModule mod_gnutls.c>
        Listen 443
</IfModule>
```
![ports2](https://user-images.githubusercontent.com/3140111/142804122-68fa4b21-2e82-4ef1-8fb8-1386ebd4c2c3.png)

2. Go to `/etc/apache2/sites-enabled`, create the file `001-test.conf` </br>
```
$ cd /etc/apache2/sites-enabled/
$ sudo touch 001-test.conf
$ sudo vim 001-test.conf
```
Copy & Paste the following code and save it. </br>
```     
<VirtualHost *:8080>
        ServerName test.domain:8080

        SecRuleEngine On

        ErrorLog ${APACHE_LOG_DIR}/test_error.log
        CustomLog ${APACHE_LOG_DIR}/test_access.log combined
        SecAuditLog ${APACHE_LOG_DIR}/test_audit.log

        ProxyPass / http://127.0.0.1:18080/
        ProxyPassReverse / http://127.0.0.1:18080/
</VirtualHost>
```
3. Go to `/etc/apache2/sites-enabled`, create the file `002-moc.conf` </br>
```
$ cd /etc/apache2/sites-enabled/
$ sudo touch 002-moc.conf
$ sudo vim 002-moc.conf
```
Copy & Paste the following code and save it. </br>
```
<VirtualHost 127.0.0.1:18080>

        ErrorLog ${APACHE_LOG_DIR}/moc_error.log
        CustomLog ${APACHE_LOG_DIR}/moc_access.log combined

        RewriteEngine On
        RewriteRule ^(.*)$ $1 [R=200,L]
</VirtualHost>
```
4. Restart apache </br>
```
$ sudo systemctl restart apache2
```
5. Create the file `wafparan01d3_rulesremove.conf` inside of /etc/apache2/conf-enabled </br>
```
$ sudo touch /etc/apache2/conf-enabled/wafparan01d3_rulesremove.conf
```
6. Reload Apache 
```
$ sudo service apache2 reload
```
#### Test your FE and BE (mock)
```
Must be specify a domain , edit the following lines  

Windows:
C:\Windows\System32\drivers\etc\hosts
192.168.56.106 test.domain <-- add this line and specify your IP address  

Linux: 
/etc/hosts
192.168.1.23 test.domain <-- add this line and specify your IP address 

$ curl -i -k -s -XGET http://test.domain:8080/
HTTP/1.1 200 OK
Date: Mon, 22 Nov 2021 06:31:41 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Length: 571
Content-Type: text/html; charset=iso-8859-1
Vary: Accept-Encoding

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>200 OK</title>
</head><body>
<h1>OK</h1>
<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator at 
 [no address given] to inform them of the time this error occurred,
 and the actions you performed just before this error.</p>
<p>More information about this error may be available
in the server error log.</p>
<hr>
<address>Apache/2.4.41 (Ubuntu) Server at 127.0.0.1 Port 18080</address>
</body></html>

$ curl -i -k -s -XGET http://localhost:18080/
HTTP/1.1 200 OK
Date: Mon, 22 Nov 2021 06:27:17 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Length: 571
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>200 OK</title>
</head><body>
<h1>OK</h1>
<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator at 
 [no address given] to inform them of the time this error occurred,
 and the actions you performed just before this error.</p>
<p>More information about this error may be available
in the server error log.</p>
<hr>
<address>Apache/2.4.41 (Ubuntu) Server at localhost Port 18080</address>
</body></html>

```
### How do I use it 
For help you can make use of the `help` option. The basic usage is to pass diferent arguments defined. </br>
Example: </br>

```
$ sudo python3 wafparan01d3.py -h 

           (                                  )   ) (       )
 (  (      ))\ )          ) (      )        ( /(( /( )\ ) ( /(
 )\))(  ( /(()/( `  )  ( /( )(  ( /(  (     )\())\()|()/( )\())
((_)()\ )(_))(_))/(/(  )(_)|()\ )(_)) )\ ) ((_)((_)\ ((_)|(_)\
_(()((_|(_)(_) _((_)_\((_)_ ((_|(_)_ _(_/( /  (_) (_)_| |__ (_)
\ V  V / _` |  _| '_ \) _` | '_/ _` | ' \)) () || |/ _` ||_ \
 \_/\_/\__,_|_| | .__/\__,_|_| \__,_|_||_| \__/ |_|\__,_|___/
                |_|

                    ~ WAFPARANO1D3 : v1.1 ~
     The Web Application Firewall Paranoia Level Test Tool.

usage: wafparan01d3.py [-h] [--run [_RUN]] [--debug [_DEBUG]] [--pl [_PARANOIALEVEL ...]] [--proxy [_PROXY]] [--payload [_PAYLOAD]] [--rules-remove [_RULESREMOVE]] [--log [_LOG]] [--domain [_DOMAIN]] [--conf-file [_CONF_FILE]]
                       [--time-sleep [_TIME_TO_SLEEP]] [--time-sleep-request [_TIME_TO_SLEEP_REQUEST]] [--desc [_DESC]] [--output-desc [_OUTPUT_DESC]]

optional arguments:
  -h, --help            show this help message and exit
  --run [_RUN]          Run script
  --debug [_DEBUG]      Debug mode
  --pl [_PARANOIALEVEL ...]
                        Define paranoia level Ex. -pl 2
  --proxy [_PROXY]      Define Proxy. Ex: http://127.0.0.1:8081
  --payload [_PAYLOAD]  Define payload file. Ex. --payload payload2.txt
  --rules-remove [_RULESREMOVE]
                        Define rules remove file. Ex. --rules-remove rules1.txt
  --log [_LOG]          Define path of the log file. Ex. --log /var/log/apache/wafparan01d3.log
  --domain [_DOMAIN]    Define your domain. Ex. --domain example.domain:8080
  --conf-file [_CONF_FILE]
                        Define configuration file. Ex. --conf-file /opt/modsecurity/crs/rules/INITIALIZATION.conf
  --time-sleep [_TIME_TO_SLEEP]
                        Sleep time per PL. Ex. --time-sleep 3
  --time-sleep-request [_TIME_TO_SLEEP_REQUEST]
                        Sleep time per Request. Ex. --time-sleep-request 3
  --desc [_DESC]        Description of the script and authors
  --output-desc [_OUTPUT_DESC]
                        Description of the output on console mode.
                                                              
```
### Optional Arguments 

```
$ sudo python3 wafparan01d3.py -h 
	- show the help message

$ sudo python3 wafparan01d3.py --run
	- run the script with default options.

$ sudo python3 wafparan01d3.py --run --debug
	- Print every line on console.
	
$ sudo python3 wafparan01d3.py --run --pl 1
	- Run the script in assigned Paranoia Level.
	- By default runs on Paranoia Level 1, 2, 3, 4

$ sudo python3 wafparan01d3.py --run --payload file_payload2.txt
	- Define the payload file that you want to send to WAF.
	- By default takes the file mysql_gosecure.txt

$ sudo python3 wafparan01d3.py --run --rules-remove rules_removex.txt
	- Define the rules that you want to remove on GWAF.
	- Example of the file: 
		- Default 920000 920001 920002
	- By default takes the files: rules_remove1.txt, rules_remove2.txt, rules_remove3.txt, rules_remove4.txt

$ sudo python3 wafparan01d3.py --run --log /home/waf_user/paranoia.log
	- Define LOG File.
	- By default print the log on paranoia_debug.log

$ sudo python3 wafparan01d3.py --run --domain mydomain.test.com
	- Define Domain of Front End WAF.
	- By default runs over domain domain.test:8080
	
$ sudo python3 wafparan01d3.py --run --conf-file /opt/modsecurity/crs/rules/INITIALIZATION.conf
	- Define the configuration file to update the Paranoia Level
	- By default takes /etc/modsecurity/crs/rules/REQUEST-901-INITIALIZATION.conf

$ sudo python3 wafparan01d3.py --run --time-sleep 3
	- Define the time to sleep per Paranoia Level.

$ sudo python3 wafparan01d3.py --run --time-sleep-request 2
	- Define the time to sleep per request send to WAF.

$ sudo python3 wafparan01d3.py --desc
	- Print the description of the script and the authors.
```
### Demos 
You can try `wafparan01d3.py` by running the VM environment (Ubuntu) that deploys WAF ModSecurity & 'Mock' using latest OWASP Core Rule Set `CRS 3.3.2` evaluating ModSecurity paranoia levels easyble customizable. 

To run: 

```
$ git clone https://github.com/alt3kx/wafparan01d3.git
$ cd wafparan01d3
$ sudo python3 wafparan01d3.py --help 
```

```
$ sudo python3 wafparan01d3.py --run
```
![wafparan01d3_001](https://user-images.githubusercontent.com/3140111/142825261-cecb5d7f-6cec-440e-874c-45f062c02168.gif)

```
$ sudo python3 wafparan01d3.py --run --debug --proxy http://192.168.56.1:8081
```
![wafparan01d3_002](https://user-images.githubusercontent.com/3140111/142826789-f293ab85-9e79-4c1b-998b-da96bd938369.gif) 
```
$ sudo python3 wafparan01d3.py --run --debug --pl 1 2 --proxy http://192.168.56.1:8081 --log test.log --domain vulnerable.domain:8080 --time-sleep-request 1 --time-sleep 1 --rules-remove my_rules_remove.txt --payload my_payload.txt
```
![wafparan01d3_003](https://user-images.githubusercontent.com/3140111/142825338-ee032136-4da9-40a5-963f-bf5a3f34690a.gif)

## WAF Rule Scientific Notation
https://github.com/mindhack03d/WAF-Rule-Scientific-Notation

### Authors
Alex Hernandez aka <em><a href="https://twitter.com/_alt3kx_" rel="nofollow">(@\_alt3kx\_)</a></em></br>
Jesus Huerta aka <em><a href="https://github.com/mindhack03d" rel="nofollow">@mindhack03d</em> </a>

