import flet as ft
from views.home import home
from views.pagePrincipal import pagePrincipal

def main(page: ft.Page):
    
    version = '- BETA - 1.0.0'
    page.window.max_width = 850
    page.window.max_height = 515

    page.window.width = 850
    page.window.height = 515

    page.window.resizable = False

    page.window.maximized = False  # Impede a maximização (expandir para tela cheia)
    
    # Aqui estamos tentando manipular a janela para não maximizar
    page.window.on_maximize = lambda e: page.window.restore()  # Restores window if maximized

    # Declara o tema da página
    # page.theme_mode = "Dark"
    page.theme_mode = "Light"

    # Define o título inicial da página
    page.title = "Carregando..."

    # Armazenar a largura e altura atuais
    current_width, current_height = page.window.width, page.window.height

    # Função para ajustar as dimensões sem redesenho completo
    def ajustaPagina(event):
        nonlocal current_width, current_height
        # Verifica se houve mudança no tamanho para atualizar somente quando necessário
        if event.width != current_width or event.height != current_height:
            current_width, current_height = event.width, event.height
            update_layout()  # Atualiza o layout com as novas dimensões

    # Função para atualizar o layout sem recriar a página
    def update_layout():
        if page.route == '/':
            # Apenas atualiza a largura e altura dos controles dentro da página sem recarregar a página
            for control in page.views[0].controls:
                if isinstance(control, ft.ResponsiveRow):
                    control.width = current_width
                    control.height = current_height
            page.update()  # Atualiza a visualização com a nova dimensãoh
        elif page.route == '/pagePrincipal':
            for control in page.views[0].controls:
                if isinstance(control, ft.ResponsiveRow):
                    control.width = current_width
                    control.height = current_height
            page.update()

    # Router para controlar as rotas
    def router(route, width, height):
        page.views.clear()  # Limpa as views da página

        # Adiciona a view correta com base na rota
        if route == '/':
            page.views.append(home(page, width, height))  # Home
            page.title = f"AVISO {version}"  # Título da página Home
        elif route == '/sfa':
            page.views.append(pagePrincipal(page, width, height))  # Outra rota
            page.title = f"Buscador de Noticias {version}"  # Título da página BOT SFA
        else:
            # Página padrão para rotas não encontradas
            page.views.append(
                ft.View(
                    route=route,
                    controls=[ft.Text("Página não encontrada!")],
                )
            )
            page.title = "404 - Não Encontrado"  # Título para rotas inválidas

        page.update()  # Atualiza a página com a nova view

    # Ativa a função de redimensionamento
    page.on_resized = ajustaPagina
    
    # Define o comportamento ao mudar de rota
    def on_route_change(e):
        router(page.route, page.window.width, page.window.height)

    page.on_route_change = on_route_change

    # Inicializa com as dimensões atuais da janela
    router(page.route, page.window.width, page.window.height)
    page.go(page.route)  # Navega para a rota inicial

if __name__ == '__main__':
    ft.app(target=main)
