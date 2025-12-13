import random

# 1. Classe Carta: O molde de uma única carta
class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    # Esta função define como a carta aparece escrita (ex: "Ás de Espadas")
    def __repr__(self):
        return f"{self.valor} de {self.naipe}"

# 2. Classe Baralho: O conjunto de cartas e ações (embaralhar, dar cartas)
class Baralho:
    def __init__(self):
        self.cartas = []
        self.montar_baralho()

    def montar_baralho(self):
        # Listas com os tipos de naipes e valores possíveis
        naipes = ['Copas', 'Ouros', 'Espadas', 'Paus']
        valores = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3'] 
        # Nota: Usei a ordem de força do Truco como exemplo base, mas podemos ajustar.
        
        self.cartas = []
        # Cria uma carta para cada combinação de valor e naipe
        for naipe in naipes:
            for valor in valores:
                nova_carta = Carta(valor, naipe)
                self.cartas.append(nova_carta)
    
    def embaralhar(self):
        random.shuffle(self.cartas)
        print("--- O baralho foi embaralhado! ---")

    def puxar_carta(self):
        if len(self.cartas) > 0:
            return self.cartas.pop() # Tira a última carta do monte
        else:
            return None

# --- TESTANDO O CÓDIGO (Simulação) ---

# Criamos um novo baralho
meu_baralho = Baralho()

print(f"Total de cartas iniciais: {len(meu_baralho.cartas)}")

# Embaralhamos
meu_baralho.embaralhar()

# Simulamos uma mão de jogador (recebendo 3 cartas)
minha_mao = []
for _ in range(3):
    carta_recebida = meu_baralho.puxar_carta()
    minha_mao.append(carta_recebida)

print(f"A minha mão é: {minha_mao}")
