menu = """

> MENU <

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair

=> """

total_saldo = 0
limite_saque = 500
historico_transacoes = ""
quantidade_saques = 0
MAX_SAQUES_DIARIOS = 5

while True:

    opcao = input(menu)

    if opcao == "1":
        valor_deposito = float(input("Informe o valor do depósito: "))

        if valor_deposito > 0:
            total_saldo += valor_deposito
            historico_transacoes += f"Depósito de: R$ {valor_deposito:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":
        valor_saque = float(input("Informe o valor do saque: "))

        saldo_insuficiente = valor_saque > total_saldo
        saque_acima_limite = valor_saque > limite_saque
        saques_excedidos = quantidade_saques >= MAX_SAQUES_DIARIOS

        if saldo_insuficiente:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif saque_acima_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif saques_excedidos:
            print("Operação falhou! Número máximo de saques diários excedido.")

        elif valor_saque > 0:
            total_saldo -= valor_saque
            historico_transacoes += f"Saque: R$ {valor_saque:.2f}\n"
            quantidade_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not historico_transacoes else historico_transacoes)
        print(f"\nSaldo: R$ {total_saldo:.2f}")
        print("===========================================")

    elif opcao == "4":
        break

    else:
        print("Opção inválida, por favor selecione uma operação válida.")
