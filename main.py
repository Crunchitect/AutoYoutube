from os import mkdir, remove
from random import sample
from PIL import Image
from glob import glob


def main():

    class ImPen:
        class Constants:
            r, g, b = 0, 0, 0
            color = r, g, b
            stroke = 3

        @staticmethod
        def impen_plot(im, x, y):
            rad = ImPen.Constants.stroke
            for dy in range(-rad, rad):
                for dx in range(-rad, rad):
                    if (dx ** 2 + dy ** 2) <= rad ** 2:
                        try:
                            im.putpixel((int(x + dx), int(y + dy)), ImPen.Constants.color)
                        except IndexError:
                            pass

        @staticmethod
        def impen_line(im, x1, y1, x2, y2):
            dx = x2 - x1
            dy = y2 - y1
            for x in range(x1, x2+1):
                y = y1 + dy * (x - x1) / dx
                ImPen.impen_plot(im, int(x), int(y))

        @staticmethod
        def set_r(val): ImPen.Constants.r = val
        @staticmethod
        def set_g(val): ImPen.Constants.g = val
        @staticmethod
        def set_b(val): ImPen.Constants.b = val

        @staticmethod
        def set_col(val, g, b):
            if isinstance(val, tuple):
                ImPen.Constants.color = val
            else:
                ImPen.Constants.color = (val, g, b)

        @staticmethod
        def set_stroke(val): ImPen.Constants.stroke = val

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
        sudoku_frame = Image.new("RGB", (1080, 1920), color=(255, 255, 255))
        ImPen.impen_line(sudoku_frame, 0, 0, 1080, 1920)
        return sudoku_frame

    create_files()
    generate_sudoku()
    generate_frame(1).save("resources/frames/1.png")


if __name__ == '__main__':
    main()
