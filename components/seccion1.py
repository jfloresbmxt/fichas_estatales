import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space

def metrics(sline, i, iconname):
    fontsize = 16

    htmlstr = f"""<p style='color:rgb(0, 0, 0, 0.9);
                            font-size: {fontsize}px;
                            margin: 10px 10px;
                            border-width: 1px;
                            border-style: solid;
                            border-color: rgb(221, 201, 163);
                            border-radius: 7px;
                            padding-left: 0px; 
                            padding-top: 0px;
                            padding-bottom: 8px;
                            text-align: center;'>
                            <span style='font-size: 20px;
                            font-weight: bold;'
                            >{sline}</style></span>
                            <br>
                            {i}
                            <br>
                            <span style='font-size: 10px;
                            font-weight: bold;
                            padding: 0px;
                            margin: 0px;'>________________________</style></span>
                            <br>
                            <span style='font-size: 16px;
                            padding: 0px;
                            margin: 0px;'>{iconname}</style></span>
                            </style></p>"""
    
    return htmlstr

def html(a,b,c):
    htmlstr = f"""<ol style =
                            '
                            color:rgb(0, 0, 0, 0.9);
                            font-size: 16px;
                            margin: 10px 10px;
                            list-style-position: inside;
                            border-width: 1px;
                            border-style: solid;
                            border-color: rgb(221, 201, 163);
                            border-radius: 7px;
                            padding: 7px 0px;
                            text-align: center;
                            '>
                            <li style ='margin: 0px;
                            padding: 0px 0px;'
                            >{a}</style></li>
                            <li style ='margin: 0px;
                            padding: 0px 0px;'>{b}</li>
                            <li style ='margin: 0px;
                            padding: 0px 0px;'>{c}</li>
                            </style></ol>"""
    
    return htmlstr

def seccion1(info, info2, info3, info4, info5, info6, info7, info8):
    valor = info[0]
    rank = info[1]
    nac = info[2]

    valor_m = info3[0]
    rank_m = info3[1]
    nac_m = info3[2]

    add_vertical_space()
    with stylable_container(
        key="container_with_border1",
        css_styles="""
            {
                border: 2px dashed rgb(221, 201, 163);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                text-align: center;
            }
            
            """,
    ):
        col4, col5 = st.columns(2)
        with col4:
            st.markdown("**Producto Interno Bruto, 2022**")
            col8, col9, col10 = st.columns(3)
            with col8:
                st.markdown(metrics(f"{rank}°", "economía del país","1° lugar CDMX"), unsafe_allow_html=True)
            with col9:
                st.markdown(metrics(f"{format(valor, ',d')}", "mil millones MXN",f"{nac}% del nacional"), unsafe_allow_html=True)
            with col10:
                st.markdown(metrics(f"{info2}%", "crec. 2021-2022",f"3.94% crec nacional"), unsafe_allow_html=True)

            add_vertical_space()
            st.markdown("**PIB Manufacturero, 2022**")
            col11, col12, col13 = st.columns(3)
            with col11:
                st.markdown(metrics(f"{rank_m}°", "economía del país","1° lugar Nuevo León"), unsafe_allow_html=True)
            with col12:
                st.markdown(metrics(f"{format(valor_m, ',d')}", "mil millones MXN",f"{nac_m}% del nacional"), unsafe_allow_html=True)
            with col13:
                st.markdown(metrics(f"{info4}%", "crec. 2021-2022",f"6.33% crec nacional"), unsafe_allow_html=True)
        
        with col5:
            st.markdown("**Exportaciones, 2022**")
            col14, col15, col16 = st.columns(3)
            with col14:
                st.markdown(metrics(f"{info5}°", "economía del país","1° lugar Chihuahua"), unsafe_allow_html=True)
            with col15:
                st.markdown(metrics(f"{format(info6, ',d')}", "millones USD",f"{info7}% del nacional"), unsafe_allow_html=True)
            with col16:
                st.markdown(metrics(f"{info8}%", "crec. 2021-2022",f"18.14% crec nacional"), unsafe_allow_html=True)