from PIL import Image
import os
import sys
try:
    import progressbar
except Exception:
    pass


if __name__ == '__main__':
    os.system("mode con cols=110 lines=30")
    print(' CROPPER '.center(110, '-'))
    print(
'''
Cropper — разрезатель изображения на части, равные по ширине и высоте, с одинаковым отступом между ними.
Убедитесь, что вокруг изображения нет никаких артефактов, а отступ между частями меньше самих частей.
Все разрезанные части будут в папке result в том же формате, что и исходное изображение.
'''
    )
    print('-' * 110)

    fname = input('Введите имя разрезаемого файла: ')
    try:
        im = Image.open(fname)
    except Exception:
        print('Файла не существует.')
        sys.exit()
    size = im.size
    crop_x, crop_y = tuple(map(int, input('Задайте размер частей через пробел: ').split()))
    shift = int(input('Задайте отступ между частями: '))

    amount = len(range(0, size[0], crop_x + shift)) * len(range(0, size[1], crop_y + shift))
    if 'progressbar' in dir():
        bar = progressbar.ProgressBar(maxval=amount, widgets=[
            'Прогресс: ',
            progressbar.Bar(left='[', marker='=', right='] '),
            progressbar.SimpleProgress(' из ') 
        ])
    else:
        bar = None

    deleted = True
    if os.path.isdir('result'):
        print('\nПапка result уже существует. Удалить текущую result?')
        deleted = not bool(os.system('rmdir result /S'))
    print()
    if deleted:
        os.mkdir('result')

    count = 0
    if bar:
        bar.start()
    for x in range(0, size[0], crop_x + shift):
        for y in range(0, size[1], crop_y + shift):
            count += 1

            temp_im = im.crop((x, y, x + crop_x, y + crop_y))
            temp_im.save('result/{}-{}-{}.{}'.format(fname.split('.')
                                                     [0], x // crop_x, y // crop_y, fname.split('.')[1]))

            if bar:
                bar.update(count)
            else:
                print('Нарезано картинок {} из {}'.format(count, amount), end='\r')
                
    if bar:
        bar.finish()
    else:
        print('Нарезано картинок {0} из {0}\n\nЗадача завершена!'.format(amount))
    print('-' * 110)
    input('Нажмите любую клавишу...')
