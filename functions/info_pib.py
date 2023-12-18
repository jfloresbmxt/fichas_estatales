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
                    sector: str|list = "Total", 
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