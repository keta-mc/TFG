import subprocess
import os 
def convert_musicxml_to_png(xml_path, output_png_path, musescore_path="musescore4"):
    try:
        subprocess.run([musescore_path, xml_path, "-o", output_png_path], check=True)
        print(f"Imagen generada: {output_png_path}")
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar MuseScore: ", e)

xml_file = "/home/catalina/Documents/tfg/musicma++/MUSICMA-pp_v1.0/v1.0/data/cropobjects_withstaff/CVC-MUSICMA_W-01_D-ideal.xml"
output_png_file = "/home/catalina/Documents/tfg/git/tfg/score.png"

convert_musicxml_to_png(xml_file, output_png_file, musescore_path="musescore4")