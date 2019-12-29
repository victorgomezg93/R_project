# Data Driven Security

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

Con lo mencionado se ha generado el siguiente dataframe:

    (tabla df)

Por último con la información de worldbank hemos generado un dataframe que contiene información relevante por país.

    (tabla df3)

## Observaciones con datos de un día
### Distribución de ips maliciosas por categoria
Se ha estudiado como se reparten las ips maliciosas en las distintas categorías definidas por firehol. 

A continuación se ha transformado la información ya limpia para representar correctamente lo que se quería observar.
Para ello se ha usado la información recopilada en el datafrme df.
Dado que df contenía ips repetidas en la misma categoría, se han llevado a cabo distintos pasos para agrupar 
la información de forma conveniente.
 
* En primer lugar, se ha agrupado toda la información del dataframe por IP/categoría y a continguación se han eliminado los duplicados.  

        (tabla df1)
    
* Por último, se ha pivotado la información para quedara una tabla representado lo que se quería observar:

        (tabla df2)

Una vez tratados los datos podemos observar la siguiente distribuión según categoría:

    (barpolt)

    (donutplot)

### Indice de peligrosidad por país
Los datos obtenidos se han utilitzado para observar y calcular un indice de peligrosidad por país.
Para conseguir dicho indice se han usado los datos de df y df3. Para poder representar la información correctamente,
se ha generado un nuevo dataframe que contiene el país con su indice calculado en base a
 **nº IPs maliciosas / Población**.
 
    (tabla df5)

### Distribución de categorías por país

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