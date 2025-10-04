import streamlit as st

def calcular_tropas_equilibrado(madera_actual, arcilla_actual, hierro_actual):
    unidades = [
        ("Lancero", [50, 30, 10]),
        ("Soldado con espada", [30, 30, 70]),
        ("Arquero", [100, 30, 60]),
        ("Espía", [50, 50, 20]),
        ("Caballería ligera", [125, 100, 250])
    ]
    costo_total_set = [sum(c) for c in zip(*[u[1] for u in unidades])]
    reclutamiento = {unidad[0]: 0 for unidad in unidades}

    while True:
        unidades_construibles = []
        for nombre, costo in unidades:
            if madera_actual >= costo[0] and arcilla_actual >= costo[1] and hierro_actual >= costo[2]:
                unidades_construibles.append((nombre, costo))
        if not unidades_construibles:
            break

        ratio_madera = madera_actual / costo_total_set[0] if costo_total_set[0] > 0 else float('inf')
        ratio_arcilla = arcilla_actual / costo_total_set[1] if costo_total_set[1] > 0 else float('inf')
        ratio_hierro = hierro_actual / costo_total_set[2] if costo_total_set[2] > 0 else float('inf')

        recurso_limitante_idx = [ratio_madera, ratio_arcilla, ratio_hierro].index(min(ratio_madera, ratio_arcilla, ratio_hierro))

        mejor_unidad_nombre = ""
        mejor_unidad_costo = []
        min_costo_limitante = float('inf')

        for nombre, costo in unidades_construibles:
            costo_del_recurso_escaso = costo[recurso_limitante_idx]
            if costo_del_recurso_escaso < min_costo_limitante:
                min_costo_limitante = costo_del_recurso_escaso
                mejor_unidad_nombre = nombre
                mejor_unidad_costo = costo

        madera_actual -= mejor_unidad_costo[0]
        arcilla_actual -= mejor_unidad_costo[1]
        hierro_actual -= mejor_unidad_costo[2]
        reclutamiento[mejor_unidad_nombre] += 1

    return reclutamiento, madera_actual, arcilla_actual, hierro_actual

# Interfaz Streamlit
st.title("⚔️ Reclutador Tribal Equilibrado de yoelbulo")
st.write("Ingresá tus recursos y obtené el plan óptimo de reclutamiento para dejar todo lo más cerca de cero.")

madera = st.number_input("🌲 Madera", min_value=0, value=8000)
arcilla = st.number_input("🧱 Arcilla", min_value=0, value=6000)
hierro = st.number_input("쇠 Hierro", min_value=0, value=9000)

if st.button("Calcular"):
    tropas, madera_restante, arcilla_restante, hierro_restante = calcular_tropas_equilibrado(madera, arcilla, hierro)
    st.subheader("✅ Plan de reclutamiento:")
    for unidad, cantidad in tropas.items():
        if cantidad > 0:
            st.write(f"{unidad}: {cantidad}")
    st.markdown("---")
    st.write(f"🌲 Madera restante: {madera_restante}")
    st.write(f"🧱 Arcilla restante: {arcilla_restante}")
    st.write(f"쇠 Hierro restante: {hierro_restante}")
