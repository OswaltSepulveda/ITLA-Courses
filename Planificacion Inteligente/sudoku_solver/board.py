class Board:
    def __init__(self, grid):
        self.grid = grid

    def mostrar(self):
        for fila in self.grid:
            print(" ".join(fila))
        print()

    def es_valido(self):
        if len(self.grid) != 9:
            return False
        for fila in self.grid:
            if len(fila) != 9:
                return False
        return True