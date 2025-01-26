import os
import pandas as pd
from datetime import date

def salvarPlanilha(dir, dados):

    if dir[-3:].lower() != 'csv':
        dir = dir + '.csv'

    try:
        df = pd.DataFrame(dados)
        df.to_csv(dir, index=False, encoding='utf-8-sig', sep=';')
        print("Arquivo salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

if __name__ == '__main__':
    
    user = os.environ.get("USERNAME")
    #criarPlanilha(f'c:\\Users\\{user}\\Downloads')


