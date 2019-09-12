from data_input import *


def test_congestion_data():
    data = congestion_data(2018, 3, 15)
    assert 900 == len(data)
    assert 0 == data[0]
    assert 0 == data[1]
    assert 0 == data[111]
    assert 1 == data[112]
    assert 1 == data[210]
    assert 0 == data[211]
    assert 0 == data[899]


def test_stack_lists():
    a = [[1, 2, 3],
         [4, 5, 6]]
    b = [[6, 5, 4],
         [3, 2, 1]]
    assert [[[1, 6], [2, 5], [3, 4]],
            [[4, 3], [5, 2], [6, 1]]] == list(map(stack_lists, a, b))


def test_sort_image_rows():
    img = [['c', '0', 0, 1, 0],
           ['b', 0, 1, '0', 0],
           ['d', 0, 0, 0, '1'],
           ['a', 1, '0', 0, 0]]
    sort_list = ['a', 'b', 'c', 'd']

    sorted_img = sort_image_rows(img, sort_list, int)

    assert [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]] == sorted_img


def test_traffic_image():
    # First 10 minutes
    img = traffic_image(2018, 3, 14, 10, 10)

    assert 50 == len(img)
    assert 10 == len(img[0])
    assert 2 == len(img[0][0])
    assert [[500, 106], [640, 108], [960, 109], [540, 107], [620, 108], [560, 112], [460, 114], [960, 104], [600, 108],
            [620, 117]] == img[0]
    assert [[160, 103], [120, 76], [240, 94], [200, 92], [240, 93], [60, 93], [240, 100], [200, 101], [240, 91],
            [160, 84]] == img[23]


def test_image_object_1():
    img = image_object(2018, 3, 14, 10, 10, 89)

    assert [[500, 106], [640, 108], [960, 109], [540, 107], [620, 108], [560, 112], [460, 114], [960, 104], [600, 108],
            [620, 117]] == img.image_data[0]
    assert [[160, 103], [120, 76], [240, 94], [200, 92], [240, 93], [60, 93], [240, 100], [200, 101], [240, 91],
            [160, 84]] == img.image_data[23]
    assert [2018, 3, 14, 10, 10, 89] == img.details
    assert True is img.is_congestion


def test_image_object_2():
    img = image_object(2018, 3, 14, 10, 10, 88)

    assert [[500, 106], [640, 108], [960, 109], [540, 107], [620, 108], [560, 112], [460, 114], [960, 104], [600, 108],
            [620, 117]] == img.image_data[0]
    assert [[160, 103], [120, 76], [240, 94], [200, 92], [240, 93], [60, 93], [240, 100], [200, 101], [240, 91],
            [160, 84]] == img.image_data[23]
    assert [2018, 3, 14, 10, 10, 88] == img.details
    assert False is img.is_congestion


def test_image_object_store():
    img = image_object(2018, 3, 14, 10, 10, 15)

    assert [[500, 106], [640, 108], [960, 109], [540, 107], [620, 108], [560, 112], [460, 114], [960, 104], [600, 108],
            [620, 117]] == img.image_data[0]
    assert [[160, 103], [120, 76], [240, 94], [200, 92], [240, 93], [60, 93], [240, 100], [200, 101], [240, 91],
            [160, 84]] == img.image_data[23]
    assert [2018, 3, 14, 10, 10, 15] == img.details
    assert False is img.is_congestion

    img.dump_pickled_image()

    img2 = ImageData.load_pickled_image(2018, 3, 14, 10, 10, 15)

    assert [[500, 106], [640, 108], [960, 109], [540, 107], [620, 108], [560, 112], [460, 114], [960, 104], [600, 108],
            [620, 117]] == img2.image_data[0]
    assert [[160, 103], [120, 76], [240, 94], [200, 92], [240, 93], [60, 93], [240, 100], [200, 101], [240, 91],
            [160, 84]] == img2.image_data[23]
    assert [2018, 3, 14, 10, 10, 15] == img2.details
    assert False is img2.is_congestion


def test_image_object_create():
    # New img requested and directly stored, improved test performance (all tests up until this one) from ~90 ms to
    # ~70 ms (approx 80%)
    img = ImageData.load_pickled_image(2018, 3, 14, 10, 10, 30, True)

    assert [[500, 106], [640, 108], [960, 109], [540, 107], [620, 108], [560, 112], [460, 114], [960, 104], [600, 108],
            [620, 117]] == img.image_data[0]
    assert [[160, 103], [120, 76], [240, 94], [200, 92], [240, 93], [60, 93], [240, 100], [200, 101], [240, 91],
            [160, 84]] == img.image_data[23]
    assert [2018, 3, 14, 10, 10, 30] == img.details
    assert False is img.is_congestion





