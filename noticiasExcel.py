from noticiasFunc import noticiasFunc
from resumeText import resumirTexto
from datetime import datetime
from funcoesFlet import mostrar_notificacao
import flet as ft

import ntplib
from datetime import datetime, timezone

def obter_data_ntp(data_limite):
    try:
        # cliente NTP para obter a data/hora atual
        cliente = ntplib.NTPClient()
        resposta = cliente.request('pool.ntp.org')

        # obter a data atual do servidor NTP
        data_atual = datetime.fromtimestamp(resposta.tx_time, tz=timezone.utc).date()

        # convertendo a data limite para um objeto date
        data_limite_obj = datetime.strptime(data_limite, "%Y-%m-%d").date()

        # compara as datas retornando true ou false
        if data_atual > data_limite_obj:
            print("Fim da DEMO")
            return False
        else:
            print("Ativado")
            return True

    # printa o erro caso não consiga pegar a data
    except Exception as e:
        return f"Erro: {e}"

# chama a funcao para comparar a data atual solicitada a uma url, retornand om valor de true ou false
data_atual = obter_data_ntp("2030-01-01")
print(data_atual)

# funcao principal que faz o app funcionar
def startarApp(page, navegadorEscondido, tema, inputPesquisa, botaoRelatorio, botoesFiltro, botaoPlay):

    # desabilita o botão relatório caso o app já tenha sido executado
    botaoRelatorio.disabled = True
    botaoRelatorio.update()

    # se a data atual for anterior a data limite
    if data_atual:
        
        try:
            # desabilida o botão play para impedir uma segunda execução
            botaoPlay.disabled=True
            botaoPlay.update()

            # opções de filtro data, a variavel será usada no URL do proprio google
            if botoesFiltro['24 horas']:
                filtroData = '&tbs=qdr:d'
            elif botoesFiltro['1 semana']:
                filtroData = '&tbs=qdr:w'
            elif botoesFiltro['Todas']:
                filtroData = ''
            
            # chama a função de noticia de acordo com as opções selecionadas dentro da pagina do app
            noticias = noticiasFunc(page=page, esconderNavegador=navegadorEscondido, fieldInput=inputPesquisa, filtroData=filtroData)

            print(noticias)

            dicionarioNoticias = []

            # para cada noticia achada 
            for textoNoticia in noticias:

                try:

                    # se o texto da noticia estiver vazio pula ela
                    if textoNoticia["texto"] == '':
                        continue
                    
                    # chama a função para resumir o texto e joga para uma variavel
                    noticiaResumida = resumirTexto(texto = textoNoticia["texto"])

                    # cria as variaveis que serão adicionadas ao dicionario
                    noticiaLink = textoNoticia['url']
                    tituloNoticia = textoNoticia['titulo']

                    # caminho e nome do arquivo
                    nome_arquivo = tema

                    # adiciona um dicionario dentro de uma lista
                    dicionarioNoticias.append({
                    "titulo": tituloNoticia,
                    "url": noticiaLink,
                    "Texto": noticiaResumida
                    })

                    # confimação que o texto foi salvo
                    print(f"Texto salvo em {nome_arquivo}")
                
                # printa o erro
                except Exception as e:
                    print(e)
                    print('ERRO')
                    continue

            # mostra notificação caso não encontre nenhuma notícia
            if not dicionarioNoticias:
                mostrar_notificacao(page=page, texto='Nenhuma notícia encontrada!', icon=ft.icons.WARNING, cor='red', titulo='Atenção')
            # ativa o botao de puxar relatorio caso ache alguma noticia
            else:
                botaoRelatorio.disabled = False
                botaoRelatorio.update()
                # msg de finalizada
                mostrar_notificacao(page=page, texto='Busca de notícias finalizada, salve antes de proseguir!', icon=ft.icons.CHECK_CIRCLE_SHARP, cor='green', titulo='FINALIZADO')
            # retorna o dicionario de noticias
            return dicionarioNoticias
    	
        # independente do que acontecer, reativa o botao de play
        finally:
            botaoPlay.disabled=False
            botaoPlay.update()