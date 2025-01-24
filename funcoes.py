import os 
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import subprocess
import psutil
import pandas as pd

class TrabalhaPlanilhas:
    def __init__(self):
        self = self
    
    # SE ASSEGURA DE QUE O DATAFRAME PARAMETRO ESTEJA COM O TIPO CORRETO (pd.DataFrame), É UTILIZADO EM TODAS AS FUNÇÕES DA CLASSE
    def assert_planilha(self, dados):    
        """Se assegura de que o dataframe parametro esteja com o tipo correto (pd.dataframe);\n
        Caso seja passado um caminho como parametro, se for válido, converte o caminho para DataFrame."""
        if isinstance(dados, str):
            if os.path.exists(dados):
                caminho = dados
                print(f"{caminho} localizada\n")

                if '.xlsx' in caminho:
                    dados = pd.read_excel(caminho)

                elif '.csv' in caminho:
                    dados = pd.read_csv(caminho)                    

            else:
                print("Planilha não encontrada, verifique o caminho")
                return
            
        if isinstance(dados,pd.DataFrame):
            dados = dados

        return dados

    # RETORNA UMA LISTA COM AS FONTES COM O NUMERO DE LINHAS RELATIVO A DIVISAO PELO NUMERO INSERIDO
    def divide_por_num(self, dataframe: pd.DataFrame, numero_divisoes: int):
        """Divide o total de linhas do DataFrame pelo valor int fornecido;\n
        Retorna um dicionário com os DataFrames separados de acordo com o numero de divisões escolhido.\n
        **Os valores retornados no dicionário são acessíveis pelo nome 'fonte{i}' sendo 'i' um valor do tipo
        int com índice de '1' até 'numero_divisoes' declarado.**"""
        dataframe = self.assert_planilha(dataframe)
        # Alerta sobre o número de divisoes caso seja alto
        if numero_divisoes > 40:
            confirma = input("O número de divisões é muito alto e pode prejudicar o processamento da máquina por alguns instantes.\nDeseja continuar mesmo assim: [S/N] >>")
            if not confirma in 'Ss':
                return

        # Prepara e exibe os dados
        tam_total = len(dataframe)
        tam_fonte = round(tam_total/numero_divisoes)
        print (f'Total de linhas: {tam_total}')
        print (f'{tam_fonte} linhas por planilha')
        
        # Dicionario que recebe e retorna os dataframes divididos
        separados = {}
        # Recorta os dataframes divididos e lista eles em separados{}
        for i in range(numero_divisoes):
            nome =  f"{i+1}"  
            valor = dataframe[tam_fonte*i:tam_fonte*(i+1)]
            separados[nome] = valor
        return separados

    # RETORNA UMA LISTA COM AS FONTES DIVIDIDAS COM O NUMERO DE LINHAS INSERIDO E CASO INFORMADO, DIVIDE SOMENTE ATÉ O MAX SELECIONADO
    def divide_por_lin(self, dataframe: pd.DataFrame, numero_linhas: int, max_planilhas: int = None):
        """Divide o total de linhas do DataFrame colocando o numero de linhas declarado em cada divisão da base;\n
        Se 'max_planilhas' for declarado, será definido um limite de DataFrames gerados **(Recomendável declarar).**\n
        Retorna um dicionário com os DataFrames separados com o numero de linhas especificado.\n
        **Os valores retornados no dicionário são acessíveis pelo nome 'fonte{i}' sendo 'i' um valor do tipo
        int a partir do índice '1'**"""
        dataframe = self.assert_planilha(dataframe)
        print(dataframe)
        # Prepara e exibe os dados
        tam_total = len(dataframe)
        max_lines = tam_total
        print (f'Total de linhas: {tam_total}')

        # Dicionario que recebe e retorna os dataframes divididos
        separados = {}
        cut_end = 0
        i = 0
        # Define qual o numero maximo de planilhas feitas, se nenhum valor for atribuido na chamada dessa função então esse bloco será pulado
        if max_planilhas != None:
            max_lines = (numero_linhas * max_planilhas)#+1
            print(max_lines)
            if max_lines > tam_total:
                print(f'{max_planilhas} planilhas com {numero_linhas} é muito alto para informação disponível!({tam_total} linhas na fonte)')
                return 
        print (f'{numero_linhas} linhas por planilha')

        # Recorta os dataframes divididos e lista eles em separados{}
        while True:
            cut_start = numero_linhas * i
            cut_end = numero_linhas * (i+1)

            if not cut_end < max_lines+1:
                break
            
            nome = f'{i+1}'
            valor = dataframe[cut_start:cut_end]
            separados[nome] = valor
            print(separados[nome])
            i += 1
        return separados 

    # SALVA A PLANILHA NO CAMINHO SELECIONADO (SE NENHUM CAMINHO FOR SELECIONADO, SALVA NO DIRETORIO ORIGEM ONDE ESTÁ SENDO EXECUTADO O CODIGO), COM O NOME SELECIONADO E CASO 'MULTIPLE = TRUE' SALVA DENTRO DE LOOPS SEM SOBRESCREVER
    def salvar_planilha(self, dataframe: pd.DataFrame, nome: str = None, formato: str = None, caminho: str = None, multiple: bool = False) -> str:
        """Salva o Dataframe em formato CSV ou XLSX;\n
        Se for atribuído a uma variável, retorna o caminho do arquivo salvo.\n
        *Caso caminho não seja declarado, o arquivo será salvo no diretório origem onde está sendo executado*,\n
        *Caso somente dataframe e um arquivo existente seja declarado como caminho, o arquivo original será sobrescrito*\n
        *Ao declarar 'multiple = True', arquivos salvos não serão sobrescritos e receberão uma numeração a partir de '1'*"""
         # Assegura que o DataFrame é válido
        dataframe = self.assert_planilha(dataframe)

        # Define o caminho e formato se fornecido um arquivo completo no caminho
        if caminho and os.path.splitext(caminho)[1]:  # Se caminho inclui nome do arquivo com extensão
            save_path = caminho
            ext = os.path.splitext(save_path)[1].lower() 
            if ext not in ['.csv', '.xlsx']:
                raise ValueError("Formato de arquivo inválido no caminho. Use '.csv' ou '.xlsx'.")
        else:
            # Formata extensão
            if formato is None:
                raise ValueError("O parâmetro 'formato' é obrigatório se 'caminho' não incluir o nome do arquivo.")
            ext = f".{formato.lower()}" if '.' not in formato else formato.lower()
            if ext not in ['.csv', '.xlsx']:
                raise ValueError("Formato inválido. Use 'csv' ou 'xlsx'.")
            
            # Define o caminho base e nome do arquivo
            if caminho is None:
                caminho = os.getcwd()  # Diretório atual
            if not os.path.exists(caminho):
                raise ValueError("Caminho para salvar é inválido!")
            if nome is None:
                raise ValueError("O parâmetro 'nome' é obrigatório se 'caminho' não incluir o nome do arquivo.")
            
            save_path = os.path.join(caminho, nome + ext)

        # Verifica duplicatas para múltiplos salvamentos
        if multiple:
            base_path, ext = os.path.splitext(save_path)
            i = 1
            while os.path.exists(save_path):
                save_path = f"{base_path}_{i}{ext}"
                i += 1

        # Salva o DataFrame no formato especificado
        if ext == '.xlsx':
            dataframe.to_excel(save_path, index=False)
        elif ext == '.csv':
            dataframe.to_csv(save_path, index=False, encoding='utf-8-sig')

        print(f"Planilha salva em {save_path}")
        return save_path

    # CRIA UM NOVO DATAFRAME EM CIMA DO DATABASE ORIGINAL PASSADO COMO PARAMETRO, O METODO IRA RELACIONAR AS INFORMAÇÕES COM BASE NO QUE O USUARIO SELECIONAR
    def nova_planilha(self, dataframe: pd.DataFrame, shark: bool = False) -> pd.DataFrame:
        """Cria um novo DataFrame baseado no DataFrame passado como parametro;\n
        Relaciona e insere colunas da base ao novo DataFrame;\n
        retorna o novo DataFrame formatado durante a execução.\n
        *Caso 'shark = True' uma base de colunas já formatada para o sistema será disponibilizada*."""
        dataframe = self.assert_planilha(dataframe)
        new_df = pd.DataFrame()
        cols = dataframe.columns.to_list()
        cols_enumerado = {i: col for i, col in enumerate(cols, start=1)}
        print('Colunas base: ' + str(cols_enumerado) + '\n')

        if shark:
            shark_model = ['Nome','Email','Telefone','Endereço','CNPJ']
            print('Digite o nome ou índice da coluna base a relacionar:')
            for col in shark_model:
                add_data = input(f'{col} >>>>>>>>> ')
                
                if add_data.isnumeric():
                    i = 0
                    while True:
                        if i > 0:
                            add_data = input(f'{col} >>>>>>>>> ')
                        if int(add_data) in cols_enumerado:
                            add_data = cols_enumerado[int(add_data)]
                            print(f'\033[F\033[14C{add_data}')
                            break
                        else:
                            print('A coluna selecionada não faz parte da base!')
                            i += 1

                data = dataframe[add_data]
                new_df = self.inserir_colunas(new_df, col, data)

            tag = input('Digite a TAG para o disparo:')
            new_df = self.inserir_colunas(new_df, 'TAG', tag)
            return new_df

        while True:
            resposta = input('Digite o nome da nova coluna e a coluna base:(nova,base)\n[tecle 0 para sair]>>>>>>')
            if resposta == '0':
                break

            try:
                nome_coluna, coluna_base = resposta.split(',')
                nome_coluna = nome_coluna.strip()
                coluna_base = coluna_base.strip()

                if coluna_base not in dataframe.columns:
                    print(f'A coluna {coluna_base} não existe na planilha.')
                    continue

                dados = dataframe[coluna_base]
                new_df = self.inserir_colunas(new_df, nome_coluna, dados)
                print(f"Coluna '{nome_coluna}' adicionada com base na coluna '{coluna_base}'.")
            except ValueError:
                print("Erro: formato inválido. Certifique-se de separar o nome da nova coluna e a coluna base com uma vírgula.")
    
        return new_df

    def inserir_colunas(self, dataframe: pd.DataFrame, nome_coluna: str, dados) -> pd.DataFrame:
        """Insere na coluna do dataframe especificada os valores declarados em 'dados'."""
        self.assert_planilha(dataframe)
        dataframe[nome_coluna] = dados
        return dataframe

    def remover_dados(self, dataframe: pd.DataFrame, numero_drops: int, axis: int = 0, sobreescrever: bool = False):
        """Retira o número de linhas especificado da planilha"""
        if axis not in [0, 1]:
            raise ValueError("O parâmetro 'axis' deve ser 0 (linhas) ou 1 (colunas).")

        if axis == 0:  # Remover linhas
            if numero_drops > len(dataframe.index):
                raise ValueError("O número de linhas a serem removidas excede o total de linhas no DataFrame.")
            drops = dataframe.index[:numero_drops]
        else:  # Remover colunas
            if numero_drops > len(dataframe.columns):
                raise ValueError("O número de colunas a serem removidas excede o total de colunas no DataFrame.")
            drops = dataframe.columns[:numero_drops]

        # Remove as linhas/colunas e aplica a alteração
        updated_df = dataframe.drop(drops, axis=axis)

        if sobreescrever:
            dataframe.drop(drops, axis=axis, inplace=True)
            return None
        else:
            return updated_df



