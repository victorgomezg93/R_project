import os
import glob
import pandas
import geoip2.database as db
import datetime

dest = r"/home/victor/Escritorio/R_project/copia/R_project/country_days.csv"

def days_repited3(df):
	#Dias en total por fuente, para sacar dependiendo de que fuente se habia sacado
	# al final no lo he usado esta
	count_series = df.groupby(['ioc','descr']).size()
	new_df = count_series.to_frame(name = 'Dias').reset_index()
	new_df.to_csv(r"IP_days_descr.csv")

def days_repited2(df):
	#Para sacar los dias en total de una IP que ha tenido en activo en dos meses
	# el nuevo mapa esta generado a partir de este
	count_series = df.groupby(['ioc']).size()
	new_df = count_series.to_frame(name = 'Dias').reset_index()
	new_df.to_csv(r"IP_days_no_repeated.csv")

def country(df1,dest = ""):
	# Sacamos el pais de cada IP maliciosa
	df = pandas.DataFrame(columns=["IP","Days","Country"])
	dftotal = pandas.DataFrame(columns=["IP","Days","Country"])
	reader = db.Reader(r"./GeoLite2-Country_20191210/GeoLite2-Country.mmdb")
	ips = []
	countrylist = []
	days = []
	s = 0
	for ip in df1.iloc[0:,1]:
		try:
			c = reader.country(ip).country.names["en"]
			countrylist.append(c)
			ips.append(df1.at[s, 'ioc'])
			days.append(df1.at[s, 'Dias'].astype(int))
		except:
			#c = ''
			pass
		s = s +1
	df["IP"] = ips
	df["days"] = days
	df["Country"] = countrylist
		
	dftotal = dftotal.append(df, ignore_index = True)

	return dftotal

def agg_country(df):
	# Agrupamos en total cuantos dias acumula cada pais de IPs maliciosas. Para saber si 
	# ese pais por ejemplo elimina rapido sus IPs reportadas como maliciosas
	count_series = df.groupby(['Country']).size()
	new_df = count_series.to_frame(name = 'Dias totales').reset_index()
	new_df.to_csv(r"IP_days_total.csv")

def code(df,df5):
	# Para meter el codigo ya que sino el mapa no se genera.
	s = -1
	country = []
	days = []
	code = []
	s1 = -1
	for c in df.iloc[1:,1]:
		s = -1
		s1 = s1 +1
		try:
			for cou in df5.iloc[0:,0]:
				s = s+1
				if cou == c:
					print (df5.at[s, 'Country Code'],df5.at[s, 'Country Name'])
					code.append(df5.at[s, 'Country Code'])
					country.append(df5.at[s, 'Country Name'])
					days.append(df.at[s1, 'Dias totales'])
		except:
			pass		
	aux = pandas.DataFrame(columns=["Country","Dias totales", "Code"])
	aux["Country"] = country
	aux["Dias totales"] = days
	aux["Code"] = code
	#El dataframe final usado para el mapa es este
	aux.to_csv(r"IP_days_total_code.csv")


#Este es el proceso, los dataframes son acumulativos

#df = pandas.read_csv(r"2019-10-15_firehol.csv")
#days_repited2(df)
#df1 = pandas.read_csv(r"IP_days_no_repeated.csv")
#df2 = country(df1,dest)
#df2.to_csv(r"country_days.csv")
#df3 = pandas.read_csv(r"country_days.csv")
#agg_country(df3)
df5 = pandas.read_csv(r"PopulationData/API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")
df4 = pandas.read_csv(r"IP_days_total.csv")
code(df4,df5)
