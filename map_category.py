import os
import glob
import pandas
import geoip2.database as db
import datetime

#Genera un dataframe amb els paisos amb el seu codi i el numero de risc donat

def correlation2(df3,df4):
	#Es creen llistes buides que anem omplint amb les dades que ens interesen
	normalized = []
	country = []
	code = []
	for c in df4.columns[2:]:
		try:
			a = int(df4[c])
			b = int(df3.loc[df3["Country Name"] == c]["2018"])
			normalized.append((a/b)*1000)
			country.append(c)
			#Es fa una cerca per trobar el país amb el que coincideix
			#i treure l'iterador per introduir el codi correcte
			s = -1
			for cou in df3.iloc[0:,0]:
				s = s+1
				if cou == c:
					code.append(df3.at[s, 'Country Code'])
		except:
			pass
	aux = pandas.DataFrame(columns=["Country","Risk", "Code"])
	aux["Country"] = country
	aux["Risk"] = normalized
	aux["Code"] = code

	return aux

#Es crean els dataframes i es criden les funcions

df3 = pandas.read_csv(r"PopulationData/API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")
df4 = pandas.read_csv(r"ipsbycountry.csv")
df5 = correlation2(df3,df4)
#df5.sort_values(by="Risk")
df5.to_csv(r"CountryRiskCode.csv")

