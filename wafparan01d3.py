#!/usr/bin/python3
#
#  WAFPARAN01D3 v1.0 Released (c) 2021
#
#  The Web Application Firewall Paranoia Level Test Tool.
#
#  Author: Alex Hernandez (aka alt3kx)
#  Author: Jesus Huerta (aka mindhack03d)
#  Release date:  22 Nov 2021
#  Version: v1.1
#  Tested on: Linux Ubuntu and OWASP CRS v3.3.2
#  Visit my site https://alt3kx.github.io
#  Visit my site https://github.com/mindhack03d
#
#  Usage: python3 wafparan0id3.py --help
#


import io, os, json, sys, argparse, subprocess, re, time

#-------------------
# GLOBAL VARIABLES
#-------------------
domain_def='test.domain:8080'
payload_file="mysql_gosecure.txt"
payload_len=30
pl_array=["1", "2", "3", "4"]
f_rr_pl1=['rules_remove1.txt', 'rules_remove2.txt', 'rules_remove3.txt', 'rules_remove4.txt']
banner = """
           (                                  )   ) (       )
 (  (      ))\ )          ) (      )        ( /(( /( )\ ) ( /(
 )\))(  ( /(()/( `  )  ( /( )(  ( /(  (     )\())\()|()/( )\())
((_)()\ )(_))(_))/(/(  )(_)|()\ )(_)) )\ ) ((_)((_)\ ((_)|(_)\\
_(()((_|(_)(_) _((_)_\((_)_ ((_|(_)_ _(_/( /  (_) (_)_| |__ (_)
\ V  V / _` |  _| '_ \) _` | '_/ _` | ' \)) () || |/ _` ||_ \\
 \_/\_/\__,_|_| | .__/\__,_|_| \__,_|_||_| \__/ |_|\__,_|___/
                |_|

                    ~ WAFPARANO1D3 : v1.1 ~
     The Web Application Firewall Paranoia Level Test Tool.
"""

banner_desc="""  WAFPARAN01D3 v1.0 Released (c) 2021

  The Web Application Firewall Paranoia Level Test Tool.

  Author: Alex Hernandez (aka alt3kx)
  Author: Jesus Huerta (aka mindhack03d)
  Release date:  22 Nov 2021
  Version: v1.1
  Tested on: Linux Ubuntu and OWASP CRS v3.3.2
  Visit my site https://alt3kx.github.io
  Visit my site https://github.com/mindhack03d

  Usage: python3 wafparan0id3.py --help
"""

banner_output="""[PL] = Paranoia Level
[RRBI] = Rule Remove By ID
[PP] = Payload Passed
[PB] = Payload Blocked

Example:
       [!][PL: 3] [RRBI: 942480] [PP: 0] [PB: 380] [LastStatus: 200] [Payload: %61%27%20%6f%72%20%27%32%2e%65[../snip]]]
"""

#-------------------
# DEFAILT PATH
#-------------------
sqlrules_remove="/etc/apache2/conf-enabled/wafparan01d3_rulesremove.conf"

def reload_apache():
	apache_response = subprocess.Popen("service apache2 reload", shell=True, stdout=subprocess.PIPE)
	return apache_response

def run_request(pl_extracted, file_to_rr, args):
	if args._log is not False:
		sqlrules_log = args._log
	else:
		sqlrules_log="wafparan01d3.log"
	read_rr = open(file_to_rr, 'r')
	ok_count = nok_count = 0
	payload_succ=""
	# Read Rules to Remove from ModSecurity
	for rr_line in read_rr.read().split(' '):
		add_rr = subprocess.Popen("echo \"SecRuleRemoveById " + str(rr_line) + "\" >> " + sqlrules_remove, shell=True, stdout=subprocess.PIPE)
		if args._payload is not False:
			payload_to_read = args._payload
		else:
			payload_to_read = "mysql_gosecure.txt"
		payload_read = open(payload_to_read,'r')
		# Read the Payload File
		for payload_line in payload_read.read().split('\n'):
			if bool(payload_line) is True:
				curl_request = "curl "
				if args._proxy is not False:
					curl_request += "-x " + args._proxy + " "
				curl_request += "-s -o /dev/null -w \"%{http_code}\" -X GET \"http://"
				if args._domain is not False:
					domain = args._domain
				else:
					domain = domain_def
				curl_request += domain + "/?id=" + str(payload_line).split('\n')[0] + "\" -H $\"Host: " + domain + "\" -H $'Accept: */*' -H $'User-Agent: testing' -H $'Connection: close'"
				curl_resp = subprocess.Popen(curl_request, shell=True, stdout=subprocess.PIPE)
				http_status = curl_resp.stdout.read().decode('ascii').split('\n')[0]
				payload_def=payload_line
				if bool(re.search("(1|2|3)[0-9][0-9]", str(http_status))) is True:
					ok_count += 1
				else:
					nok_count += 1
				if len(payload_def) >= payload_len:
					payload_def=payload_def[0:payload_len] + "[../snip]"
				if args._debug is True:
					print(" [!][PL: " + str(pl_extracted) + "] [RRBI: " + str(rr_line).split('\n')[0] + "] [PP: " + str(ok_count) + "] [PB: " + str(nok_count) + "] [LastStatus: " + str(http_status) + "] [Payload: " + payload_def + "]")
				else:
					print(" [!][PL: " + str(pl_extracted) + "] [RRBI: " + str(rr_line).split('\n')[0] + "] [PP: " + str(ok_count) + "] [PB: " + str(nok_count) + "] [LastStatus: " + str(http_status) + "] [Payload: " + payload_def + "]\t\b\r", end ='')
				add_log = subprocess.Popen("echo \" [!][ParanoiaLevel: " + str(pl_extracted) + "] [RulesRemoveById: " + str(rr_line).split('\n')[0] + "] [PayloadPassed: " + str(ok_count) + "] [PayloadBlocked: " + str(nok_count) + "] [CurrentStatus: " + str(http_status) + "] [CurrentPayload: " + payload_line + "]\" >> " + sqlrules_log, shell=True, stdout=subprocess.PIPE)
				if args._time_to_sleep_request is not False:
					time.sleep(int(args._time_to_sleep_request))
		payload_read.close()
	read_rr.close()
	