def navegador(porta, caminhoChrome="navegador"):
    global driver

    diretorio_atual = os.getcwd()
    profile_dir = os.path.join(diretorio_atual, 'chrome_profiles', caminhoChrome)

    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    
    remote_debugging_port = porta
    chrome_executable_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    # Verifica se o Chrome já está aberto com as opções especificadas
    chrome_aberto = False
    for proc in psutil.process_iter(['name', 'cmdline']):
        if (proc.info['name'] and 'chrome' in proc.info['name'] and
                proc.info['cmdline'] and
                f'--remote-debugging-port={remote_debugging_port}' in proc.info['cmdline'] and
                f'--user-data-dir={profile_dir}' in proc.info['cmdline']):
            chrome_aberto = True
            break

    # Abre o Chrome com as opções especificadas se não estiver aberto
    if not chrome_aberto:
        subprocess.Popen([chrome_executable_path, 
                          f'--remote-debugging-port={remote_debugging_port}', 
                          f'--user-data-dir={profile_dir}'])

    # Configura as opções do Chrome para o WebDriver
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"localhost:{remote_debugging_port}")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        print('\nNavegador Iniciado! \n')
    except Exception as e:
        print(f'\nErro ao iniciar o navegador: {e}')

    return driver   

def logado():

    driver.get('https://simplifiquevivoemp.com.br/default?ReturnUrl=%2fview%2fhome%2fdefault')
    # se achar o texto no url significa que esta na pagina de login
    while True:
        # le o url atual do navegador
        url = driver.current_url
        if 'LoginCorp' in url:
            print('Aguardando Login')
            sleep(10)
        else:
            print('Simplifique já logado!')
            break


