from classes import Carta, Baralho
import time

class JogoTruco:
    def __init__(self):
        self.baralho = Baralho()
        self.pontos_jogador = 0
        self.pontos_cpu = 0
        
        # Tabelas de força
        self.tabela_forca = {'4':1, '5':2, '6':3, '7':4, 'Q':5, 'J':6, 'K':7, 'A':8, '2':9, '3':10}
        self.ordem_cartas = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.forca_naipes = {'Paus': 4, 'Copas': 3, 'Espadas': 2, 'Ouros': 1}

    # --- LÓGICA DE MANILHA ---
    def descobrir_manilha(self, carta_vira):
        indice_vira = self.ordem_cartas.index(carta_vira.valor)
        indice_manilha = (indice_vira + 1) % len(self.ordem_cartas)
        return self.ordem_cartas[indice_manilha]

    def calcular_forca_real(self, carta, valor_manilha):
        if carta.valor == valor_manilha:
            return 100 + self.forca_naipes[carta.naipe]
        else:
            return self.tabela_forca[carta.valor]

    # --- INTERFACE COM O JOGADOR ---
    def escolher_carta_humano(self, mao):
        """
        Mostra as cartas e pede para o usuário escolher pelo índice.
        """
        print("\n>>> SUA VEZ DE JOGAR <<<")
        print(f"Suas cartas:")
        
        # Exibe as cartas com seus índices
        for i, carta in enumerate(mao):
            print(f"  [{i}] {carta}")

        # Loop de Validação
        while True:
            try:
                escolha = int(input("Escolha o número da carta (0, 1 ou 2): "))
                
                # Verifica se o número escolhido é válido para o tamanho atual da mão
                if 0 <= escolha < len(mao):
                    carta_escolhida = mao.pop(escolha) # Remove da mão e retorna
                    return carta_escolhida
                else:
                    print("❌ Número inválido! Escolha um número que aparece na lista.")
            except ValueError:
                print("❌ Isso não é um número! Digite apenas o número (ex: 0).")

    # --- MOTOR DO JOGO ---
    def jogar_mao(self):
        self.baralho.montar_baralho()
        self.baralho.embaralhar()
        
        # 1. Definir o Vira
        vira = self.baralho.puxar_carta()
        valor_manilha = self.descobrir_manilha(vira)
        
        print(f"\n========================================")
        print(f"🃏 O VIRA É: [{vira}] -> MANILHA É: {valor_manilha}")
        print(f"========================================")
        
        # 2. Distribuir cartas
        mao_jogador = [self.baralho.puxar_carta() for _ in range(3)]
        mao_cpu = [self.baralho.puxar_carta() for _ in range(3)]
        
        vitorias_jogador = 0
        vitorias_cpu = 0

        # 3. Loop das 3 Vazas
        for rodada in range(1, 4):
            print(f"\n--- Rodada {rodada}/3 ---")
            
            # --- HUMANO JOGA ---
            c_jog = self.escolher_carta_humano(mao_jogador)
            
            # --- CPU JOGA ---
            # CPU joga a primeira carta disponível
            c_cpu = mao_cpu.pop(0) 
            print(f"🤖 CPU jogou: {c_cpu}")

            # --- QUEM GANHOU? ---
            f_jog = self.calcular_forca_real(c_jog, valor_manilha)
            f_cpu = self.calcular_forca_real(c_cpu, valor_manilha)
            
            if f_jog > f_cpu:
                print("✨ VOCÊ levanta a vaza!")
                vitorias_jogador += 1
                quem_fez_a_vaza = "JOGADOR"
            else:
                print("💀 CPU levanta a vaza!")
                vitorias_cpu += 1
                quem_fez_a_vaza = "CPU"
            
            time.sleep(1.5)

            # Verifica se acabou a mão
            if vitorias_jogador == 2:
                print("\n🏆 VOCÊ GANHOU A MÃO!")
                return "JOGADOR"
            if vitorias_cpu == 2:
                print("\n😭 CPU GANHOU A MÃO!")
                return "CPU"

        return "EMPATE"

    def iniciar_partida(self):
        print("\n--- BEM-VINDO AO MESTRE DO TRUCO v1.0 ---")
        while self.pontos_jogador < 12 and self.pontos_cpu < 12:
            print(f"\nPLACAR: Você {self.pontos_jogador} x {self.pontos_cpu} CPU")
            input("Pressione ENTER para dar as cartas...")
            
            vencedor = self.jogar_mao()
            
            if vencedor == "JOGADOR":
                self.pontos_jogador += 1
            elif vencedor == "CPU":
                self.pontos_cpu += 1
        
        if self.pontos_jogador >= 12:
            print("PARABÉNS! VOCÊ É O CAMPEÃO!")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    jogo = JogoTruco()
    jogo.iniciar_partida()