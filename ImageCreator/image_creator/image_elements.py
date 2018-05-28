from PIL import Image
from PIL import ImageDraw


class MyImage:

    def __init__(self, width, height, bg_color):
        self.image = Image.new('RGB', (width, height), color=bg_color)

    def draw_image(self, figures):
        draw = ImageDraw.Draw(self.image)
        for figure in figures:
            figure.draw_figure(draw)
        del draw

    def display(self):
        self.image.show()

    def save_to_file(self, file_name):
        self.image.save(file_name)


class Figure:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw_figure(self, draw):
        pass


class Point(Figure):

    def draw_figure(self, draw):
        draw.point([self.x, self.y], fill=self.color)


class Polygon(Figure):

    def __init__(self, points, color):
        super().__init__(points[0][0], points[0][1], color)
        self.points = [x for sublist in points for x in sublist]

    def draw_figure(self, draw):
        draw.polygon(self.points, fill=self.color)


class Circle(Figure):

    def __init__(self, x, y, radius, color):
        super().__init__(x, y, color)
        self.radius = radius

    def draw_figure(self, draw):
        x0 = self.x - self.radius
        y0 = self.y - self.radius
        draw.ellipse([x0, y0, x0 + self.radius, y0 + self.radius], fill=self.color)


class Rectangle(Figure):

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def draw_figure(self, draw):
        x0 = self.x - self.width/2
        y0 = self.y - self.height/2
        draw.rectangle([x0, y0, x0 + self.width, y0 + self.height], fill=self.color)


class Square(Rectangle):

    def __init__(self, x, y, width, color):
        super().__init__(x, y, width, width, color)
        self.width = width
