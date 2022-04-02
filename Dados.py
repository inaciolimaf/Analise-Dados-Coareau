import pandas as pd
import os
import pdfkit


class DadosCoreau:
    def __init__(self):
        self.dados = pd.read_csv(
            "Portal da Transparência - PREFEITURA MUNICIPAL DE COREAÚ (CE).csv", encoding="utf-8")

    def mostrar_arquivo(self):
        print(self.dados)

    def mostrar_cargos(self):
        cargos = set(self.dados['Cargo'])
        # Pega o valores das colunas e converte para conjunto para não repetir valores
        print(f"Os {len(cargos)} cargos são: ")
        for cargo in cargos:
            print(cargo)

    def filtrar_cargo(self, cargo, html_file_path="", pdf_file_path="", ordenar_salario=False):
        # Para filtrar um cago em específico
        dfFiltrado = self.dados.loc[self.dados['Cargo'] == cargo]
        if ordenar_salario:
            dfFiltrado = self.ordenar_salarios(dfFiltrado)

        if html_file_path == "" or pdf_file_path == "":
            self._exportar_pdf(dfFiltrado, f"{cargo}.html", f"{cargo}.pdf")
        else:
            self._exportar_pdf(dfFiltrado, html_file_path, pdf_file_path)

    @staticmethod
    def ordenar_salarios(dfFiltrado):
        quantidade_de_linhas = dfFiltrado.loc[:, "Cargo"].count()
        salarioFloatTotal = []
        for i in range(0, quantidade_de_linhas):
            salario = ''.join(
                x for x in dfFiltrado.iloc[i]["Líquido"] if x in "0123456789,")
            # Trata o valor do salário considerando apenas os númeoros e a vírgula
            salario = float(salario.replace(',', '.'))
            # Troca , por . e converte para float
            salarioFloatTotal.append(salario)
        dfFiltrado = dfFiltrado.assign(salarioFloat=salarioFloatTotal)
        # Cria uma nova coluna com os salário em float
        dfFiltrado = dfFiltrado.sort_values(by=['salarioFloat'])
        # Valores ordenados
        dfFiltrado = dfFiltrado.drop(columns="salarioFloat")
        # Remove a coluna
        return dfFiltrado

    @staticmethod
    def _exportar_pdf(df: pd.DataFrame, html_file_path: str, pdf_file_path: str):
        html_file_path = os.path.join("resultados", html_file_path)
        html_file_path = str.format(html_file_path)
        pdf_file_path = os.path.join("resultados", pdf_file_path)
        pdf_file_path = str.format(pdf_file_path)
        # Adiciona no path a pasta resultados
        print(pdf_file_path)
        # Mostra o path para se ter o progresso
        if not os.path.isdir("resultados"):
            os.mkdir("resultados")
            # Cria a pasta resultados
        df.to_html(html_file_path, index=False, encoding="utf-8")
        # Cria o arquivo html

        # Para usar isso é necessário instalar algumas coisas
        # Mais informaçãoes em: https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
        try:
            pdfkit.from_file(html_file_path, pdf_file_path)
            # Converte para pdf
        except OSError:
            pass
        os.remove(html_file_path)

    def filtrar_todos_cargos(self, html_file_path="", pdf_file_path="",  ordenar_salario=False):
        cargos = set(self.dados['Cargo'])
        for cargo in cargos:
            self.filtrar_cargo(cargo, html_file_path,
                               pdf_file_path, ordenar_salario)

    def exportar_dados_completos(self):
        self._exportar_pdf(self.dados, f"Todos os dados.html",
                           f"Todos os dados.pdf")


if __name__ == "__main__":
    dados = DadosCoreau()
    dados.filtrar_todos_cargos(ordenar_salario=True)
    dados.exportar_dados_completos()
