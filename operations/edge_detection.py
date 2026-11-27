import cv2
import numpy as np

# SOBEL EDGE DETECTION
def sobel_edge_detection(image):
    """
    Mendeteksi tepi citra menggunakan operator Sobel.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array

    sobel_x = cv2.Sobel(
        gray,
        cv2.CV_64F,
        1, 0,
        ksize=3
    )

    sobel_y = cv2.Sobel(
        gray,
        cv2.CV_64F,
        0, 1,
        ksize=3
    )

    magnitude = cv2.magnitude(
        sobel_x.astype(np.float32),
        sobel_y.astype(np.float32)
    )

    result = cv2.normalize(
        magnitude,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return result.astype(np.uint8)

# PREWITT EDGE DETECTION
def prewitt_edge_detection(image):
    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array

    kernel_x = np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ], dtype=np.float32)

    kernel_y = np.array([
        [1, 1, 1],
        [0, 0, 0],
        [-1, -1, -1]
    ], dtype=np.float32)

    prewitt_x = cv2.filter2D(
        gray,
        cv2.CV_32F,
        kernel_x
    )

    prewitt_y = cv2.filter2D(
        gray,
        cv2.CV_32F,
        kernel_y
    )

    magnitude = cv2.magnitude(
        prewitt_x,
        prewitt_y
    )

    result = cv2.normalize(
        magnitude,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return result.astype(np.uint8)

# ==================================================
# ROBERT EDGE DETECTION
# ==================================================
def robert_edge_detection(image):
    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array

    kernel_x = np.array([
        [1, 0],
        [0, -1]
    ], dtype=np.float32)

    kernel_y = np.array([
        [0, 1],
        [-1, 0]
    ], dtype=np.float32)

    robert_x = cv2.filter2D(
        gray,
        cv2.CV_32F,
        kernel_x
    )

    robert_y = cv2.filter2D(
        gray,
        cv2.CV_32F,
        kernel_y
    )

    magnitude = cv2.magnitude(
        robert_x,
        robert_y
    )

    result = cv2.normalize(
        magnitude,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return result.astype(np.uint8)

# LAPLACIAN EDGE DETECTION
def laplacian_edge_detection(image):
    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array

    laplacian = cv2.Laplacian(
        gray,
        cv2.CV_64F,
        ksize=3
    )

    result = np.abs(laplacian)

    result = cv2.normalize(
        result,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return result.astype(np.uint8)

# LAPLACIAN OF GAUSSIAN (LOG)
def log_edge_detection(image, kernel_size=5, sigma=1.0):
    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array

    blurred = cv2.GaussianBlur(
        gray,
        (kernel_size, kernel_size),
        sigma
    )

    laplacian = cv2.Laplacian(
        blurred,
        cv2.CV_64F
    )

    result = np.abs(laplacian)

    result = cv2.normalize(
        result,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return result.astype(np.uint8)

# CANNY EDGE DETECTION
def canny_edge_detection(image, threshold1=100, threshold2=200):
    image_array = np.asarray(image, dtype=np.uint8)

    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array

    result = cv2.Canny(
        gray,
        threshold1,
        threshold2
    )

    return result