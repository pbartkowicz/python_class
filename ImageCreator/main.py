import sys
import image_creator


def run(file, output_file):

    val, file = image_creator.load_file(file)

    if not val:
        print(file)
        sys.exit()

    image = image_creator.draw(file)

    if output_file == "":
        image.display()
    else:
        image.save_to_file(output_file)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        run(sys.argv[1], "")

    elif len(sys.argv) == 4 and (sys.argv[2] == "-o" or sys.argv[2] == "--output"):
        run(sys.argv[1], sys.argv[3])

    else:
        print("Invalid arguments")
        print("In order to display: main.py [file.json]")
        print("In order to save: main.py [file.json] [-o | --output] [output.png]")
