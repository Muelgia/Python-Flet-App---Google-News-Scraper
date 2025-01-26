import flet as ft
from controllers.planilha import salvarPlanilha
import pandas as pd
from datetime import datetime
from noticiasExcel import startarApp


def pagePrincipal(page: ft.Page, width: int, height: int):

    valor_retorno = []

    corContainer = ft.colors.GREY_400
    subContainer = ft.colors.GREY_300

        
    #-------------------------------------------------------------------------------------------------------------------------------
    #borda arredondada dos containers
    borderContainers = 15

    #barra de rolagem
    rolagem = ft.ListView(expand=1, spacing=5, padding=5, auto_scroll=False,)

# ----------------------------------------------------------------------------------------------------------------------------

    tituloTemplate = ft.Text("Buscar", text_align="center", size="20", weight=ft.FontWeight.BOLD)
 
    # Botão para abrir o FilePicker no modo de salvar
    inputPesquisa = ft.TextField(hint_text='Desejo notícias sobre: ')

    TemplateColumn = ft.Column(
        controls=[
            tituloTemplate, inputPesquisa
            ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    ContainerTemplate = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        TemplateColumn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )
# ----------------------------------------------------------------------------------------------------------------
 
    def clicarBotaoPlay(e):
        nonlocal valor_retorno
        valor_retorno = startarApp(botaoRelatorio=relatorioBotao, page=page, navegadorEscondido=esconderNavegador.value,
                                   tema=inputPesquisa.value, inputPesquisa=inputPesquisa, botoesFiltro=botoes_estado, botaoPlay=botaoPlay)

    # Botão com a função on_click
    botaoPlay = ft.ElevatedButton(
        text="Play",
        on_click=clicarBotaoPlay
    )
    
    tituloPlayGrid = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ 
            ft.Text("Iniciar Busca", text_align="center", size="20", weight=ft.FontWeight.BOLD),
        ]
    )

    ContainerPlay = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        tituloPlayGrid, botaoPlay
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )


