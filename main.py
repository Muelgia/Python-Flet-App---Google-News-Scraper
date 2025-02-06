import flet as ft
from views.home import home
from views.pagePrincipal import pagePrincipal

# pagina main 
def main(page: ft.Page):
    
    # tamanho e titulo da pagina
    version = '- BETA - 1.0.0'
    page.window.max_width = 850
    page.window.max_height = 515

    page.window.width = 850
    page.window.height = 515

    page.window.resizable = False

    page.window.maximized = False  # impede a maximização (expandir para tela cheia)
    
    # tenta manipular a janela para não maximizar
    page.window.on_maximize = lambda e: page.window.restore()  # Restores window if maximized

    # declara o tema da página
    # page.theme_mode = "Dark"
    page.theme_mode = "Light"

    # define o título inicial da página
    page.title = "Carregando..."

    # armazenar a largura e altura atuais
    current_width, current_height = page.window.width, page.window.height

    # Função para ajustar as dimensões sem redesenho completo
    def ajustaPagina(event):
        nonlocal current_width, current_height
        # verifica se houve mudança no tamanho para atualizar somente quando necessário
        if event.width != current_width or event.height != current_height:
            current_width, current_height = event.width, event.height
            update_layout()  # atualiza o layout com as novas dimensões

    # função para atualizar o layout sem recriar a página
    def update_layout():
        if page.route == '/':
            # apenas atualiza a largura e altura dos controles dentro da página sem recarregar a página
            for control in page.views[0].controls:
                if isinstance(control, ft.ResponsiveRow):
                    control.width = current_width
                    control.height = current_height
            page.update()  # atualiza a visualização com a nova dimensãoh
        elif page.route == '/pagePrincipal':
            for control in page.views[0].controls:
                if isinstance(control, ft.ResponsiveRow):
                    control.width = current_width
                    control.height = current_height
            page.update()

    # router para controlar as rotas
    def router(route, width, height):
        page.views.clear()  # limpa as views da página

        # adiciona a view correta com base na rota
        if route == '/':
            page.views.append(home(page, width, height))  # home
            page.title = f"AVISO {version}"  # título da página Home
        elif route == '/sfa':
            page.views.append(pagePrincipal(page, width, height))  # outra rota
            page.title = f"Buscador de Noticias {version}"  # título da página BOT SFA
        else:
            # página padrão para rotas não encontradas
            page.views.append(
                ft.View(
                    route=route,
                    controls=[ft.Text("Página não encontrada!")],
                )
            )
            page.title = "404 - Não Encontrado"  # título para rotas inválidas

        page.update()  # atualiza a página com a nova view

    # ativa a função de redimensionamento
    page.on_resized = ajustaPagina
    
    # define o comportamento ao mudar de rota
    def on_route_change(e):
        router(page.route, page.window.width, page.window.height)

    page.on_route_change = on_route_change

    # inicializa com as dimensões atuais da janela
    router(page.route, page.window.width, page.window.height)
    page.go(page.route)  # navega para a rota inicial

# caso o codigo for executado da pagina main
if __name__ == '__main__':
    ft.app(target=main)
