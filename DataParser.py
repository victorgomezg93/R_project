import os
import glob
import pandas
import geoip2.database as db
import datetime

# source = r"D:\Master_Cybersecurity_management\05-Data_driven_security\blocklist-ipsets-master"
# dest = r"D:\Master_Cybersecurity_management\05-Data_driven_security\Practica\data.csv"

def getdataframe(source,dest = ""):
	files = glob.glob(os.path.join(source,"*.ipset"))

	dftotal = pandas.DataFrame(columns=["IP","Category","Maintainer","Country","Date"])
	reader = db.Reader(r"./GeoLite2-Country_20191210/GeoLite2-Country.mmdb")
	for f in files:
		ips = []
		countrylist = []
		cat = ""
		main = ""
		date = ""
		df = pandas.DataFrame(columns=["IP","Category","Maintainer","Country","Date"])

		aux = open(f,"r")
		content = aux.readlines()
		aux.close()

		for l in  content:
			if "Category" in l:
				cat = str(l.split(":")[-1]).strip()
			elif "Maintainer" in l:
				main = str(l.split(":")[-1]).strip().replace("/","")
			elif "#" not in l:
				ips.append(str(l).strip())
			elif "This File Date" in l:
				date = str(l.split(" : ")[-1]).strip().replace("  "," ")
				try:
					date = str(datetime.datetime.strptime(date, "%a %b %d %H:%M:%S UTC %Y"))
				except:
					print(str(l))

		df["IP"] = ips
		df["Category"] = [cat]*len(ips)
		df["Maintainer"] = [main]*len(ips)
		df["Date"] = [date]*len(ips)

		for ip in df.IP.values:
			try:
				c = reader.country(ip).country.names["en"]
			except:
				c = ''
			countrylist.append(c)

		df["Country"] = countrylist
		
		dftotal = dftotal.append(df, ignore_index = True)

	return dftotal
	
def dropduplicates(df):
	aux = df
	aux["Occurrence"] = df.groupby(["IP","Category"]).cumcount() + 1
	return aux.drop_duplicates(subset = ["IP","Category"], keep = "last")

def dropduplicates2(df):
	aux = df
	aux["Occurrence"] = df.groupby("IP").cumcount() + 1
	return aux.drop_duplicates(subset = "IP", keep = "last")

def dropduplicates3(df):
	aux = df
	aux["Occurrence"] = df.groupby(["Category","Country"]).cumcount() + 1
	return aux.drop_duplicates(subset = ["Category", "Country"], keep = "last")

def spread(df):
	return df.pivot(index = "IP", columns = "Category", values = "Occurrence")

def spread2(df):
	return df.pivot(index = "IP", columns = "Country", values = "Occurrence")

def spread3(df):
	return df.pivot(index = "Country", columns = "Category", values = "Occurrence")

def correlation(df3,df4):
	normalized = []
	country = []
	for c in df4.columns[2:]:
		try:
			a = int(df4[c])
			b = int(df3.loc[df3["Country Name"] == c]["2018"])
			normalized.append((a/b)*1000)
			country.append(c)
		except:
			pass
	aux = pandas.DataFrame(columns=["Country","Risk"])
	aux["Country"] = country
	aux["Risk"] = normalized

	return aux

def correlation2(df):
	it = df.iterrows()
	try:
		next(it)
		country = []
		category = []
		for i in range(len(df.index)):
			aux = next(it)
			country.append(aux[0])
			a1 = aux[1].keys().to_list()
			a2 = list(aux[1].values)
			c = a1[a2.index(max(a2))]
			category.append(c)
	except:
		pass
	dfret = pandas.DataFrame(columns=["Country","Category"])
	dfret["Country"] = country
	dfret["Category"] = category
	return dfret