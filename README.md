# TFG
Diseño e Implementación de un sistema de transcripción de partituras en imágenes a sonido mediante reconocimiento de notas

Los datos estan distribuidos en las imagenes de las partituras, archivos agnostic, semantic y midi. Estos tres ultimos sirven para supervisar el algoritmo ya que se incluyen en el PrIMuS dataset. Las imagenes incorporadas en la carpeta se ha elegido de manera aleatoria del PrIMuS dataset.

En main.py se lleva a cabo el proceso para todas las imagenes incorporadas al repositorio.

En preprocessing.py se encuentran dos funciones. La primera binariza la imagen y la guarda bajo el nombre de cleaned_score.png. La segunda elimina las staff lines de la partitura y lo vuelve a guardar en cleaned_score.png.

En filter.py que luego se incorporará a preprocessing.py, se utiliza para eliminar los restos de staff lines que quedan al principio de la partitura antes de la clave de sol, fa o do.

En symbolRecognition.py se identifican los elementos de la partitura colocando rectángulos azules alrededor de estos.
