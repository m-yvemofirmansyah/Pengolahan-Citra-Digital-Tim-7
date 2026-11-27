import numpy as np
import cv2

def brightness_adjustment(image, value=0):
    """
    Mengatur tingkat kecerahan citra.

    Parameter:
    image : Citra input.
    value : Nilai perubahan brightness.
            Positif = lebih terang.
            Negatif = lebih gelap.
            Nol = tidak ada perubahan.

    Return:
    Citra hasil penyesuaian brightness.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    # Konversi ke integer agar operasi penjumlahan
    # tidak mengalami overflow pada tipe uint8.
    image_int = image_array.astype(np.int16)

    # Tambahkan nilai brightness ke setiap piksel.
    result = image_int + value

    # Batasi nilai piksel antara 0 sampai 255.
    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)

# contrast
def contrast_adjustment(image, factor=1.0):
    """
    Mengatur tingkat kontras citra.

    Parameter:
    image  : Citra input.
    factor : Faktor pengali kontras.
             < 1.0 = kontras berkurang.
             1.0   = tidak ada perubahan.
             > 1.0 = kontras meningkat.

    Return:
    Citra hasil penyesuaian contrast.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    # Konversi ke float agar perhitungan lebih akurat.
    image_float = image_array.astype(np.float32)

    # Sesuaikan kontras berdasarkan titik tengah 128.
    result = 128 + factor * (image_float - 128)

    # Batasi nilai piksel antara 0 sampai 255.
    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)

# histogram equalization
def histogram_equalization(image):
    """
    Meningkatkan kontras citra menggunakan Histogram Equalization.

    Parameter:
    image : Citra input RGB atau grayscale.

    Return:
    Citra hasil Histogram Equalization.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    # Jika citra grayscale, langsung lakukan equalization.
    if len(image_array.shape) == 2:
        result = cv2.equalizeHist(image_array)

    # Jika citra berwarna, lakukan equalization pada kanal luminance.
    else:
        ycrcb = cv2.cvtColor(image_array, cv2.COLOR_RGB2YCrCb)

        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])

        result = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)

    return result


# ==================================================
# LOWPASS FILTERING (SPATIAL DOMAIN)
# ==================================================

def lowpass_filtering(image, kernel_size=3):
    """
    Menghaluskan citra menggunakan Lowpass Filtering
    dengan metode Mean/Average Filter.

    Parameter:
    image       : Citra input.
    kernel_size : Ukuran kernel filter (harus ganjil).

    Return:
    Citra hasil Lowpass Filtering.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    # Pastikan ukuran kernel ganjil.
    if kernel_size % 2 == 0:
        raise ValueError("Ukuran kernel harus ganjil.")

    # Terapkan Mean/Average Filter.
    result = cv2.blur(
        image_array,
        (kernel_size, kernel_size)
    )

    return result

# MEDIAN FILTERING (SPATIAL DOMAIN)

def median_filtering(image, kernel_size=3):
    """
    Mengurangi noise pada citra menggunakan Median Filtering.

    Parameter:
    image       : Citra input.
    kernel_size : Ukuran kernel filter (harus ganjil).

    Return:
    Citra hasil Median Filtering.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    # Pastikan ukuran kernel ganjil dan minimal 3.
    if kernel_size < 3 or kernel_size % 2 == 0:
        raise ValueError("Ukuran kernel harus ganjil dan minimal 3.")

    # Terapkan Median Filter.
    result = cv2.medianBlur(
        image_array,
        kernel_size
    )

    return result


# ==================================================
# IDEAL HIGH PASS FILTER (IHPF) - FREQUENCY DOMAIN
# ==================================================

def ideal_highpass_filtering(image, cutoff=30, strength=1.0):
    """
    Mempertajam citra menggunakan Ideal High Pass Filter.

    Parameter:
    image    : Citra input RGB atau grayscale.
    cutoff   : Jarak cutoff frequency dari pusat spektrum.
    strength : Kekuatan penajaman.

    Return:
    Citra hasil IHPF.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    rows, cols = image_array.shape[:2]

    # Membuat koordinat frekuensi dengan pusat di tengah.
    u = np.arange(rows) - rows // 2
    v = np.arange(cols) - cols // 2
    U, V = np.meshgrid(v, u)

    # Menghitung jarak setiap frekuensi dari pusat.
    distance = np.sqrt(U ** 2 + V ** 2)

    # Membuat mask Ideal High Pass Filter.
    mask = np.ones((rows, cols), dtype=np.float32)
    mask[distance <= cutoff] = 0

    # Memproses citra grayscale.
    if image_array.ndim == 2:
        channels = [image_array]
    else:
        channels = [
            image_array[:, :, i]
            for i in range(image_array.shape[2])
        ]

    results = []

    for channel in channels:
        # Transformasi Fourier.
        spectrum = np.fft.fft2(channel)
        spectrum_shift = np.fft.fftshift(spectrum)

        # Menerapkan filter frekuensi tinggi.
        filtered_spectrum = spectrum_shift * mask

        # Transformasi Fourier balik.
        high_frequency = np.fft.ifft2(
            np.fft.ifftshift(filtered_spectrum)
        ).real

        # Menambahkan detail frekuensi tinggi ke citra asli.
        sharpened = channel.astype(np.float32) + (
            strength * high_frequency
        )

        results.append(
            np.clip(sharpened, 0, 255).astype(np.uint8)
        )

    if image_array.ndim == 2:
        return results[0]

    return np.stack(results, axis=2)


