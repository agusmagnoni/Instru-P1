CUADERNO INSTRUMENTACIÓN 

Miércoles 22/08

No fui. La idea de la clase es medir la curva de respuesta de un diodo y algo más con transistores FET que no sé. Para hacerlo la idea esusar el micrófono y el parlante de la computadora como medidores de voltaje y generadores de funciones. 

Lunes 27/08

Trabajamos con Ioni para por lo menos empezar a ver cómo usar el micrófono y los parlantes como medidores. Los podemos controlar e hicimos una función test, que es una instancia de prueba a ver si todo funciona. Después, empezamos a tratar de programar algunas funciones: senoidal, cuadrada y ahí quedamos. Quedaría una constante, una arbitraria y eso. En el repositorio, el archivo de python se llama "test.py". Por ahora ahí está todo. 

Miércoles 29/08

Primero entendimos un poco más como funciona git. Volvimos para atrás con lo que habíamos hecho y ahora cada uno tiene su repositorio personal original (el de Agus es agusmagnoni y el de ioni no sé) y lo que vamos a ir haciendo es: nos alternamos en cada práctica quién tiene el original y quién tiene el fork para así todos entendemos como funciona el asunto. 
Además agregamos algunas funciones al generador y vimos si el osciloscopio las veía. No veía la cuadrada, no veía el serrucho. Con el serrucho lo que pasaba era que tenía muy baja frecuencia y el generador que es la placa de audio no funciona bien para bajas. Le puse frecuencia 440 Hz y funcionó bien. 

Domingo 02/09 

Chusmeé que onda las funciones que teníamos. Logré hacer que serrucho suene, pero no puedo hacer que suene la cuadrada. No sé porque porque le modifiqué los valores de amp (puse 2) y de offset (-1) para que se vea como la senoidal de 440 Hz que sí suena. Pero no escucho nada. 
Agregué funciones de playrec de la senoidal y de la serrucho que pueden servir la senoidal para ver que onda y la serrucho para eventualmente medir el diodo. 
Estaría bueno lograr lo de la cuadrada para medir el tiempo de respuesta de la placa de audio como generador. Pero no sé. 
Agregué un barrido en frecuencia también para ver como responde a distintas señales. 
Todo lo hice con sonido real porque tengo un solo cable pelado y, lo más importante, una única salida de audio in/out. Habría que ver de comprar el cable de los pibes estos. 
