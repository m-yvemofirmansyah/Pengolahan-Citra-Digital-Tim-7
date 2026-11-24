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

# ==============================
# COLOURING - RGB ADJUSTMENT
# ==============================

def rgb_adjustment(image, red=0, green=0, blue=0):
    """
    Mengatur intensitas kanal Red, Green, dan Blue
    pada citra RGB.

    Parameter:
        image : Citra Pillow RGB.
        red   : Perubahan intensitas kanal merah (-255 hingga 255).
        green : Perubahan intensitas kanal hijau (-255 hingga 255).
        blue  : Perubahan intensitas kanal biru (-255 hingga 255).

    Return:
        Citra hasil dalam bentuk NumPy array.
    """

    image_array = np.asarray(image.convert("RGB"), dtype=np.int16)

    result = image_array.copy()

    result[:, :, 0] += int(red)
    result[:, :, 1] += int(green)
    result[:, :, 2] += int(blue)

    result = np.clip(result, 0, 255).astype(np.uint8)

    return result

# psudo
def pseudo_color(image, colormap="JET"):
    """
    Mengubah citra grayscale menjadi citra berwarna
    menggunakan teknik pseudocolor.
    """

    image_array = np.array(image)

    # Konversi citra RGB menjadi grayscale
    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array.astype(np.uint8)

    # Pilihan colormap
    colormaps = {
        "JET": cv2.COLORMAP_JET,
        "HOT": cv2.COLORMAP_HOT,
        "OCEAN": cv2.COLORMAP_OCEAN,
        "RAINBOW": cv2.COLORMAP_RAINBOW
    }

    if colormap not in colormaps:
        raise ValueError("Colormap tidak tersedia.")

    # Terapkan colormap
    result = cv2.applyColorMap(gray, colormaps[colormap])

    # Konversi BGR ke RGB agar sesuai dengan PIL/Tkinter
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    return result

# hsv
def hsv_conversion(image, channel="HSV"):
    """
    Mengonversi citra RGB ke ruang warna HSV
    dan menampilkan kanal HSV yang dipilih.
    """

    image_array = np.array(image, dtype=np.uint8)

    # Konversi RGB ke HSV
    hsv_image = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2HSV
    )

    if channel == "HSV":
        # Kembalikan ke RGB untuk tampilan warna normal
        result = cv2.cvtColor(
            hsv_image,
            cv2.COLOR_HSV2RGB
        )

    elif channel == "H":
        result = hsv_image[:, :, 0]

    elif channel == "S":
        result = hsv_image[:, :, 1]

    elif channel == "V":
        result = hsv_image[:, :, 2]

    else:
        raise ValueError("Kanal HSV tidak valid.")

    return result

# Boolean


def _prepare_boolean_image(image):
    """
    Mengubah citra PIL menjadi array grayscale uint8
    untuk operasi Boolean.
    """
    image_array = np.array(image)

    if len(image_array.shape) == 3:
        image_array = cv2.cvtColor(
            image_array,
            cv2.COLOR_RGB2GRAY
        )

    return image_array.astype(np.uint8)


def boolean_not(image):
    """Operasi Boolean NOT pada satu citra."""
    image_array = _prepare_boolean_image(image)

    return cv2.bitwise_not(image_array)


def boolean_and(image1, image2):
    """Operasi Boolean AND pada dua citra."""
    img1 = _prepare_boolean_image(image1)
    img2 = _prepare_boolean_image(image2)

    img2 = cv2.resize(
        img2,
        (img1.shape[1], img1.shape[0]),
        interpolation=cv2.INTER_NEAREST
    )

    return cv2.bitwise_and(img1, img2)


def boolean_or(image1, image2):
    """Operasi Boolean OR pada dua citra."""
    img1 = _prepare_boolean_image(image1)
    img2 = _prepare_boolean_image(image2)

    img2 = cv2.resize(
        img2,
        (img1.shape[1], img1.shape[0]),
        interpolation=cv2.INTER_NEAREST
    )

    return cv2.bitwise_or(img1, img2)


def boolean_xor(image1, image2):
    """Operasi Boolean XOR pada dua citra."""
    img1 = _prepare_boolean_image(image1)
    img2 = _prepare_boolean_image(image2)

    img2 = cv2.resize(
        img2,
        (img1.shape[1], img1.shape[0]),
        interpolation=cv2.INTER_NEAREST
    )

    return cv2.bitwise_xor(img1, img2)

# Geometri
def translation(image, tx=50, ty=30):
    """
    Menggeser citra secara horizontal dan vertikal.
    tx: pergeseran sumbu X.
    ty: pergeseran sumbu Y.
    """
    image_array = np.asarray(image, dtype=np.uint8)

    height, width = image_array.shape[:2]

    matrix = np.float32([
        [1, 0, tx],
        [0, 1, ty]
    ])

    result = cv2.warpAffine(
        image_array,
        matrix,
        (width, height)
    )

    return result


