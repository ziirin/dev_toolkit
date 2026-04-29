import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Seguimiento semanal", layout="centered")

st.title('Seguimiento semanal')

now = datetime.now()
current_weekday = now.weekday() % 7
current_monday = now - timedelta(days=current_weekday)
months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
st.subheader(f'Semana en curso ({current_monday.day} {months[current_monday.month - 1]})')

# 1. Inicializar el estado de la lista de inputs si no existe
if 'lista_tareas' not in st.session_state:
    st.session_state.lista_tareas = [""] # Empezamos con un input vacío

# 2. Función para añadir un nuevo campo
def añadir_campo():
    st.session_state.lista_tareas.append("")

# 3. Mostrar los inputs dinámicamente
# Usamos un formulario para que los botones de abajo no refresquen la página constantemente
with st.container():
    for i, tarea in enumerate(st.session_state.lista_tareas):
        # Creamos cada input con una clave única basada en su índice
        st.session_state.lista_tareas[i] = st.text_input(
            f"Tarea {i+1}:", 
            value=tarea, 
            key=f"input_{i}"
        )

# 4. Botón para añadir más (estilo lista)
st.button("➕ Añadir otra tarea", on_click=añadir_campo)

st.markdown("---") # Separador visual para el footer

# 5. Footer con dos columnas para los botones de acción
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("❌ Cancelar", use_container_width=True):
        st.session_state.lista_tareas = [""]
        st.rerun()

with col2:
    if st.button("🚀 Enviar", type="primary", use_container_width=True):
        # Aquí iría la lógica para enviar el correo o procesar los datos
        tareas_finales = [t for t in st.session_state.lista_tareas if t.strip() != ""]
        if tareas_finales:
            st.success(f"Enviando {len(tareas_finales)} tareas...")
            st.write(tareas_finales)
        else:
            st.warning("No hay tareas válidas para enviar.")