# ----------------------------------------------------------------------------------------------------------------

    def salvarRelatorio(e: ft.FilePickerResultEvent):
        nonlocal valor_retorno
        print('TO AQUI POHA')
        if e.path:  # No modo de salvar, e.path contém o caminho escolhido
            caminho_arquivo = e.path  # Obtém o caminho correto do arquivo salvo
            nome_arquivo = caminho_arquivo.split("\\")[-1]  # Obtém o nome do arquivo a partir do caminho
            
            mensagem = f'{nome_arquivo} salvo com sucesso'
            salvarPlanilha(dir=caminho_arquivo, dados=valor_retorno)
            
            # Exibe uma mensagem ao usuário
            page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor="lightgray",  # Cor de fundo cinza claro
                open=True  # Exibe o SnackBar com a mensagem
            )
            page.update()
        else:
            print('entrei no else')



    # Criação do FilePicker no modo de salvar arquivo
    save_file_relatorio = ft.FilePicker(on_result=salvarRelatorio)
    page.overlay.append(save_file_relatorio)

    # Botão para abrir o FilePicker no modo de salvar, permitindo escolher nome
    relatorioBotao = ft.ElevatedButton(
        text="Salvar Relatório", disabled=True,
        on_click=lambda e: save_file_relatorio.save_file(
            file_name="noticias.csv",  # Sugestão de nome inicial
            allowed_extensions=["csv"]  # Extensões permitidas
        )
    )

    rowBotoesData = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text("Salvar Relatório", text_align="center", size="20", weight=ft.FontWeight.BOLD),
        ]
    )

    textoIntrucaoRelatorio = ft.Text(
        "O botão ficará disponível assim que a busca por notícias finalizar.",
        size=10
    )

    relatorioColumn = ft.Column(
        controls=[
            rowBotoesData, relatorioBotao, textoIntrucaoRelatorio
            ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    ContainerRelatorio = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        relatorioColumn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )
    
# --------------------------------------Botoes filtro data------------------------------------------------------

    tituloPeriodo = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ 
            ft.Text("Período notícias", text_align="center", size="20", weight=ft.FontWeight.BOLD),
        ]
    )


    botoes_estado = {
        "24 horas": True,   # Desabilitado (padrão)
        "1 semana": False,  # Ativado
        "Todas": False      # Ativado
    }

    def atualizar_botoes(botao_clicado):
        for key in botoes_estado:
            botoes_estado[key] = key == botao_clicado  # Desativa o botão clicado e ativa os outros
        
        # Atualiza a interface com os novos estados
        rowBotoesData.controls = [
            ft.ElevatedButton(
                text=key,
                disabled=botoes_estado[key],
                expand=True,  # Distribui igualmente o espaço entre os botões
                on_click=lambda e, k=key: atualizar_botoes(k),
            )
            for key in botoes_estado
        ]
        page.update()

    rowBotoesData = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.ElevatedButton(
                text=key,
                disabled=botoes_estado[key],
                expand=True,  # Distribui igualmente o espaço entre os botões
                on_click=lambda e, k=key: atualizar_botoes(k),
            )
            for key in botoes_estado
        ]
    )

    ContainerPeriodo = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        tituloPeriodo, rowBotoesData
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )
# -------------------------------------------Esconder o navegador-----------------------------------------------------

    def mudar_estado(e):
        esconderNavegador.label = "Ativado" if esconderNavegador.value else "Desativado"
        page.update()

    esconderNavegador = ft.Switch(
        value=True,  # O switch vem ativado por padrão
        label="Ativado",
        on_change=mudar_estado
    )

    tituloEsconder = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ 
            ft.Text("Esconder Navegador", text_align="center", size=20, weight=ft.FontWeight.BOLD),
        ]
    )

    switchCentralizado = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[esconderNavegador]
    )

    ContainerEsconder = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        tituloEsconder, switchCentralizado
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )

#------------------------------------------------------------------------------------------------------------------

    tituloAtivacao = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ 
            ft.Text("Status Ativação", text_align="center", size="20", weight=ft.FontWeight.BOLD),
        ]
    )

    validoAte = ft.Text(
        "Demo - Validá até 31/01/2025",
        size=15
    )

    ano_atual = datetime.now().year
    direitos_reservados = ft.Text(
        f"© {ano_atual} Desenvolvido por Samuel Garcia. Todos os direitos reservados.",
        size=10
    )


    ContainerDireitos = ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        tituloAtivacao, validoAte, direitos_reservados
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=subContainer,
                #altura da pagina total
                height=135, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers),
            )

# -----------------------------------------------------------------------------------------------------------------
    #responsive row adiciona a barra de rolagem
    rolagem.controls.append(ft.ResponsiveRow(
        #chaves do responsive row
        [   
            #container como parametro do responsive row
            ft.Container(
                #cadastro emails
                content=ft.Column(
                    [  
                        ContainerTemplate, ContainerPlay,ContainerRelatorio
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=corContainer,
                #altura da pagina total
                height=445, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers) 
            ),

            ft.Container(
                #cadastro emails
                content=ft.Column(
                    [   
                        ContainerPeriodo, ContainerEsconder, ContainerDireitos
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                #padding do container
                padding=10,
                #cor do container
                bgcolor=corContainer,
                #altura da pagina total
                height=445, 
                #tamanho em colunas MAX12 de acordo com os tamanhos de dispositivos
                col={'sm':12, 'md':6, 'xl':6},  
                #borda arredondada 
                border_radius=ft.border_radius.all(borderContainers) 
            ),

            
        ],
    ))

    view = ft.View(
        route='/disparador',
        bgcolor=ft.colors.SURFACE_CONTAINER_HIGHEST,
        controls=[
            ft.ResponsiveRow(
                [
                    rolagem, 
                ]
            )
        ]
    )

    return view