# Update Paranoia Level
def update_paranoia(paranoia_array, files_ruleremove, flag_type_rr, args):
	if args._conf_file is not False:
		modsec_initial=args._conf_file
	else:
		modsec_initial="/etc/modsecurity/crs/rules/REQUEST-901-INITIALIZATION.conf"
	for paranoia_line in paranoia_array:
		str_pl="sed -i \'s,    setvar:\\x27tx.paranoia_level=.*,    setvar:\\x27tx.paranoia_level=" + str(paranoia_line) + "\\x27\\\",g\' " + modsec_initial
		sed_resp = subprocess.Popen(str_pl, shell=True, stdout=subprocess.PIPE)
		null_resp = subprocess.Popen("cp /dev/null " + sqlrules_remove,  shell=True, stdout=subprocess.PIPE)
		pl_resp = subprocess.Popen("grep \"tx.paranoia_level=\" " + modsec_initial + " | cut -d\"=\" -f2 | cut -d\"\'\" -f1 ", shell=True, stdout=subprocess.PIPE)
		pl_extracted=str(pl_resp.stdout.read().decode('ascii').split('\n')[0]) 
		pl_resp = subprocess.Popen("echo \"#Paranoia Level " + pl_extracted  + " \" > " + sqlrules_remove, shell=True, stdout=subprocess.PIPE)
		apache_response = reload_apache()
		if flag_type_rr == "array":
			file_to_rr= str(f_rr_pl1[1 - int(paranoia_line)])
			run_request(pl_extracted, file_to_rr, args)
		else:
			file_to_rr = str(files_ruleremove)
			run_request(pl_extracted, file_to_rr, args)
		if args._time_to_sleep is not False:
			time.sleep(int(args._time_to_sleep))

# Select default Rules Remove File or
# select Custom Rules Remove File
def rules_remove(args):
	files_ruleremove=[]
	if args._rulesremove is False:
		files_ruleremove = f_rr_pl1
		flag_file_rr = True
		flag_type_rr = "array"
	else:
		files_ruleremove = args._rulesremove
		flag_file_rr= os.path.exists(files_ruleremove)
		flag_type_rr = "file"
	return files_ruleremove, flag_file_rr, flag_type_rr

# Select Default Paranoia Level or 
# Custom Paranoia Level
def paranoia_level(args):
	paranoia_array=[]
	if args._paranoialevel is True:
		paranoia_array = ["1", "2", "3", "4"]
	else:
		paranoia_array = args._paranoialevel
	return paranoia_array

if __name__ == "__main__":
	print(banner)
	parser = argparse.ArgumentParser()
	parser.add_argument('--run', nargs='?', dest='_run', default=False, const=True, help='Run script')
	parser.add_argument('--debug', nargs='?', dest='_debug', default=False, const=True, help='Debug mode')
	parser.add_argument('--pl', nargs='*', dest='_paranoialevel', default=True,  help='Define paranoia level Ex. -pl 2')
	parser.add_argument('--proxy', nargs='?', dest='_proxy', default=False, help='Define Proxy. Ex: http://127.0.0.1:8081')
	parser.add_argument('--payload', nargs='?', dest='_payload', default=False, help='Define payload file. Ex. --payload payload2.txt')
	parser.add_argument('--rules-remove', nargs='?', dest='_rulesremove', default=False, help='Define rules remove file. Ex. --rules-remove rules1.txt')
	parser.add_argument('--log', nargs='?', dest='_log', default=False, help='Define path of the log file. Ex. --log /var/log/apache/wafparan01d3.log')
	parser.add_argument('--domain', nargs='?', dest='_domain', default=False, help='Define your domain. Ex. --domain example.domain:8080')
	parser.add_argument('--conf-file', nargs='?', dest='_conf_file', default=False, help='Define configuration file. Ex. --conf-file /opt/modsecurity/crs/rules/INITIALIZATION.conf')
	parser.add_argument('--time-sleep', nargs='?', dest='_time_to_sleep', default=False, help='Sleep time per PL. Ex. --time-sleep 3')
	parser.add_argument('--time-sleep-request', nargs='?', dest='_time_to_sleep_request', default=False, help='Sleep time per Request. Ex. --time-sleep-request 3')
	parser.add_argument('--desc', nargs='?', dest='_desc', default=False, const=True, help='Description of the script and authors')
	parser.add_argument('--output-desc', nargs='?', dest='_output_desc', default=False, const=True, help='Description of the output on console mode.')
	args=parser.parse_args()
	if args._run is True:
		paranoia_array = paranoia_level(args)
		files_ruleremove, flag_file_rr, flag_type_rr = rules_remove(args)
		if flag_file_rr is True:
			update_paranoia(paranoia_array, files_ruleremove, flag_type_rr, args)
		else:
			print("[!] Error on File: " + files_ruleremove)
	elif args._desc is True:
                print(banner_desc)
	elif args._output_desc is True:
                print(banner_output)
	else:
		parser.print_help()
