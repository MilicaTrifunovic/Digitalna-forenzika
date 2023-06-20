KNIGHT_MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

from PIL import Image
from functions import _unmerge_rgb, _merge_rgb

class KnightTour:
    def __init__(self, frame_name):
        self.frame = Image.open(frame_name)
        self.frame_map = self.frame.load()
        self.board_size = self.frame.size[0]  # tuple
        self.lista = []
        self.scores = {}
        for i in range(self.frame.size[0]):
            for j in range(self.frame.size[1]):
                self.scores[(i, j)] = -1
        self.move = 0

    def print_list(self):
        size = len(self.lista)
        for i in range(20):
            print(self.lista[i], end="")
        print("\n")

    def stego_encode(self, start_pos, encode_img):
        x_pos,  y_pos = start_pos
        self.lista.append((x_pos, y_pos))
        img_map = encode_img.load()

        new_image = self.frame
        new_map = new_image.load()

        frame_rgb = self.frame_map[x_pos, y_pos]
        img_rgb = img_map[0, 0]
        new_map[x_pos, y_pos] = _merge_rgb(frame_rgb, img_rgb)
        self.scores[(x_pos, y_pos)] = 0

        for i in range(encode_img.size[0]):
            for j in range(encode_img.size[1]):
                self.move += 1
                next_pos = self.find_next_pos((x_pos, y_pos))
                if next_pos:
                    x_pos, y_pos = next_pos

                    frame_rgb = self.frame_map[x_pos, y_pos]
                    img_rgb = img_map[i, j]
                    new_map[x_pos, y_pos] = _merge_rgb(frame_rgb, img_rgb)

                    self.scores[(x_pos, y_pos)] = [self.move]
                    self.lista.append((x_pos, y_pos))
                else:
                    self.print_list()
        return new_image

    def stego_decode(self, start_pos, encode_img_h, encode_img_w):
        x_pos,  y_pos = start_pos
        self.lista.append((x_pos, y_pos))

        new_image = Image.new(self.frame.mode, (encode_img_w, encode_img_h))
        new_map = new_image.load()

        frame_rgb = self.frame_map[x_pos, y_pos]
        new_map[0, 0] = _unmerge_rgb(frame_rgb)
        self.scores[(x_pos, y_pos)] = 0

        for i in range(encode_img_w):
            for j in range(encode_img_h):
                self.move += 1
                next_pos = self.find_next_pos((x_pos, y_pos))
                if next_pos:
                    x_pos, y_pos = next_pos

                    frame_rgb = self.frame_map[x_pos, y_pos]
                    new_map[i, j] = _unmerge_rgb(frame_rgb)

                    self.scores[(x_pos, y_pos)] = [self.move]
                    self.lista.append((x_pos, y_pos))
                else:
                    self.print_list()
        return new_image

    def find_next_pos(self, current_pos):
        empty_neighbours = self.find_neighbours(current_pos)
        if len(empty_neighbours) is 0:
            return
        least_neighbour = 8
        least_neighbour_pos = ()
        for neighbour in empty_neighbours:
            neighbours_of_neighbour = self.find_neighbours(pos=neighbour)
            if len(neighbours_of_neighbour) <= least_neighbour:
                least_neighbour = len(neighbours_of_neighbour)
                least_neighbour_pos = neighbour
        return least_neighbour_pos

    def find_neighbours(self, pos):
        neighbours = []
        for dx, dy in KNIGHT_MOVES:
            x = pos[0] + dx
            y = pos[1] + dy
            if 0 <= x < self.board_size and 0 <= y < self.board_size and self.scores[(x, y)] is -1:
                neighbours.append((x, y))
        return neighbours
