import DataParser as dp
import pandas
from plotnine import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# df es un dataframe con la informacion parseada: ip, categoria, fuente, pais y fecha
# df = dp.getdataframe(r"./blocklist-ipsets-master")
# df.to_pickle(r"./brutedataframe_country_date.pkl")
df = pandas.read_pickle(r".\brutedataframe_country_date.pkl")
# df1 es un dataframe quitando los duplicados teniendo en cuenta la combinacion ip+categoria
# tiene una columna que cuenta las ocurrencias de los duplicados eliminados
# df1 = dp.dropduplicates(df)
# df1.to_pickle(r"./noduplicatesdataframe_country_date.pkl")
df1 = pandas.read_pickle(r".\noduplicatesdataframe_country_date.pkl")
# df2 es un datafreme que tiene como indice las ips y como columnas los distintos tipos de categoria
# df2 = dp.spread(df1)
# df2.to_pickle(r"./categorydataframe.pkl")
df2 = pandas.read_pickle(r".\categorydataframe.pkl")
#df3 es un dataframe que contiene informacion demografica por pais
df3 = pandas.read_csv(r".\PopulationData\API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")

# df4 = dp.dropduplicates2(df)
# df4 = dp.spread2(df4)
# df4 = df4.agg(["sum"])
# df4.to_csv(r".\ipsbycountry.csv")
df4 = pandas.read_csv(r".\ipsbycountry.csv")

df5 = dp.correlation(df3,df4)
df5.sort_values(by="Risk")
df5.to_csv(r".\CountryRisk.csv")


#bar plot that shows Category weights for 1 day of malicious IPS
ggplot(df, aes(x="Category")) + geom_bar(stat = 'count')

#donut plot that shows Category weights for 1 day of malicious IPS
fig = plt.figure()
fig.patch.set_facecolor("black")
plt.rcParams["text.color"] = "white"
my_circle = plt.Circle((0,0), 0.7, color="black")
a = df2.agg("sum")
plt.pie(a.values,labels=df2.columns)
p = plt.gcf()
p.gca().add_artist(my_circle)
plt.show()

#map plot
# merc
m=Basemap(llcrnrlon=-180, llcrnrlat=-60,urcrnrlon=180,urcrnrlat=80, projection='merc')
m.drawmapboundary(fill_color='#A6CAE0')
m.fillcontinents(color='grey', alpha=0.3)
