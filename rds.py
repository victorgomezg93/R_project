import os
import glob
import pandas
import geoip2.database as db
import datetime

def days_repited3(df):
	#Dias en total por fuente
	count_series = df.groupby(['ioc','descr']).size()
	new_df = count_series.to_frame(name = 'Dias').reset_index()
	new_df.to_csv(r"IP_days_descr.csv")

def days_repited2(df):
	#Para sacar los dias en total de una IP
	count_series = df.groupby(['ioc']).size()
	new_df = count_series.to_frame(name = 'Dias').reset_index()
	new_df.to_csv(r"IP_days_no_repeated.csv")

def days_repited(df):
	#No es eficiente, no usar, cerca de 2 horas sin resultado
	ip = []
	category = []
	descr = []
	mnt = []
	Days = []
	aux = pandas.DataFrame(columns=["IP","Category","Desc","Mantainer, Days"])
	s = 0
	for i in df.iloc[0:,1]:
		num = 0
		for j in df.iloc[0:,1]:
			if i == j:
				num = num+1
		ip.append(df.at[s, 'ioc'])
		category.append(df.at[s, 'category'])
		descr.append(df.at[s, 'descr'])
		mnt.append(df.at[s, 'mnt'])
		Days.append(num)
		s = s+1

	aux["IP"] = ip
	aux["Category"] = category
	aux["Desc"] = descr
	aux["Mantainer"] = mnt
	aux["Days"] = Days

	aux.to_csv(r"IP_days.csv")


def eliminar_repetidos(df):
	#No es eficiente, no usar, cerca de 2 horas sin resultado
	ip = []
	category = []
	descr = []
	mnt = []
	Days = []
	aux = pandas.DataFrame(columns=["IP","Category","Desc","Mantainer, Days"])
	s = 0
	for i in df.iloc[0:,1]:
		t = False
		for j in ip:
			if i == j:
				t = True
		if t == False:
			ip.append(df.at[s, 'IP'])
			category.append(df.at[s, 'Category'])
			descr.append(df.at[s, 'Desc'])
			mnt.append(df.at[s, 'Mantainer'])
			Days.append(df.at[s, 'Days'])
		s = s+1

	aux["IP"] = ip
	aux["Category"] = category
	aux["Desc"] = descr
	aux["Mantainer"] = mnt
	aux["Days"] = Days

	aux.to_csv(r"IP_days_no_repeated.csv")


df = pandas.read_csv(r"2019-10-15_firehol.csv")
days_repited2(df)