import flet as ft
import hashlib
from Backend import *


class Gui:
    def __init__(self) -> None:
        pass

    def main(page: ft.Page):
        back = Backend()
        page.title = 'controle de acesso de pessoas'.title()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        alinhamento = ft.MainAxisAlignment.CENTER
        #Criação dos campos
        field_nome = ft.TextField(label='Nome*', width=300)
        field_email = ft.TextField(label='Email*', width=300, keyboard_type=ft.KeyboardType.EMAIL)
        field_tel = ft.TextField(label='Telefone*', width=250, keyboard_type=ft.KeyboardType.PHONE,max_length=11)
        field_sexo = ft.Dropdown(
            width=100,
            options=[
                ft.dropdown.Option('Masculino'),
                ft.dropdown.Option('feminino')
            ]
            , label='SEXO'  
        )
        field_senha = ft.TextField(label='Senha*', width=250, password=True)
        field_choise = ft.Dropdown(
            width=350,
            options=[
                ft.dropdown.Option('Nome'),
                ft.dropdown.Option('Email'),
                ft.dropdown.Option('Telefone'),
            ]
            , label='Escolha o campo para alterar'

        )
        field_new_choise = ft.TextField(label='Novo campo', width=500)
        field_ID = ft.TextField(label='Digite o ID', width=200, keyboard_type=ft.KeyboardType.NUMBER)

        # criando a ação dos botões
        def botao_cadastar(e):
            if not field_nome.value:
                field_nome.error_text = "digite seu nome!"
                page.update()
            elif not field_senha.value:
                field_senha.error_text = 'Digite uma senha!'
                page.update()
            elif 8 > len(field_senha.value) < 16:
                field_senha.error_text = 'Digite uma senha no minimo 8 digitos e maximo de 16'
                page.update()
            elif not field_tel.value:
                field_tel.error_text = 'Digite o seu telefone'
                page.update()
            elif not field_tel.value.isdigit():
                field_tel.error_text = 'o telefone só pode ser numeros'
            elif not field_email.value:
                field_email.error_text = 'Digite seu e-mail!'
                page.update()
            elif not field_sexo.value:
                field_sexo.error_text = 'escolha o seu sexo!'
                page.update()

            else:
                field_nome.error_text = ''
                field_senha.error_text = ''
                field_email.error_text = ''
                field_sexo.error_text = ''
                field_tel.error_text = ''
                senha_hash = hashlib.sha256(field_senha.value.encode())
                senha = senha_hash.hexdigest()
                back.inserir(field_nome.value, field_email.value, senha, field_tel.value, field_sexo.value)
                field_nome.value = ''
                field_email.value = ''
                field_sexo.value = ''
                field_tel.value = ''
                field_senha.value = ''
                

            page.update()

        def editar(event,id):
            page._id = id
            page.go('/editar')
            
        def btn_editar(e):
            try:
                id = page._id
                if not field_choise.value:
                    field_choise.error_text = 'Escolha uma opção'
                    page.update()
                elif not field_new_choise.value:
                    field_new_choise.error_text = 'o campo não pode estar vazio'
                    page.update()
                elif field_choise.value == 'Telefone' and not field_new_choise.value.isdigit():
                    field_new_choise.error_text = 'O telefone só pode ser numeros'
                    page.update()
                else:
                    field_choise.error_text = ''
                    field_new_choise.error_text = ''
                    back.editar_dado(id, field_choise.value, field_new_choise.value)
                page.update()
                page.go('/')
            except Exception as e:
                print(f'OCORREU UM ERRO:{e}')
         # adicionado a pagina e as rotas
        def route_change(route):
            back_color = ft.colors.SURFACE_VARIANT
            page.views.clear()
            page.views.append(
                ft.View(
                    '/',
                    [
                        ft.AppBar(title=ft.Text('Cadastro de pessoas'), bgcolor='#141414',center_title=True),
                        ft.Row(
                            [
                                field_nome,
                                field_email
                            ],
                           alignment=alinhamento
                        ),
                        ft.Row(
                            [
                                field_tel,
                                field_senha
                            ],
                           alignment=alinhamento
                        ),

                        ft.Row(

                            [
                                field_sexo
                            ],
                            alignment=alinhamento
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton('Cadastrar', on_click=botao_cadastar),
                                ft.ElevatedButton('Visualizar', on_click=lambda _:page.go('/visualizar')),
                            ],
                            alignment=alinhamento
                        )
                    ],
                    bgcolor='#171717',horizontal_alignment=alinhamento,vertical_alignment=alinhamento
                ),
                                                     
            )
            
            if page.route == '/editar':
                page.views.append(
                    ft.View(
                        '/editar',
                        [
                            ft.AppBar(title=ft.Text('Editar cadastro'), bgcolor=ft.colors.BLACK12,center_title=True),
                            ft.Row([field_choise],alignment=alinhamento),
                            ft.Row([field_new_choise],alignment=alinhamento),
                            ft.Row([ft.ElevatedButton('Registrar', on_click=btn_editar, width=250)],alignment=alinhamento)
                        ]
                    )
                )
            elif page.route == '/visualizar':
                data = back.visualizar()
                list_view = ft.ListView(spacing=8,expand=True)
    
                if data is not None:
                    for row in data:
                        id = row['ID']
                        nome = row['Nome']
                        email = row['Email']
                        tel = row['Telefone']
                        sexo = row['sexo']
                        senha = row['Senha']
                        btn_editar_id = ft.ElevatedButton('Editar',on_click=lambda event, id=id:editar(event,id))
                        delete_btn = ft.ElevatedButton('Deletar',on_click=lambda event, id=id:delete_linha(id))
                        list_view.controls.append(
                        ft.Row(
                            [
                            ft.Container(
                                    ft.Text(f'NOME: {nome}'),
                                    
                                ),
                            ft.Container(
                                    ft.Text(f'E-MAIL: {email}'),       
                                ),
                            ft.Container(
                                    ft.Text(f'TELEFONE: {tel}'), 
                  
                                ),
                            ft.Container(
                                    ft.Text(f'SEXO: {sexo}'),       
                                ),
                            ft.Container(
                                    ft.Text(f'SENHA: {senha}'), 
                                ),
                            btn_editar_id,
                            delete_btn
                            ],  
                            alignment=alinhamento
                                )
                        
                        )      
            
                page.views.append(
                    ft.View(
                        '/visualizar',
                        [
                            list_view
                        ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )

            
            page.update()
        

        def delete_linha(index):
            back.excluir(index)
            page.go('/')
        
        def pop_view(view):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = pop_view
        page.go(page.route)

           
    #ft.app(target=main)   rodar desktop
    ft.app(target=main,view=ft.AppView.WEB_BROWSER)#rodar no browser