def formatarCNPJ(cnpj):

    # tira a formatacao do cnpj
    cnpjFormatado = ''
    cnpj = str(cnpj)
    if '.' in cnpj:
        for numero in cnpj:
            if numero in ('.', '/', '-'):
                continue
            else: 
                cnpjFormatado += numero
    else:
        cnpjFormatado = cnpj
    while len(cnpjFormatado) < 14:
            cnpjFormatado = "0" + cnpjFormatado
    return cnpjFormatado


def existePasta(diretorioDestino):
    if os.path.exists(diretorioDestino) == False:
        os.mkdir(diretorioDestino)


def existeNotas(diretorioNotas):
    # LE O BLOCO DE NOTAS PARA PEGAR ULTIMA FONTE USADA SEM SER O CRM5
    if os.path.exists(diretorioNotas) == False:
        with open(diretorioNotas, 'w', encoding='utf-8') as ultima:
            ultima.write('CRIADO - CRIADO\n')
        ultima.close()


def InformacaoNotas(diretorioNotas):
    existeNotas(diretorioNotas)
    with open(diretorioNotas, 'r', encoding='utf-8') as ultima:
        informacao = ultima.readline().strip()
    ultima.close()
    return informacao


def salvarInformacaoNotas(nomeNotas, ultimaFonte):
    existeNotas(nomeNotas)
    with open(nomeNotas, 'w', encoding='utf-8') as ultimaInformacao:
        ultimaInformacao.write(str(ultimaFonte))
    ultimaInformacao.close()


def pularCNPJ(nomeNotas, CNPJS):
    print('\nLendo Bloco de notas\n')
    with open(nomeNotas,'r', encoding='utf-8') as notas:
        for linha in notas:
            linha = str(linha)
            CNPJ = linha[0: 14]
            CNPJS.append(CNPJ)
        notas.close()
    print('\nBloco de notas lido\n')


