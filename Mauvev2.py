#!/usr/bin/env python3
import os
import subprocess
import shutil

def find_fasta_files(directory):
    """Busca archivos .fasta y .fna en el directorio."""
    fasta_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.fasta', '.fna'))]
    return fasta_files

def run_mauve(fasta_files):
    """Ejecuta progressiveMauve con los archivos FASTA detectados."""
    if not fasta_files:
        print("❌ No se encontraron archivos .fasta o .fna en el directorio.")
        return

    if not shutil.which("progressiveMauve"):
        print("❌ Error: progressiveMauve no está instalado o no está en el PATH.")
        return

    print("📂 Archivos encontrados para alineamiento:")
    for file in fasta_files:
        print(f" - {file}")
    
    output_file = input("📄 Ingresa el nombre para el archivo de salida (incluye .xmfa): ").strip()
    if not output_file.endswith(".xmfa"):
        output_file += ".xmfa"

    # 🧱 También se generará un archivo backbone
    backbone_file = output_file.replace(".xmfa", ".backbone")

    # Ejecutar Mauve con backbone
    command = ["progressiveMauve", "--output=" + output_file, "--backbone-output=" + backbone_file] + fasta_files
    print("🚀 Ejecutando Mauve...")

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        with open("mauve_log.txt", "w") as log_file:
            log_file.write(result.stdout + "\n" + result.stderr)

        if os.path.exists(output_file):
            print(f"\n✅ Alineamiento completado: {output_file}")
            print(f"📎 Archivo backbone generado: {backbone_file}")
        else:
            print("❌ Error en el alineamiento. Revisa mauve_log.txt para más detalles.")
    except Exception as e:
        print(f"❌ Error al ejecutar Mauve: {e}")

if __name__ == "__main__":
    directory = os.getcwd()
    fasta_files = find_fasta_files(directory)
    run_mauve(fasta_files)
