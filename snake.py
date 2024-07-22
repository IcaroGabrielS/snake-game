import curses
import time 
import random
import sys

def cria_cobra(NLINS, NCOLS):
    centro_linha = NLINS // 2
    centro_coluna = NCOLS //2 
    
    corpo = [(centro_linha, centro_coluna - 1), (centro_linha, centro_coluna), (centro_linha, centro_coluna + 1)]
    
    return (corpo)

def move_cobra(corpo, direcao):
    cabeca = corpo[0]

    if direcao == curses.KEY_UP:
        nova_cabeca = (cabeca[0] - 1, cabeca[1])
    
    elif direcao == curses.KEY_DOWN:
        nova_cabeca = (cabeca[0] + 1, cabeca[1])
    
    elif direcao == curses.KEY_LEFT:
        nova_cabeca = (cabeca[0], cabeca[1] - 1)
    
    elif direcao == curses.KEY_RIGHT:
        nova_cabeca = (cabeca[0], cabeca[1] + 1)

    corpo.insert(0, nova_cabeca)
    corpo.pop()
    return(corpo)

def gera_comida(NLINS, NCOLS, corpo_cobra):
    while True:
        
        linha_comida = random.randint(1, NLINS - 4)
        coluna_comida = random.randint(1, NCOLS - 4)
        
        if (linha_comida, coluna_comida) not in corpo_cobra:
            
            return(linha_comida, coluna_comida)

def aumenta_cobra(corpo, comida, velocidade):
    if corpo[0] == comida:
        corpo.append(corpo[-1])
        velocidade -= 2
        condicao = True
    
    else: condicao = False
    
    return corpo, condicao, velocidade

def verifica_colisao(corpo, NLINS, NCOLS):
    cabeca = corpo[0]
    
    if cabeca in corpo[1:]:
        return True

    if (cabeca[0] == 0 or cabeca[0] == NLINS - 1) or (cabeca[1] == 0 or cabeca[1] == NCOLS - 1):
        return True

    return False


def snake(stdscr):
    
    velocidade = 100
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(velocidade)

    NLINS, NCOLS = stdscr.getmaxyx()
    corpo = cria_cobra(NLINS, NCOLS)
    direcao = curses.KEY_LEFT
    comida = gera_comida(NLINS, NCOLS, corpo)
    pontuacao = 0
    

    while True:
        stdscr.clear()
            # Desenhar bordas verticais
        for i in range(1, NLINS - 1):
            stdscr.addch(i, 0, "|")
            stdscr.addch(i, NCOLS - 1, "|")
    
    # Desenhar bordas horizontais
        for i in range(1, NCOLS - 1):
            stdscr.addch(0, i, "-")
            stdscr.addch(NLINS - 1, i, "-")
        stdscr.addch(comida[0], comida[1], "#")

        cont = 0
        for posicao in corpo:
            
            if cont == 0:
                stdscr.addch(posicao[0], posicao[1], "+")
                cont += 1
            else:
                stdscr.addch(posicao[0], posicao[1], "=")

        
        stdscr.addstr(0, 2, f"Pontuação: {pontuacao}.")
            
        
        tecla = stdscr.getch()

        if tecla in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
           
           # Sim, eu sei que essa sequência pode ser simplificada mas acho que ficaria grande demais pra ler no meu monitor

            if (tecla == curses.KEY_UP) and (direcao != curses.KEY_DOWN):
                direcao = tecla
            
            elif (tecla == curses.KEY_DOWN) and (direcao != curses.KEY_UP):
                direcao = tecla
            
            elif (tecla == curses.KEY_LEFT) and (direcao != curses.KEY_RIGHT):
                direcao = tecla
            
            elif (tecla == curses.KEY_RIGHT) and (direcao != curses.KEY_LEFT):
                direcao = tecla
        
        corpo = move_cobra(corpo, direcao)
        corpo, troca_comida, velocidade = aumenta_cobra(corpo, comida, velocidade)
        
        if velocidade < 5:
            velocidade = 5
        
        if troca_comida:
            comida = gera_comida(NLINS, NCOLS, corpo)

        if verifica_colisao(corpo, NLINS, NCOLS):
            stdscr.clear()
            stdscr.addstr(NLINS // 2, (NCOLS - 20) // 2, "! G A M E  O V E R !")
            stdscr.addstr((NLINS // 2) + 2, (NCOLS - 23) // 2, "PRESSIONE 'Q' PARA SAIR")
            stdscr.addstr((NLINS // 2) + 4, (NCOLS - 20) // 2, f"PONTUACÃO FINAL: {pontuacao}")
            stdscr.refresh()
            while True:
                tecla = stdscr.getch()
                if tecla == ord("q") or tecla == ord("Q"):
                    sys.exit()
        
        pontuacao = len(corpo) - 3
        stdscr.refresh()
        time.sleep(0.1)

def main():
    curses.wrapper(snake)
    time.sleep(0.1)

if __name__ == "__main__":
    main()

