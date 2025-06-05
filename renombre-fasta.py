# renombrar_nhx_interno.py
import re

# Solicita el nombre del archivo original y del archivo de salida
input_file = input("📝 Ingresa el nombre del archivo .nhx: ").strip()
output_file = input("📁 Ingresa el nombre del archivo de salida: ").strip()

# Lee el contenido
with open(input_file, 'r') as f:
    contenido = f.read()

# Elimina la parte final ".fasta" de todos los nombres
contenido_modificado = re.sub(r'(\d+_GCF|GCA|GCF.*?)(\.fasta)', r'\1', contenido)

# Guarda el resultado
with open(output_file, 'w') as f:
    f.write(contenido_modificado)

print(f"✅ Nombres internos corregidos y guardados en: {output_file}")