def rotation(image, angle=70, scale=1.0):
    """
    Memutar citra berdasarkan sudut tertentu.
    Titik pusat rotasi berada di tengah citra.
    """
    image_array = np.asarray(image, dtype=np.uint8)

    height, width = image_array.shape[:2]

    center = (width // 2, height // 2)

    rotation_matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        scale
    )

    result = cv2.warpAffine(
        image_array,
        rotation_matrix,
        (width, height)
    )

    return result


def zooming(image, scale_x=3.0, scale_y=2.0):
    """
    Memperbesar atau memperkecil citra berdasarkan
    faktor skala sumbu X dan Y.
    """
    image_array = np.asarray(image, dtype=np.uint8)

    if scale_x <= 0 or scale_y <= 0:
        raise ValueError("Faktor skala harus lebih besar dari 0.")

    height, width = image_array.shape[:2]

    new_width = max(1, int(width * scale_x))
    new_height = max(1, int(height * scale_y))

    result = cv2.resize(
        image_array,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR
    )

    return result


def cropping(image, x1=25, y1=25, x2=75, y2=75):
    """
    Memotong area citra berdasarkan persentase koordinat.
    Nilai koordinat berada pada rentang 0 sampai 100.
    """
    image_array = np.asarray(image, dtype=np.uint8)

    height, width = image_array.shape[:2]

    if not (0 <= x1 < x2 <= 100):
        raise ValueError(
            "Koordinat X harus memenuhi 0 <= X1 < X2 <= 100."
        )

    if not (0 <= y1 < y2 <= 100):
        raise ValueError(
            "Koordinat Y harus memenuhi 0 <= Y1 < Y2 <= 100."
        )

    start_x = int(width * x1 / 100)
    end_x = int(width * x2 / 100)

    start_y = int(height * y1 / 100)
    end_y = int(height * y2 / 100)

    result = image_array[start_y:end_y, start_x:end_x]

    return result

# Tresholding

def thresholding(image, threshold_value=127):
    """
    Mengubah citra grayscale menjadi citra biner
    berdasarkan nilai threshold.
    """
    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(
            image_array,
            cv2.COLOR_RGB2GRAY
        )
    else:
        gray = image_array

    _, result = cv2.threshold(
        gray,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    return result

# Convolution
def convolution(image, kernel_type="sharpen"):
    image_array = np.asarray(image, dtype=np.uint8)

    kernels = {
        "identity": np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], dtype=np.float32),

        "blur": np.ones((3, 3), dtype=np.float32) / 9,

        "sharpen": np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32),

        "edge": np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ], dtype=np.float32),

        "emboss": np.array([
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
        ], dtype=np.float32)
    }

    if kernel_type not in kernels:
        raise ValueError("Jenis kernel tidak tersedia.")

    result = cv2.filter2D(
        image_array,
        -1,
        kernels[kernel_type]
    )

    return result

# Fourier
def fourier_transform(image):
    image_array = np.asarray(image, dtype=np.uint8)

    # Mengubah citra RGB menjadi grayscale
    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array

    # Mengubah citra menjadi format float32
    gray_float = np.float32(gray)

    # Melakukan Discrete Fourier Transform
    dft = cv2.dft(
        gray_float,
        flags=cv2.DFT_COMPLEX_OUTPUT
    )

    # Memindahkan frekuensi rendah ke bagian tengah
    dft_shift = np.fft.fftshift(dft)

    # Menghitung magnitude spektrum
    magnitude = cv2.magnitude(
        dft_shift[:, :, 0],
        dft_shift[:, :, 1]
    )

    # Menggunakan log scale agar spektrum terlihat
    magnitude_spectrum = 20 * np.log(magnitude + 1)

    # Normalisasi hasil ke rentang 0-255
    result = cv2.normalize(
        magnitude_spectrum,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return np.uint8(result) 

# cmy
def cmy_conversion(image, channel="C"):
    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) != 3:
        image_array = cv2.cvtColor(
            image_array,
            cv2.COLOR_GRAY2RGB
        )

    # Normalisasi nilai RGB
    rgb = image_array.astype(np.float32) / 255.0

    # Konversi RGB ke CMY
    cmy = 1.0 - rgb

    # Memisahkan kanal CMY
    cyan = cmy[:, :, 0]
    magenta = cmy[:, :, 1]
    yellow = cmy[:, :, 2]

    if channel == "C":
        result = cyan
    elif channel == "M":
        result = magenta
    elif channel == "Y":
        result = yellow
    else:
        raise ValueError("Kanal CMY tidak tersedia.")

    return np.uint8(result * 255)

# yuv
def yuv_conversion(image, channel="Y"):
    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) != 3:
        image_array = cv2.cvtColor(
            image_array,
            cv2.COLOR_GRAY2RGB
        )

    rgb = image_array.astype(np.float32)

    # Konversi RGB ke YUV (BT.601)
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]

    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = -0.14713 * r - 0.28886 * g + 0.436 * b
    v = 0.615 * r - 0.51499 * g - 0.10001 * b

    if channel == "Y":
        result = y
    elif channel == "U":
        result = u + 128
    elif channel == "V":
        result = v + 128
    else:
        raise ValueError("Kanal YUV tidak tersedia.")

    return np.uint8(np.clip(result, 0, 255))