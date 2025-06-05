import os
import subprocess
import glob

# Mensaje inicial
print("📂 Ingresa el nombre de la carpeta con los archivos .gff3:", end=" ")
folder = input().strip()

# Buscar archivos .gff3 en la carpeta
gff3_files = sorted(glob.glob(os.path.join(folder, "*.gff3")))

if not gff3_files:
    print(f"❌ No se encontraron archivos .gff3 en la carpeta '{folder}'")
    exit()

# Crear carpeta de salida
outdir = f"panaroo_out_{os.path.basename(folder)}"
os.makedirs(outdir, exist_ok=True)

# Mostrar información
print(f"\n🔧 Ejecutando Panaroo con {len(gff3_files)} archivos de '{folder}'...")
print("📌 Modo: clean-mode sensitive + alineamiento de genes core con MAFFT\n")

# Ejecutar Panaroo
cmd = [
    "panaroo",
    "-i", *gff3_files,
    "-o", outdir,
    "--clean-mode", "sensitive",
    "--aligner", "mafft",
    "--remove-invalid-genes"
]

try:
    subprocess.run(cmd, check=True)
    print("\n✅ Panaroo finalizado exitosamente.")
    print(f"📁 Archivos de salida en: {outdir}")
except subprocess.CalledProcessError:
    print("\n⚠️ Panaroo finalizó, pero no se generó el archivo core_gene_alignment.aln.")
    print("🔍 Revisa si aún hay demasiados genes truncados o si los genomas tienen baja intersección de genes core.")

