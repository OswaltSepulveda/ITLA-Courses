import sys
sys.path.append("C:/Users/oswal/Desktop/ITLA/Planificacion Inteligente")
from sudoku_solver.board import Board

class CandidateReducer:
    def reduce(self, candidates: dict[tuple[int,int], set[str]]) -> None:
        raise NotImplementedError

class NakedTwinsReducer(CandidateReducer):
    def reduce(self, candidates):
        # Construir unidades (filas, columnas y cajas 3x3)
        units = []
        for i in range(9):
            units.append([(i, j) for j in range(9)])
        for j in range(9):
            units.append([(i, j) for i in range(9)])
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                units.append([(br + r, bc + c) for r in range(3) for c in range(3)])

        # Aplicar Naked Twins en cada unidad
        for unit in units:
            twin_map = {}
            for cell in unit:
                if cell in candidates and len(candidates[cell]) == 2:
                    key = tuple(sorted(candidates[cell]))
                    twin_map.setdefault(key, []).append(cell)
            for key, cells in twin_map.items():
                if len(cells) == 2:
                    for cell in unit:
                        if cell not in cells and cell in candidates:
                            candidates[cell] -= set(key)

class Solver:
    def __init__(self, board: Board, reducers: list[CandidateReducer] = None):
        self.board = board
        self.reducers = reducers or [NakedTwinsReducer()]

    def verificar_fila(self, fila: int, columna: int, numero: str) -> bool:
        # Verificar fila
        if numero in self.board.grid[fila]:
            return False
        # Verificar columna
        for i in range(9):
            if self.board.grid[i][columna] == numero:
                return False
        # Verificar caja 3x3
        fr, fc = 3*(fila//3), 3*(columna//3)
        for i in range(fr, fr+3):
            for j in range(fc, fc+3):
                if self.board.grid[i][j] == numero:
                    return False
        return True

    def find_empty_location(self) -> tuple[int,int] | None:
        for i in range(9):
            for j in range(9):
                if self.board.grid[i][j] == ".":
                    return (i, j)
        return None

    def find_candidates(self) -> dict[tuple[int,int], set[str]]:
        candidates = {}
        for i in range(9):
            for j in range(9):
                if self.board.grid[i][j] == ".":
                    options = set(map(str, range(1, 10)))
                    # Eliminar fila
                    for v in self.board.grid[i]: options.discard(v)
                    # Eliminar columna
                    for ii in range(9): options.discard(self.board.grid[ii][j])
                    # Eliminar caja
                    fr, fc = 3*(i//3), 3*(j//3)
                    for r in range(fr, fr+3):
                        for c in range(fc, fc+3):
                            options.discard(self.board.grid[r][c])
                    candidates[(i, j)] = options
        return candidates

    def solve(self) -> bool:
        loc = self.find_empty_location()
        if not loc:
            return True  # Sudoku resuelto

        # Calcular y reducir candidatos
        candidates = self.find_candidates()
        for reducer in self.reducers:
            reducer.reduce(candidates)

        i, j = loc
        if (i, j) not in candidates or not candidates[(i, j)]:
            return False

        for n in sorted(candidates[(i, j)]):
            if self.verificar_fila(i, j, n):
                self.board.grid[i][j] = n
                if self.solve():
                    return True
                self.board.grid[i][j] = "."
        return False

class SolverX(Solver):
    def verificar_fila(self, fila: int, columna: int, numero: str) -> bool:
        # Validación clásica
        if not super().verificar_fila(fila, columna, numero):
            return False
        # Diagonal principal
        if fila == columna:
            for d in range(9):
                if self.board.grid[d][d] == numero:
                    return False
        # Diagonal secundaria
        if fila + columna == 8:
            for d in range(9):
                if self.board.grid[d][8 - d] == numero:
                    return False
        return True