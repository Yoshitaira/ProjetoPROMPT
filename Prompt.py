import sqlite3
import hashlib
from email_validator import validate_email, EmailNotValidError
import binascii
import sqlite3
import getpass
from tabulate import tabulate

#----------------------------------------NAVEGAÇÃO-------------------------------------------------#
# Menu inicial do Projeto
def main_menu():# Menu Principal
    while True:
        print("(1) - Cadastrar Usuário")
        print("(2) - Fazer Login")
        print("(0) - Sair")
        opcao = int(input("Digite a opção desejada: "))

        if opcao == 1: # Cadastrar Usuário
            def cadastrar_user():

                conn = sqlite3.connect("projectdbt.db")
                cursor = conn.cursor()
                # Verifica se o CPF tem apenas números
                def  verificar_cpf(vcpf):
                    if vcpf.isdigit() and len(vcpf) == 11:
                        return True
                    else:
                        return False
                    
                # Verifica se o email é válido
                def verificar_email(vemail):
                    try:
                        #V alida o email usando a função validate_email
                        valid = validate_email(vemail)
                        return True
                    except EmailNotValidError as e:
                        # Captura a exceção EmailNotValidError caso o email não seja válido
                        print(str(e))
                        return False

                # Verificar se o nome contém apenas letras
                def verificar_nome(vnome):
                    if all((c.isalpha() or c.isspace()) for c in vnome) and  len(vnome) > 0:
                        return True
                    else:
                        return False

                # Verificar senha e criptografa
                def verificar_senha(vsenha):
                    # Verifica se a senha contém pelo menos 1 caracter de cada
                    letter = any(c.isalpha() for c in vsenha)
                    number = any(c.isdigit() for c in vsenha)
                    spchar = any(c in "!@#$%&*?" for c in vsenha)
                    lenght = len(vsenha) <= 18
                    
                    return letter and number and spchar and lenght

                def cript_pass(vsenha):

                    if verificar_senha(vsenha):
                        hasher = hashlib.sha256()
                        hasher.update(vsenha.encode('utf-8'))
                        senha_hash = hasher.digest()
                        vsenhacrip = binascii.hexlify(senha_hash)
                        return vsenhacrip
                        
                #input do CPF 
                while True:
                    print("------------\nCADASTRE-SE\n------------")
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
                        break 
                             
                else:
                    print("Senha inválida. Tente novamente!")

                conn.close()   
            cadastrar_user()
        elif opcao == 2: # Fazer Login
            
            def Login():# função principal
                global vcpf

                def user_login(vcpf, vsenha):
                    conn = sqlite3.connect("projectdbt.db")
                    cursor = conn.cursor()
                        
                    cursor.execute("SELECT SENHA, AUTORIZAÇÃO FROM user WHERE CPF = ?", (vcpf,))
                    rs = cursor.fetchone()
                    
                    if rs is None:
                        return False
                #criptografia armazenada no cadastro     
                    vs_crip_arm = rs[0]
                    auth = rs[1]

                #criptografia atual
                    hasher = hashlib.sha256()
                    hasher.update(vsenha.encode('utf-8'))
                    vs_crip_forn = hasher.hexdigest()

                    return str(vs_crip_arm.decode('utf-8')) == vs_crip_forn and auth ==2
                
                def adm_login(vcpf, vsenha):
                    conn = sqlite3.connect("projectdbt.db")
                    cursor = conn.cursor()
                        
                    cursor.execute("SELECT SENHA, AUTORIZAÇÃO FROM user WHERE CPF = ?", (vcpf,))
                    rs = cursor.fetchone()
                    
                    if rs is None:
                        return False
                #criptografia armazenada no cadastro     
                    vs_crip_arm = rs[0]
                    auth = rs[1]

                #criptografia atual
                    hasher = hashlib.sha256()
                    hasher.update(vsenha.encode('utf-8'))
                    vs_crip_forn = hasher.hexdigest()

                    return str(vs_crip_arm.decode('utf-8')) == vs_crip_forn and auth ==1

                t = 3 # number of tries to login 
                while t > 0:
                    print("------------\nFAÇA SEU LOGIN!\n------------")
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
                        
                    elif opcao == 0: # Finalizar Programa
                        print("Obrigado por utilizar nosso sistema!")
                        quit()
            Login()

        elif opcao == 0:
            print("Obrigado por utilizar nosso sistema!")
            quit()
        else:
            print("Opção inválida. Tente novamente.")
            main_menu()

