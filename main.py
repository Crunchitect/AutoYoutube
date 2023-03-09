from os import mkdir, remove
from random import sample
from PIL import Image
from glob import glob


def main():
    def create_files():
        try:
            mkdir('resources')
        except FileExistsError:
            pass

        try:
            mkdir('resources/frames')
            files = glob('/YOUR/PATH/*')
            for f in files:
                remove(f)
        except FileExistsError:
            pass

    def generate_sudoku():
        # Generate Sudoku
        base = 3
        side = base * base

        # pattern for a baseline valid solution
        def pattern(r, c): return (base * (r % base) + r // base + c) % side

        def shuffle(s): return sample(s, len(s))

        r_base = range(base)
        rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
        cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
        nums = shuffle(range(1, base * base + 1))

        # produce board using randomized baseline pattern
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = squares * 3 // 4
        for p in sample(range(squares), empties):
            board[p // side][p % side] = 0

    def generate_frame(no):
        # import image
        sudoku_frame = Image.new("RGB", (1080, 1920))
        pixels = sudoku_frame.load()
        return sudoku_frame

    create_files()
    generate_sudoku()
    generate_frame(1).save("resources/frames/1.png")


if __name__ == '__main__':
    main()
