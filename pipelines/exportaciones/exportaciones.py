import pandas as pd
from janitor import clean_names
import zipfile, urllib.request, shutil

class EXPORTACIONES:
    
    def __init__(self) -> None:
        pass
    
    def __read_data(self):
        types = {"E03": str, "CODIGO_SCIAN":str}
        cols = ["ANIO", "TRIMESTRE", "E03", "CODIGO_SCIAN", "VAL_USD"]

        df = (pd.read_csv("data/conjunto_de_datos/eef_trimestral_tr_cifra_2007_2023.csv",
                          usecols = cols,
                         dtype=types)
                         .fillna(0)
                         .rename(columns={"E03":"cve"})
                         )
    
        df = clean_names(df)
        df["val_usd"] = df["val_usd"]/1000

        return df
    

    def __change_letter(self, x):
        
        if x == "I":
            return "1"
        elif x == "II":
            return "2"
        elif x == "III":
            return "3"
        elif x == "IV":
            return "4"
        else:
            
            return x
    
    def __format_dates(self, df):

        df["anio"] = df["anio"].astype(str)
        df["trimestre"] = df["trimestre"].apply(self.__change_letter)
        df["fecha"] = df["anio"] + "/" + df["trimestre"]
        df["fecha"] =pd.to_datetime(df["fecha"], format="mixed")

        df["year"] = df["fecha"].dt.year.apply(str)
        df["Q"] = df["fecha"].dt.month.apply(str)
        df["Q"] = "Q" + df["Q"]

        df["Period"] = df["year"] + df["Q"]

        df["Period"] = pd.PeriodIndex(df["Period"], freq="Q")

        df.drop(columns={"anio", "trimestre"}, inplace=True)

        df = df.set_index("Period")

        return df
    

    def _merge_entidad(self):
        df = self.__read_data()

        entidades =  pd.read_csv("data/catalogos/tc_entidad.csv", dtype = {"E03":str})
        entidades = clean_names(entidades)

        df = (df
              .merge(entidades, left_on="cve", right_on="e03")
              .drop(columns={"e03"}))
        df.rename(columns = {"nom_entidad":"entidad"}, inplace=True)

        return df
    

    def _merge_scian(self):
        df = self._merge_entidad()

        scian = pd.read_csv("data/catalogos/tc_scian.csv", dtype={"CODIGO_SCIAN":str})
        scian = clean_names(scian)

        df = (df
              .merge(scian)
              .drop(columns={"version"})
              .rename(columns={"descripcion":"subsector",
                               "val_usd":"monto"}
                               )
              )
        
        return df

        
    def donwload_data(self):
        url = "https://www.inegi.org.mx/contenidos/programas/exporta_ef/datosabiertos/conjunto_de_datos_eef_trimestral_csv.zip"
        file_name = "exportacions.zip"

        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            with zipfile.ZipFile(file_name) as zf:
                zf.extractall("data")

    
    def group_by_(self, by : list|str = ["entidad"]):
        df = self._merge_scian()

        df = self.__format_dates(df)

        df = (df
              .groupby(by)
              .agg({"monto":"sum"})
              .reset_index()
              )

        return df
    

    def filter(self,
               entidad = "Aguascalientes"):
        
        df = self._merge_scian()

        df = self.__format_dates(df)

        return df
    

    def _gen_nacional(self):
        df = self._merge_scian()

        df = self.__format_dates(df)

        df = df[(df["year"]>"2020") & (df["year"]<"2023")]

        df_montos = (df.groupby(["year"]).agg({"monto":"sum"}))

        monto = df_montos.loc["2022", "monto"]
        crecimiento = (df_montos.pct_change()*100).loc["2022", "monto"]

        ranking = (df[df["year"] == "2022"]
                .groupby("entidad").agg({"monto":"sum"})
                .rank(ascending=False)
                .sort_values("monto"))

        return [monto, crecimiento, ranking]
    

    def gen_entidad(self, entidad: str = "Aguascalientes"):
        monto_nacional = self._gen_nacional()[1]
        ranking = self._gen_nacional()[2]
        exp = self.filter()

        df = exp[exp["entidad"] == entidad].reset_index()

        df = df[(df["year"]>"2020") & (df["year"]<"2023")]
        df = df.groupby(["year"]).agg({"monto":"sum"})
        
        monto_estatal = round(df.loc["2022", "monto"],2)
        porcentaje_estatal = round((monto_nacional/monto_estatal)*100, 1)

        crecimiento = (df.groupby(["year"]).agg({"monto":"sum"})
                    .pct_change()*100).loc["2022","monto"]
        
        r_estatal = ranking[ranking.index == entidad].loc[entidad, "monto"]

        return [monto_estatal,porcentaje_estatal, crecimiento, r_estatal]