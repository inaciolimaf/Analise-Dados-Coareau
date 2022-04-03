import pandas as pd
import os
import pdfkit


class DadosCoreau:
    def __init__(self):
        self.dados = pd.read_csv(
            "Portal da Transparência - PREFEITURA MUNICIPAL DE COREAÚ (CE).csv", encoding="utf-8")
        self.dfFiltrado = None

    def mostrar_arquivo(self):
        print(self.dados)

    def mostrar_cargos(self):
        cargos = set(self.dados['Cargo'])
        # Pega o valores das colunas e converte para conjunto para não repetir valores
        print(f"Os {len(cargos)} cargos são: ")
        for cargo in cargos:
            print(cargo)

    def filtrar_por_cargo(self, cargo, html_file_path="", pdf_file_path="", ordenar_salario=False):
        # Para filtrar um cago em específico
        self.dfFiltrado = self.dados.loc[self.dados['Cargo'] == cargo]
        if ordenar_salario:
            self._ordenar_salarios()

        if html_file_path == "" or pdf_file_path == "":
            self._exportar_pdf(
                self.dfFiltrado, f"{cargo}.html", f"{cargo}.pdf")
        else:
            self._exportar_pdf(self.dfFiltrado, html_file_path, pdf_file_path)

    def _ordenar_salarios(self):
        self._cria_coluna_float()
        self.dfFiltrado = self.dfFiltrado.sort_values(by=['salarioFloat'])
        # Valores ordenados
        self.dfFiltrado = self.dfFiltrado.drop(columns="salarioFloat")
        # Remove a coluna criada na função

    def _cria_coluna_float(self):
        quantidade_de_linhas = self.dfFiltrado.loc[:, "Cargo"].count()
        salarioFloatTotal = []
        for i in range(0, quantidade_de_linhas):
            salario = ''.join(
                x for x in self.dfFiltrado.iloc[i]["Líquido"] if x in "0123456789,")
            # Trata o valor do salário considerando apenas os númeoros e a vírgula
            salario = float(salario.replace(',', '.'))
            # Troca , por . e converte para float
            salarioFloatTotal.append(salario)
        self.dfFiltrado = self.dfFiltrado.assign(
            salarioFloat=salarioFloatTotal)
        # Cria uma nova coluna com os salário em float

    def _exportar_pdf(self, df: pd.DataFrame, html_file_path: str, pdf_file_path: str):
        html_file_path = self._concertar_path(html_file_path)
        pdf_file_path = self._concertar_path(pdf_file_path)
        print(pdf_file_path)
        # Mostra o path para se ter o progresso
        self._criar_pasta("resultados")
        df.to_html(html_file_path, index=False, encoding="utf-8")
        # Cria o arquivo html
        try:
            # Para usar isso é necessário instalar algumas coisas
            # Mais informaçãoes em: https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
            pdfkit.from_file(html_file_path, pdf_file_path)
            # Converte para pdf
        except OSError:
            pass
        os.remove(html_file_path)

    @staticmethod
    def _criar_pasta(nome_da_pasta):
        if not os.path.isdir(nome_da_pasta):
            os.mkdir(nome_da_pasta)

    @staticmethod
    def _concertar_path(file_path):
        file_path = os.path.join("resultados", file_path)
        # Adiciona no path a pasta resultados
        file_path = str.format(file_path)
        # Formata a string para tirar o \\
        file_path = ''.join(
            x for x in file_path if x not in "/")
        # Tira caracteres indesejados
        return file_path

    def filtrar_todos_cargos(self, html_file_path="", pdf_file_path="",  ordenar_salario=False):
        cargos = set(self.dados['Cargo'])
        for cargo in cargos:
            self.filtrar_por_cargo(cargo, html_file_path,
                                   pdf_file_path, ordenar_salario)

    def exportar_dados_completos(self):
        self._exportar_pdf(self.dados, f"Todos os dados.html",
                           f"Todos os dados.pdf")


if __name__ == "__main__":
    dados = DadosCoreau()
    dados.filtrar_todos_cargos(ordenar_salario=True)
    dados.exportar_dados_completos()