def menu_user():# Menu do usuário comum
    
    def cpf_save():
        cpf_salvo = vcpf
        return cpf_salvo
    
    print("------------------\nPERFIL USUÁRIO\n------------------")
    print("(1) - Carrinho")
    print("(2) - Alterar meus dados")
    print("(3) - Excluir meu perfil")
    print("(0) - LOGOFF")
    opcaouser = int(input("Digite a opção desejada: "))

    if opcaouser == 1: # Carrinho
        
        def shopcart():# função carrinho de compras

            cart = []

            conn = sqlite3.connect("projectdbt.db")
            cursor = conn.cursor()

            while True:# menu do carrinho
                print("----------------\nCARRINHO\n----------------")
                print("1 - Ver catálogo de produtos")
                print("2 - Adionar itens ao carrinho")
                print("3 - Finalizar compra")
                print("0 - Voltar ao menu anterior")

                vescolha = int(input("O que deseja fazer? "))

                if vescolha == 1: # Adicionar produto
                    cursor.execute("SELECT * FROM products")
                    products = cursor.fetchall()# mostra o catálogo de produtos para o cliente

                    print("Catálogo de produtos")
                    headers = ["ID","CATEGORIA", "PRODUTO", "PRECO", "QUANTIDADE"]
                    print(tabulate(products, headers = headers))
                    
                    
                elif vescolha == 2: # Remover produto
                    product_id = int(input("Digite o ID do produto:"))
                    quantity = int(input("Digite a quantidade: "))

                    cursor.execute("SELECT * FROM products WHERE ID=?", (product_id,))
                    product = cursor.fetchone()

                    if product and product[4] >= quantity:
                        cart.append((product_id, quantity))
                        print(f"Adicionado {quantity} {product[1]} no carrinho.")

                        new_quantity = product[4] - quantity
                        cursor.execute("UPDATE products SET QUANTIDADE=? WHERE ID=?", (new_quantity, product_id))
                    else:
                        print("Produto não encontrado ou quantidade insuficiente.")
                
                elif vescolha == 3: # Finalizar compra
                    total_cost = 0

                    for item in cart:
                        cursor.execute("SELECT PRECO FROM products WHERE ID=?", (item[0],))
                        price = cursor.fetchone()

                        total_cost += price[0] * item[1]

                    print(f"Custo da compra: R${total_cost}")
                    break
                
                elif vescolha == 0: # Sair
                    print("Obrigado por comprar, volte sempre!")
                else:
                    print("Opção inválida")
            cart.clear()
            
            conn.commit()
            conn.close()
        shopcart()
        menu_user()

    elif opcaouser == 2: # Alterar meus dados
        
        def alterar_user():
            global vcpf
            conn = sqlite3.connect("projectdbt.db")
            cursor = conn.cursor()

            # encripta a nova senha
            def criptar_novasenha(altersenha):
                #verifica se a senha contém pelo menos 1 caracter de cada
                letter = any(c.isalpha() for c in altersenha)
                number = any(c.isdigit() for c in altersenha)
                spchar = any(c in "!@#$%&*?" for c in altersenha)
                lenght = len(altersenha) <= 18
                
                return letter and number and spchar and lenght

            def cript_pass(altersenha):

                if criptar_novasenha(altersenha):
                    hasher1 = hashlib.sha256()
                    hasher1.update(altersenha.encode('utf-8'))
                    senha_hash = hasher1.digest()
                    vsenhacrip = binascii.hexlify(senha_hash)
                    return vsenhacrip

            def verificar_email(alteremail):
                try:
                    # Valida o email usando a função validate_email
                    valid = validate_email(alteremail)
                    return True
                except EmailNotValidError as e:
                    # Captura a exceção EmailNotValidError caso o email não seja válido
                    print(str(e))
                    return False

            def verificar_nome(alternome):
                if all((c.isalpha() or c.isspace()) for c in alternome) and  len(alternome) > 0:
                    return True
                else:
                    return False
            print("----------------\nALTERAR USUÁRIO\n----------------")
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
                            break
                        
                        elif campo.upper() == "E": # Seleção de alteração para email
                            altermail = input("Novo email: ")
                            cursor.execute("UPDATE user SET EMAIL = ? WHERE CPF = ?", (altermail, vcpf))
                            conn.commit()
                        
                        elif campo.upper() == "N": # Seleção de alteração para nome
                            alternome = input("Novo nome: ")
                            cursor.execute("UPDATE user SET NOME =? WHERE CPF =?", (alternome, vcpf))
                            conn.commit()

                        elif campo.upper() == "S": # Seleção de alteração para senha
                            print("LEMBRE-SE! A senha deve conter ao menos um caracter especial, um número e letras!")
                            altersenha = getpass.getpass("Nova senha: ")
                            vsenhacrip = cript_pass(altersenha)
                                
                            cursor.execute("UPDATE user SET SENHA =? WHERE CPF =?", (vsenhacrip, vcpf))
                            conn.commit()
                        
                        conn.close()
                        print("DADOS ALTERADOS COM SUCESSO!")
        alterar_user()
        menu_user()

    elif opcaouser == 3: # Excluir meu perfil
       
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
            print("----------------\nEXCLUIR USUÁRIO\n----------------")
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
                
                conn.close()
        excluir_user()
        main_menu()

    elif opcaouser == 0: #
        print("Obrigado por utilizar nosso sistema!")
        main_menu()
    
