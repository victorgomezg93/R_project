# Data Driven Security

## Introducción

Esto es una copia del resultado mostrado en Documentacion.html. Aquí no se muestran las tablas ni el mapa debido a
que Github no soporta estas imagenes así que para una correcta lectura de nuestro documento hay que:

  * Clonar el directorio
  
  * Abrir el archivo Documentación.html haciendo doble click y abriendose en el navegador


## Recolección de los Datos
Se ha recogido datos de distintas fuentes para realizar un estudio sobre IPs maliciosas en blacklists.
La información tratada se ha recogido de las siguientes fuentes:

[Listas IPs maliciosas](https://github.com/firehol/blocklist-ipsets)  
[Base de datos de geolocalización](https://dev.maxmind.com/geoip/geoip2/geolite2/)  
[Datos de población](https://data.worldbank.org/indicator/SP.POP.TOTL)

Los datos obtenidos, se han parseado y limpiado para poder sacar la información relevante.
De firehol se ha extraido la siguiente información : IP, Categoría, Quien matiene la lista donde aparece dicha ip y 
fecha de la lista.
De maxmind hemos obtenido la geolocalización de cada ip mediante su API.

## Definición de funciones
A continuación definimos las funciones utilitzadas para el tratamiento de datos, hay que tener en cuenta que la función
*getdataframe* tiene bastante coste temporal, por ello, es preferible guardar el dataframe en disco para luego cargarlo.

```python, term=True
    import os
    import glob
    import pandas
    import geoip2.database as db
    import datetime
    from plotnine import *
    import matplotlib.pyplot as plt
    
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
        if dest != "" and not os.path.exists(dest):
            dftotal.to_csv(dest,index=False)
        return dftotal

    def dropduplicates(df,groupcolumns):
        aux = df
        aux["Occurrence"] = df.groupby(groupcolumns).cumcount() + 1
        return aux.drop_duplicates(subset = groupcolumns, keep = "last")
```

## Datos limpios
Con lo mencionado se ha generado el siguiente dataframe con toda la información limpia, con la primera linea generamos
de nuevo el dataframe, con la segunda, cargamos uno preguardado.

```python, term=True
    #df = getdataframe(r"/home/victor/Escritorio/R_project/copia/R_project/blocklist-ipsets-master")
    df = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/brutedataframe_country_date.csv")
    df
```

Por último con la información de worldbank hemos generado un dataframe que contiene información relevante por país.

```python, term=True
    df1 = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/PopulationData/API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")
    df1
```

## Observaciones con datos de un día
Inicialmente se ha esbozado un primer estudio solo con los datos de un solo día obtenidos de firehol.
Con ello se quiere realizar observaciones a pequeña escara antes de pasar a grandes conjuntos de datos.

### Distribución de ips maliciosas por categoria
Se ha estudiado como se reparten las ips maliciosas en las distintas categorías definidas por firehol. 

A continuación se ha transformado la información ya limpia para representar correctamente lo que se quería observar.
Para ello se ha usado la información recopilada en el datafrme df.
Dado que df contenía ips repetidas en la misma categoría, se han llevado a cabo distintos pasos para agrupar 
la información de forma conveniente.
 
En primer lugar, se ha agrupado toda la información del dataframe por IP/categoría y a continguación se han
eliminado los duplicados.

```python, term=True
    df2 = dropduplicates(df,["IP","Category"])
    df2
```

Por último, se ha pivotado la información para quedara una tabla representado lo que se quería observar
y se ha realizado una aggregado por columnas.

```python, term=True
    df3 = df2.pivot(index = "IP", columns = "Category", values = "Occurrence")
    df3
```

```python, term=True
    a = df3.agg("sum")
    a
```

Con los datos obtenidos en distintas etapas del tratamieto,
podemos representar de varias formas la distribuión según categoría:

```python, term=True
    ggplot(df, aes(x="Category")) + geom_bar(stat = 'count')
```

```python, term=True
    def donutplot(a):
        fig = plt.figure()
        fig.patch.set_facecolor("white")
        plt.rcParams["text.color"] = "black"
        my_circle = plt.Circle((0,0), 0.7, color="white")
        plt.pie(a.values,labels=df3.columns)
        p = plt.gcf()
        p.gca().add_artist(my_circle)
        return p
```

```python, term=True
    p = donutplot(a)
```

### Indice de peligrosidad por país
Los datos obtenidos se han utilitzado para observar y calcular un indice de peligrosidad por país.
Para conseguir dicho indice se han usado los datos de df y df3. Para poder representar la información correctamente,
se ha generado un nuevo dataframe que contiene el país con su indice calculado en base a
 **nº IPs maliciosas / Población**.
 
```python, term=True
    df5 = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/CountryRiskCode_simple.csv")
    df5
```

### Distribución de categorías por país

Una vez hemos encontrado este indice de peligrosidad hemos pensado en añadir tambien que país mantenía más IPs
de qué categoría ya que nos ha parecido interesante saber la distribución de estos países. Para eso hemos agrupado
el numero de IPs de cada categoria que mantenía cada país y el más grande es el que hemos anotado.

Una vez hecho el agregado nos ha quedado el siguiente dataframe.

```python, term=True
    df6 = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/CategorybyCountry.csv")
    df6
```

El problema que se puede observar es que la gran mayoria de bloques de cada país es de abuse por lo tanto, viendo que se
repetía mucho, hemos optado a hacer la lista sin contar esta categoría de cara a mostrar otros datos relevantes como es
el segundo bloque mas mantenido.

```python, term=True
    df7 = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/CategorybyCountry_Noabuse.csv")
    df7
```

### Agrupacion y ordenación

Ahora que ya teniamos los datos en bruto que queríamos hemos necesitado coordinar los diversos dataframes. Mayormente,
el problema que hemos tenido es que cada dataframe ponía los paises de una forma diferente o ponía más o menos paises por lo
que nunca estaban cerca en las posiciones de los dataframes.

Así que la solución ha sido hacer un script para buscar las coincidencias y así escrbir un dataframe final con esto.
Con esto evitabamos tener que construir nosotros unos dataframes identicos y sólo tener que invertir tiempo para
que nos construyera nuestro dataframe final.

```python, term=True
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
```

### Reescripción y normalización del mapa

Otro problema como hemos comentado ha sido los nombres, ya que no siempre se han mantenido iguales en cada dataframe,
por lo tanto, viendo que esto a la larga también podría ser un problema, hemos normalizado los nombres en cada dataframe
con una función.

```python, term=True
def rewrite(df3):
  	d = {'Venezuela, RB':'Venezuela',"Egypt, Arab Rep.":"Egypt","Korea, Rep.":"South Korea","Iran, Islamic Rep.":"Iran","Yemen, Rep.":"Yemen",
  	"Czech Republic":"Czechia","Syrian Arab Republic":"Syria","Congo, Rep.":"Congo Republic",
  	"Slovak Republic":"Slovakia","Lithuania":"Republic of Lithuania","Moldova":"Republic of Moldova",
  	"Kyrgyz Republic":"Kyrgyzstan","Lao PDR":"Laos","Jordan":"Hashemite Kingdom of Jordan","Congo, Dem. Rep.":"DR Congo",
  	"Cote d'Ivoire":"Ivory Coast","Seychelles":"Sey","British Virgin Islands":"BR","Russian Federation":"Russia"}
  	df3 = df3.replace(d)
  	df3.to_csv("PopulationData/API_SP.POP.TOTL_DS2_en_csv_v2_566132.csv")

```

El último problema que hemos afrontado ya de cara a normalizar los colores del mapa y adelantandonos un poco a la conclusión,
es que algunos de los países que tienen bastantes bloques maliciosos no estaban representados en ningun mapa de cloropeth debido
a ser paraísos fiscales muy pequeños y negligibles como puede ser Seychelles o Virgin Islands, así que los hemos tenido que retirar
por la falta de posibilidad de mostrarlo.

### Dataframe final

Finalmente, una vez agrupado todo en un dataframe, hemos aplicado esta información para construir un modelo de mapa de cara a mostrar
más visualmente la cantidad de bloques maliciosos de IPs por pobalción.

El resultado es el dataframe con el que hemos hecho los estudios.

**dataframe final**

```python, term=True
    df8 = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/CountryRiskCode.csv")
    df8
```

## Observaciones temporales (Datos varios días)

Evolución temporal de ips por categoria

Evolución temporal de países según peligrosidad

Evolución temporal de categorías por país 

## Predicciónes

Predecir la posibilidad que una IP se vaya a incluir en blacklist y en que categoria se incluiria.

### Datos relevantes para Predecir
Para poder entrenar un modelo de predicción hay que disponer de suficientes datos con atributos releventes
diferenciados. De este modo y en base a los atributos se puede realizar la predicción.

* País de origen
* Veces en blacklist días distintos
* Veces en blacklist mismo día
* Tiempo en uso (mismo propietario)
* Categoría en blacklist
* Tiempo en blacklist

## Tiempos de ejecucion
* Parser -> 617.61s 878.29s
* Drop duplicates -> 9.66s
* spread -> 8.47s

## Mapa

El mapa esta hecho con la libreria plotly. A partir de los codigos que hemos añadido en los dataframes
se ha generado un mapa interactivo que nos permite ver como de peligroso es un pais.

<iframe id="mapa" src="mapa.html" width="1250" height="1000"  frameborder="1000"></iframe>

## Conclusiones

El resultado que podemos sacar al final es bastante obvio con respecto al mapa. Los países que son
paraísos fiscales como Belize, Seychelles o Virgin Islands por ejemplo, mantienen un número muy
elevado de bloques maliciosos para su población.

Seguidamente el segundo grupo con más bloques maliciosos es el sovietico, y también se puede remarcar
Islandia y Holanda que se cuelan en la estadistica.

Esto es debido a que estos paises al tener una legislación más laxa, son una oportunidad para la
gente que le interese mantener bloques de IPs que pueden servir para atacar al resto de paises
ya que así evitaran que les cierren estas o que les repecturan acciones legales.

## Estudios generados a partir del Dataset de dos meses

El estudio que hemos generado a partir del dataset de dos meses es algo diferente. En este caso,
partiendo de que teniamos las IPs de dos meses, lo que hemos hecho es coger todos los dias en
activo que ha tenido cada IP reportada como maliciosa y agruparlo por país de cara a ver que paises
podían acumular mas días con bloques maliciosos reportados y confirmados.

##  Distribución por dias

Concretamente en este caso hemos utilizado 4 funciones y hemos generado 4 dataframes distintos
hasta llegar al final que hemos utilizado para generar este último mapa.

Primeramente hemos hecho el agregado de cuantos dias ha estado una IP activa en estos dos meses

```python, term=True
def days_repited2(df):
	#Para sacar dias en total que una IP que se ha tenido en activo en dos meses
	count_series = df.groupby(['ioc']).size()
	new_df = count_series.to_frame(name = 'Dias').reset_index()
	new_df.to_csv(r"IP_days_no_repeated.csv")
```

Esto nos permite ver cuantos dias se ha repetido esta IP como podemos ver en esta tabla

```python, term=True
    df9 = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/IP_days_no_repeated.csv")
    df9
```
##  Distribución por paises

Seguidamente hemos pensado que podíamos analizar de estos datos así que hemos decidido
agrupar estas IPs por países de cara a consultar si los bloques reportados maliciosos solían
aguantar mucho o no. 

Para ello primero hemos tenido que averiguar el país de cada IP, así que hemos usado la siguiente
función.

```python, term=True
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
```
Una vez que teníamos el país, hemos hecho el agregado de cada país para ver cuantos dias
acumulaban en total a partir de la siguiente función.

```python, term=True
def agg_country(df):
	# Agrupamos en total cuantos dias acumula cada pais de IPs maliciosas. Para saber si 
	# ese pais por ejemplo elimina rapido sus IPs reportadas como maliciosas
	count_series = df.groupby(['Country']).size()
	new_df = count_series.to_frame(name = 'Dias totales').reset_index()
	new_df.to_csv(r"IP_days_total.csv")
```
El resultado era bastante interesante ya que se podía ver países que apenas acumulaban dias y
paises que por el contrario acumulaban bastantes.

El dataframe generado era el siguiente:

```python, term=True
    df10 = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/IP_days_total.csv")
    df10
```

## Normalización para el uso del mapa y dataframe final

Hemos tenido que generar otra vez el codigo para el uso del mapa con la siguiente función

```python, term=True
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
```
El dataframe final usado para el mapa es el siguiente:

```python, term=True
    df11 = pandas.read_csv(r"/home/victor/Escritorio/R_project/copia/R_project/IP_days_total_code.csv")
    df11
```

## Segundo mapa

Este mapa nos muestra el numero total de dias acumulados por cada país de sus IPs maliciosas
reportadas en estos dos meses del dataframe.

<iframe id="mapa" src="mapa2.html" width="1250" height="1000"  frameborder="1000"></iframe>

## Conclusiones

Las conclusiones que podemos sacar de este mapa son bastante curiosas. Principalmente podemos
observar claramente que el país que más dias en activo mantiene bloques maliciosos de IPs es
Uruguay. Uruguay precisamente no es uno de los paises más problematicos en este aspecto pero
parece ser que tiene una politica de eliminación de contenido malicioso en Internet bastante pesima.

Otro conjunto intenresante es el de Indonesia donde parece que tampoco hay mucha legislación
para retirar contenido malicioso.

Podemos observar donde en España y en general en el resto de Europa, los bloques maliciosos apenas
duran pocos dias. Rusia o China a pesar de ser unos gigantes en cuanto a ataques maliciosos parece
ser que tampoco mantienen en activo por mucho tiempo sus IPs problemáticas.
