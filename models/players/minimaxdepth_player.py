class MiniMaxDepth:

    MAXTIME = 3                # Constante que define tempo maximo que a IA pode demorar por jogada em segundos
    MAXRECURSIONDEPTH = 4      # Constante que define profundidade maxima de recursao, necessaria para que a arvore de busca gerada nao seja extremamente desequilibrada

    def __init__(self, color):
        self.color = color

    def play(self, board):
        import time
        self.start_time = time.time() # Tempo que a jogada comecou

        bestValue = -999 # Numero arbitrariamente pequeno
        bestMove = None

        for move in self.better_valid_moves(board, self.color):


            boardAfterMove = board.get_clone()
            boardAfterMove.play(move, self.color)

            value = self.minimaxdepth(boardAfterMove, board._opponent(self.color), self.MAXRECURSIONDEPTH - 1, time)

            if value > bestValue:
                bestValue = value
                bestMove = move


        print "Joguei na Casa: [" + str(bestMove) + "] e demorei " + str(time.time() - self.start_time) + " segundos."


        return bestMove


    # METODO RECURSIVO:
    def minimaxdepth(self, currentBoard, currentColor, depth, time):

        possibleMoves = self.better_valid_moves(currentBoard, currentColor)
        
        timeElapsed = time.time() - self.start_time # Tempo decorrido desde que a jogada comecou

        # Tabuleiro cheio ou tempo decorrido passara do MAXTIME estabelecido:
        if depth == 0 or not possibleMoves or timeElapsed > self.MAXTIME - 0.13: # 0.13 para levar em conta o tempo que pode vir a demorar para a jogada ser finalizada apos o backtracking comecar
            if self.color == currentBoard.WHITE: # Retorna como heuristica a pontuacao da cor da IA no tabuleiro/node-folha atual
                return currentBoard.score()[0] - currentBoard.score()[1]
            else: return currentBoard.score()[1] - currentBoard.score()[0]


        # Vez do jogador MAX (IA):
        if currentColor is self.color:

            bestValue = -999 # Numero arbitrariamente pequeno (menor que 0)

            for move in possibleMoves:

                boardAfterMove = currentBoard.get_clone()
                boardAfterMove.play(move, currentColor)

                value = self.minimaxdepth(boardAfterMove, currentBoard._opponent(currentColor), depth - 1, time)
                if value > bestValue: 
                    bestValue = value # no final do for, bestValue == value MAXIMO

            return bestValue

        # Vez do jogador MIN (oponente da IA):
        if currentColor is currentBoard._opponent(self.color): 
            
            bestValue = 999 # Numero arbitrariamente grande

            for move in possibleMoves:

                boardAfterMove = currentBoard.get_clone()
                boardAfterMove.play(move, currentColor)

                value = self.minimaxdepth(boardAfterMove, currentBoard._opponent(currentColor), depth - 1, time)
                if value < bestValue:
                    bestValue = value # no final do for, bestValue == value MINIMO
            
            return bestValue




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