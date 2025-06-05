from Bio import AlignIO

# Pedir nombres de archivo al usuario
input_file = input("Nombre del archivo de entrada (.aln): ").strip()
output_file = input("Nombre del archivo de salida (ej. .fasta o .nexus): ").strip()

# Deducir el formato de salida
if output_file.endswith(".fasta") or output_file.endswith(".fa"):
    output_format = "fasta"
elif output_file.endswith(".nexus"):
    output_format = "nexus"
else:
    raise ValueError("El archivo de salida debe terminar en .fasta, .fa o .nexus")

# Leer el archivo como fasta alineado
alignment = AlignIO.read(input_file, "fasta")
AlignIO.write(alignment, output_file, output_format)

print(f"Conversión completada: '{input_file}' → '{output_file}'")
