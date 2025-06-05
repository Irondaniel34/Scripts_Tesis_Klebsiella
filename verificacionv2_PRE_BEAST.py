import re

def verificar_formato_y_tipdates(filepath):
    with open(filepath, 'r') as file:
        contenido = file.read()

    errores = []
    advertencias = []

    # Verificaciones estructurales
    if not contenido.strip().startswith("#NEXUS"):
        errores.append("❌ Falta cabecera '#NEXUS' al inicio.")

    if "Begin taxa;" not in contenido:
        errores.append("❌ Falta bloque 'Begin taxa;'.")

    if "Begin trees;" not in contenido:
        errores.append("❌ Falta bloque 'Begin trees;'.")

    if "Translate" not in contenido:
        errores.append("❌ Falta sección 'Translate' dentro del bloque de árboles.")

    if "tree STATE_" not in contenido:
        errores.append("❌ No se detectaron líneas de árboles como 'tree STATE_...'.")

    bloques_begin = contenido.lower().count("begin")
    bloques_end = contenido.lower().count("end;")
    if bloques_begin != bloques_end:
        errores.append(f"❌ Desbalance entre bloques 'Begin' ({bloques_begin}) y 'End;' ({bloques_end}).")

    # Verificación de calibración temporal (tip dates)
    heights = re.findall(r'height=([0-9]+\.[0-9]+)', contenido)
    if heights:
        alturas = [float(h) for h in heights]
        alturas_mayores_1900 = [h for h in alturas if h > 1900]
        alturas_cero = all(h == 0.0 for h in alturas)

        if alturas_cero:
            advertencias.append("⚠️ Todas las alturas de los nodos están en cero: podrían no haberse aplicado fechas de muestreo (tip dates).")
        elif len(alturas_mayores_1900) > 0:
            print("✅ ¡El árbol parece estar calibrado en años calendario! Ej: height ≈", alturas_mayores_1900[0])
        else:
            advertencias.append("⚠️ Las alturas de los nodos no parecen estar en escala de años (no se detectan valores > 1900).")
    else:
        advertencias.append("⚠️ No se encontraron campos 'height=' en los nodos.")

    # Resultados
    print("\n📋 RESULTADO DE VERIFICACIÓN:")
    if not errores:
        print("✅ Estructura básica NEXUS válida.")
    else:
        print("❌ Problemas estructurales encontrados:")
        for err in errores:
            print("   -", err)

    if advertencias:
        print("\n🔎 Advertencias sobre calibración temporal:")
        for adv in advertencias:
            print("   -", adv)

# === USO ===
# Reemplaza con tu archivo real:
verificar_formato_y_tipdates("Klebsiella_Def_core_gene.trees")
