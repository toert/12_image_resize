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


def open_image(filepath_to_image):
    return Image.open(filepath_to_image)


def save_image(image_to_save, path_to_save):
    image_to_save.save(path_to_save)


def resize_image(initial_image, width, height):
    img_resized = initial_image.resize((width, height), Image.ANTIALIAS)
    return img_resized


def get_final_filepath(path_to_original, path_to_final_dir, width, height):
    if path_to_final_dir is None:
        path_to_final_dir = ''
    full_name_initial = os.path.basename(path_to_original)
    extension = os.path.splitext(path_to_original)[1]
    name_without_ext_initial = full_name_initial.replace(extension,'')
    final_name = '{}__{}x{}{}'.format(name_without_ext_initial, width,\
                                      height, extension)
    final_path = os.path.join(path_to_final_dir, final_name)
    return final_path


def get_final_height_and_width(init_width, init_height, user_width,\
                               user_height, scale):
    ratio = init_width / init_height
    if user_width is not None or user_height is not None:
        if user_width is not None and user_height is None:
            final_width = user_width
            final_height = int(user_width / ratio)
        elif user_width is None and user_height is not None:
            final_height = user_height
            final_width = int(user_height * ratio)
        elif user_width is not None and user_height is not None:
            final_width = user_width
            final_height = user_height
        else:
            final_width = int(init_width)
            final_height = int(init_height)
    else:
        final_width = int(init_width * scale)
        final_height = int(init_height * scale)
    return final_width, final_height


def check_errors(initial_image, user_width, user_height, scale):
    """
    return 1 = don't enter pixel-size and scale at the same time
    return 2 = wrong ratio. the image will be compressed on one of axe
    """
    if (user_width is not None or user_height is not None) \
            and scale is not None:
            return int(1)
    if user_width is not None and user_height is not None:
        init_width, init_height = get_size(initial_image)
        if init_width / init_height != user_width / user_height:
            return int(2)


def handle_errors(image, error_code):
    if error_code == 1:
        print('ERROR: Enter pixel-size or scale. Not at the same time!!')
        image.close()
        exit(1)
    if error_code == 2:
        print('Warning, wrong ratio!')


def get_size(initial_image):
    init_width, init_height = initial_image.size
    return init_width, init_height


if __name__ == '__main__':
    data_about_user_choise = parse_args()
    initial_filepath = data_about_user_choise.path
    user_width = data_about_user_choise.width
    user_height = data_about_user_choise.height
    scale = data_about_user_choise.scale
    dir_to_save_image = data_about_user_choise.output

    init_img = open_image(initial_filepath)
    init_width, init_height = get_size(init_img)
    handle_errors(init_img, check_errors(init_img, user_width,\
                                         user_height, scale))

    final_width, final_height = get_final_height_and_width\
        (init_width, init_height, user_width, user_height, scale)

    filepath_to_resized = get_final_filepath(initial_filepath, \
                                 dir_to_save_image, final_width, final_height)
    save_image(resize_image(init_img, final_width, final_height), \
               filepath_to_resized)
    init_img.close()
    print('Done!')
