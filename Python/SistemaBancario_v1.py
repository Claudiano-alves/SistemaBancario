def menu():
    menu = """

        =============    MENU    =============
        [1] - Novo usuário
        [2] - Nova conta
        [3] - Lista de contas
        [4] - Depositar
        [5] - Sacar
        [6] - Extrato
        [0] - Sair
        =============------------=============

    => """
    return input(menu)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = filtrar_usuarios(cpf, usuarios)
    if usuario:
        print("\n Já existe um usuário com esse CPF!")
        return
    nome = input("Informe o nome e sobrenome do usuário: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço da seguinte forma: [rua, número: bairro - cidade/sigla estado]: ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print(">>>\t\t\tUsuário criado com sucesso\t\t\t<<<")

def filtrar_usuarios(cpf, usuarios):
    filtra_usuarios = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return filtra_usuarios[0] if filtra_usuarios else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CFP do usuário: ")
    usuario = filtrar_usuarios(cpf, usuarios)
    if usuario:
        print("\n>>>\t\t\tConta criada com sucesso\t\t\t<<<")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n Usuário não encontrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t\t\t\t{conta['agencia']}        
            Conta:\t\t\t\t{conta['numero_conta']}        
            Titular:\t\t\t\t{conta['usuario']['nome']}    
        """
        print("-" * 100)
        print(linha)

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n>>>\t\t\tDepósito realizado com sucesso!\t\t\t<<<")
    else:
        print("\nvalor informado inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, valor_limite_saque, numero_saques, limite_saques):
    saldo_excedido = valor > saldo
    limite_excedido = valor > valor_limite_saque
    saques_excedido = numero_saques >= limite_saques

    if saldo_excedido:
        print("\nVocê não tem saldo suficiente.")
    elif limite_excedido:
        print("\nO valor do saque não corresponde ao seu limite.")
    elif saques_excedido:
        print("\nNúmero máximo de saques atingido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n>>>\t\t\tSaque realizado com sucesso!\t\t\t<<<")
    else:
        print("\nValor informado inválido.")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("=============    EXTRTATO    =============")
    print("Não foram realizadas transações." if not extrato else extrato)
    print(f"\nSaldo:\t\t\t\tR$ {saldo:.2f}")
    print("=============----------------=============")

def main():
    LIMITE_D_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    valor_limite_saque = 500
    numero_saques = 0
    usuarios = []
    contas = []
    extrato = ""

    while True:
        opcao = menu()

        if opcao == "1":
            criar_usuario(usuarios)
        elif opcao == "2":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "3":
            listar_contas(contas)
        elif opcao == "4":
            valor = float(input("Informe o valor de depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "5":
            valor = float(input("Informe o valor de saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                valor_limite_saque=valor_limite_saque,
                numero_saques=numero_saques,
                limite_saques=LIMITE_D_SAQUES,
            )
        elif opcao == "6":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "0":
            break
        else:
            print("Digite uma valor válido!")

main()
