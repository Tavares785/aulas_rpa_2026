"""
AULA 03 - Arquitetura Modular de Dados
Exemplo do PROFESSOR

Tema didatico: funcoes com type hints, dicionarios, listas e menu while.
Cenario: catalogo de patrimonio de equipamentos de laboratorio, mapeando
cada item ao seu setor e numero de tombamento (controle de ativos).
"""


def registrar_equipamento(nome: str, setor: str, tombamento: str) -> dict:
    """Retorna um dicionario padronizado representando um equipamento."""
    return {"nome": nome, "setor": setor, "tombamento": tombamento}


def listar_equipamentos(equipamentos: list) -> None:
    """Percorre a lista e imprime cada equipamento formatado."""
    if not equipamentos:
        print("Nenhum equipamento no catalogo ainda.")
        return
    print("\n--- CATALOGO DE EQUIPAMENTOS ---")
    for i, eq in enumerate(equipamentos, start=1):
        print(f"{i}. {eq['nome']} | Setor: {eq['setor']} | Tombo: {eq['tombamento']}")


def menu() -> None:
    """Menu interativo. Em aula, mostre o fluxo do while True + break."""
    equipamentos: list = []
    while True:
        print("\n[1] Registrar equipamento  [2] Ver catalogo  [9] Encerrar")
        opcao = input("Opcao: ").strip()

        if opcao == "1":
            nome = input("Nome do equipamento: ")
            setor = input("Setor: ")
            tombamento = input("Tombamento: ")
            equipamentos.append(registrar_equipamento(nome, setor, tombamento))
            print("Equipamento registrado!")
        elif opcao == "2":
            listar_equipamentos(equipamentos)
        elif opcao == "9":
            print("Encerrando...")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    # DICA DE AULA: a demo abaixo roda sem interacao para provar o fluxo.
    # Troque pela chamada menu() para a versao com entrada do usuario.
    demo = [
        registrar_equipamento("Microscopio Binocular", "Biologia", "LAB-00412"),
        registrar_equipamento("Centrifuga Refrigerada", "Quimica", "LAB-00873"),
    ]
    listar_equipamentos(demo)
    # menu()  # descomente para a versao interativa
