import sys

def ler_input_de_stdin():
    # Lê todo o conteúdo da entrada padrão
    dados = sys.stdin.read().strip().splitlines()
    
    # Lê a primeira linha com n, m, t
    n, m, t = map(int, dados[0].split())
    
    # Lê as fábricas
    fabricas = {}
    for i in range(1, n+1):
        id_fabrica, id_pais, fmax = map(int, dados[i].split())
        fabricas[id_fabrica] = {'país': id_pais, 'fmax': fmax}
    
    # Lê os países
    paises = {}
    for i in range(n+1, n+m+1):
        id_pais, pmax, pmin = map(int, dados[i].split())
        paises[id_pais] = {'pmax': pmax, 'pmin': pmin}
    
    # Lê os pedidos das crianças
    criancas = []
    for i in range(n+m+1, n+m+t+1):
        pedido = list(map(int, dados[i].split()))
        id_crianca = pedido[0]
        id_pais_crianca = pedido[1]
        fabrica_onde_os_brinquedos_sao_produzidos = pedido[2:]
        criancas.append({'id da criança': id_crianca, 'id do país da criança': id_pais_crianca, 'fabrica dos brinquedos': fabrica_onde_os_brinquedos_sao_produzidos})
    
    return n, m, t, fabricas, paises, criancas

# Exemplo de uso da função
n, m, t, fabricas, paises, criancas = ler_input_de_stdin()

# Aqui, podemos imprimir ou processar os dados conforme necessário
print("\nn:", n)
print("m:", m)
print("t:", t)
print("Fábricas:", fabricas)
print("Países:", paises)
print("Crianças:", criancas)


"""
INPUT:
n(numFábricas) m(numPaíses) t(numCrianças)
n linhas:
i (FabricaID) j(PaisID) fMaxi(stockMaximoDaFabrica)
m linhas:
j(PaisID) pmaxJ(limiteExportacaoDoPais) pMinJ(minimoPresentesADistribuir)
t linhas:
k(CriançaID) j(PaisIDDaCriança) fi(FabricaOndeOsBrinquedosSaoProduzidos)

o que quero que faças em python:
1)ler um input inteiro e guardar
2)no programa temos de pegar nesse input inteiro e ver que:
    2.1.)primeira linha são n m t
    2.2.)fazer um for (for _ in range(n)) e por cada linha fazemos um for (for _ in range(3)) que sao os i,j,fMaxi
    2.3.)depois fazer outro for (for _ in range(m)) e por cada linha fazemos um for (for _ in range(3)) que sao os j,pmaxJ,pMinJ
    2.4.)por fim fazer outro for (for _ in range(t)) e por cada linha fazemos um for (for _ in range(3+t)) que sao o k,j,fi(fi é uma lista de tamanho t)
"""