from classes import Baralho
import time

class JogoTruco:
    def __init__(self):
        self.baralho = Baralho()
        self.pontos_jogador = 0
        self.pontos_cpu = 0
        self.valor_mao = 1 # O jogo começa valendo 1 ponto
        self.modo_tutorial = False # Será definido no início
        
        # Tabelas de força
        self.tabela_forca = {'4':1, '5':2, '6':3, '7':4, 'Q':5, 'J':6, 'K':7, 'A':8, '2':9, '3':10}
        self.ordem_cartas = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.forca_naipes = {'Paus': 4, 'Copas': 3, 'Espadas': 2, 'Ouros': 1}

    # --- LÓGICA AUXILIAR ---
    def descobrir_manilha(self, carta_vira):
        indice_vira = self.ordem_cartas.index(carta_vira.valor)
        indice_manilha = (indice_vira + 1) % len(self.ordem_cartas)
        return self.ordem_cartas[indice_manilha]

    def calcular_forca_real(self, carta, valor_manilha):
        if carta.valor == valor_manilha:
            return 100 + self.forca_naipes[carta.naipe]
        else:
            return self.tabela_forca[carta.valor]

    # --- IA: CÉREBRO DA MÁQUINA ---
    def ia_escolher_carta(self, mao_cpu, carta_oponente, valor_manilha):
        """Define qual carta a CPU vai jogar."""
        # Organiza a mão da CPU
        mao_cpu.sort(key=lambda c: self.calcular_forca_real(c, valor_manilha))

        # Se a CPU joga primeiro
        if carta_oponente is None:
            return mao_cpu.pop(0) # Joga a mais fraca (esconde o jogo)

        # Se a CPU responde ao jogador
        else:
            forca_oponente = self.calcular_forca_real(carta_oponente, valor_manilha)
            for indice, carta in enumerate(mao_cpu):
                forca_cpu = self.calcular_forca_real(carta, valor_manilha)
                if forca_cpu > forca_oponente:
                    return mao_cpu.pop(indice) # Ganha com a menor possível
            return mao_cpu.pop(0) # Perde descartando lixo

    def ia_responder_truco(self, mao_cpu, valor_manilha):
        """A IA decide se aceita o Truco ou corre."""
        print("\n🤖 CPU está analisando a própria mão...")
        time.sleep(1.5)
        
        # Lógica simples: Soma a força de todas as cartas
        forca_total = sum([self.calcular_forca_real(c, valor_manilha) for c in mao_cpu])
        
        # Se tiver cartas fortes (ex: uma manilha vale 100, então > 15 é razoável)
        # Ajuste esse valor para deixar a IA mais ou menos corajosa
        if forca_total > 15: 
            print("🤖 CPU: 'PODE VIR! EU ACEITO!'")
            return True
        else:
            print("🤖 CPU: 'Tô fora... Corri!'")
            return False

    # --- TUTORIAL: O TREINADOR ---
    def dar_dica_tutorial(self, mao, carta_oponente, valor_manilha):
        """Analisa sua mão e explica a melhor jogada."""
        print("\n💡 --- DICA DO TREINADOR ---")
        
        # Verifica se tem manilha
        tem_manilha = False
        for c in mao:
            if c.valor == valor_manilha:
                print(f"-> OPA! Você tem o {c}, que é MANILHA! É a carta mais forte da rodada.")
                tem_manilha = True
        
        if not tem_manilha:
            print("-> Você não tem manilhas. Terá que jogar com estratégia.")

        if carta_oponente:
            print(f"-> A CPU jogou {carta_oponente}. Tente jogar uma carta um pouco maior para ganhar,")
            print("   ou jogue a sua pior carta se não conseguir ganhar.")
        else:
            print("-> Você começa. Geralmente é bom jogar uma carta fraca para não gastar as fortes agora.")
        print("---------------------------")

    # --- INTERFACE HUMANA ---
    def escolher_carta_humano(self, mao, carta_oponente, valor_manilha):
        if self.modo_tutorial:
            self.dar_dica_tutorial(mao, carta_oponente, valor_manilha)

        print(f"\nSuas cartas: ", end="")
        for i, carta in enumerate(mao):
            print(f"[{i}] {carta}  ", end="")
        
        # Só pode pedir truco se o jogo ainda valer 1
        pode_pedir_truco = self.valor_mao == 1
        if pode_pedir_truco:
            print("[9] PEDIR TRUCO!", end="")
        print()

        while True:
            try:
                escolha = int(input("👉 Qual sua jogada? "))
                
                # Opção de TRUCO
                if escolha == 9 and pode_pedir_truco:
                    return "TRUCO"
                
                # Opção de Carta
                elif 0 <= escolha < len(mao):
                    return mao.pop(escolha)
                else:
                    print("❌ Opção inválida.")
            except ValueError:
                print("❌ Digite apenas números.")

    # --- MOTOR DO JOGO ---
    def jogar_mao(self):
        self.baralho.montar_baralho()
        self.baralho.embaralhar()
        self.valor_mao = 1 # Reseta o valor da aposta
        
        vira = self.baralho.puxar_carta()
        valor_manilha = self.descobrir_manilha(vira)
        
        print(f"\n========================================")
        print(f"🃏 VIRA: {vira} | MANILHA (A Forte): {valor_manilha}")
        if self.modo_tutorial:
            print(f"ℹ️ (Tutorial: Qualquer carta com número '{valor_manilha}' é invencível!)")
        print(f"========================================")
        
        mao_jogador = [self.baralho.puxar_carta() for _ in range(3)]
        mao_cpu = [self.baralho.puxar_carta() for _ in range(3)]
        
        vitorias_jogador = 0
        vitorias_cpu = 0
        quem_comeca = "JOGADOR"

        for rodada in range(1, 4):
            print(f"\n--- Rodada {rodada}/3 (Vale {self.valor_mao} pts) ---")
            
            c_jog = None
            c_cpu = None

            # --- TURNO DO JOGADOR ---
            if quem_comeca == "JOGADOR":
                acao = self.escolher_carta_humano(mao_jogador, None, valor_manilha)
                
                # Lógica do Truco
                if acao == "TRUCO":
                    print("🗣️  VOCÊ: 'TRUUUUCO, MARRECO!!'")
                    aceitou = self.ia_responder_truco(mao_cpu, valor_manilha)
                    if aceitou:
                        self.valor_mao = 3
                        # Se aceitou, você tem que jogar uma carta agora
                        print(">> O jogo continua valendo 3! Escolha sua carta agora.")
                        acao = self.escolher_carta_humano(mao_jogador, None, valor_manilha)
                        # (Nota: simplificação, removemos a opção de pedir truco de novo aqui)
                        if acao == "TRUCO": # Se o usuário tentar trucar de novo, pega a 1ª carta (bug fix rápido)
                             acao = mao_jogador.pop(0)
                    else:
                        print("🏆 CPU fugiu! Você ganhou a mão.")
                        return "JOGADOR"
                
                c_jog = acao
                print(f"Você jogou: {c_jog}")
                
                c_cpu = self.ia_escolher_carta(mao_cpu, c_jog, valor_manilha)
                print(f"🤖 CPU jogou: {c_cpu}")

            # --- TURNO DA CPU ---
            else: 
                c_cpu = self.ia_escolher_carta(mao_cpu, None, valor_manilha)
                print(f"🤖 CPU jogou: {c_cpu}")
                
                acao = self.escolher_carta_humano(mao_jogador, c_cpu, valor_manilha)
                
                 # Lógica do Truco (Repetida - idealmente seria uma função separada, mas mantendo simples)
                if acao == "TRUCO":
                    print("🗣️  VOCÊ: 'TRUUUUCO!!'")
                    aceitou = self.ia_responder_truco(mao_cpu, valor_manilha)
                    if aceitou:
                        self.valor_mao = 3
                        print(">> Jogo valendo 3! Jogue sua carta.")
                        acao = self.escolher_carta_humano(mao_jogador, c_cpu, valor_manilha)
                        if acao == "TRUCO": acao = mao_jogador.pop(0)
                    else:
                        print("🏆 CPU correu! Ponto pra você.")
                        return "JOGADOR"

                c_jog = acao
                print(f"Você jogou: {c_jog}")

            # --- RESOLUÇÃO DA VAZA ---
            f_jog = self.calcular_forca_real(c_jog, valor_manilha)
            f_cpu = self.calcular_forca_real(c_cpu, valor_manilha)
            
            if f_jog > f_cpu:
                print("✨ VOCÊ levou!")
                vitorias_jogador += 1
                quem_comeca = "JOGADOR"
            else:
                print("💀 CPU levou!")
                vitorias_cpu += 1
                quem_comeca = "CPU"
            
            time.sleep(1)
            
            # --- FIM DA MÃO ---
            if vitorias_jogador == 2:
                print(f"\n🏆 VOCÊ GANHOU A MÃO! (+{self.valor_mao} pontos)")
                return "JOGADOR"
            if vitorias_cpu == 2:
                print(f"\n😭 CPU GANHOU A MÃO! (+{self.valor_mao} pontos)")
                return "CPU"

        return "EMPATE"

    def iniciar_partida(self):
        print("\n♠️ ♥️  MESTRE DO TRUCO - AULA PRÁTICA ♦️ ♣️")
        
        resp = input("Deseja ativar o Modo Tutorial (Dicas)? (s/n): ").lower()
        self.modo_tutorial = (resp == 's')

        while self.pontos_jogador < 12 and self.pontos_cpu < 12:
            print(f"\n📢 PLACAR: Você {self.pontos_jogador} x {self.pontos_cpu} CPU")
            input("Pressione ENTER para dar as cartas...")
            
            vencedor = self.jogar_mao()
            
            # Agora somamos o self.valor_mao (que pode ser 1 ou 3)
            if vencedor == "JOGADOR":
                self.pontos_jogador += self.valor_mao 
            elif vencedor == "CPU":
                self.pontos_cpu += self.valor_mao
        
        if self.pontos_jogador >= 12:
            print("\n🎉 PARABÉNS! VOCÊ ZEROU O JOGO!")

if __name__ == "__main__":
    jogo = JogoTruco()
    jogo.iniciar_partida()