# ==================================================
# BUTTERWORTH HIGH PASS FILTER (BHPF) - FREQUENCY DOMAIN
# ==================================================

def butterworth_highpass_filtering(
    image,
    cutoff=30,
    order=2,
    strength=1.0
):
    """
    Mempertajam citra menggunakan Butterworth High Pass Filter.

    Parameter:
    image    : Citra input RGB atau grayscale.
    cutoff   : Jarak cutoff frequency dari pusat spektrum.
    order    : Orde filter Butterworth.
    strength : Kekuatan penajaman.

    Return:
    Citra hasil BHPF.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    if cutoff <= 0:
        raise ValueError("Cutoff frequency harus lebih besar dari 0.")

    if order < 1:
        raise ValueError("Order filter minimal 1.")

    rows, cols = image_array.shape[:2]

    # Membuat koordinat frekuensi dengan pusat di tengah.
    u = np.arange(rows) - rows // 2
    v = np.arange(cols) - cols // 2
    U, V = np.meshgrid(v, u)

    # Menghitung jarak setiap frekuensi dari pusat.
    distance = np.sqrt(U ** 2 + V ** 2)

    # Menghindari pembagian dengan nol.
    distance = np.maximum(distance, 1e-6)

    # Membuat mask Butterworth High Pass Filter.
    mask = 1 / (
        1 + (cutoff / distance) ** (2 * order)
    )

    # Memproses citra grayscale.
    if image_array.ndim == 2:
        channels = [image_array]
    else:
        channels = [
            image_array[:, :, i]
            for i in range(image_array.shape[2])
        ]

    results = []

    for channel in channels:
        # Transformasi Fourier.
        spectrum = np.fft.fft2(channel)
        spectrum_shift = np.fft.fftshift(spectrum)

        # Menerapkan filter frekuensi tinggi.
        filtered_spectrum = spectrum_shift * mask

        # Transformasi Fourier balik.
        high_frequency = np.fft.ifft2(
            np.fft.ifftshift(filtered_spectrum)
        ).real

        # Menambahkan detail frekuensi tinggi ke citra asli.
        sharpened = channel.astype(np.float32) + (
            strength * high_frequency
        )

        results.append(
            np.clip(sharpened, 0, 255).astype(np.uint8)
        )

    if image_array.ndim == 2:
        return results[0]

    return np.stack(results, axis=2)


# ==================================================
# IDEAL HIGH PASS FILTER (IHPF) - FREQUENCY DOMAIN
# ==================================================

def ideal_highpass_filtering(image, cutoff=30, strength=1.0):
    """
    Mempertajam citra menggunakan Ideal High Pass Filter.

    Parameter:
    image    : Citra input RGB atau grayscale.
    cutoff   : Jarak cutoff frequency dari pusat spektrum.
    strength : Kekuatan penajaman.

    Return:
    Citra hasil IHPF.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    rows, cols = image_array.shape[:2]

    # Membuat koordinat frekuensi dengan pusat di tengah.
    u = np.arange(rows) - rows // 2
    v = np.arange(cols) - cols // 2
    U, V = np.meshgrid(v, u)

    # Menghitung jarak setiap frekuensi dari pusat.
    distance = np.sqrt(U ** 2 + V ** 2)

    # Membuat mask Ideal High Pass Filter.
    mask = np.ones((rows, cols), dtype=np.float32)
    mask[distance <= cutoff] = 0

    # Memproses citra grayscale.
    if image_array.ndim == 2:
        channels = [image_array]
    else:
        channels = [
            image_array[:, :, i]
            for i in range(image_array.shape[2])
        ]

    results = []

    for channel in channels:
        # Transformasi Fourier.
        spectrum = np.fft.fft2(channel)
        spectrum_shift = np.fft.fftshift(spectrum)

        # Menerapkan filter frekuensi tinggi.
        filtered_spectrum = spectrum_shift * mask

        # Transformasi Fourier balik.
        high_frequency = np.fft.ifft2(
            np.fft.ifftshift(filtered_spectrum)
        ).real

        # Menambahkan detail frekuensi tinggi ke citra asli.
        sharpened = channel.astype(np.float32) + (
            strength * high_frequency
        )

        results.append(
            np.clip(sharpened, 0, 255).astype(np.uint8)
        )

    if image_array.ndim == 2:
        return results[0]

    return np.stack(results, axis=2)


