import os
import glob
import pandas
import geoip2.database as db
import datetime

#Genera un dataframe amb els paisos amb el seu codi i el numero de risc donat

def rewrite(df3):
	d = {'Venezuela, RB':'Venezuela',"Egypt, Arab Rep.":"Egypt","Korea, Rep.":"South Korea","Iran, Islamic Rep.":"Iran","Yemen, Rep.":"Yemen",
	"Czech Republic":"Czechia","Syrian Arab Republic":"Syria","Congo, Rep.":"Congo Republic",
	"Slovak Republic":"Slovakia","Lithuania":"Republic of Lithuania","Moldova":"Republic of Moldova",
	"Kyrgyz Republic":"Kyrgyzstan","Lao PDR":"Laos","Jordan":"Hashemite Kingdom of Jordan","Congo, Dem. Rep.":"DR Congo",
	"Cote d'Ivoire":"Ivory Coast","Seychelles":"NO","British Virgin Islands":"BR"}
	df3 = df3.replace(d)
	df3.to_csv("PopulationData/API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")
	#for i in df3.iloc[0:,0]:
		#if i == "Venezuela, RB":
		#	df3.loc["Country Name","Venezuela, RB"] = "Venezuela"

def correlation2(df3,df4,df6,df7):
	#Es creen llistes buides que anem omplint amb les dades que ens interesen
	normalized = []
	country = []
	code = []
	category = []
	category2 = []
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
			it = -1
			for i in df6.iloc[0:,1]:
				it = it+1
				if i == c:
					category.append(df6.at[it, 'Category'])
			it2 = 0
			t = False
			for i2 in df7.iloc[0:,1]:		
				if i2 == c:
					category2.append(df7.at[it2, 'Category'])
					t = True
				it2 = it2+1
				if it2 == 225:
					if t == False:
						category2.append("No data")
					t = False

		except:
			pass
	aux = pandas.DataFrame(columns=["Country","Risk", "Code", "Category","No Abuse"])
	aux["Country"] = country
	aux["Risk"] = normalized
	aux["Code"] = code
	aux["Category"] = category
	aux["No Abuse"] = category2

	return aux

#Es crean els dataframes i es criden les funcions


df6 = pandas.read_csv(r"CategorybyCountry.csv")
df7 = pandas.read_csv(r"CategorybyCountry_Noabuse.csv")
df3 = pandas.read_csv(r"PopulationData/API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")
df4 = pandas.read_csv(r"ipsbycountry.csv")
# El rewrite cambia el dataframe para ajustar los nombres de paises pero
# crea una columna extra en el csv que hay que borrar manualmente
#rewrite(df3)
df5 = correlation2(df3,df4,df6,df7)
df5.to_csv(r"CountryRiskCode.csv")

