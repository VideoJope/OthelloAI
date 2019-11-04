class MiniMaxAlphaBeta:

    MAXTIME = 3               # Constante que define tempo maximo que a IA pode demorar por jogada em segundos
    MAXRECURSIONDEPTH = 5     # Constante que define profundidade maxima de recursao, necessaria para que a arvore de busca gerada nao seja extremamente desequilibrada no fim do tempo estabelecido
    MINRECURSIONDEPTH = 1     # Constante que define profundidade minima de recursao, forcando que pelo menos um nivel apartir da raiz seja levado em consideracao antes de decidir uma jogada (independentemente do tempo levado)

    def __init__(self, color):
        self.color = color

    def play(self, board):
        import time
        self.start_time = time.time() # Tempo que a jogada comecou

        bestValue = None # Numero arbitrariamente pequeno

        for move in self.better_valid_moves(board, self.color):


            boardAfterMove = board.get_clone()
            boardAfterMove.play(move, self.color)

            alphaInicial = -999 # Numero arbitrariamente pequeno
            betaInicial = 999   # Numero arbitrariamente grande

            value = self.minimaxalphabeta(boardAfterMove, board._opponent(self.color), 0, time, alphaInicial, betaInicial)

            if value > bestValue:
                bestValue = value
                bestMove = move


        print "Joguei na Casa: [" + str(bestMove) + "] e demorei " + str(time.time() - self.start_time) + " segundos."


        return bestMove


    # METODO RECURSIVO:
    def minimaxalphabeta(self, currentBoard, currentColor, depth, time, alpha, beta):

        possibleMoves = self.better_valid_moves(currentBoard, currentColor)
        
        timeElapsed = time.time() - self.start_time # Tempo decorrido desde que a jogada comecou

        # Tabuleiro cheio ou tempo decorrido passara do MAXTIME estabelecido:
        if (depth >= self.MINRECURSIONDEPTH) and ((depth == self.MAXRECURSIONDEPTH) or (not possibleMoves) or (timeElapsed > self.MAXTIME - 0.13)): # 0.13 para levar em conta o tempo que pode vir a demorar para a jogada ser finalizada apos o backtracking comecar
            if self.color == currentBoard.WHITE: # Retorna como heuristica a ((pontuacao da cor da IA) - (pontuacao da cor do oponente)) no tabuleiro/node-folha atual
                return currentBoard.score()[0] - currentBoard.score()[1]
            else: return currentBoard.score()[1] - currentBoard.score()[0]


        # Vez do jogador MAX (IA):
        if currentColor is self.color:

            maxValue = -1000 # Numero arbitrariamente pequeno

            for move in possibleMoves:

                boardAfterMove = currentBoard.get_clone()
                boardAfterMove.play(move, currentColor)

                value = self.minimaxalphabeta(boardAfterMove, currentBoard._opponent(currentColor), depth + 1, time, alpha, beta)
                
                maxValue = max(value, maxValue)
                alpha = max(alpha, maxValue)


                if alpha >= beta:
                    return maxValue # realiza a poda na arvore, nao gerando mais nodes filhos
            return maxValue

        # Vez do jogador MIN (oponente da IA):
        if currentColor is currentBoard._opponent(self.color): 
            
            minValue = 1000 # Numero arbitrariamente grande

            for move in possibleMoves:

                boardAfterMove = currentBoard.get_clone()
                boardAfterMove.play(move, currentColor)

                value = self.minimaxalphabeta(boardAfterMove, currentBoard._opponent(currentColor), depth + 1, time, alpha, beta)
                
                minValue = min(value, minValue)
                beta = min(beta, minValue)

                if alpha >= beta:
                    return minValue # realiza a poda na arvore, nao gerando mais nodes filhos
            return minValue




    # VERSAO MELHORADA DO METODO valid_moves() PRESENTE NO MODULO board.py
    #   Esta versao nao retorna movimentos repetidos na lista de retorno 'ret'
    def better_valid_moves(self, board, color):
        from models.move import Move

        ret = []
        for i in range(1, 9):
            for j in range(1, 9):
                if board.board[i][j] == board.EMPTY:
                    for direction in board.DIRECTIONS:
                        move = Move(i, j)
                        bracket = board._find_bracket(move, color, direction)
                        if bracket and move not in ret:
                            ret += [move]
        return ret