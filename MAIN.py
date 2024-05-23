from menus import *
from funcoes import *

def main_menu():
    while True:
        resposta = menu(['Fazer Login', 'Cadastrar usuário', 'Sair'])
        if resposta == 1:
            print("Opção 1")
            def Login():# função principal
                global vcpf

                t = 3 # number of tries to login 
                while t > 0: 
                    vcpf = input("CPF: ")
                    vsenha = getpass.getpass("Senha: ")
                    
                    if user_login(vcpf, vsenha):
                        print(f"Login bem-sucedido!")
                        menu_user()
                        break
                    elif adm_login(vcpf, vsenha):
                        print("Login bem-sucedido!")
                        menu_admin()
                        break
                    else:
                        t -= 1 
                        print(f"CPF ou senha incorretos. Tente novamente. Restam {t} tentativas")

                    if t == 0:
                        print("Você excedeu o número de tentativas permitidas. Tente novamente mais tarde.")
                quit()
            Login() 
            
        elif resposta == 2:
            print("Opção 2")
            def cadastrar_user():
                # Verifica se o CPF tem apenas números
                #input do CPF 
                while True:
                    vcpf = input("Digite o CPF: ")
                    if verificar_cpf(vcpf):
                        print("CPF válido.")
                        break
                    else:
                        print("CPF inválido. Certifique-se de digitar apenas números e que o CPF tenha 11 dígitos.")

                #input email
                while True:
                    vemail = input("Digite o email: ")
                    if verificar_email(vemail):
                        print("Email válido.")
                        break
                    else:
                        print("Email inválido. Tente novamente.")

                #input nome
                while True:
                    vnome = input("NOME: ")
                    if verificar_nome(vnome):
                        print("Nome válido.")
                        break
                    else:
                        print("Nome inválido. Certifique-se de digitar apenas letras e não deixe vazio.")

                #input senha
                while True:
                    print("LEMBRE-SE! A senha deve conter ao menos um caracter especial, um número e letras!")
                    vsenha = input("SENHA: ")
                    sec = input("REPITA A SENHA: ")
                    
                    if vsenha == sec and verificar_senha(vsenha):
                        vsenhacrip = cript_pass(vsenha)
                        print("Cadastrado com sucesso!")
                        aunthenticate = 2 
                        # enviar instrução sql para ser executada pelo banco
                        cursor.execute("insert into user values (?, ?, ?, ?, ?)", (vcpf, vemail, vnome, vsenhacrip, aunthenticate))
                        conn.commit()
                        menu_user()
                        break 
                    
                    else:
                        print("Senha inválida. Tente novamente!")

                    conn.close()
            cadastrar_user()

        elif resposta == 3:
            print("Obrigado por utilizar nosso sistema!")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_user():
    def cpf_save():
        cpf_salvo = vcpf
        return cpf_salvo
    
    while True:
        resposta = menu_usuario(['Nossa loja', 'Alterar meus dados', 'Excluir minha conta', 'Sair'])
        if resposta == 1:
            print("Opção 1")
            shopcart()

        elif resposta == 2:
            print("Opção 2")
            def alterar_user():
                global vcpf
                conn = sqlite3.connect("projectdbt.db")
                cursor = conn.cursor()

                print("------------------------------------------\nALTERAR USUÁRIO\n------------------------------------------")
                vcpf = cpf_save()

                cursor.execute("SELECT count(*), EMAIL, NOME, AUTORIZAÇÃO FROM user WHERE CPF = ?", (vcpf,))
                rs = cursor.fetchone()

                if rs[0] > 0:
                    print ("Usuário localizado")
                    print ("Email: ", rs[1])
                    print ("Nome: ", rs[2])
                    vconfirma = input("Quer alterar este usuário? (S/N)")

                    if vconfirma.upper() == "S":

                        while True:
                            print("O que deseja alterar? (EMAIL(E), NOME(N), SENHA(S), SAIR(X))")
                            campo = input("Campo: ")

                            if campo.upper() == "X": # Seleção de alteração para sair
                                menu_user()
                                break
                            
                            elif campo.upper() == "E": # Seleção de alteração para email
                                altermail = input("Novo email: ")
                                if verificar_email(altermail):
                                    cursor.execute("UPDATE user SET EMAIL = ? WHERE CPF = ?", (altermail, vcpf))
                                    conn.commit()

                            elif campo.upper() == "N": # Seleção de alteração para nome
                                alternome = input("Novo nome: ")
                                if verificar_nome(alternome):
                                    cursor.execute("UPDATE user SET NOME =? WHERE CPF =?", (alternome, vcpf))
                                    conn.commit()

                            elif campo.upper() == "S": # Seleção de alteração para senha
                                print("LEMBRE-SE! A senha deve conter ao menos um caracter especial, um número e letras!")
                                altersenha = getpass.getpass("Nova senha: ")
                                vsenhacrip = cript_pass(altersenha)
                                if verificar_senha(vsenhacrip):
                                    cursor.execute("UPDATE user SET SENHA =? WHERE CPF =?", (vsenhacrip, vcpf))
                                    conn.commit()
                            
                            conn.close()
                            print("DADOS ALTERADOS COM SUCESSO!")
                    else:
                        print("OPERAÇÃO CANCELADA...")
                        menu_user()
            alterar_user()

        elif resposta == 3:
            print("Opção 3")
            def excluir_user():
                conn = sqlite3.connect("projectdbt.db")
                cursor = conn.cursor()
                def confirmar(vcpf, vsenha):

                    cursor.execute("SELECT SENHA FROM user WHERE CPF = ?", (vcpf,))
                    rs = cursor.fetchone()

                    if rs is None:
                        return False
                    #cirptografia armazenada no cadastro     
                    vs_crip_arm = rs[0]

                    #criptografia atual
                    hasher = hashlib.sha256()
                    hasher.update(vsenha.encode('utf-8'))
                    vs_crip_forn = hasher.hexdigest()
                    
                    if str(vs_crip_arm.decode('utf-8')) == vs_crip_forn:
                        return True
                    else: 
                        return False
                    
                vcpf = cpf_save()
                cursor.execute("SELECT count(*), EMAIL, NOME, AUTORIZAÇÃO FROM user WHERE CPF = ?", (vcpf,))
                rs = cursor.fetchone()

                if rs[0] > 0:
                    print ("Usuário localizado")
                    print ("Email: ", rs[1])
                    print ("Nome: ", rs[2])
                    vconfirma = input("Confirma a exclusão deste usuário? (S/N)")

                    if vconfirma.upper() == "S":
                        print("QUAL A SENHA DO USUÁRIO QUE DESEJA EXCLUIR?")

                        vsenha = getpass.getpass("Senha: ")

                        if confirmar(vcpf, vsenha):
                        # Enviar instrução SQL para ser executada
                            conn.execute("DELETE FROM user WHERE CPF = " + vcpf)
                            conn.commit()
                            print("USUÁRIO EXCLUÍDO COM SUCESSO!")
                
                        else:
                            print("VOCÊ NÃO PODE EXCLUIR ESTE USUÀRIO!")
                    
                    else:
                        print("OPERAÇÃO CANCELADA...")
                        menu_user()
                    
                    conn.close()
            excluir_user()

        elif resposta == 4:
            print("Obrigado por utilizar nosso sistema!")
            main_menu()
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_admin():
    while True:
        resposta = menu_adm(['Consultar', 'Cadastrar Produto', 'Alterar', 'Excluir', 'Sair'])
        if resposta == 1:
            print("Opção 1")
            consultar()
        elif resposta == 2:
            print("Opção 2")
            cadastrar_produto()
        elif resposta == 3:
            print("Opção 3")
            alterar()
        elif resposta == 4:
            print("Opção 4")
            excluir()
        elif resposta == 5:
            print("Obrigado por utilizar nosso sistema!")
            main_menu()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()