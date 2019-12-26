import os
import glob
import pandas
import geoip2.database as db
import datetime

def correlation2(df3,df4):
	normalized = []
	country = []
	code = []
	i = 0
	for c in df4.columns[2:]:
		try:
			a = int(df4[c])
			b = int(df3.loc[df3["Country Name"] == c]["2018"])
			normalized.append((a/b)*1000)
			country.append(c)
			code.append(df3.at[i, 'Country Code'])
			i = i+1
		except:
			i = i+1
			pass
	aux = pandas.DataFrame(columns=["Country","Risk", "Code"])
	aux["Country"] = country
	aux["Risk"] = normalized
	print (code)
	aux["Code"] = code

	return aux

df3 = pandas.read_csv(r"PopulationData/API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")
df4 = pandas.read_csv(r"ipsbycountry.csv")
df5 = correlation2(df3,df4)
#df5.sort_values(by="Risk")
df5.to_csv(r"CountryRiskCode.csv")

