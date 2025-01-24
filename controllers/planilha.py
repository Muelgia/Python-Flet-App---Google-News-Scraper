import os
import pandas as pd
from datetime import date

class ExcelFunc():
    def __init__(self):
        self.self = self
    
    def subirExcel(self, planilha):
        
        if planilha[-4:] == 'xlsx':
            try:
                planilhaXlsx = pd.read_excel(planilha)
                print(planilhaXlsx)
            except Exception as e:
                print(e)
                return "Erro ao ler a planilha em formato xlsx"
        
        else:
            return "Formato de arquivo inválido!"

        return planilhaXlsx

def criarPlanilha(dir):

    dir = dir+'\\Template.xlsx'

    dataFrameExcel = {'CNPJ': [], 'Adabas': []}
    dataFrame = pd.DataFrame(dataFrameExcel)
    dataFrame.to_excel(dir, index=False)

    print(f'Planilha template criada em {dir}')
    return f'Planilha template criada em {dir}'


def salvarPlanilha(dir):



    dir = dir+f'\\Relatório SFA {date.today()}.xlsx'

    csv_file = 'controllers/cacheDF.txt'
    df = pd.read_csv(csv_file, sep=';', quotechar='"')
    df.to_excel(dir, index=False, engine='openpyxl')

    print(f'Relatório salvo em {dir}')
    return f'Relatório salvo em {dir}'

if __name__ == '__main__':
    
    user = os.environ.get("USERNAME")
    #criarPlanilha(f'c:\\Users\\{user}\\Downloads')


