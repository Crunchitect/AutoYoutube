from os import mkdir, rmdir, remove
from random import sample
from PIL import Image, ImageFont, ImageDraw
from glob import glob
from time import perf_counter
from copy import deepcopy
import cv2


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
            canvas = ImageDraw.Draw(im)
            canvas.line(((x1, y1), (x2, y2)), ImPen.Constants.color, ImPen.Constants.stroke)

        @staticmethod
        def impen_rect(im, x1, y1, x2, y2):
            ImPen.impen_line(im, x1, y1, x2, y1)
            ImPen.impen_line(im, x1, y2, x2, y2)
            ImPen.impen_line(im, x1, y1, x1, y2)
            ImPen.impen_line(im, x2, y1, x2, y2)

        @staticmethod
        def impen_grid(im, tl, tr, sz_tl, sz_tr):
            w, h = im.size
            for k in range(tl):
                for j in range(tr):
                    ImPen.impen_rect(im, int(w // 2 + (k - tl // 2 - 0.5) * sz_tl),
                                     int(h // 2 + (j - tr // 2 - 0.5) * sz_tr),
                                     int(w // 2 + (k - tl // 2 - 0.5) * sz_tl + sz_tl),
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

    class SudokuSolver:
        @staticmethod
        def sudoku(board):
            def solve(g, row, col, num):
                for x in range(9):
                    if g[row][x] == num:
                        return False

                for x in range(9):
                    if g[x][col] == num:
                        return False

                start_row = row - row % 3
                start_col = col - col % 3
                for k in range(3):
                    for j in range(3):
                        if g[k + start_row][j + start_col] == num:
                            return False
                return True

            def sudoku_solve(g, row, col, grid_history):
                if row == 9 - 1 and col == 9:
                    return True
                if col == 9:
                    row += 1
                    col = 0
                if g[row][col] > 0:
                    return sudoku_solve(g, row, col + 1, grid_history)
                for num in range(1, 9 + 1, 1):

                    if solve(g, row, col, num):

                        g[row][col] = num
                        grid_history.append(deepcopy(g))
                        if sudoku_solve(g, row, col + 1, grid_history):
                            return True
                    g[row][col] = 0
                return False

            board_prime = [deepcopy(board)]
            if sudoku_solve(board, 0, 0, board_prime):
                return board_prime
            else:
                assert False, "Solution does not exist :("

    def create_files():
        try:
            mkdir('resources')
        except FileExistsError:
            pass

        try:
            rmdir('resources/frames')
        except FileNotFoundError:
            pass
        except OSError:
            files = glob(__file__[::-1][__file__[::-1].index('\\')+1:][::-1] + '\\resources\\frames\\*')
            for f in files:
                remove(f)
            rmdir("resources/frames")

        try:
            mkdir('resources/frames')
        except FileExistsError:
            pass

        try:
            mkdir('resources/video')
        except FileExistsError:
            pass

    def generate_sudoku():
        base = 3
        side = base * base

        def pattern(rx, c): return (base * (rx % base) + rx // base + c) % side

        def shuffle(s): return sample(s, len(s))

        r_base = range(base)
        rows = [g * base + rx for g in shuffle(r_base) for rx in shuffle(r_base)]
        cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
        nums = shuffle(range(1, base * base + 1))

        board = [[nums[pattern(rx, c)] for c in cols] for rx in rows]

        squares = side * side
        empties = squares * 9 // 16
        for p in sample(range(squares), empties):
            board[p // side][p % side] = 0

        return board

    def generate_frame(b, b_prime, difficulty):
        w = 1080
        h = 1920
        sudoku_frame = Image.new("RGB", (w, h), color=(255, 255, 255))
        ImPen.set_stroke(10)
        ImPen.impen_grid(sudoku_frame, 9, 9, 100, 100)
        ImPen.set_col(0, 0, 0)
        ImPen.impen_text(sudoku_frame, 0, 0, "Sudoku Difficulty: ")
        if difficulty >= 400:
            ImPen.set_col(128, 0, 0)
            ImPen.impen_text(sudoku_frame, 700, 0, "Very Hard")
        elif difficulty >= 300:
            ImPen.set_col(255, 0, 0)
            ImPen.impen_text(sudoku_frame, 700, 0, "Hard")
        elif difficulty >= 200:
            ImPen.set_col(255, 255, 0)
            ImPen.impen_text(sudoku_frame, 700, 0, "Normal")
        elif difficulty >= 100:
            ImPen.set_col(128, 255, 0)
            ImPen.impen_text(sudoku_frame, 700, 0, "Easy")
        else:
            ImPen.set_col(0, 255, 0)
            ImPen.impen_text(sudoku_frame, 700, 0, "Very Easy")
        ImPen.set_col(0, 0, 0)
        for x in range(0, 9):
            for y in range(0, 9):
                ImPen.set_col(0, 0, 0)
                if b[y][x] == b_prime[y][x]:
                    ImPen.set_col(0, 0, 0)
                    ImPen.impen_text_grid(sudoku_frame, 9, 9, 100, 100, x, y, b[y][x] if b[y][x] != 0 else " ")
                elif b[y][x] > b_prime[y][x]:
                    ImPen.set_col(0, 255, 255)
                    ImPen.impen_text_grid(sudoku_frame, 9, 9, 100, 100, x, y, b[y][x] if b[y][x] != 0 else " ")
        return sudoku_frame

    def generate_video(n, fps):
        img_array = []
        size = ()
        for filename in glob(__file__[::-1][__file__[::-1].index('\\')+1:][::-1] + '\\resources\\frames\\*.png'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        out = cv2.VideoWriter(f'resources/video/vid_{n+1}.mp4', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

        for k in range(len(img_array)):
            out.write(img_array[k])
        out.release()
    fps = 30
    no_videos = int(input("How Many Videos would you like?: "))
    for m in range(no_videos):
        print(f"\u001b[33;1m ⓘ Creating Video #{m+1}/{no_videos} \u001b[0;0m" if verbose else "")
        print("\u001b[36m ⓘ Creating Files" if verbose else "")
        create_files()
        print("\u001b[36m ⓘ Generating Sudoku" if verbose else "")
        print("\u001b[36m ⓘ Creating Frames" if verbose else "")
        grid = generate_sudoku()
        store_grid = SudokuSolver.sudoku(grid)
        starter_frame = generate_frame(store_grid[0], store_grid[0], len(store_grid))
        ImPen.impen_text(starter_frame, 250, 200, "Sudoku of the Hour!")
        ImPen.impen_text(starter_frame, 250, 250, "Can you do it?")
        for i in range(fps * 5):
            seconds = i // fps
            seconds_true = i / fps
            ImPen.set_col(int(255 * seconds / 5), int(255 * (1 - seconds / 5)), 0)
            ImPen.impen_text(starter_frame, 300, 300, f"{round(5-seconds_true, 3)}")
            starter_frame.save(f"resources/frames/{i+1:04}.png")
            ImPen.set_col(255, 255, 255)
            ImPen.impen_text(starter_frame, 300, 300, f"{round(5-seconds_true, 3)}")

        for r, i in enumerate(store_grid):
            print(f"\t\u001b[36m ⓘ Creating Frame: #{r+1}/{len(store_grid)+30}" if verbose else "")
            if r == 0:
                frame = generate_frame(store_grid[r], store_grid[r], len(store_grid))
            else:
                frame = generate_frame(store_grid[r], store_grid[r - 1], len(store_grid))
            frame.save(f"resources/frames/{r+1+fps*5:04}.png")
        print(f"\t\u001b[36m ⓘ Creating Frame: #{len(store_grid) + 1}/{len(store_grid) + 1}" if verbose else "")
        frame = generate_frame(store_grid[len(store_grid)-1], store_grid[len(store_grid)-1], len(store_grid))
        for i in range(int(fps * 1.5)):
            frame.save(f"resources/frames/{len(store_grid)+1+i+fps*5:04}.png")
        print(f"\t\u001b[36m ⓘ Generating Video" if verbose else "")
        generate_video(m, fps=fps)


if __name__ == '__main__':
    start = perf_counter()
    main(verbose=True)
    print(f"\u001b[32;1m ✅ Done In: \u001b[38;5;166m{perf_counter() - start}\u001b[32;1ms  \u001b[0m")
