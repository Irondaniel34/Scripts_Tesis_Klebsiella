import pandas as pd
import os

# === Entradas ===
blast_file = input("🔬 Archivo BLAST filtrado (.tsv): ").strip()
output_file = input("📄 Nombre del archivo de salida final (sin extensión): ").strip() + ".xlsx"

# === Archivos fijos ===
script_dir = os.path.dirname(os.path.abspath(__file__))
gene_data_file = os.path.join(script_dir, "gene_data.csv")
gpa_file = os.path.join(script_dir, "gene_presence_absence.csv")

# === Cargar datos ===
blast_df = pd.read_csv(blast_file, sep="\t")
gene_data_df = pd.read_csv(gene_data_file)
gpa_df = pd.read_csv(gpa_file)

# === Funciones para extraer info del Subject_ID ===
def get_nombre_funcional(subject_id):
    parts = str(subject_id).split("|")
    if parts[-1] == "RequiresSNPConfirmation" and len(parts) >= 2:
        return parts[-2].strip()
    return parts[-1].strip()

def get_id_funcional(subject_id):
    parts = str(subject_id).split("|")
    nombre = get_nombre_funcional(subject_id)
    return f"{nombre} ({parts[0].strip()})" if parts else nombre

def get_familia_funcional(subject_id):
    parts = str(subject_id).split("|")
    if parts[-1] == "RequiresSNPConfirmation" and len(parts) >= 3:
        return parts[-3].strip()
    elif len(parts) >= 2:
        return parts[-2].strip()
    return "No identificado"

# === Aplicar funciones ===
blast_df["Nombre_funcional"] = blast_df["Subject_ID"].apply(get_nombre_funcional)
blast_df["ID_funcional_completo"] = blast_df["Subject_ID"].apply(get_id_funcional)
blast_df["Familia_funcional"] = blast_df["Subject_ID"].apply(get_familia_funcional)

# === Crear diccionarios por Query_ID ===
nombre_funcional_dict = blast_df.groupby("Query_ID")["Nombre_funcional"].first().to_dict()
id_funcional_dict = blast_df.groupby("Query_ID")["ID_funcional_completo"].first().to_dict()
familia_funcional_dict = blast_df.groupby("Query_ID")["Familia_funcional"].first().to_dict()

# === Generar tabla final ===
genes_blast = blast_df["Query_ID"].unique()
resultados = []

for gen in genes_blast:
    if gen in gpa_df["Gene"].values:
        fila = gpa_df[gpa_df["Gene"] == gen]
        columnas_genomas = gpa_df.columns[14:]
        cepas_presentes = fila[columnas_genomas].notna().values[0]
        lista_cepas = columnas_genomas[cepas_presentes].tolist()
        n_cepas = len(lista_cepas)
    else:
        lista_cepas = []
        n_cepas = 0

    nombre_funcional = nombre_funcional_dict.get(gen, "No identificado")
    id_funcional = id_funcional_dict.get(gen, "No definido")
    familia_funcional = familia_funcional_dict.get(gen, "No identificada")

    # Descripción (desde gene_data o por defecto)
    info_gene = gene_data_df[gene_data_df["annotation_id"] == gen]
    if info_gene.empty:
        info_gene = gene_data_df[gene_data_df["gene_name"] == gen]
    if info_gene.empty:
        info_gene = gene_data_df[gene_data_df["annotation_id"].astype(str).str.contains(gen, na=False) |
                                  gene_data_df["gene_name"].astype(str).str.contains(gen, na=False)]

    if not info_gene.empty:
        descripcion = info_gene["description"].dropna().unique()
        descripcion = descripcion[0] if len(descripcion) > 0 else "Sin descripción"
    else:
        descripcion = "Sin descripción"

    # Clasificación tipo genómico
    tipo = "no identificado"
    total_cepas = len(gpa_df.columns[14:])
    if n_cepas == total_cepas:
        tipo = "core"
    elif n_cepas > 1:
        tipo = "accessory"
    elif n_cepas == 1:
        tipo = "singleton"

    resultados.append([
        gen,
        ";".join(lista_cepas),
        n_cepas,
        nombre_funcional,
        id_funcional,
        familia_funcional,
        descripcion,
        tipo
    ])

# === Guardar Excel final ===
columnas = [
    "Gene", "Cepa(s)_presentes", "N°_Cepas", "Nombre_funcional", "ID_funcional_completo",
    "Familia_funcional", "Descripción", "Tipo_genoma"
]
df_final = pd.DataFrame(resultados, columns=columnas)
df_final.to_excel(output_file, index=False)

print(f"✅ Archivo Excel generado correctamente con identificadores funcionales y familia: {output_file}")
