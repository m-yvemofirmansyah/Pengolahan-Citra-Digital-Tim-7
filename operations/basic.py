# operations/basic.py

import cv2
import numpy as np


def flip_horizontal(image):
    """
    Membalik citra secara horizontal (kiri ke kanan).
    """
    image_array = np.array(image)
    result = cv2.flip(image_array, 1)

    return result


def flip_vertical(image):
    """
    Membalik citra secara vertikal (atas ke bawah).
    """
    image_array = np.array(image)
    result = cv2.flip(image_array, 0)

    return result


def flip_both(image):
    """
    Membalik citra secara horizontal dan vertikal.
    """
    image_array = np.array(image)
    result = cv2.flip(image_array, -1)

    return result


def image_negative(image):
    """
    Menghasilkan citra negatif dengan membalik intensitas setiap piksel.

    Parameter:
        image: Citra Pillow dalam mode RGB atau grayscale.

    Return:
        Citra hasil dalam bentuk NumPy array.
    """
    image_array = np.asarray(image, dtype=np.uint8)
    result = 255 - image_array

    return result


# ==============================
# ARITHMETIC OPERATIONS
# ==============================

def add_scalar(image, value=50):
    """Penjumlahan citra dengan nilai skalar."""
    image_array = np.array(image)
    result = cv2.add(image_array, float(value))
    return result


def subtract_scalar(image, value=50):
    """Pengurangan citra dengan nilai skalar."""
    image_array = np.array(image)
    result = cv2.subtract(image_array, float(value))
    return result


def multiply_scalar(image, value=2):
    """Perkalian citra dengan nilai skalar."""
    image_array = np.array(image)
    result = cv2.multiply(image_array, float(value))
    return result


def divide_scalar(image, value=2):
    """Pembagian citra dengan nilai skalar."""
    if value == 0:
        raise ValueError("Nilai pembagi tidak boleh nol.")

    image_array = np.array(image)
    result = cv2.divide(image_array, float(value))
    return result


def add_images(image1, image2):
    """Penjumlahan dua citra."""
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2GRAY)
    image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2GRAY)

    image2 = cv2.resize(
        image2, (image1.shape[1], image1.shape[0])
    )

    return cv2.add(image1, image2)


def subtract_images(image1, image2):
    """Pengurangan dua citra."""
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2GRAY)
    image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2GRAY)

    image2 = cv2.resize(
        image2, (image1.shape[1], image1.shape[0])
    )

    return cv2.subtract(image1, image2)


def multiply_images(image1, image2):
    """Perkalian dua citra."""
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2GRAY)
    image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2GRAY)

    image2 = cv2.resize(
        image2, (image1.shape[1], image1.shape[0])
    )

    return cv2.multiply(image1, image2)


def divide_images(image1, image2):
    """Pembagian dua citra."""
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2GRAY)
    image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2GRAY)

    image2 = cv2.resize(
        image2, (image1.shape[1], image1.shape[0])
    )

    image2[image2 == 0] = 1

    return cv2.divide(image1, image2)

# ==============================
# COLOURING - GRAYSCALE
# ==============================

def grayscale_conversion(image):
    """
    Mengubah citra RGB menjadi grayscale.
    """
    image_array = np.array(image)
    result = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

    return result


def grayscale_gradient(width=256, height=256):
    result = np.linspace(
        0, 255,
        width * height,
        dtype=np.uint8
    ).reshape((height, width))

    return result

# ==============================
# COLOURING - BINARY
# ==============================

def binary_image(width=100, height=100):
    """
    Membuat citra biner berukuran 100x100
    dengan area putih di bagian tengah.
    """
    result = np.zeros((width, height), dtype=np.uint8)

    result[25:75, 25:75] = 255

    return result