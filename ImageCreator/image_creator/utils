import json
import re
from .image_elements import MyImage, Point, Polygon, Rectangle, Square, Circle


# converts string rgb to int rgb
def rgb_to_int(color):

    if color[0] == '(':
        color = tuple(list(map(int, re.findall('\d+', color))))

    return color


# converts color name to value in palette
# or eventually changes it to int rgb
def convert_color(color, palette):

    if color in palette:
        color = palette[color]
    else:
        color = rgb_to_int(color)

    return color


def parse_figures(figures, fg_color, palette):

    figures_list = []

    for figure in figures:

        if 'color' in figure:
            color = convert_color(figure['color'], palette)
        else:
            color = fg_color

        if figure['type'] == 'polygon':
            figures_list.append(Polygon(figure['points'], color))

        else:
            x = figure['x']
            y = figure['y']

            if figure['type'] == 'point':
                figures_list.append(Point(x, y, color))

            elif figure['type'] == 'rectangle':
                figures_list.append(Rectangle(x, y, figure['width'], figure['height'], color))

            elif figure['type'] == 'square':

                if 'size' in figure:
                    figures_list.append(Square(x, y, figure['size'], color))

                elif 'radius' in figure:
                    figures_list.append(Circle(x, y, figure['radius'], color))

    return figures_list


def load_file(file):

    try:
        file = json.load(open(file, "r"))
    except Exception as e:
        return False, e

    return True, file


def draw(file):

    palette = file['Palette']
    palette = {rgb_to_int(palette[color_key]) for color_key in palette}

    bg_color = file['Screen']['bg_color']
    bg_color = convert_color(bg_color, palette)

    fg_color = file['Screen']['fg_color']
    fg_color = convert_color(fg_color, palette)

    image = MyImage(file['Screen']['width'], file['Screen']['height'], bg_color)
    image.draw_image(parse_figures(file['Figures'], fg_color, palette))

    return image
