import sys

factories = {}
countries = {}
children = []

def parse_input():
    global factories, countries, children_by_country
    # Lê todo o conteúdo da entrada padrão
    lines = sys.stdin.read().strip().splitlines()

    # Lê a primeira linha com n, m, t
    n, m, t = map(int, lines[0].split())
    
    # Lê as fábricas
    for i in range(1, n+1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories[factory_id] = {'country': country_id, 'stock': stock, 'wanted': 0}
    
    # Lê os países
    for i in range(n+1, n+m+1):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        countries[country_id] = {'max_export': max_export, 'min_delivery': min_delivery, 'current_delivery': 0}
    
    # Lê os pedidos das crianças
    for i in range(n+m+1, n+m+t+1):
        data = list(map(int, lines[i].split()))
        child_id = data[0]
        country_id = data[1]
        factories_list = data[2:]
        for factory in factories_list:
            factories[factory]["wanted"] +=1
        children.append({"id": child_id, "country": country_id, "factories": factories_list})
    
    return n, m, t

def can_country_export(country):
    return countries[country]["current_delivery"] < countries[country]["max_export"]

def can_factory_produce(factory):
    return factories[factory]["stock"] > 0;

def export(country, factory):
    factories[factory]["stock"] -= 1
    factories[factory]["wanted"] -= 1
    countries[country]["current_delivery"] += 1

def merry_hanukkah():
    global factories, countries, children_by_country
    happy_children = 0

    children.sort(key=lambda c: len(c["factories"]))

    for child in children:
        country = child["country"]
        child["factories"].sort(key=lambda factory_id: factories[factory_id]['wanted'])
        
        if not can_country_export(country):
            continue
        
        for factory in child["factories"]:
            if not can_country_export(country):
                break
            if can_factory_produce(factory):
                export(country, factory)
                happy_children += 1
                break
            
    for country, data in countries.items():
        if data["current_delivery"] < data["min_delivery"]:
            return -1
    
    return happy_children

if __name__ == "__main__":
    import sys
    end_early = False
    
    n, m, t = parse_input()
    if n == 0:
        end_early = True
        result = -1
    
    if t == 0:
        end_early = True
        result = 0

    if not end_early:
        result = merry_hanukkah()
    
    print(result)
# Aqui, podemos imprimir ou processar os dados conforme necessário
#print("\nn:", n)
#print("m:", m)
#print("t:", t)
#print("Fábricas:", fabricas)
#print("Países:", paises)
#print("Crianças:", criancas)


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