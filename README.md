## Simulador de memoria cache

Este pequeño simulador está dirigido a estudiantes de arquitectura de computadoras, con la idea de ayudarles a entender el funcionamiento de la memoria cache, y a verificar sus propias intuiciones y resultados. La nomenclatura sigue los textos tradicionales (M. Mano, Hennessy-Patterson, etcetera). Está escrito en Python. Considere este simulador como un punto de partida para sus propias exploraciones en este tema.

### Para qué sirve?

La idea es simular la ejecución de un programa en una computadora con una memoria cache dada. Dependiendo del grado de localidad, el tiempo promedio que toma accesar la memoria cambia: para localidad baja, el tiempo de acceso será similar al tiempo de acceso a la memoria principal, mientras que para localidad alta, será apenas un poco más alta que el tiempo de acceso a la memoria cache.

### Cómo funciona?

Al inicio, el simulador pide la configuración de la memoria cache. Una vez proporcionados todos los parámetros, la simulación procede paso a paso (un acceso a la memoria cada vez que oprima la barra espaciadora). Si se oprime la tecla `i`, se simularán 10,000 accesos de un solo golpe.

Esta imagen muestra al simulador en acción:

![sreenshot](/simulator.png)

### Detalles sobre la localidad

El simulador usa un modelo simple pero sin sofisticación. Al inicio, la computadora sólo accesa direcciones del primer bloque de memoria (donde un bloque cabe completo en cache). Con cierta probabilidad, el programa brinca a otro bloque a cierta distancia del bloque original. Si el bloque ya está en cache, entonces se accesa directamente; si no, entonces el bloque entero se baja a la cache (si la cache está llena, entonces un bloque al azar se descarta usando una política "random replacement").

Hay tres niveles de localidad:
* Nivel bajo: cada acceso es a un bloque nuevo.
* Nivel medio: con probabilidad 30%, un acceso brinca a un bloque que está a distancia entre -10 y +10 del bloque actual.
* Nivel alto: con probalidad 10%, un acceso brinca a un bloque que está a distancia entre -5 y +5 del bloque actual.

Los tiempos de acceso a memoria se pueden configurar cambiando las variables globales `TA_MEM` y `TA_CACHE`.
