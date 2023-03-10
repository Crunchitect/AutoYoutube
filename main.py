from os import mkdir, remove
from random import sample
from PIL import Image, ImageFont, ImageDraw
from glob import glob
from time import perf_counter


def main(*, verbose=False):
    if verbose:
        print("\u001b[36m ⓘ Starting ImPen")

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
            if x1 > x2:
                x2, x1 = x1, x2
            if y1 > y2:
                y2, y1 = y1, y2
            dx = x2 - x1
            dy = y2 - y1
            for x in range(x1, x2+1):
                y = y1 + dy * (x - x1) / dx if dx != 0 else -1
                ImPen.impen_plot(im, int(x), int(y))
            for y in range(y1, y2+1):
                x = x1 + dx * (y - y1) / dy if dy != 0 else -1
                ImPen.impen_plot(im, int(x), int(y))

        @staticmethod
        def impen_rect(im, x1, y1, x2, y2):
            ImPen.impen_line(im, x1, y1, x2, y1)
            ImPen.impen_line(im, x1, y2, x2, y2)
            ImPen.impen_line(im, x1, y1, x1, y2)
            ImPen.impen_line(im, x2, y1, x2, y2)

        @staticmethod
        def impen_grid(im, tl, tr, sz_tl, sz_tr):
            w, h = im.size
            for i in range(tl):
                for j in range(tr):
                    ImPen.impen_rect(im, int(w // 2 + (i - tl // 2 - 0.5) * sz_tl),
                                     int(h // 2 + (j - tr // 2 - 0.5) * sz_tr),
                                     int(w // 2 + (i - tl // 2 - 0.5) * sz_tl + sz_tl),
                                     int(h // 2 + (j - tr // 2 - 0.5) * sz_tr + sz_tr))

        @staticmethod
        def impen_text(im, x, y, text):
            font = ImageFont.truetype("assets/font.ttf", 60)
            canvas = ImageDraw.Draw(im)

            canvas.text((x, y), text, font=font, fill=ImPen.Constants.color)

        @staticmethod
        def impen_text_grid(im, tl, tr, sz_tl, sz_tr, tx, ty, text):
            text = str(text)
            w, h = im.size
            ImPen.impen_text(im,
                             int(w // 2 + (tx - tl // 2 - 0.25) * sz_tl),
                             int(h // 2 + (ty - tr // 2 - 0.5) * sz_tr), text)

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

    if verbose:
        print("\u001b[36m ⓘ Defining Functions")

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

        return board

    def generate_frame(board):
        # import image
        w = 1080
        h = 1920
        sudoku_frame = Image.new("RGB", (w, h), color=(255, 255, 255))
        ImPen.set_stroke(5)
        ImPen.impen_grid(sudoku_frame, 9, 9, 100, 100)
        ImPen.impen_text(sudoku_frame, 0, 0, "Easy Sudoku")
        for x in range(0, 9):
            for y in range(0, 9):
                ImPen.impen_text_grid(sudoku_frame, 9, 9, 100, 100, x, y, board[y][x] if board[y][x] != 0 else " ")
        return sudoku_frame

    print("\u001b[36m ⓘ Creating Files" if verbose else "")
    create_files()
    print("\u001b[36m ⓘ Generating Sudoku" if verbose else "")
    print("\u001b[36m ⓘ Creating Frames" if verbose else "")
    generate_frame(generate_sudoku()).save("resources/frames/1.png")


if __name__ == '__main__':
    start = perf_counter()
    main(verbose=True)
    print(f"\u001b[32;1m ✅ Done In: \u001b[38;5;166m{perf_counter() - start}\u001b[32;1ms  \u001b[0m")
