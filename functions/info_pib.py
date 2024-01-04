import pandas as pd

class INFO_PIB:

    def __init__(self) -> None:
        pass


    def __read_entidades(self):
        entidades = (pd.read_parquet("data/catalogos/estados/estados.parquet")
             ).nom_agee.apply(lambda x: x.capitalize())
        
        return entidades


    def _ranking(self, df, sector, year):
        ranking = pd.DataFrame()
        year = str(year)
        entidades = self.__read_entidades()

        for entidad in entidades:
            temp = df[df["entidad"] == entidad].loc[[year]]
            temp["entidad"] = entidad
            ranking = pd.concat([ranking,temp])
        
        ranking = ranking.reset_index(drop=True)
        ranking = ranking.set_index("entidad")
        ranking = ranking[[sector]]
        ranking["rank"] = (ranking.rank(method="first", ascending=False))
        ranking = ranking.sort_values(by="rank")

        X = ranking[sector].sum()

        ranking["% nacional"] = (ranking[sector]/X)*100

        return ranking
    

    def _variacion(self, df, sector, year):
        df_f = pd.DataFrame()
        yeari = str(year - 1)
        yearf = str(year)
        entidades = self.__read_entidades()

        for entidad in entidades:
            temp = df[df["entidad"] == entidad].loc[[yeari, yearf]]
            temp["entidad"] = entidad
            temp = temp[["entidad",sector]]
            temp["cambio %"] = (temp[sector].pct_change())*100
            temp = temp.dropna()
            df_f = pd.concat([df_f,temp])
        

        return df_f
    
    
    def get_ranking(self,
                    df: pd.DataFrame,
                    sector: str = "Total", 
                    year: int = 2022,
                    estado: str = "Aguascalientes"
                    ):
        
        ranking = self._ranking(df, sector, year)
        ranking = ranking.loc[estado]
        val = round(ranking[0]/1000)
        rank = str(round(ranking[1]))
        nac =  round(ranking[2],2)


        return [val, rank, nac]
    

    def get_var(self, 
                df: pd.DataFrame,
                sector: str = "Total",
                year: int = 2022,
                estado: str = "Aguascalientes",
                ):
        
        var = self._variacion(df, sector, year).set_index("entidad")
        var = round(var.loc[estado][1], 2)

        return var
    

    def actividades_secundarias(self, 
                                df: pd.DataFrame, 
                                entidad: str = "Aguascalientes"):
        df = df[df["entidad"] == entidad]
        df = df[df["entidad"] == entidad]
        df = (df.iloc[-1:,7:13]).T
        total = df.loc["Total actividades secundarias"]

        df["% Actividades secundarias"] =  (df/total)*100
        df = df.reset_index()
        df.columns = ["Actividad","PIB 2022", "% Actividades secundarias"]
        df = df.sort_values("PIB 2022", ascending=False)

        return df
    

    def manufacturas(self,
                     df: pd.DataFrame,
                     entidad: str = "Aguascalientes"):
        
        df = df[df["entidad"] == entidad]
        df = (df.iloc[-1:,13:26]).T
        total = df.loc["Total industria manufacturera"]

        df["% manufacturas"] =  (df/total)*100
        df = df.reset_index()
        df.columns = ["Actividad","PIB 2022", "% de industria manufacturera"]
        df = df.sort_values("PIB 2022", ascending=False)

        return df
    

    def actividades_terciarias(self, 
                               df: pd.DataFrame, 
                               entidad: str = "Aguascalientes"):
        df = df[df["entidad"] == entidad]
        df = (df.iloc[-1:,26:-1]).T
        total = df.loc["Total actividades terciarias"]

        df["% actividades terciarias"] =  (df/total)*100
        df = df.reset_index()
        df.columns = ["Actividad","PIB 2022", "% Total actividades terciarias"]

        df = df.sort_values("PIB 2022", ascending=False)

        return df
    

    def table_style(self,
                    df:pd.DataFrame):

        th_props = [
        ('font-size', '16px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', '#ffffff'),
        ('background-color', '#B38E5D')
        ]

        td_props = [
        ('font-size', '14px')
        ]

        styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
        ]

        # table
        df = (df.style
            .format(precision=1, thousands=",")
            .set_properties(**{'text-align': 'left'})
            .set_table_styles(styles))
        
        return df