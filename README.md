# Quick WAF "paranoid" Evaluation 

<img src="https://user-images.githubusercontent.com/3140111/142721218-469e835e-cb27-4f17-913a-7aeb0665f905.png" width="650" height="650">

### Introduction to Paranoia Levels 

In essence, the Paranoia Level (PL) allows you to define how aggressive the Core Rule Set is. </br>
Reference: https://coreruleset.org/20211028/working-with-paranoia-levels/

### How it works 

The `wafparanoid.sh` bash script takes malicious requests using encoded payloads placed in different parts of HTTP requests based at the moment only on GET parameters, The results of the evaluation are recorded in the report debug file created on your machine.  
  
### Approach

`Pentester`: GreyBox Scope with limited access to WAFbox using a "shell" with privileges to start/reload WAF apache on DEV/STG enviroments sending diferent payloads</br>
`Secutity Officers`: Define the best level of paranoid for each solution  in your organization, customize virtual rules patches</br>
`Blueteamers`: Rule enforcement and best alerting less false positive/negative results for your organization</br>
`Integrators`: Define the adequate level of paranoid customizing rules according your webapp. </br>

