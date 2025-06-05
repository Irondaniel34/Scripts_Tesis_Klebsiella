import os
import subprocess
import pandas as pd

def convertir_a_fasta(input_txt, output_fasta):
    with open(input_txt, "r") as infile, open(output_fasta, "w") as outfile:
        for line in infile:
            if line.startswith(">>"):
                line = ">" + line[2:]
            outfile.write(line)

def obtener_longitudes_query(fasta_file):
    longitudes = {}
    with open(fasta_file, "r") as f:
        header = ""
        seq = ""
        for linea in f:
            linea = linea.strip()
            if linea.startswith(">"):
                if header:
                    longitudes[header] = len(seq)
                header = linea[1:].split()[0]
                seq = ""
            else:
                seq += linea
        if header:
            longitudes[header] = len(seq)
    return longitudes

def main():
    print("📡 Script completo: conversión, BLAST y filtrado con valores estándar bibliográficos")

    txt_file = input("📄 Ingresa el archivo .txt con secuencias (ej. aminoglicosidos.txt): ").strip()
    if not os.path.exists(txt_file):
        print(f"❌ El archivo '{txt_file}' no existe.")
        return

    fasta_file = txt_file.replace(".txt", ".fasta")
    convertir_a_fasta(txt_file, fasta_file)

    query_file = "pan_genome_reference.fa"
    if not os.path.exists(query_file):
        print("❌ Falta el archivo 'pan_genome_reference.fa'.")
        return

    print("🔧 Creando base BLAST...")
    subprocess.run([
        "makeblastdb", "-in", fasta_file, "-dbtype", "nucl", "-out", "resist_db"
    ], check=True)

    raw_output = "blast_temp.tsv"
    print("🚀 Ejecutando BLAST...")
    subprocess.run([
        "blastn",
        "-query", query_file,
        "-db", "resist_db",
        "-evalue", "1e-10",
        "-outfmt", "6",
        "-num_threads", "2",
        "-out", raw_output
    ], check=True)

    output_file = input("📝 Nombre del archivo de salida filtrado (sin extensión): ").strip() + ".tsv"

    print("📏 Calculando longitudes de los queries...")
    query_lengths = obtener_longitudes_query(query_file)

    print("🔬 Aplicando filtros (≥95% identidad, ≥80% longitud, ≤2 mismatches/gaps, E≤1e-10)...")
    columnas = [
        "Query_ID", "Subject_ID", "%_Identity", "Alignment_Length", "Mismatch",
        "Gaps", "Query_Start", "Query_End", "Subject_Start", "Subject_End",
        "E-value", "Bit_Score"
    ]
    df = pd.read_csv(raw_output, sep="\t", names=columnas)
    df["E-value"] = pd.to_numeric(df["E-value"], errors="coerce")

    filtrados = []
    for _, row in df.iterrows():
        qid = row["Query_ID"]
        expected_len = query_lengths.get(qid, None)
        if expected_len is None:
            continue
        min_len = expected_len * 0.8
        if (
            row["%_Identity"] >= 95 and
            row["Alignment_Length"] >= min_len and
            row["Mismatch"] <= 2 and
            row["Gaps"] <= 2 and
            row["E-value"] <= 1e-10
        ):
            filtrados.append(row)

    df_filtrado = pd.DataFrame(filtrados)
    df_filtrado.to_csv(output_file, sep="\t", index=False)
    os.remove(raw_output)

    print(f"✅ {len(df_filtrado)} resultados filtrados guardados en '{output_file}'.")

if __name__ == "__main__":
    main()
