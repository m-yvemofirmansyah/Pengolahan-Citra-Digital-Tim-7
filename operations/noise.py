import numpy as np
import cv2

# GAUSSIAN NOISE
def gaussian_noise(image, mean=0, variance=25):
    """
    Menambahkan Gaussian Noise pada citra.

    mean     : Rata-rata distribusi noise.
    variance : Variansi noise.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    # Menghasilkan noise dengan distribusi Gaussian.
    noise = np.random.normal(
        mean,
        np.sqrt(variance),
        image_array.shape
    )

    # Menambahkan noise ke citra.
    result = image_array.astype(np.float32) + noise

    # Membatasi nilai piksel antara 0-255.
    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)

# RAYLEIGH NOISE
def rayleigh_noise(image, scale=10):
    """
    Menambahkan Rayleigh Noise pada citra.

    scale : Parameter skala distribusi Rayleigh.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    # Menghasilkan noise dengan distribusi Rayleigh.
    noise = np.random.rayleigh(
        scale,
        image_array.shape
    )

    # Mengurangi nilai rata-rata noise agar tidak
    # menghasilkan peningkatan kecerahan secara terus-menerus.
    noise = noise - (scale * np.sqrt(np.pi / 2))

    # Menambahkan noise ke citra.
    result = image_array.astype(np.float32) + noise

    # Membatasi nilai piksel antara 0-255.
    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)

# ERLANG (GAMMA) NOISE
def erlang_noise(image, shape=2, scale=10):
    image_array = np.asarray(image, dtype=np.uint8)

    if shape < 1 or int(shape) != shape:
        raise ValueError("Shape harus berupa bilangan bulat positif.")

    if scale <= 0:
        raise ValueError("Scale harus lebih besar dari 0.")

    noise = np.random.gamma(
        shape,
        scale,
        image_array.shape
    )
    noise = noise - (shape * scale)

    result = image_array.astype(np.float32) + noise

    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)

# EXPONENTIAL NOISE
def exponential_noise(image, scale=10):
    """
    Menambahkan Exponential Noise pada citra.

    scale : Parameter skala distribusi eksponensial.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    if scale <= 0:
        raise ValueError("Scale harus lebih besar dari 0.")

    # Menghasilkan noise dengan distribusi eksponensial.
    noise = np.random.exponential(
        scale,
        image_array.shape
    )

    # Mengurangi rata-rata noise agar tidak terus-menerus
    # meningkatkan kecerahan citra.
    noise = noise - scale

    # Menambahkan noise ke citra.
    result = image_array.astype(np.float32) + noise

    # Membatasi nilai piksel antara 0-255.
    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)

# UNIFORM NOISE
def uniform_noise(image, strength=20):
    """
    Menambahkan Uniform Noise pada citra.

    strength : Mengatur rentang intensitas noise.
    """
    image_array = np.asarray(image, dtype=np.uint8)

    if strength <= 0:
        raise ValueError("Strength harus lebih besar dari 0.")

    noise = np.random.uniform(
        -strength,
        strength,
        image_array.shape
    )

    result = image_array.astype(np.float32) + noise
    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)
 
# IMPULSE NOISE (SALT AND PEPPER)
def impulse_noise(image, amount=0.05, salt_vs_pepper=0.5):
    image_array = np.asarray(image, dtype=np.uint8).copy()

    if not 0 <= amount <= 1:
        raise ValueError("Amount harus berada di antara 0 dan 1.")

    if not 0 <= salt_vs_pepper <= 1:
        raise ValueError("Salt vs pepper harus berada di antara 0 dan 1.")

    random_values = np.random.random(image_array.shape[:2])

    pepper_threshold = amount * (1 - salt_vs_pepper)
    salt_threshold = amount

    result = image_array.copy()

    result[random_values < pepper_threshold] = 0
    result[
        (random_values >= pepper_threshold) &
        (random_values < salt_threshold)
    ] = 255

    return result