from inegi import INEGI
import pandas as pd

class PIB:

    def __init__(self, token):
        self.__token = token

    def __choice_actividad(self, df, actividad):

        if actividad == "total":
            return df
        if actividad == "sector":
            df = df[(df["sector"].str.len() == 2) | (df["sector"].str.len() == 5)]
            return df
        if actividad == "subsector":
            df = df[df["sector"].str.len() == 3]
            return df
        if actividad == "rama":
            df = df[df["sector"].str.len() == 4]
            return df
        else:
            print("La máxima desagregación es a nivel Rama (4 digitos)")
    

    def __choice_actividad_estatal(self, df, actividad):

        if actividad == "total":
            return df
        if actividad == "sector":
            df = df[(df["sector"].str.len() == 2) | (df["sector"].str.len() == 5)]
            return df
        if actividad == "subsector":
            df = df[(df["sector"].str.len() != 2) & (df["sector"].str.len() != 5)]
            return df
        else:
            print("La máxima desagregación es a nivel Rama (4 digitos)")


    def gen_claves_nacional(self,indicador,actividad):
        
        dic = pd.read_excel("diccionarios/diccionario_inegi.xlsx", 
                                     sheet_name="trimestral", 
                                     dtype={"clave":str, "sector": str}
                                     )
        claves = (dic[dic["indicador"] == indicador])

        claves =  self.__choice_actividad(claves, actividad)[["clave", "descripcion"]].set_index("clave")    
        
        claves =list(claves.to_records())

        return claves
    
    def gen_claves_estatal_sectorial(self, indicador, actividad, sector):
        
        dic = pd.read_excel("diccionarios/diccionario_inegi.xlsx", 
                                     sheet_name="anual", 
                                     dtype={"clave":str, "sector": str}
                                     )
        claves = (dic[dic["indicador"] == indicador])
        if sector:
            claves = (dic[(dic["indicador"] == indicador) & (dic["sector"] == sector)])

        claves =  self.__choice_actividad_estatal(claves, actividad)[["clave", "entidad", "descripcion"]].set_index("clave")
        
        claves =list(claves.to_records())
        
        return claves
    
    def gen_claves_estatal(self, indicador, actividad, entidad):
        
        dic = pd.read_excel("diccionarios/diccionario_inegi.xlsx", 
                                     sheet_name="anual", 
                                     dtype={"clave":str, "sector": str}
                                     )
        claves = (dic[(dic["indicador"] == indicador) & (dic["entidad"] == entidad)])

        claves =  self.__choice_actividad_estatal(claves, actividad)[["clave", "entidad", "descripcion"]].set_index("clave")
        
        claves =list(claves.to_records())
        
        return claves

    def get_data_nacional(self,
                 indicador: str = "PIB trimestral a precios de 2018",
                 grupo: str = "nacional",
                 actividad: str = "total",
                 ):
        
        API_INEGI_BI= INEGI('490dcd21-44b2-fef6-0ade-e6431a8c8fb9')
        
        if grupo == "nacional":
            claves = self.gen_claves_nacional(indicador, actividad)
            
            # return claves
        pib = API_INEGI_BI.obtener_datos(indicadores = claves[0][0])
        pib.columns = [claves[0][1]]

        claves.pop(0)

        for index, clave in enumerate(claves):
            df = API_INEGI_BI.obtener_datos(indicadores = clave[0])
            df.columns = [clave[1]]

            pib = pd.merge(pib, df, left_index=True, right_index=True)
            
        
        return pib
    
    def get_data_estatal(self,
                 indicador: str = "PIB anual a precios de 2018",
                 grupo: str = "estado",
                 actividad: str = "total",
                 entidad: str = "Aguascalientes",
                 sector: str = None
                 ):
        
        API_INEGI_BI= INEGI(self.__token)

        if grupo == "estado":
            claves = self.gen_claves_estatal(indicador, actividad, entidad)
            pib = API_INEGI_BI.obtener_datos(indicadores = claves[0][0])
            pib.columns = [claves[0][2]]

            claves.pop(0)

            for index, clave in enumerate(claves):
                df = API_INEGI_BI.obtener_datos(indicadores = clave[0])
                df.columns = [clave[2]]

                pib = pd.merge(pib, df, left_index=True, right_index=True)            
        
            return pib
        if grupo == "sector":
            claves = self.gen_claves_estatal_sectorial(indicador, actividad, sector)
            pib = API_INEGI_BI.obtener_datos(indicadores = claves[0][0])
            pib.columns = [claves[0][1]]

            claves.pop(0)

            for index, clave in enumerate(claves):
                df = API_INEGI_BI.obtener_datos(indicadores = clave[0])
                df.columns = [clave[1]]

                pib = pd.merge(pib, df, left_index=True, right_index=True)
                
            
            return pib