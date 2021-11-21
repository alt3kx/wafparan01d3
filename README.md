# Quick WAF "paranoid" Doctor Evaluation 

<h1 align="center">
  <a href="https://github.com/alt3kx/wafparanoid/"><img src="https://user-images.githubusercontent.com/3140111/142735562-7f223d9c-0da0-485c-9d06-e256ee7bdabd.png" alt="wafparanoid" width="500" height="500"></a>
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
</p>

### Introduction to Paranoia Levels 

In essence, the Paranoia Level (PL) allows you to define how aggressive the Core Rule Set is. </br>
Reference: https://coreruleset.org/20211028/working-with-paranoia-levels/

### How it works 

- The `wafparan01d3.sh` bash script takes malicious requests using encoded payloads placed in different parts of HTTP requests based at the moment only on GET parameters, The results of the evaluation are recorded in the report debug file created on your machine. 
- Observe the behavior and response for each WAF paranoia level setting different attacks or payloads by using the default config level.
- The PoC below provide de basic installation and configuration from scratch and re-use byself the current WAF deployed by settting a basic "Mock" and simulate the backend.
- The detault payload avaiable was called `mysql_gosecure.txt` based on the research "A Scientific Notation Bug in MySQL left AWS WAF Clients Vulnerable to SQL Injection" from gosecure available here https://www.gosecure.net/blog/2021/10/19/a-scientific-notation-bug-in-mysql-left-aws-waf-clients-vulnerable-to-sql-injection/ evaluating our WAFs in their different levels of paranoia either in a default configuration or by disabling different rules / IDs in a staggered and quick way.

### Approach

- `Pentester`: GreyBox scope with limited access to WAF Linux box using a "shell" with privileges to start/reload and edit WAF Apache config files on DEV/STG/TEST enviroments sending diferent payloads.</br>
- `Secutity Officers`: Take the best desicion to apply the level of WAF paranoid for each solution in your organization. </br>
- `Blueteamers`: Rule enforcement, best alerting , less false positive/negative results in your organization. </br>
- `Integrators`: Define the adequate level of WAF paranoia quickly customizing rules or creating virtual patches. </br>

### Proof of Concept: Based on Ubuntu 20.04.3 and OWASP Core Rule Set (CRS) v3.3.2 
Reference: https://www.inmotionhosting.com/support/server/apache/install-modsecurity-apache-module/ </br>

#### Initial installation 
1. Update software repos: </br>
`$ sudo apt update -y && apt dist-upgrade -you`
2. Install Essentials: </br>
`$ sudo apt-get install build-essential`
3. Install apache2 for ubuntu (if it is not installed): </br>
`$ sudo apt-get install apache2`
4. Download and install the ModSecurity Apache module: </br>
`$ sudo apt install libapache2-mod-security2`
5. Install curl for ubuntu (if it is not installed): </br>
`$ sudo apt-get install curl vim gridsite-clients`
6. Type `Y`.
7. Restart the Apache service: </br>
`$ sudo systemctl restart apache2`
8. Ensure the installed software version is at least 2.9: </br>
`$ apt-cache show libapache2-mod-security2 `

#### Configure ModSecurity 
1. Copy and rename the file: </br>
`$ sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf` </br>
Next, change the ModSecurity detection mode. First, move into the `/etc/modsecurity` folder: </br>
2. Edit the ModSecurity configuration file with vi, vim, emacs, or nano. </br>
`$ sudo vi /etc/modsecurity/modsecurity.conf`
3. Near the top of the file, you’ll see `SecRuleEngine DetectionOnly`. Change `DetectionOnly` to `On`. </br>

  Original value: `SecRuleEngine DetectionOnly` </br>
  New value: `SecRuleEngine On` </br>

4. Save changes. </br>
5. Restart Apache: </br>
`$ sudo systemctl restart apache2`

