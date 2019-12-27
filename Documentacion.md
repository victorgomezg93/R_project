# Data Driven Security

## Recolección de los Datos
Se ha recogido datos de distintas fuentes para realizar un estudio sobre IPs maliciosas en blacklists.
La información tratada se ha recogido de las siguientes fuentes:

[Listas IPs maliciosas](https://github.com/firehol/blocklist-ipsets)
[Base de datos de geolocalización](https://dev.maxmind.com/geoip/geoip2/geolite2/)
[Datos de población](https://data.worldbank.org/indicator/SP.POP.TOTL)

### Observaciones Datos 1 día
Distribución de ips maliciosas por categoria (barplot + donutplot)

Indice de peligrosidad por país: número de ips maliciosas / población (choropleth map)

Distribución de categorías por país

### Observaciones temporales (Datos varios días)

Evolución temporal de ips por categoria

Evolución temporal de países según peligrosidad

Evolución temporal de categorías por país 

### Predicciónes

Predecir la posibilidad que una IP sea maliciosa sin estar explicitamente en una blacklist

En caso de serlo predecir la categoria 

### Datos relevantes para Predecir
Para poder entrenar un modelo de predicción hay que disponer de suficientes datos con atributos releventes
diferenciados. De este modo y en base a los atributos se puede realizar la predicción.

* País de origen
* Veces en blacklist
* Tiempo en uso (mismo propietario)
* Categoría en blacklist
* 

### Tiempos de ejecucion
* Parser -> 617.61s
* Drop duplicates -> 9.66s
* spread -> 8.47s
* 