import streamlit as st
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
from components.header import header, subheader
from components.seccion1 import seccion1
from functions.info_pib import INFO_PIB

st.set_page_config(
    page_title="Fichas estatales",
    layout="wide"
)

## CACHE
@st.cache_data
def get_catalogos():
    entidades = (pd.read_parquet("data/catalogos/estados/estados.parquet")
                 .sort_values(by="nom_agee")).nom_agee.apply(lambda x: x.capitalize())
    
    pib_nom = pd.read_excel("data/pib/pib_nominalv2.xlsx",
                            dtype={"periodo":str}).set_index("periodo")
    
    pib_real = pd.read_excel("data/pib/pib_realv2.xlsx",
                            dtype={"periodo":str}).set_index("periodo")
    
    
    return [entidades, pib_nom, pib_real]


entidad = st.selectbox("Selecciona entidad", get_catalogos()[0])

## HEADER
header(entidad)
subheader("Panorama general del estado")


info = INFO_PIB()

data = info.get_ranking(get_catalogos()[1], estado = entidad)
data2 = info.get_var(get_catalogos()[2], estado = entidad)

data3 = info.get_ranking(get_catalogos()[1], sector="Total industria manufacturera", estado=entidad)
data4 = info.get_var(get_catalogos()[2], sector="Total industria manufacturera", estado=entidad)

seccion1(data, data2, data3, data4)


hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </>
                    """
actividades_sec = info.actividades_secundarias(get_catalogos()[2], entidad)
actividades_sec = info.table_style(actividades_sec)

st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.table(actividades_sec)

actividades_man = info.manufacturas(get_catalogos()[2], entidad)
actividades_man = info.table_style(actividades_man)

st.table(actividades_man)
