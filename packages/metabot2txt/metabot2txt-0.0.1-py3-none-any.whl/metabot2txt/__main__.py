import re
from metabot2txt import display
from metabot2txt import convert


def main():
    name = input('enter the image or directory relative path: ')

    if re.search('\.png$', name):
        display.display_on_editor(convert.convert_img(name))
    else:
        display.display_list_on_editor(convert.convert_dir(name))


if __name__ == '__main__':
    main()
