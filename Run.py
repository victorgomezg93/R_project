import DataParser as dp
import pandas
# df es un dataframe con la informacion parseada: ip, categoria y fuente
# df = dp.getdataframe(r"./blocklist-ipsets-master")
# df.to_pickle(r"./brutedataframe.pkl")
df = pandas.read_pickle(r"./brutedataframe.pkl")
# df1 es un dataframe quitando los duplicados teniendo en cuenta la combinacion ip+categoria
# tiene una columna que cuenta las ocurrencias de los duplicados eliminados
# df1 = dp.dropduplicates(df)
# df1.to_pickle(r"./noduplicatesdataframe.pkl")
df1 = pandas.read_pickle(r"./noduplicatesdataframe.pkl")
# df2 es un datafreme que tiene como indice las ips y como columnas los distintos tipos de categoria
# df2 = dp.spread(df1)
# df2.to_pickle(r"./categorydataframe.pkl")
df2 = pandas.read_pickle(r"./categorydataframe.pkl")
