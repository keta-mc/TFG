import subprocess

def inferencia(ruta_imagen, ruta_modelo, ruta_vocabulario):
    resultado = subprocess.run(
        [
            "python3", "ctc_predict.py",
            "-image", ruta_imagen,
            "-model", ruta_modelo,
            "-vocabulary", ruta_vocabulario
        ],
        capture_output=True,
        text=True
    )
    prediccion = resultado.stdout.strip()
    return(prediccion.split())