import itertools
import random


class Minesweeper():

    def __init__(self, height=8, width=8, mines=8):

        self.height = height
        self.width = width
        self.mines = set()

        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def print(self):

        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):

        count = 0

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence():

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):

        if self.count == len(self.cells):
            return set(self.cells)

        return set()

    def known_safes(self):

        if self.count == 0:
            return set(self.cells)

        return set()

    def mark_mine(self, cell):

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():

    def __init__(self, height=8, width=8):

        self.height = height
        self.width = width

        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):

        self.mines.add(cell)

        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):

        self.safes.add(cell)

        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):

        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = set()
        adjusted_count = count

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                neighbor = (i, j)

                if neighbor == cell:
                    continue

                if not (0 <= i < self.height and 0 <= j < self.width):
                    continue

                if neighbor in self.mines:
                    adjusted_count -= 1

                elif neighbor not in self.safes:
                    neighbors.add(neighbor)

        new_sentence = Sentence(neighbors, adjusted_count)

        if new_sentence.cells and new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        while True:

            new_mines = set()
            new_safes = set()

            for sentence in self.knowledge:
                new_mines.update(sentence.known_mines())
                new_safes.update(sentence.known_safes())

            new_mines -= self.mines
            new_safes -= self.safes

            for mine in new_mines:
                self.mark_mine(mine)

            for safe in new_safes:
                self.mark_safe(safe)

            self.knowledge = [
                sentence for sentence in self.knowledge
                if sentence.cells
            ]

            unique_knowledge = []

            for sentence in self.knowledge:
                if sentence not in unique_knowledge:
                    unique_knowledge.append(sentence)

            self.knowledge = unique_knowledge

            new_sentences = []

            for sentence1, sentence2 in itertools.combinations(
                self.knowledge, 2
            ):

                if sentence1.cells < sentence2.cells:

                    difference = sentence2.cells - sentence1.cells
                    difference_count = sentence2.count - sentence1.count

                    inferred = Sentence(difference, difference_count)

                    if inferred.cells and inferred not in self.knowledge:
                        new_sentences.append(inferred)

                elif sentence2.cells < sentence1.cells:

                    difference = sentence1.cells - sentence2.cells
                    difference_count = sentence1.count - sentence2.count

                    inferred = Sentence(difference, difference_count)

                    if inferred.cells and inferred not in self.knowledge:
                        new_sentences.append(inferred)

            added = False

            for sentence in new_sentences:
                if sentence not in self.knowledge:
                    self.knowledge.append(sentence)
                    added = True

            if not new_mines and not new_safes and not added:
                break

    def make_safe_move(self):

        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        return None

    def make_random_move(self):

        possible_moves = []

        for i in range(self.height):
            for j in range(self.width):

                cell = (i, j)

                if cell not in self.moves_made and cell not in self.mines:
                    possible_moves.append(cell)

        if possible_moves:
            return random.choice(possible_moves)

        return None