# ==================================================
# BUTTERWORTH HIGH PASS FILTER (BHPF) - FREQUENCY DOMAIN
# ==================================================

def butterworth_highpass_filtering(
    image,
    cutoff=30,
    order=2,
    strength=1.0
):
    """
    Mempertajam citra menggunakan Butterworth High Pass Filter.

    Parameter:
    image    : Citra input RGB atau grayscale.
    cutoff   : Jarak cutoff frequency dari pusat spektrum.
    order    : Orde filter Butterworth.
    strength : Kekuatan penajaman.

    Return:
    Citra hasil BHPF.
    """

    image_array = np.asarray(image, dtype=np.uint8)

    if cutoff <= 0:
        raise ValueError("Cutoff frequency harus lebih besar dari 0.")

    if order < 1:
        raise ValueError("Order filter minimal 1.")

    rows, cols = image_array.shape[:2]

    # Membuat koordinat frekuensi dengan pusat di tengah.
    u = np.arange(rows) - rows // 2
    v = np.arange(cols) - cols // 2
    U, V = np.meshgrid(v, u)

    # Menghitung jarak setiap frekuensi dari pusat.
    distance = np.sqrt(U ** 2 + V ** 2)

    # Menghindari pembagian dengan nol.
    distance = np.maximum(distance, 1e-6)

    # Membuat mask Butterworth High Pass Filter.
    mask = 1 / (
        1 + (cutoff / distance) ** (2 * order)
    )

    # Memproses citra grayscale.
    if image_array.ndim == 2:
        channels = [image_array]
    else:
        channels = [
            image_array[:, :, i]
            for i in range(image_array.shape[2])
        ]

    results = []

    for channel in channels:
        # Transformasi Fourier.
        spectrum = np.fft.fft2(channel)
        spectrum_shift = np.fft.fftshift(spectrum)

        # Menerapkan filter frekuensi tinggi.
        filtered_spectrum = spectrum_shift * mask

        # Transformasi Fourier balik.
        high_frequency = np.fft.ifft2(
            np.fft.ifftshift(filtered_spectrum)
        ).real

        # Menambahkan detail frekuensi tinggi ke citra asli.
        sharpened = channel.astype(np.float32) + (
            strength * high_frequency
        )

        results.append(
            np.clip(sharpened, 0, 255).astype(np.uint8)
        )

    if image_array.ndim == 2:
        return results[0]

    return np.stack(results, axis=2)


# GEOMETRIC CORRECTION
def geometric_correction(image, points):

    image_array = np.asarray(image, dtype=np.uint8)
    height, width = image_array.shape[:2]

    # Konversi koordinat persentase menjadi koordinat piksel.
    source_points = np.array([
        (x * width / 100, y * height / 100)
        for x, y in points
    ], dtype=np.float32)

    # Menghitung lebar dan tinggi hasil transformasi.
    top_width = np.linalg.norm(source_points[1] - source_points[0])
    bottom_width = np.linalg.norm(source_points[2] - source_points[3])
    left_height = np.linalg.norm(source_points[3] - source_points[0])
    right_height = np.linalg.norm(source_points[2] - source_points[1])

    output_width = max(1, int(max(top_width, bottom_width)))
    output_height = max(1, int(max(left_height, right_height)))

    # Menentukan empat titik tujuan berbentuk persegi panjang.
    destination_points = np.array([
        [0, 0],
        [output_width - 1, 0],
        [output_width - 1, output_height - 1],
        [0, output_height - 1]
    ], dtype=np.float32)

    # Menghitung matriks transformasi perspektif.
    matrix = cv2.getPerspectiveTransform(
        source_points,
        destination_points
    )

    # Melakukan transformasi perspektif.
    result = cv2.warpPerspective(
        image_array,
        matrix,
        (output_width, output_height)
    )

    return result