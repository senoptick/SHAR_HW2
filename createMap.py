import random
import csv
from numpy import genfromtxt


class Map:
    def __init__(self, colors):
        self.d = {}
        self.data = genfromtxt('map.csv', delimiter=';', dtype=str)
        self.world_height, self.world_width = self.data.shape

        for color in list(colors):
            self.d[color] = []
        for x in range(self.world_height):
            for y in range(self.world_width):
                self.d[self.data[x, y]].append((x, y))

    def coordinates(self):
        return self.d

    def shape(self, n=1):
        return self.world_height*n, self.world_width*n


def create_csv(colors, size):
    colors = list(colors)
    with open('map.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["B" for _ in range(size[1] + 2)])
        for i in range(size[0]):
            filewriter.writerow(["B"] + [colors[random.randint(0, len(colors)-1)] for _ in range(size[1])] + ["B"])
        filewriter.writerow(["B" for _ in range(size[1] + 2)])

