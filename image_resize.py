import os
from PIL import Image


def get_enter_data(): 
    user_choise = -1
    orig_path = ''
    width = 0
    height = 0
    scale = 1
    output_path = ''
    while True:  #do {} while()
        print('Choose what you want to change:')
        print('{}: {}'.format('1. Filepath to original image (necessary)',\
            orig_path))
        print('{}: {}'.format('2. Width of result image', width))
        print('{}: {}'.format('3. Height of result image', height))
        print('{}: {}'.format('4. How much multiply size?', scale))
        print('{}: {}'.format('5. Filepath to result image', output_path))
        print('6. That\' all, i want to execute script')
        user_choise = int(input('Your choise:'))
        if user_choise == 1:
            orig_path = input('Filepath to original image: ')
        elif user_choise == 2:
            width = int(input('Width of result image: '))
        elif user_choise == 3:
            height = int(input('Height of result image: '))
        elif user_choise == 4:
            scale = int(input('How much multiply size: '))
        elif user_choise == 5:
            output_path = input('Filepath to result image: ')
        os.system('cls')
        if (width or height) and scale != 1:
            print('ERROR: Enter pixel-size or scale. Not at the same time!!')
            width = 0
            height = 0
            scale = 1
        else:
            if user_choise == 6:
                if orig_path:
                    break
                print('ERROR: Enter initial filepath!')
    return orig_path, width, height, scale, output_path


def resize_image(path_to_original, path_to_result, width, height):
    img = Image.open(initial_filepath)
    img_resized = img.resize((width, height), Image.ANTIALIAS)
    img.close()
    img_resized.save(path_to_result)


def get_final_filepath(path_to_original, path_to_result, width, height):
    full_name_initial = path_to_original.split('\\')[-1]
    extension = '.' + path_to_original.split('.')[-1]
    name_without_ext_initial = full_name_initial.replace(extension,'')
    if path_to_result:
        path_to_final_dir = path_to_result + '\\'
    else:
        path_to_final_dir = path_to_result
    final_path = '{}{}__{}x{}{}'.format(path_to_final_dir, \
        name_without_ext_initial, width, height, extension)
    return final_path


if __name__ == '__main__':
    data_about_user_choise = get_enter_data()
    
    initial_filepath = data_about_user_choise[0]
    final_width = data_about_user_choise[1]
    final_height = data_about_user_choise[2]
    dir_to_save_image = data_about_user_choise[4]

    img = Image.open(initial_filepath)
    init_width, init_height = img.size
    img.close()
    ratio = init_width / init_height
    if final_width > 0 or final_height > 0:
        if final_width > 0 and final_height == 0:
            final_height = int(final_width / ratio)
        elif final_width == 0 or final_height > 0:
            final_width = int(final_height * ratio)
        elif final_width > 0 and final_height > 0:
            final_ratio = final_width / final_height
            if final_ratio != ratio:
                print('Warning, wrong ratio!')
    else:
        scale = data_about_user_choise[3]
        final_width = int(init_width * scale)
        final_height = int(init_height * scale)

    filepath_to_resized = get_final_filepath(initial_filepath, \
        dir_to_save_image, final_width, final_height)
    resize_image(initial_filepath, filepath_to_resized, final_width, \
        final_height)
    
