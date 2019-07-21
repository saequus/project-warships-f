from random import randrange


class Board:
    def __init__(self):
        self.board_size = 100
        self.board = [{'id': _, 'status': 'alive', 'part_of': ''} for _ in
                      range(1, self.board_size + 1)]
        self.occupied = []
        self.grand_ship = {}
        self.middle_ships = {}
        self.small_ships = {}
        self.boats = {}

    def fill_board_with_ships(self):
        ships = list()
        ships.append(self.create_grand_ship())
        for ship in ships:
            for cell in ship:
                self.board[cell]['status'] = 'ship'

    def create_grand_ship(self):
        grand_ship_cells = []
        grand_ship_start_cell = self.get_random_inside_cell()
        grand_random = randrange(1, 3)
        if grand_random == 1 and grand_ship_start_cell % 10 < 5:
            grand_ship_cells = [_ for _ in range(
                grand_ship_start_cell, grand_ship_start_cell + 5)]
        elif grand_random == 2 and grand_ship_start_cell < 50:
            for i in range(5):
                grand_ship_cells.append(grand_ship_start_cell + i * 10)
        else:
            return self.create_grand_ship()
        self.occupied.append(grand_ship_start_cell)
        self.occupied.append(grand_ship_start_cell + 6)
        for cell in range(grand_ship_start_cell-11, grand_ship_start_cell-5):
            self.occupied.append(cell)
        for cell in grand_ship_cells:
            self.occupied.append(cell)
        for cell in range(grand_ship_start_cell+9, grand_ship_start_cell+15):
            self.occupied.append(cell)

        return grand_ship_cells

    def get_random_inside_cell(self):
        r = randrange(1, self.board_size + 1)
        while r < 11 or r > 90:
            r = randrange(1, self.board_size + 1)
        if r % 10 == 0:
            r += 2
        if r % 10 == 1:
            r += 1
        return r
