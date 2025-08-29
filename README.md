# Sistema de Transcripción Automática de Partituras (TFG)

Este proyecto implementa un sistema de Optical Music Recognition (OMR) de partituras monofónicas y las convierte en archivos MIDI reproducibles.

## Descripción

Este es un sistema que reconoce elementos musicales en imágenes de partituras monofónicas, los convierte a un archivo MIDI mediante music21 y reproduce automáticamente con pygame. Utiliza los archivos de inferencia desarrollados por Jorge Calvo Zaragoza que son parte del repositorio utilizado para el paper [End-to-End Neural Optical Music Recognition of Monophonic Scores](http://www.mdpi.com/2076-3417/8/4/606). 


## Instalación

Para poder ejecutar el main.py es necesario descargar el modelo semántico utilizado en el github de Jorge Calvo Zaragoza [tf-end-to-end](https://github.com/OMR-Research/tf-end-to-end.git). 

* [modelo semantico](https://grfia.dlsi.ua.es/primus/models/PrIMuS/Semantic-Model.zip)

Además, es necesario clonar archivos de esta repo como vocabulary_semantic.txt, ctc_predict.py y ctc_utils.py.

También es necesario descargar las siguientes librerías de python:
- OpenCV
- TensorFlow
- music21
- pygame
```
pip3 install opencv-python tensorflow music21 pygame
```

## Uso

```
python3 main.py 
```
Esto realiza los siguiente pasos:
1. Pide que se introduzca el número de pentagramas que tiene la imagen
2. 1. Si el número de líneas de pentagrama es 1: Reconoce los elementos musicales de la imagen indicada en `RUTA_IMAGEN`
2. 2. Si el número de líneas de pentagrama es mayor que 1: Crea una carpeta con las diferentes líneas de pentagrama en diferentes imágenes y realiza el proceso de inferencia sobre estas imágenes
3. Pide introducir el nombre del instrumento con el que se desea reproducir la partitura 
4. Convierte el resultado de la inferencia (semantic) en un archivo MIDI mediante music21
5. Guarda la salida en el archivo seleccionado en `SALIDA_MIDI`
6. Reproduce automáticamente el archivo con pygame
7. Elimina automáticamente la carpeta creada para procesar las diferentes líneas de pentagrama 

En la terminal se ve algo del tipo:
```console
$ python3 main.py
pygame 2.6.1 (SDL 2.28.4, Python 3.10.12)
Hello from the pygame community. https://www.pygame.org/contribute.html
Introduce el número de pentagramas de la imagen: 1
Tokens reconocidos:
['clef-G2', 'timeSignature-4/4', 'note-C5_eighth', 'note-A4_eighth', 'note-A4_eighth', 'note-E5_eighth', 'note-C5_eighth', 'note-B4_eighth', 'note-A4_eighth', 'note-E5_eighth', 'barline-', 'note-C5_eighth', 'note-C5_eighth', 'note-A4_eighth', 'note-E5_eighth', 'note-C5_eighth', 'note-D5_eighth', 'note-A4_eighth', 'note-E5_eighth', 'barline-', 'note-C5_eighth', 'note-E5_eighth', 'note-A4_eighth', 'note-E5_eighth', 'note-C5_eighth', 'note-F5_eighth', 'note-A4_eighth', 'note-E5_eighth', 'barline-']
Introduce el instrumento(por defecto 'Piano'): Flauta
Archivo MIDI guardado en salida.mid
Reproduciendo música...
Reproducción terminada.
```


## Estructura del proyecto
### preprocesamiento.py: Identificar líneas de pentagrama

En este archivo se define la funcion que identifica las líneas de pentagrama a través de la librería OpenCV. 

Primero se crea una carpeta en la que se guardarán las diferentes imágenes con las diferentes líneas de pentagrama. A continuación, se binariza la imagen y se detectan las líneas horizontales y las posiciones de sus contornos. Luego se agrupan en grupos de 5 líneas en las cuales se conforma un pentagrama. Se forma un rectángulo en la imagen bordeando el grupo con los parámetros x_min, x_max, y_min e y_max, y se recorta la imagen inicial por estas coordenadas. Las imágenes recortadas se guardan en la carpeta creada anteriormente. La función devuelve la ruta de la carpeta en la que se guardan las imágenes.


### ctc_predict.py: OMR

Los archivos ctc_predict.py y ctc_utils.py son importados del github tf-end-to-end de Jorge Calvo Zaragoza. Ambos archivos utilizan OpenCV para el reconocimiento de imágenes.

En el archivo reconocimiento.py se define la función de inferencia que hace uso del archivo .meta del modelo semántico. Estos modelos son el resultado del proceso de entrenamiento realizado por Jorge Calvo Zaragoza utilizando parte del dataset PrIMuS. Las imágenes de la carpeta /datos/imagenes_test son imágenes de este dataset que no fueron utilizadas en el proceso de entrenamiento, por lo que fueron utilizadas para comprobar que el proceso de inferencia funcionaba correctamente.

Para las imágenes 000110346-1_1_1.png y 000113818-1_1_1.png, el proceso de inferencia no captó las últimas barras finales. Por ello en el archivo de conversión de semantic a midi se añade una barra final si no la hay. 


### reconocimiento.py: Inferencia

El proceso de reconocimiento de los elementos de la partitura los realiza la función inferencia del archivo reconocimiento.py. Esta función ejecuta el archivo ctc_predict.py dándole las ubicaciones de la imagen, el archivo semantic_model.meta y el archivo vocabulary_semantic.txt en el que se encuentran todos los posibles elementos de la partitura con sus diferentes posibilidades.


### semantic_midi.py: Conversión

En el archivo semantic_midi.py se realiza la conversión de semantic que es lo que se obtuvo en el proceso de inferencia a midi. Para realizar este proceso primero se pasa a MusicXML y luego se transforma a midi. Esto se hace utilizando la librería music21 que recrea la partitura a partir de los elementos reconocidos. Al finalizar guarda el archivo en formato midi en el archivo "salida.mid".

Para utilizar la librería music21 el python utilizado por VS Code debe ser el que se encuentra donde se instala music21, por ello se debe crear el settings.json con la ubicación de music21.

Para comprobar la correcta conversión de todos los diferentes y posibles elementos de semantic a la partitura se utilizaron los archivos que se encuentran tanto en /datos/imagenes_test como en /datos/imagenes_conv ya que pertenecen al dataset PrIMuS. De las imágenes en /datos/imagenes, las progresiones están sacadas del dataset DoReMi que se puede descargar a través del siguiente enlace: [dataset DoReMi](https://github.com/steinbergmedia/DoReMi/releases/download/v1.0/DoReMi_v1.zip) y el resto son de mis partituras.


### reproducir.py: Reproducción

A través de la librería pygame se reproduce automáticamente el archivo midi.


## Dependencias

- Python 3.10
- [music21](https://www.music21.org/music21docs/#)
- pygame
- [OpenCV](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- TensorFlow

Nota: Si usas VS Code asegúrate de configurar el intérprete de Python en settings.json para que incluya la ruta donde está instalado music21.


## Créditos

- [tf-end-to-end](https://github.com/OMR-Research/tf-end-to-end.git) - modelo y repo de Jorge Calvo Zaragoza
- [Dataset PrIMuS](https://grfia.dlsi.ua.es/primus/)
- [Dataset DoReMi](https://github.com/steinbergmedia/DoReMi/releases/download/v1.0/DoReMi_v1.zip)


## Licencia

Este proyecto es parte de un Trabajo de Fin de Grado (TFG). No se aceptan contribuciones externas.