#### Download OWASP Core Rule Set 
1. Download the latest CRS from CoreRuleSet.org/installation </br>
`$ wget https://github.com/coreruleset/coreruleset/archive/refs/tags/v3.3.2.zip`
2. Verify the checksum, be sure match of public available here: https://coreruleset.org/installation/ </br>
`$ sha1sum v3.3.2.zip && echo ProvidedChecksum` </br>
88f336ba32a89922cade11a4b8e986f2e46a97cf  v3.3.2.zip</br>
ProvidedChecksum </br>
alex@ubuntu:~$ `</br>
3. Uncompress the zip file. </br>
`$ unzip v3.3.2.zip`
4. Move the CRS setup file from the new directory into your ModSecurity directory:  </br>
`$ sudo mv coreruleset-3.3.2/crs-setup.conf.example /etc/modsecurity/crs-setup.conf` </br>
  (Optional but recommended) Move the rules directory from the new directory to your ModSecurity directory:  </br>
`$ sudo mv coreruleset-3.3.2/rules/ /etc/modsecurity/`
5. Edit your Apache security2.conf file to ensure it’ll load ModSecurity rules:  </br>
`$ sudo vim /etc/apache2/mods-enabled/security2.conf` 

```     IncludeOptional /etc/modsecurity/crs-setup.conf
        IncludeOptional /etc/modsecurity/rules/*.conf

        # Include OWASP ModSecurity CRS rules if installed
        #IncludeOptional /usr/share/modsecurity-crs/*.load
```
6. Ensure both the default ModSecurity and new CRS configuration files are listed. The first line conf file path may already be included. 
The second file path should be wherever you moved the /rules directory.  </br>
7. Edit /etc/apache2/apache2.conf  </br>
`$ sudo vim /etc/apache2/apache2.conf`

```     Include /etc/modsecurity/modsecurity.conf
        Include /etc/modsecurity/crs/crs-setup.conf
        Include /etc/modsecurity/crs/rules/*.conf 
```

#### Apache Load Modules Rewrite & Proxy
1. Copy the following modules. Enable Proxy and Rewrite module.  </br>
``` 
$ /etc/apache2
$ sudo cp mods-available/proxy_http.load mods-enabled
$ sudo cp mods-available/proxy.load mods-enabled/
$ sudo cp mods-available/rewrite.load mods-enabled/
```

2. Restart Apache </br>
`$ sudo systemctl restart apache2`

#### Add Virtualhosts for testing "Mocks"
1. Add ports </br>
Edit `/etc/apache2/ports.conf`, add the following lines:

```
Listen 8080
Listen 18080
```

2. Go to `/etc/apache2/sites-enabled`, create the file `001-test.conf` </br>
Copy & Paste the following code. </br>

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
Copy & Paste the following code. </br>

```
<VirtualHost 127.0.0.1:18080>

        ErrorLog ${APACHE_LOG_DIR}/moc_error.log
        CustomLog ${APACHE_LOG_DIR}/moc_access.log combined

        RewriteEngine On
        RewriteRule ^(.*)$ $1 [R=200,L]
</VirtualHost>
```

4. Restart apache </br>
`$ sudo systemctl restart apache2` </br>
5. Create the file sqlrules.conf inside of /etc/apache2/conf-enabled </br>
`$ sudo touch /etc/apache2/conf-enabled/sqlrules.conf`
6. Reload Apache </br>
`$ sudo service apache2 reload`

### How do I use it 
For help you can make use of the `help` option. The basic usage is to pass diferent arguments defined. </br>
Example: </br>

```
$ sudo ./wafparan0id3.sh help 

           (                                  )   ) (       )  
 (  (      ))\ )          ) (      )        ( /(( /( )\ ) ( /(  
 )\))(  ( /(()/( `  )  ( /( )(  ( /(  (     )\())\()|()/( )\()) 
((_)()\ )(_))(_))/(/(  )(_)|()\ )(_)) )\ ) ((_)((_)\ ((_)|(_)\  
_(()((_|(_)(_) _((_)_\((_)_ ((_|(_)_ _(_/( /  (_) (_)_| |__ (_) 
\ V  V / _` |  _| '_ \) _` | '_/ _` | ' \)) () || |/ _` ||_ \   
 \_/\_/\__,_|_| | .__/\__,_|_| \__,_|_||_| \__/ |_|\__,_|___/   
                |_|                                             

                    ~ WAFPARANO1D3 : v1.0 ~
     The Web Application Firewall Paranoia Level Test Tool.
    
[*] Checking https://example.org
[+] The site https://example.org is behind Edgecast (Verizon Digital Media) WAF.
[~] Number of requests: 2
`                                                                      
```
### Demos 
You can try `wafparan01d3.sh` by running the demo environment that deploys WAF ModSecurity & 'Mock' using latest OWASP Core Rule Set `CRS 3.3.2` and `wafparan01d3.sh` evaluating ModSecurity paranoia levels easyble customizable. 


