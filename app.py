import streamlit as st
import pandas as pd
from components.header import header, subheader
from components.seccion1 import seccion1
from streamlit_extras.metric_cards import style_metric_cards
from functions.info_pib import INFO_PIB
from functions.exportaciones import EXPORTACIONES


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


exp = EXPORTACIONES()
data5 = exp.gen_entidad(entidad)[3]
data6 = exp.gen_entidad(entidad)[0]
data7 = exp.gen_entidad(entidad)[1]
data8 = exp.gen_entidad(entidad)[2]

seccion1(data, data2, data3, data4, data5, data6, data7, data8)

def example():
    col1, col2, col3 = st.columns(3)

    col1.metric(label="Gain", value=5000, delta=1000)
    col2.metric(label="Loss", value=5000, delta=-1000)
    col3.metric(label="No Change", value=5000, delta=0)

    style_metric_cards()


hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </>
                    """

st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.subheader("Participación")

participacion = info.participación_sectores(get_catalogos()[1], entidad)
participacion = info.table_style(participacion)
st.table(participacion)

st.header("PIB Secundario")

actividades_sec = info.actividades_secundarias(get_catalogos()[1], entidad)
actividades_sec = info.table_style(actividades_sec)

actividades_man = info.manufacturas(get_catalogos()[1], entidad)
actividades_man = info.table_style(actividades_man)

with st.expander("PIB Secundario"):
    st.table(actividades_sec)
    st.table(actividades_man)

st.header("PIB Terciario")
actividades_ter = info.actividades_terciarias(get_catalogos()[1], entidad)
actividades_ter =  info.table_style(actividades_ter)

with st.expander("PIB terciario"):
    st.table(actividades_ter)
