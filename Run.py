import DataParser as dp
import pandas
from plotnine import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import time
# df es un dataframe con la informacion parseada: ip, categoria, fuente, pais y fecha
# start = time.time()
# df = dp.getdataframe(r"./blocklist-ipsets-master", r"./brutedataframe_country_date.csv")
# print("Parseado+pais: ", time.time()-start)
df = pandas.read_csv(r".\brutedataframe_country_date.csv")

#df1 es un dataframe que contiene informacion demografica por pais
df1 = pandas.read_csv(r".\PopulationData\API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")

# df2 es un dataframe quitando los duplicados teniendo en cuenta la combinacion ip+categoria
# tiene una columna que cuenta las ocurrencias de los duplicados eliminados
# start = time.time()
# df2 = dp.dropduplicates(df,["IP","Category"])
# df2.to_csv(r"./noduplicatesdataframe_country_date.csv",index=False)
# print("dropduplicates: ", time.time()-start)
df2 = pandas.read_csv(r".\noduplicatesdataframe_country_date.csv")

# df3 es un datafreme que tiene como indice las ips y como columnas los distintos tipos de categoria
# start = time.time()
# df3 = dp.spread(df2)
# df3.to_csv(r"./categorydataframe.csv",index=False)
# print("spread: ", time.time()-start)
df3 = pandas.read_csv(r".\categorydataframe.csv")
# a = df3.agg("sum")
# a.to_csv(r"./CategoryAgg.csv",index=False)
a = pandas.read_csv(r".\CategoryAgg.csv")

# df4 = dp.dropduplicates2(df)
# df4 = dp.spread2(df4)
# df4 = df4.agg(["sum"])
# df4.to_csv(r".\ipsbycountry.csv",index=False)
# start = time.time()
df4 = pandas.read_csv(r".\ipsbycountry.csv")
df5 = dp.correlation(df3,df4)
df5.sort_values(by="Risk")
# df5.to_csv(r".\CountryRisk.csv",index=False)
# print("CountryRisk: ", time.time()-start)

# start = time.time()
dfcat = df # df[df.Category != "abuse"]
df6 = dp.dropduplicates3(dfcat)
df6 = dp.spread3(df6)
df6 = dp.correlation2(df6)
# df6.to_csv(r".\CategorybyCountry.csv",index=False)
# print("CategorybyCountry: ", time.time()-start)


#bar plot that shows Category weights for 1 day of malicious IPS
ggplot(df, aes(x="Category")) + geom_bar(stat = 'count')

#donut plot that shows Category weights for 1 day of malicious IPS
fig = plt.figure()
fig.patch.set_facecolor("black")
plt.rcParams["text.color"] = "white"
my_circle = plt.Circle((0,0), 0.7, color="black")
plt.pie(a.values,labels=df3.columns)
p = plt.gcf()
p.gca().add_artist(my_circle)
plt.show()

#map plot
# merc
m=Basemap(llcrnrlon=-180, llcrnrlat=-60,urcrnrlon=180,urcrnrlat=80, projection='merc')
m.drawmapboundary(fill_color='#A6CAE0')
m.fillcontinents(color='grey', alpha=0.3)
