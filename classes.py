import random

# Classe Carta
class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    # Representação da carta como string
    def __repr__(self):
        return f"{self.valor} de {self.naipe}"

# Classe Baralho
class Baralho:
    def __init__(self):
        self.cartas = []
        self.montar_baralho()

    def montar_baralho(self):
        # Naipes e valores do Truco
        naipes = ['Copas', 'Ouros', 'Espadas', 'Paus']
        valores = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3'] 
        
        self.cartas = []
        # Gera todas as combinações
        for naipe in naipes:
            for valor in valores:
                nova_carta = Carta(valor, naipe)
                self.cartas.append(nova_carta)
    
    def embaralhar(self):
        random.shuffle(self.cartas)
        print("--- O baralho foi embaralhado! ---")

    def puxar_carta(self):
        if len(self.cartas) > 0:
            return self.cartas.pop()
        else:
            return None

if __name__ == "__main__":
    # Teste das classes
    meu_baralho = Baralho()
    print(f"Total de cartas iniciais: {len(meu_baralho.cartas)}")

    meu_baralho.embaralhar()

    minha_mao = []
    for _ in range(3):
        carta_recebida = meu_baralho.puxar_carta()
        minha_mao.append(carta_recebida)

    print(f"A minha mão é: {minha_mao}")
