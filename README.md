# Quick WAF "paranoid" Doctor Evaluation 

<img src="https://user-images.githubusercontent.com/3140111/142721218-469e835e-cb27-4f17-913a-7aeb0665f905.png" width="650" height="650">

### Introduction to Paranoia Levels 

In essence, the Paranoia Level (PL) allows you to define how aggressive the Core Rule Set is. </br>
Reference: https://coreruleset.org/20211028/working-with-paranoia-levels/

### How it works 

The `wafparanoid.sh` bash script takes malicious requests using encoded payloads placed in different parts of HTTP requests based at the moment only on GET parameters, The results of the evaluation are recorded in the report debug file created on your machine. 

### Approach

`Pentester`: GreyBox scope with limited access to WAF Linux box using a "shell" with privileges to start/reload WAF Apache on DEV/STG/TEST enviroments sending diferent payloads.</br>
`Secutity Officers`: Take the best desicion to apply the level of WAF paranoid for each solution in your organization. </br>
`Blueteamers`: Rule enforcement, best alerting , less false positive/negative results in your organization. </br>
`Integrators`: Define the adequate level of WAF paranoid quickly customizing rules or creating virtal patches. </br>

### Proof of Concept: Based on Ubuntu 20.04.3 and CRS 3.3.0 
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
3. Near the top of the file, you’ll see `SecRuleEngine DetectionOnly`. Change DetectionOnly to `On`. </br>

  Original value: `SecRuleEngine DetectionOnly` </br>
  New value: `SecRuleEngine On` </br>

4. Save changes. </br>
5. Restart Apache: </br>
`$ sudo systemctl restart apache2`

