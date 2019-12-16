import os
import glob

source = r"D:\Master_Cybersecurity_management\05-Data_driven_security\blocklist-ipsets-master"

files = glob.glob(os.path.join(source,"*.ipset"))

ips = []
data = {}
datadic = {}
for f in files:
	aux = open(f,"r")
	content = aux.readlines()
	aux.close()
	for l in  content:
		if "Category" in l:
			data["Category"] = str(l.split(":")[-1]).strip()
		elif "Maintainer" in l:
			data["Maintainer"] = str(l.split(":")[-1]).strip()
		elif "#" not in l:
			ips.append(l)

	for ip in ips:
		datadic[str(ip).strip()] = data
	print(datadic)
	break