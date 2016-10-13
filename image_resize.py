import os
from PIL import Image
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to the image')
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--scale', type=float)
    parser.add_argument('--output')
    return parser.parse_args()


def resize_image(path_to_original, path_to_result, width, height):
    img = Image.open(initial_filepath)
    img_resized = img.resize((width, height), Image.ANTIALIAS)
    img.close()
    img_resized.save(path_to_result)


def get_final_filepath(path_to_original, path_to_result, width, height):
    full_name_initial = path_to_original.split('\\')[-1]
    extension = '.' + path_to_original.split('.')[-1]
    name_without_ext_initial = full_name_initial.replace(extension,'')
    if path_to_result is not None:
        path_to_final_dir = path_to_result 
    else:
        path_to_final_dir = ''
    final_name = '{}__{}x{}{}'.format(name_without_ext_initial, width, height, extension)
    final_path = os.path.join(path_to_final_dir, final_name)
    return final_path


def get_final_height_and_width(initial_filepath, user_width, user_height, scale):
    initial_image = Image.open(initial_filepath)
    init_width, init_height = initial_image.size
    initial_image.close()
    ratio = init_width / init_height
    if user_width is not None or user_height is not None:
        if user_width is not None and user_height is None:
            final_height = int(user_width / ratio)
        elif user_width is None and user_height is not None:
            print(user_width, user_height)
            final_width = int(user_height * ratio)
        elif user_width is not None and user_height is not None:
            final_width = user_width
            final_height = user_height
    else:
        final_width = int(init_width * scale)
        final_height = int(init_height * scale)
    return final_width, final_height


def check_errors_or_print_warning(initial_filepath, user_width, user_height, scale):
    initial_image = Image.open(initial_filepath)
    init_width, init_height = initial_image.size
    initial_image.close()
    if init_width / init_height != user_width / user_height:
        print('Warning, wrong ratio!')
    if (user_width is not None or user_height is not None) and scale is not None:
            print('ERROR: Enter pixel-size or scale. Not at the same time!!')
            exit(1)


if __name__ == '__main__':
    data_about_user_choise = parse_args()
    initial_filepath = data_about_user_choise.path
    user_width = data_about_user_choise.width
    user_height = data_about_user_choise.height
    scale = data_about_user_choise.scale
    dir_to_save_image = data_about_user_choise.output
    check_errors_or_print_warning(initial_filepath, user_width, user_height, scale)

    print(data_about_user_choise)
    final_width, final_height = get_final_height_and_width(initial_filepath, user_width, user_height, scale)

    filepath_to_resized = get_final_filepath(initial_filepath, dir_to_save_image, final_width, final_height)
    resize_image(initial_filepath, filepath_to_resized, final_width, final_height)