# Menu para admin
def menu_admin():# menu exclusivo de administradores
    
    print("------------------\nPERFIL DE ADMINISTRADOR\n------------------")
    print("(1) - CONSULTAR")
    print("(2) - CADASTRAR")
    print("(3) - ALTERAR")
    print("(4) - EXCLUIR")
    print("(0) - Sair")
    opcaoadm = int(input("Digite a opção desejada: "))

    if opcaoadm == 1: 
        def consultar():
            conn = sqlite3.connect("projectdbt.db")
            cursor = conn.cursor()

            select = input("SELECIONE PRODUTOS, USUÁRIOS ou SAIR: ").upper()
            
            if select == "PRODUTOS":
                print("----------------\nCONSULTA DE PRODUTOS\n----------------")

                cursor.execute("SELECT * FROM products")
                rs = cursor.fetchall()
                headers = ["ID","CATEGORIA", "SABOR", "PRECO", "QUANTIDADE"]
                print(tabulate(rs, headers = headers, tablefmt="psql"))

                def filtrar_id():

                    vId = input("ID: ")
                    cursor.execute("SELECT * FROM products WHERE ID =?", (vId,))
                    rs = cursor.fetchall()
                    headers = ["ID","CATEGORIA", "SABOR", "PRECO", "QUANTIDADE"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))
                    

                def filtrar_categoria():

                    vcat = input("CATEGORIA: ")
                    cursor.execute("SELECT * FROM products WHERE PRODUTO =?", (vcat,))
                    rs = cursor.fetchall()
                    headers = ["ID","CATEGORIA", "SABOR", "PRECO", "QUANTIDADE"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))
                
                def filtrar_sabor():

                    vsab = input("SABOR: ")
                    cursor.execute("SELECT * FROM products WHERE SABOR =?", (vsab,))
                    rs = cursor.fetchall()
                    headers = ["ID","CATEGORIA", "SABOR", "PRECO", "QUANTIDADE"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))
                
                def filtrar_preco():

                    vpreco = input("PRECO: ")
                    cursor.execute("SELECT * FROM products WHERE PRECO =?", (vpreco,))
                    rs = cursor.fetchall()
                    headers = ["ID","CATEGORIA", "SABOR", "PRECO", "QUANTIDADE"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))
                
                def filtrar_quantidade():

                    vquantidade = input("QUANTIDADE: ")
                    cursor.execute("SELECT * FROM products WHERE QUANTIDADE =?", (vquantidade,))
                    rs = cursor.fetchall()
                    headers = ["ID","CATEGORIA", "SABOR", "PRECO", "QUANTIDADE"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))

                print("ESCOLHA UM FILTRO PARA CONSULTAR")
                print("1 - ID")
                print("2 - CATEGORIA")
                print("3 - SABOR")
                print("4 - PRECO")
                print("5 - QUANTIDADE")
                print("0- Voltar")
                opcaofilter = int(input("Digite a opção desejada: "))

                if opcaofilter == 1:
                    filtrar_id()
                    consultar()

                elif opcaofilter == 2:
                    filtrar_categoria()
                    consultar()

                elif opcaofilter == 3:
                    filtrar_sabor()
                    consultar()

                elif opcaofilter == 4:
                    filtrar_preco()
                    consultar()

                elif opcaofilter == 5:
                    filtrar_quantidade()
                    consultar()
                
                elif opcaofilter == 0:
                    consultar()

                else:
                    print("Digite uma opção válida")
                    consultar()
                
            elif select ==  "USUÁRIOS":
                print("----------------\nCONSULTA DE USUÁRIOS\n----------------")

                cursor.execute("SELECT * FROM user")
                rs = cursor.fetchall()
                headers = ["CPF", "EMAIL", "NOME", "SENHA", "AUTHS"]
                print(tabulate(rs, headers = headers, tablefmt="psql"))

                def filtrar_cpf():

                    vcpf = input("CPF: ")
                    cursor.execute("SELECT * FROM user WHERE CPF =?", (vcpf,))
                    rs = cursor.fetchall()
                    headers = ["CPF", "EMAIL", "NOME", "SENHA", "AUTHS"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))
                    

                def filtrar_email():

                    vemail = input("EMAIL: ")
                    cursor.execute("SELECT * FROM user WHERE EMAIL =?", (vemail,))
                    rs = cursor.fetchall()
                    headers = ["CPF", "EMAIL", "NOME", "SENHA", "AUTHS"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))
                
                def filtrar_nome():

                    vnome = input("NOME: ")
                    cursor.execute("SELECT * FROM user WHERE NOME =?", (vnome,))
                    rs = cursor.fetchall()
                    headers = ["CPF", "EMAIL", "NOME", "SENHA", "AUTHS"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))
                
                def filtrar_auth():

                    vauth = input("AUTHS: ")
                    cursor.execute("SELECT * FROM user WHERE AUTORIZAÇÃO =?", (vauth,))
                    rs = cursor.fetchall()
                    headers = ["CPF", "EMAIL", "NOME", "SENHA", "AUTHS"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))

                print("ESCOLHA UM FILTRO PARA CONSULTAR")
                print("1 - CPF")
                print("2 - EMAIL")
                print("3 - NOME")
                print("4 - AUTH")
                print("0- Voltar")
                opcaofilter = int(input("Digite a opção desejada: "))

                if opcaofilter == 1:
                    filtrar_cpf()
                    consultar()

                elif opcaofilter == 2:
                    filtrar_email()
                    consultar()
                
                elif opcaofilter == 3:
                    filtrar_nome()
                    consultar()
                
                elif opcaofilter == 4:
                    filtrar_auth()
                    consultar()
                
                elif opcaofilter == 0:
                    consultar()

                else:
                    print("Digite uma opção válida")
                    consultar()
            
            elif select == "SAIR":
                menu_admin()
            
            else:
                print("POR FAVOR SELECIONE UMA OPÇÃO VÁLIDA. PRODUTOS OU USUÁRIOS")
                consultar()
        consultar()
        menu_admin()

    elif opcaoadm == 2: 
        def cadastrar_produto():
            # Conexão com SGDB
            conn = sqlite3.connect("projectdbt.db")
            cursor = conn.cursor()
            # Gerar ID automaticamente
            def gerador_de_id():

                counter = 1
                generated_ids = set()
                
                formatted_ID = f"{counter:04d}"
                counter += 1

                while formatted_ID in generated_ids:
                    formatted_ID = f"{counter:04d}"
                    counter += 1

                    generated_ids.add(formatted_ID)
                    return int(formatted_ID)
            # verifica se o categoria contém apenas letras
            def verificar_produto(vprod):
                if all((c.isalpha() or c.isspace()) for c in vprod) and  len(vprod) > 0:
                    return vprod
                else:
                    return False
            # verificar se o sabor contém apenas letras
            def verificar_sabor(vsabor):
                if all((c.isalpha() or c.isspace()) for c in vsabor) and  len(vsabor) > 0:
                    return vsabor
                else:
                    return None
                
            def verificar_preco(vpreco):
            # verifica se a senha contém pelo menos 1 caracter de cada
                try:
                    preco = float(vpreco)
                    return preco
                except ValueError:
                    return None
            # Verifica se as condições esão corretas
            while True:
                print("------------\nCADASTRAR PRODUTO!\n------------")
                vID = gerador_de_id()
            #input produto
                while True:
                    vprod = input("Categoria: ")
                    if verificar_produto(vprod):
                            break
                    else:
                            print("Certifique-se de digitar apenas letras e não deixe vazio.")
            #input sabor
                while True:
                    vsabor = input("Sabor: ")
                    if verificar_sabor(vsabor):
                            break
                    else:
                            print("Certifique-se de digitar apenas letras e não deixe vazio.")
            #input preço
                while True:
                    vpreco = float(input("Preço: "))
                    preco = verificar_preco(vpreco)
                    if preco is not None:
                            break
                    else:
                            print("Certifique-se de digitar apenas números e não deixe vazio.")

                while True:
                    vqtd = input("Quantidade: ")
                    try:
                            qtd = int(vqtd)
                            if qtd > 0:
                                break
                            else:
                                print("Quantidade deve ser maior que zero.")
                    except ValueError:
                            print("Certifique-se de digitar apenas números.")

                print("Produto cadstrado com sucesso!")

                cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (vID, vprod, vsabor, vpreco, vqtd))
                conn.commit()

                vcontinuar = input(" X FINALIZA o processo OU TECLA ENTER para CONTINUAR: ")
                if vcontinuar.upper() != '':
                    break
        cadastrar_produto()
        menu_admin()

    elif opcaoadm == 3:
        def alterar():

            select = input("SELECIONE PRODUTOS, USUÁRIOS ou SAIR: ").upper()

            # Seleção efetivada
            if select == "PRODUTOS":
        
                    # conexão com banco de dados
                    conn = sqlite3.connect("projectdbt.db")
                    cursor = conn.cursor()
                    
                    # trazer inforações do banco de dados
                    cursor.execute("SELECT * FROM products")
                    products = cursor.fetchall()

                    # colocar as informações em forma de tabela 
                    print("Catálogo de produtos")
                    headers = ["ID","CATEGORIA", "SABOR", "PRECO", "QUANTIDADE"]
                    print(tabulate(products, headers = headers))

                    print("------------\nALTERAR PRODUTO\n------------")
                    product_id = input("ID: ")

                    cursor.execute("SELECT * FROM products WHERE ID=?", (product_id,))
                    rs = cursor.fetchone()

                    if rs[0] > 0:
                        print ("Produto localizado")
                        print ("CATEGORIA: ", rs[1])
                        print ("SABOR: ", rs[2])
                        vconfirma = input("Quer alterar este produto? (S/N)")

                        if vconfirma.upper() == "S":

                            while True:
                                print("O que deseja alterar? (CATEGOGRIA(C), SABOR(S), PREÇO(P), QUANTIDADE(Q), SAIR(X))")
                                campo = input("Campo: ")

                                if campo.upper() == "X": # Seleção de alteração para sair
                                    break
                                
                                elif campo.upper() == "C": # Seleção de alteração para email
                                    altercat = input("Nova categoria: ")
                                    cursor.execute("UPDATE products SET PRODUTO = ? WHERE ID = ?", (altercat, product_id))
                                
                                elif campo.upper() == "S": # Seleção de alteração para nome
                                    altersab = input("Novo sabor: ")
                                    cursor.execute("UPDATE products SET SABOR =? WHERE ID =?", (altersab, product_id))

                                elif campo.upper() == "P": # Seleção de alteração para senha
                                    alterpre = input("Novo preço: ")
                                    cursor.execute("UPDATE products SET PRECO =? WHERE ID =?", (alterpre, product_id))

                                elif campo.upper() == "Q": # Seleção de alteração para senha
                                    alterqtd = input("Nova quantidade: ")
                                    cursor.execute("UPDATE products SET QUANTIDADE =? WHERE ID =?", (alterqtd, product_id))

                            # Enviar instrução SQL para ser executada
                                conn.commit()
                                print("DADOS ALTERADOS COM SUCESSO!")
                                menu_admin()

            elif select == "USUÁRIOS":
                
                    conn = sqlite3.connect("projectdbt.db")
                    cursor = conn.cursor()
                    
                    # lista dos usuários cadastrados no sistema
                    cursor.execute("SELECT * FROM user")
                    rs = cursor.fetchall()
                    headers = ["CPF", "EMAIL", "NOME", "SENHA", "AUTHS"]
                    print(tabulate(rs, headers = headers, tablefmt="psql"))
                    
                    # encripta a nova senha
                    def criptar_novasenha(altersenha):
                        #verifica se a senha contém pelo menos 1 caracter de cada
                        letter = any(c.isalpha() for c in altersenha)
                        number = any(c.isdigit() for c in altersenha)
                        spchar = any(c in "!@#$%&*?" for c in altersenha)
                        lenght = len(altersenha) <= 18
                        
                        return letter and number and spchar and lenght

                    def cript_pass(altersenha):

                        if criptar_novasenha(altersenha):
                            hasher1 = hashlib.sha256()
                            hasher1.update(altersenha.encode('utf-8'))
                            senha_hash = hasher1.digest()
                            vsenhacrip = binascii.hexlify(senha_hash)
                            return vsenhacrip

                    def verificar_email(alteremail):
                        try:
                            # Valida o email usando a função validate_email
                            valid = validate_email(alteremail)
                            return True
                        except EmailNotValidError as e:
                            # Captura a exceção EmailNotValidError caso o email não seja válido
                            print(str(e))
                            return False

                    def verificar_nome(alternome):
                        if all((c.isalpha() or c.isspace()) for c in alternome) and  len(alternome) > 0:
                            return True
                        else:
                            return False
                    print("------------\nALTERAR USUÁRIOS\n------------")
                    vcpf = input("CPF: ")

                    cursor.execute("SELECT count(*), CPF, EMAIL, NOME, AUTORIZAÇÃO FROM user WHERE CPF = ?", (vcpf,))
                    rs = cursor.fetchone()

                    if rs[0] > 0:
                        print ("Usuário localizado!")
                        print ("CPF: ", rs[0])
                        print ("EMAIL: ", rs[1])
                        print ("NOME: ", rs[2])
                        
                        vconfirma = input("Quer alterar este usuário? (S/N)")

                        if vconfirma.upper() == "S":

                            while True:
                                print("O que deseja alterar? (EMAIL(E), NOME(N), SENHA(S), SAIR(X))")
                                campo = input("Campo: ")

                                if campo.upper() == "X": # Seleção de alteração para sair
                                    break
                                
                                elif campo.upper() == "E": # Seleção de alteração para email
                                    altermail = input("Novo email: ")
                                    cursor.execute("UPDATE user SET EMAIL = ? WHERE CPF = ?", (altermail, vcpf))
                                
                                elif campo.upper() == "N": # Seleção de alteração para nome
                                    alternome = input("Novo nome: ")
                                    cursor.execute("UPDATE user SET NOME =? WHERE CPF =?", (alternome, vcpf))

                                elif campo.upper() == "S": # Seleção de alteração para senha
                                    print("LEMBRE-SE! A senha deve conter ao menos um caracter especial, um número e letras!")
                                    altersenha = getpass.getpass("Nova senha: ")
                                    vsenhacrip = cript_pass(altersenha)
                                        
                                    cursor.execute("UPDATE user SET SENHA =? WHERE CPF =?", (vsenhacrip, vcpf))

                            # Enviar instrução SQL para ser executada
                                conn.commit()
                                print("DADOS ALTERADOS COM SUCESSO!")
                                menu_admin()
                
            elif select == "SAIR":
                print ("------------\nVOLTANDO AO MENU\n------------")
                menu_admin()  
        
            else:
                print ("DIGITE UMA OPÇÃO VÁLIDA")
        alterar()
        menu_admin()

    elif opcaoadm == 4:
        def excluir():
            conn = sqlite3.connect("projectdbt.db")
            cursor = conn.cursor()
            select = input("SELECIONE PRODUTOS, USUÁRIOS ou SAIR: ").upper()

            if select == "PRODUTOS":
                print("CUIDADO A AÇÃO EXECUTADA É IRREVERSÍVEL")

                cursor.execute("SELECT * FROM products")
                productos = cursor.fetchall()

                # colocar as informações em forma de tabela 
                print("Catálogo de produtos")
                headers = ["ID","CATEGORIA", "SABOR", "PRECO", "QUANTIDADE"]
                print(tabulate(productos, headers = headers))

                print("------------\nEXCLUIR PRODUTO\n------------")
                print("Digite o ID do produto que deseja EXCLUIR")
                product_id = input("ID: ")

                cursor.execute("SELECT * FROM products WHERE ID=?", (product_id,))
                rs = cursor.fetchone()
                    
                if rs[0] > 0:
                    print ("PRODUTO LOCALIZADO!")
                    print ("ID: ", rs[0])
                    print ("CATEGORIA: ", rs[1])
                    print ("SABOR: ", rs[2])
                    print("PREÇO: ", rs[3])
                    print ("QUANTIDADE: ", rs[4])

                    vconfirma = input("Confirma a EXCLUSÃO deste produto? (S/N): ")

                    if vconfirma.upper() == "S":
                                # Enviar instrução SQL para ser executada
                        cursor.execute("DELETE FROM products WHERE ID = ?", (product_id,))
                        conn.commit()
                        print("PRODUTO EXCLUÍDO COM SUCESSO!")
                    else:
                        print("Exlcusão cancelada.")
                else:
                    print("Este produto não existe no catálogo.")
                        
                vcontinuar = input("Deseja excluir mais algum produto? (S/N): ")

                if vcontinuar.upper() == "S":
                    excluir()
                elif vcontinuar.upper() == "N":
                    menu_admin()

            elif select == "USUÁRIOS":
                print("CUIDADO A AÇÃO EXECUTADA É IRREVERSÍVEL")

                cursor.execute("SELECT * FROM user")
                users = cursor.fetchall()

                # colocar as informações em forma de tabela 
                print("Catálogo de produtos")
                headers = ["CPF", "EMAIL", "NOME", "SENHA", "AUTHS"]
                print(tabulate(users, headers = headers))

                print("------------\nEXCLUIR USUÁRIO\n------------")
                print("Digite o CPF do usuário que deseja EXCLUIR")
                vcpf = int(input("CPF: "))

                cursor.execute("SELECT * FROM user WHERE CPF=?", (vcpf,))
                rs = cursor.fetchone()
                    
                if rs[0] > 0:
                    print ("PRODUTO LOCALIZADO!")
                    print ("EMAIL: ", rs[1])
                    print ("NOME: ", rs[2])
                    print("SENHA: ", rs[3])
                    print ("AUTHS: ", rs[4])

                    vconfirma = input("Confirma a EXCLUSÃO deste usuário? (S/N): ")

                    if vconfirma.upper() == "S":
                                # Enviar instrução SQL para ser executada
                        cursor.execute("DELETE FROM user WHERE CPF = ?", (vcpf,))
                        conn.commit()
                        print("USUÁRIO EXCLUÍDO COM SUCESSO!")
                    else:
                        print("Exlcusão cancelada.")
                else:
                    print("Este usuário não esta cadastrado.")
                        
                vcontinuar = input("Deseja excluir mais algum usuário? (S/N): ")

                if vcontinuar.upper() == "N":
                    excluir()

            elif select == "SAIR":
                print("------------\nVOLTANDO AO MENU\n------------")
                menu_admin()
            else:
                print("POR FAVOR SELECIONE UMA OPÇÃO VÁLIDA. PRODUTOS OU USUÁRIOS")
        excluir()
        menu_admin()

    elif opcaoadm == 0: # Finalizar Programa
        print("Obrigado por utilizar nosso sistema!")
        main_menu()

if __name__ == "__main__": # incia a aplicação
    main_menu()