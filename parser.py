import os
import glob
import pandas

source = r"D:\Master_Cybersecurity_management\05-Data_driven_security\blocklist-ipsets-master"
dest = r"D:\Master_Cybersecurity_management\05-Data_driven_security\Practica\data.csv"

files = glob.glob(os.path.join(source,"*.ipset"))

dftotal = pandas.DataFrame(columns=["IP","Category","Maintainer"])

for f in files:
	ips = []
	cat = ""
	main = ""
	df = pandas.DataFrame(columns=["IP","Category","Maintainer"])

	aux = open(f,"r")
	content = aux.readlines()
	aux.close()

	for l in  content:
		if "Category" in l:
			cat = str(l.split(":")[-1]).strip()
		elif "Maintainer" in l:
			main = str(l.split(":")[-1]).strip()
		elif "#" not in l:
			ips.append(str(l).strip())

	df["IP"] = ips
	df["Category"] = [cat]*len(ips)
	df["Maintainer"] = [main]*len(ips)

	dftotal = dftotal.append(df, ignore_index = True)


print(dftotal)
	