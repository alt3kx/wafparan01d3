# Quick WAF "paranoid" Evaluation 

<img src="https://user-images.githubusercontent.com/3140111/142721218-469e835e-cb27-4f17-913a-7aeb0665f905.png" width="650" height="650">

### Introduction to Paranoia Levels 

In essence, the Paranoia Level (PL) allows you to define how aggressive the Core Rule Set is. </br>
Reference: https://coreruleset.org/20211028/working-with-paranoia-levels/

### How it works 

The `wafparanoid.sh` bash script takes malicious requests using encoded payloads placed in different parts of HTTP requests based at the moment only on GET parameters, The results of the evaluation are recorded in the report debug file created on your machine.  

### Approach

`Pentester`: GreyBox scope with limited access to WAF Linux box using a "shell" with privileges to start/reload WAF apache on DEV/STG/TEST enviroments sending diferent payloads.</br>
`Secutity Officers`: Take the best desicion to apply the level of WAF paranoid for each solution in your organization</br>
`Blueteamers`: Rule enforcement and best alerting less false positive/negative results for your organization</br>
`Integrators`: Define the adequate level of WAF paranoid customizing rules, according your webapp. </br>

### PoC using Ubuntu Linux Box 
