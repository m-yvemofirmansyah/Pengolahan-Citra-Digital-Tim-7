"""PicLab - Seven | PCD - Kelompok 7
Aplikasi Pengolahan Citra Digital berbasis Tkinter.

Menu mengikuti struktur rekomendasi:
File, Basic Ops, Enhancement, Noise, Edge Detection,
Segmentation, dan About.

Operasi yang sudah aktif: Negative dan Flipping (horizontal, vertical, both).
Operasi lainnya ditampilkan sebagai placeholder sampai algoritmanya diintegrasikan.

Kebutuhan: pip install pillow numpy opencv-python
Jalankan: python main.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

import numpy as np

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    Image = None
    ImageTk = None
    PIL_OK = False

from operations.basic import (
    flip_horizontal,
    flip_vertical,
    flip_both,
    image_negative,
    add_scalar,
    subtract_scalar,
    multiply_scalar,
    divide_scalar,
    add_images,
    subtract_images,
    multiply_images,
    divide_images,
    grayscale_conversion,
    grayscale_gradient,
    binary_image,
    rgb_adjustment,
    pseudo_color,
    hsv_conversion,
    boolean_not,
    boolean_and,
    boolean_or,
    boolean_xor,
    translation,
    rotation,
    zooming,
    cropping,
    thresholding,
    convolution,
    fourier_transform,
)


# ============================================================
# KONFIGURASI TAMPILAN
# ============================================================
class C:
    PRIMARY = "#1A4FD6"
    PRIMARY_DARK = "#1440B0"
    PRIMARY_SOFT = "#E3EAFB"
    BG = "#F0F2FB"
    PANEL = "#F5F6FF"
    CANVAS = "#E6E8F7"
    WHITE = "#FFFFFF"
    BORDER = "#D9DCEC"
    TEXT = "#111827"
    MUTED = "#6B7280"
    HOVER = "#EEF1FB"
    DARK = "#2F3447"
    GREEN = "#22D3A0"


FONT = "Segoe UI"
MONO = "Consolas"


def F(size=10, weight="normal"):
    return (FONT, size, weight)


# ============================================================
# KOMPONEN BANTU
# ============================================================
class FlatButton(tk.Label):
    """Tombol datar berbasis Label."""

    def __init__(self, parent, text, command=None, bg=C.WHITE, fg=C.TEXT,
                 hover=C.HOVER, border=C.BORDER, font=None,
                 padx=14, pady=8, **kwargs):
        super().__init__(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=font or F(10, "bold"),
            padx=padx,
            pady=pady,
            cursor="hand2",
            highlightthickness=1 if border else 0,
            highlightbackground=border or bg,
            highlightcolor=border or bg,
            **kwargs
        )
        self._bg = bg
        self._hover = hover
        self._command = command
        self.bind("<Enter>", lambda _e: self.config(bg=self._hover))
        self.bind("<Leave>", lambda _e: self.config(bg=self._bg))
        self.bind("<Button-1>", self._on_click)

    def _on_click(self, _event):
        if self._command:
            self._command()


class ImagePanel(tk.Frame):
    """Panel untuk menampilkan citra asli atau hasil."""

    def __init__(self, parent, title, placeholder, status_text, status_fg):
        super().__init__(parent, bg=C.PANEL, highlightthickness=1,
                         highlightbackground=C.BORDER)
        self.placeholder = placeholder
        self._pil_image = None
        self._tk_image = None

        head = tk.Frame(self, bg=C.PANEL)
        head.pack(fill="x", padx=16, pady=(14, 10))
        dot = tk.Canvas(head, width=14, height=14, bg=C.PANEL,
                        highlightthickness=0)
        dot.create_oval(2, 2, 12, 12, fill=C.PRIMARY, outline=C.PRIMARY)
        dot.pack(side="left")
        tk.Label(head, text=title, bg=C.PANEL, fg=C.TEXT,
                 font=F(12, "bold")).pack(side="left", padx=8)

        bar = tk.Frame(self, bg=C.WHITE, highlightthickness=1,
                       highlightbackground=C.BORDER)
        bar.pack(fill="x", padx=1)
        tk.Label(bar, text="100%", bg=C.PRIMARY_SOFT, fg=C.TEXT,
                 font=(MONO, 9, "bold"), padx=8, pady=3).pack(
                     side="left", padx=(14, 6), pady=8)
        for glyph in ("⛶", "−", "+"):
            FlatButton(bar, glyph, bg=C.WHITE, border=None,
                       padx=8, pady=2, font=F(12)).pack(side="left", pady=8)

        self.canvas = tk.Canvas(self, bg=C.CANVAS, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _e: self._redraw())

        status = tk.Frame(self, bg=C.PANEL)
        status.pack(fill="x", padx=16, pady=12)
        self.status = tk.Label(status, text=status_text, bg=C.DARK,
                               fg=status_fg, font=(MONO, 9),
                               anchor="w", padx=14, pady=8)
        self.status.pack(fill="x")

    def show_image(self, pil_image):
        self._pil_image = pil_image
        self._redraw()

    def _redraw(self):
        self.canvas.delete("all")
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 10 or ch < 10:
            return

        if self._pil_image is None:
            self.canvas.create_text(
                cw // 2, ch // 2,
                text=self.placeholder,
                fill=C.MUTED,
                font=F(11),
                justify="center"
            )
            return

        w, h = self._pil_image.size
        scale = min(cw / w, ch / h, 1.0)
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        resized = self._pil_image.resize(new_size, Image.LANCZOS)
        self._tk_image = ImageTk.PhotoImage(resized)
        self.canvas.create_image(cw // 2, ch // 2, image=self._tk_image)


# ============================================================
# APLIKASI UTAMA
# ============================================================
class PicLabApp(tk.Tk):
    MENU_STRUCTURE = {
        "File": {
            "Open...": "file_open",
            "Save": "file_save",
            "Save As": "file_save_as",
            "Exit": "file_exit",
        },
        "Basic Ops": {
            "Negative": "negative",
            "Arithmetic": {
                "Add (+)": "add",
                "Subtract (-)": "subtract",
                "Multiply (*)": "multiply",
                "Divide (/)": "divide",
            },
            "Boolean": {
                "NOT": "not",
                "AND": "and",
                "OR": "or",
                "XOR": "xor",
            },
            "Geometrics": {
                "Translation": "translation",
                "Rotation": "rotation",
                "Zooming": "zooming",
                "Flipping": "flipping",
                "Cropping": "cropping",
            },
            "Thresholding": "thresholding",
            "Convolution": "convolution",
            "Fourier Transform": "fourier_transform",
            "Colouring": {
                "Binary": "binary",
                "Grayscale": "grayscale",
                "RGB": "rgb",
                "HSV": "hsv",
                "CMY": "cmy",
                "YUV": "yuv",
                "Pseudo": "pseudo",
            },
        },
        "Enhancement": {
            "Brightness": "brightness",
            "Contrast": "contrast",
            "Histogram Equalization": "histogram_equalization",
            "Smoothing": {
                "Spatial Domain": {
                    "Lowpass Filtering": "lowpass_filtering",
                    "Median Filtering": "median_filtering",
                },
                "Frequency Domain": {
                    "ILPF": "ilpf",
                    "BLPF": "blpf",
                },
            },
            "Sharpening": {
                "Spatial Domain": {
                    "Highpass Filtering": "highpass_filtering",
                    "Highboost Filtering": "highboost_filtering",
                },
                "Frequency Domain": {
                    "IHPF": "ihpf",
                    "BHPF": "bhpf",
                },
            },
            "Geometric Correction": "geometric_correction",
        },
        "Noise": {
            "Gaussian Noise": "gaussian_noise",
            "Rayleigh Noise": "rayleigh_noise",
            "Erlang (Gamma) Noise": "erlang_noise",
            "Exponential Noise": "exponential_noise",
            "Uniform Noise": "uniform_noise",
            "Impulse Noise": "impulse_noise",
        },
        "Edge Detection": {
            "1st Differential Gradient": {
                "Sobel": "sobel",
                "Prewitt": "prewitt",
                "Robert": "robert",
            },
            "2nd Differential Gradient": {
                "Laplacian": "laplacian",
                "Laplacian of Gaussian (LoG)": "log",
                "Canny": "canny",
            },
        },
        "Segmentation": {},
        "About": {
            "Info Tim Developer": "about_team",
            "GitHub": "about_github",
            "YouTube Tutorial": "about_youtube",
        },
    }

    OPERATION_INFO = {
        "flipping": ("Flipping", "Membalik citra secara horizontal, vertikal, atau keduanya."),
        "negative": ("Negative", "Menghasilkan citra negatif dengan membalik intensitas piksel."),
        "add": ("Add (+)", "Menjumlahkan dua citra atau citra dengan nilai konstanta."),
        "subtract": ("Subtract (-)", "Mengurangkan nilai piksel dua citra atau konstanta."),
        "multiply": ("Multiply (*)", "Mengalikan nilai piksel citra."),
        "divide": ("Divide (/)", "Membagi nilai piksel citra."),
        "not": ("Boolean NOT", "Operasi logika NOT pada citra biner."),
        "and": ("Boolean AND", "Operasi logika AND pada dua citra biner."),
        "or": ("Boolean OR", "Operasi logika OR pada dua citra biner."),
        "xor": ("Boolean XOR", "Operasi logika XOR pada dua citra biner."),
        "translation": ("Translation", "Menggeser posisi citra pada sumbu horizontal dan vertikal."),
        "rotation": ("Rotation", "Memutar citra berdasarkan sudut tertentu."),
        "zooming": ("Zooming", "Mengubah skala atau ukuran citra."),
        "cropping": ("Cropping", "Memotong bagian tertentu dari citra."),
        "thresholding": ("Thresholding", "Mengubah citra menjadi citra biner berdasarkan nilai ambang."),
        "convolution": ("Convolution", "Melakukan operasi konvolusi menggunakan kernel."),
        "fourier_transform": ("Fourier Transform", "Mengubah representasi citra ke domain frekuensi."),
        "binary": ("Binary", "Mengubah citra menjadi dua tingkat intensitas."),
        "grayscale": ("Grayscale", "Mengubah citra berwarna menjadi citra keabuan."),
        "rgb": ("RGB", "Menampilkan atau mengolah citra dalam ruang warna RGB."),
        "hsv": ("HSV", "Mengolah citra menggunakan ruang warna HSV."),
        "cmy": ("CMY", "Mengolah citra menggunakan ruang warna CMY."),
        "yuv": ("YUV", "Mengolah citra menggunakan ruang warna YUV."),
        "pseudo": ("Pseudo Colour", "Memberikan pewarnaan semu pada citra keabuan."),
        "brightness": ("Brightness", "Mengatur tingkat kecerahan citra."),
        "contrast": ("Contrast", "Mengatur perbedaan intensitas terang dan gelap."),
        "histogram_equalization": ("Histogram Equalization", "Memperbaiki distribusi intensitas menggunakan histogram."),
        "lowpass_filtering": ("Lowpass Filtering", "Menghaluskan citra pada domain spasial."),
        "median_filtering": ("Median Filtering", "Mengurangi derau menggunakan filter median."),
        "ilpf": ("Ideal Lowpass Filter (ILPF)", "Menyaring komponen frekuensi tinggi dengan filter ideal."),
        "blpf": ("Butterworth Lowpass Filter (BLPF)", "Menyaring komponen frekuensi tinggi menggunakan Butterworth."),
        "highpass_filtering": ("Highpass Filtering", "Menonjolkan detail dan perubahan intensitas citra."),
        "highboost_filtering": ("Highboost Filtering", "Mempertajam citra menggunakan teknik highboost."),
        "ihpf": ("Ideal Highpass Filter (IHPF)", "Menekan komponen frekuensi rendah dengan filter ideal."),
        "bhpf": ("Butterworth Highpass Filter (BHPF)", "Menekan komponen frekuensi rendah menggunakan Butterworth."),
        "geometric_correction": ("Geometric Correction", "Mengoreksi distorsi geometris pada citra."),
        "gaussian_noise": ("Gaussian Noise", "Menambahkan derau dengan distribusi Gaussian."),
        "rayleigh_noise": ("Rayleigh Noise", "Menambahkan derau dengan distribusi Rayleigh."),
        "erlang_noise": ("Erlang (Gamma) Noise", "Menambahkan derau dengan distribusi Erlang/Gamma."),
        "exponential_noise": ("Exponential Noise", "Menambahkan derau dengan distribusi eksponensial."),
        "uniform_noise": ("Uniform Noise", "Menambahkan derau dengan distribusi uniform."),
        "impulse_noise": ("Impulse Noise", "Menambahkan derau impuls atau salt-and-pepper."),
        "sobel": ("Sobel", "Deteksi tepi menggunakan operator Sobel."),
        "prewitt": ("Prewitt", "Deteksi tepi menggunakan operator Prewitt."),
        "robert": ("Robert", "Deteksi tepi menggunakan operator Robert."),
        "laplacian": ("Laplacian", "Deteksi tepi menggunakan turunan kedua Laplacian."),
        "log": ("Laplacian of Gaussian (LoG)", "Menggabungkan Gaussian smoothing dan Laplacian."),
        "canny": ("Canny", "Deteksi tepi menggunakan tahapan algoritma Canny."),
        "about_team": ("Info Tim Developer", "PicLab - Seven dikembangkan untuk proyek Pengolahan Citra Digital."),
        "about_github": ("GitHub", "Tautan repositori GitHub tim dapat ditambahkan di sini."),
        "about_youtube": ("YouTube Tutorial", "Tautan video tutorial aplikasi dapat ditambahkan di sini."),
    }

    def __init__(self):
        super().__init__()
        self.title("PicLab | PCD Kelompok 7")
        self.geometry("1400x860")
        self.minsize(1180, 700)
        self.configure(bg=C.BG)

        self.original_image = None
        self.current_image = None
        self.history = []
        self.threshold = tk.IntVar(value=128)
        self.selected_operation = tk.StringVar(value="flip_horizontal")

        # Variabel untuk operasi Arithmetic
        self.arithmetic_mode = tk.StringVar(value="scalar")
        self.scalar_value = tk.StringVar(value="50")
        self.second_image = None
        self.second_image_path = None
        self.second_image_label = None

        #boolean
        self.boolean_image2 = None

        self.expanded_categories = {"Basic Ops"}
        self.active_category = "Basic Ops"
        self.active_operation = "flipping"
        self.sidebar_buttons = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._refresh_sidebar()
        self._show_operation_panel("flipping")

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self, bg=C.WHITE, height=68)
        header.grid(row=0, column=0, sticky="ew")
        header.pack_propagate(False)

        tk.Label(header, text="◉", bg=C.WHITE, fg=C.PRIMARY,
                 font=F(20, "bold")).pack(side="left", padx=(26, 6))
        tk.Label(header, text="PicLab - Seven", bg=C.WHITE, fg=C.TEXT,
                 font=F(15, "bold")).pack(side="left")
        tk.Frame(header, bg=C.BORDER, width=1, height=22).pack(side="left", padx=16)
        tk.Label(header, text="PCD - Kelompok 7", bg=C.WHITE, fg=C.MUTED,
                 font=F(10)).pack(side="left")

        tk.Label(header, text="👤", bg=C.PRIMARY, fg=C.WHITE,
                 font=F(13), width=3).pack(side="right", padx=(10, 24))
        FlatButton(header, "⬇  Simpan / Unduh Hasil", self.save_image_as,
                   bg=C.PRIMARY, fg=C.WHITE, hover=C.PRIMARY_DARK,
                   border=None, padx=18, pady=10).pack(side="right", padx=6)
        FlatButton(header, "↶", self.undo, padx=10, pady=8,
                   font=F(12, "bold")).pack(side="right", padx=4)
        FlatButton(header, "⟳  Reset ke Asli", self.reset_image).pack(side="right", padx=4)
        FlatButton(header, "⭱  Upload/Ganti Gambar", self.upload_image).pack(side="right", padx=4)

        tk.Frame(self, bg=C.BORDER, height=1).grid(
            row=0, column=0, sticky="sew"
        )

    # --------------------------------------------------------
    # BODY: SIDEBAR | WORKSPACE | CONTROL PANEL
    # --------------------------------------------------------
    def _build_body(self):
        body = tk.Frame(self, bg=C.BG)
        body.grid(row=1, column=0, sticky="nsew")
        body.rowconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        self._build_sidebar(body)
        self._build_workspace(body)
        self._build_control_panel(body)

    # --------------------------------------------------------
    # SIDEBAR DINAMIS DAN BERTINGKAT
    # --------------------------------------------------------
    def _build_sidebar(self, parent):
        self.sidebar = tk.Frame(parent, bg=C.WHITE, width=270)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        tk.Label(self.sidebar, text="MENU UTAMA", bg=C.WHITE,
                 fg=C.MUTED, font=F(9, "bold")).pack(
                     anchor="w", padx=22, pady=(22, 12)
                 )

        # Canvas + scrollbar agar seluruh submenu tetap dapat diakses.
        nav_container = tk.Frame(self.sidebar, bg=C.WHITE)
        nav_container.pack(fill="both", expand=True, padx=(10, 4), pady=(0, 8))
        self.nav_canvas = tk.Canvas(nav_container, bg=C.WHITE,
                                    highlightthickness=0, borderwidth=0)
        scrollbar = tk.Scrollbar(nav_container, orient="vertical",
                                 command=self.nav_canvas.yview)
        self.nav_inner = tk.Frame(self.nav_canvas, bg=C.WHITE)
        self.nav_inner.bind(
            "<Configure>",
            lambda _e: self.nav_canvas.configure(
                scrollregion=self.nav_canvas.bbox("all")
            )
        )
        self.nav_canvas_window = self.nav_canvas.create_window(
            (0, 0), window=self.nav_inner, anchor="nw"
        )
        self.nav_canvas.configure(yscrollcommand=scrollbar.set)
        self.nav_canvas.bind(
            "<Configure>",
            lambda e: self.nav_canvas.itemconfigure(
                self.nav_canvas_window, width=e.width
            )
        )
        self.nav_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.nav_canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.nav_canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            )
        )

        footer = tk.Frame(self.sidebar, bg=C.WHITE)
        footer.pack(side="bottom", fill="x", padx=20, pady=12)
        tk.Frame(footer, bg=C.BORDER, height=1).pack(fill="x", pady=(0, 8))
        tk.Label(footer, text="PicLab - Seven", bg=C.WHITE,
                 fg=C.MUTED, font=F(9)).pack(anchor="w")

        tk.Frame(parent, bg=C.BORDER, width=1).grid(
            row=0, column=0, sticky="nse"
        )

    def _refresh_sidebar(self):
        for widget in self.nav_inner.winfo_children():
            widget.destroy()
        self.sidebar_buttons.clear()

        category_icons = {
            "File": "▤",
            "Basic Ops": "☷",
            "Enhancement": "✦",
            "Noise": "⁘",
            "Edge Detection": "⌁",
            "Segmentation": "◔",
            "About": "ⓘ",
        }

        for category, children in self.MENU_STRUCTURE.items():
            is_expanded = category in self.expanded_categories
            is_active_category = category == self.active_category
            row = tk.Frame(self.nav_inner, bg=C.WHITE)
            row.pack(fill="x", pady=2)

            has_children = bool(children)
            arrow = "▾" if is_expanded else "▸"
            label_text = f"{category_icons.get(category, '•')}   {category}"
            if has_children:
                label_text += f"   {arrow}"

            bg = C.PRIMARY if is_active_category else C.WHITE
            fg = C.WHITE if is_active_category else C.TEXT
            btn = tk.Label(row, text=label_text, bg=bg, fg=fg,
                           font=F(10, "bold" if is_active_category else "normal"),
                           anchor="w", padx=12, pady=10, cursor="hand2")
            btn.pack(fill="x")
            btn.bind(
                "<Button-1>",
                lambda _e, cat=category: self._on_category_click(cat)
            )
            self.sidebar_buttons[category] = btn

            if is_expanded:
                self._render_menu_children(category, children, self.nav_inner)

    def _render_menu_children(self, category, children, parent, level=1):
        """Render submenu secara rekursif, termasuk grup bertingkat."""
        for label, value in children.items():
            if isinstance(value, dict):
                group = tk.Frame(parent, bg=C.WHITE)
                group.pack(fill="x", padx=(level * 13, 4), pady=(5, 1))
                tk.Label(group, text=label.upper(), bg=C.WHITE,
                         fg=C.MUTED, font=F(8, "bold"),
                         anchor="w").pack(fill="x", padx=10, pady=(4, 2))
                self._render_menu_children(category, value, parent, level + 1)
            else:
                selected = value == self.active_operation
                bg = C.PRIMARY_SOFT if selected else C.WHITE
                fg = C.PRIMARY if selected else C.TEXT
                item = tk.Label(
                    parent,
                    text=f"{'    ' * level}›  {label}",
                    bg=bg,
                    fg=fg,
                    font=F(9, "bold" if selected else "normal"),
                    anchor="w",
                    padx=10,
                    pady=6,
                    cursor="hand2"
                )
                item.pack(fill="x", padx=(level * 10, 4))
                if category == "File":
                    item.bind(
                        "<Button-1>",
                        lambda _e, action=value: self._run_file_menu_action(action)
                    )
                else:
                    item.bind(
                        "<Button-1>",
                        lambda _e, cat=category, op=value, title=label:
                            self._select_operation(cat, op, title)
                    )

    def _on_category_click(self, category):
        self.active_category = category
        children = self.MENU_STRUCTURE[category]

        if children:
            if category in self.expanded_categories:
                self.expanded_categories.remove(category)
            else:
                self.expanded_categories.add(category)

            # Klik kategori utama juga menampilkan halaman ringkasan kategori.
            self.active_operation = None
            self._show_category_panel(category)
        else:
            self.active_operation = None
            self._show_category_panel(category)

        self._refresh_sidebar()

    def _run_file_menu_action(self, action):
        """Menjalankan perintah pada submenu File."""
        if action == "file_open":
            self.upload_image()
        elif action == "file_save":
            self.save_image()
        elif action == "file_save_as":
            self.save_image_as()
        elif action == "file_exit":
            self.destroy()

    def _select_operation(self, category, operation, title):
        self.active_category = category
        self.active_operation = operation
        self._show_operation_panel(operation, title)
        self._refresh_sidebar()

    # --------------------------------------------------------
    # WORKSPACE GAMBAR
    # --------------------------------------------------------
    def _build_workspace(self, parent):
        work = tk.Frame(parent, bg=C.BG)
        work.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        work.rowconfigure(0, weight=1)
        work.columnconfigure(0, weight=1, uniform="img")
        work.columnconfigure(1, weight=1, uniform="img")

        self.panel_before = ImagePanel(
            work,
            "Citra Asli (Sebelum)",
            "Belum ada gambar\n\nKlik 'Ganti Citra Baru' untuk mengunggah",
            "X: ----  Y: ----   |   RGB [---, ---, ---]",
            C.WHITE
        )
        self.panel_before.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.panel_after = ImagePanel(
            work,
            "Citra Hasil (Sesudah)",
            "Hasil operasi akan tampil di sini",
            "X: ----  Y: ----   |   Hasil pengolahan",
            C.GREEN
        )
        self.panel_after.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    # --------------------------------------------------------
    # PANEL KONTROL DINAMIS
    # --------------------------------------------------------
    def _build_control_panel(self, parent):
        self.control_panel = tk.Frame(parent, bg=C.WHITE, width=390)
        self.control_panel.grid(row=0, column=2, sticky="ns")
        self.control_panel.grid_propagate(False)
        tk.Frame(parent, bg=C.BORDER, width=1).grid(
            row=0, column=2, sticky="nsw"
        )

        header = tk.Frame(self.control_panel, bg=C.WHITE)
        header.pack(fill="x", padx=20, pady=(22, 12))
        tk.Label(header, text="☰  Panel Kontrol Operasi", bg=C.WHITE,
                 fg=C.TEXT, font=F(16, "bold")).pack(anchor="w")
        tk.Label(header,
                 text="Pilih operasi dan sesuaikan parameter pengolahan citra.",
                 bg=C.WHITE, fg=C.MUTED, font=F(9),
                 wraplength=345, justify="left").pack(anchor="w", pady=(5, 0))

        tk.Frame(self.control_panel, bg=C.BORDER, height=1).pack(fill="x")

        # Area konten yang dapat di-scroll.
        content_wrap = tk.Frame(self.control_panel, bg=C.WHITE)
        content_wrap.pack(fill="both", expand=True)
        self.control_canvas = tk.Canvas(content_wrap, bg=C.WHITE,
                                        highlightthickness=0)
        control_scroll = tk.Scrollbar(content_wrap, orient="vertical",
                                      command=self.control_canvas.yview)
        self.control_content = tk.Frame(self.control_canvas, bg=C.WHITE)
        self.control_content.bind(
            "<Configure>",
            lambda _e: self.control_canvas.configure(
                scrollregion=self.control_canvas.bbox("all")
            )
        )
        self.control_canvas_window = self.control_canvas.create_window(
            (0, 0), window=self.control_content, anchor="nw"
        )
        self.control_canvas.configure(yscrollcommand=control_scroll.set)
        self.control_canvas.bind(
            "<Configure>",
            lambda e: self.control_canvas.itemconfigure(
                self.control_canvas_window, width=e.width
            )
        )
        self.control_canvas.pack(side="left", fill="both", expand=True)
        control_scroll.pack(side="right", fill="y")

        actions = tk.Frame(self.control_panel, bg=C.WHITE)
        actions.pack(side="bottom", fill="x", padx=20, pady=16)
        FlatButton(
            actions,
            "▶  Terapkan Operasi",
            self.apply_operation,
            bg=C.PRIMARY,
            fg=C.WHITE,
            hover=C.PRIMARY_DARK,
            border=None,
            font=F(10, "bold"),
            pady=13
        ).pack(fill="x")
        action_row = tk.Frame(actions, bg=C.WHITE)
        action_row.pack(fill="x", pady=(8, 0))
        action_row.columnconfigure(0, weight=1)
        action_row.columnconfigure(1, weight=1)
        FlatButton(action_row, "⟳  Reset", self.reset_image).grid(
            row=0, column=0, sticky="ew", padx=(0, 4)
        )
        FlatButton(action_row, "‹›  Kode Python", self.show_code_info).grid(
            row=0, column=1, sticky="ew", padx=(4, 0)
        )

    def _clear_control_content(self):
        for widget in self.control_content.winfo_children():
            widget.destroy()

    def _show_category_panel(self, category):
        self._clear_control_content()
        descriptions = {
            "File": "Kelola citra yang digunakan dalam aplikasi.",
            "Basic Ops": "Pilih operasi dasar untuk memanipulasi citra.",
            "Enhancement": "Pilih metode untuk meningkatkan kualitas citra.",
            "Noise": "Pilih jenis derau yang akan ditambahkan pada citra.",
            "Edge Detection": "Pilih metode untuk mendeteksi tepi objek pada citra.",
            "Segmentation": "Kategori segmentasi citra. Submenu dapat ditambahkan setelah materi atau algoritmanya ditentukan.",
            "About": "Informasi aplikasi dan tim pengembang PicLab - Seven.",
        }
        tk.Label(self.control_content, text=category, bg=C.WHITE,
                 fg=C.TEXT, font=F(15, "bold")).pack(
                     anchor="w", padx=20, pady=(20, 6)
                 )
        tk.Label(self.control_content, text=descriptions.get(category, ""),
                 bg=C.WHITE, fg=C.MUTED, font=F(10), wraplength=330,
                 justify="left").pack(anchor="w", padx=20, pady=(0, 16))

        if category == "File":
            self._add_menu_action("Open Citra", self.upload_image)
            self._add_menu_action("Save", self.save_image)
            self._add_menu_action("Save As", self.save_image_as)
            self._add_menu_action("Exit", self.destroy)
        elif category == "About":
            self._add_info_card("PicLab - Seven", "Aplikasi proyek Pengolahan Citra Digital Kelompok 7.")
            self._add_info_card("Tutorial", "Tautan GitHub dan YouTube dapat ditambahkan setelah tersedia.")
        elif category == "Segmentation":
            self._add_info_card("Belum ada submenu", "Referensi menu yang diberikan belum merinci metode segmentasi.")
        else:
            self._add_info_card("Pilih submenu", "Buka kategori di sidebar, kemudian pilih salah satu operasi untuk melihat pengaturannya.")

    def _show_operation_panel(self, operation, display_title=None):
        self._clear_control_content()

        if operation not in self.OPERATION_INFO:
            self._show_category_panel(self.active_category)
            return

        title, description = self.OPERATION_INFO[operation]

        if display_title:
            title = display_title

        tk.Label(
            self.control_content,
            text=title,
            bg=C.WHITE,
            fg=C.TEXT,
            font=F(15, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        tk.Label(
            self.control_content,
            text=description,
            bg=C.WHITE,
            fg=C.MUTED,
            font=F(9),
            wraplength=330,
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 16))

        if operation == "flipping":
            self._build_flipping_controls(self.control_content)

        elif operation in (
            "translation",
            "rotation",
            "zooming",
            "cropping"
        ):
            self._build_geometric_controls(
                operation,
                self.control_content
            )

        elif operation == "negative":
            self._add_info_card(
                "Image Negative",
                "Membalik nilai intensitas setiap piksel menggunakan "
                "rumus 255 - nilai piksel."
            )

        elif operation == "grayscale":
            self.grayscale_mode = tk.StringVar(value="conversion")

            tk.Label(
                self.control_content,
                text="Grayscale Method",
                bg=C.WHITE,
                fg=C.TEXT,
                font=F(10, "bold")
            ).pack(anchor="w", padx=20, pady=(5, 8))

            tk.Radiobutton(
                self.control_content,
                text="Convert to Grayscale",
                variable=self.grayscale_mode,
                value="conversion",
                bg=C.WHITE,
                fg=C.TEXT,
                activebackground=C.WHITE,
                font=F(9)
            ).pack(anchor="w", padx=25)

            tk.Radiobutton(
                self.control_content,
                text="Generate Grayscale Gradient",
                variable=self.grayscale_mode,
                value="gradient",
                bg=C.WHITE,
                fg=C.TEXT,
                activebackground=C.WHITE,
                font=F(9)
            ).pack(anchor="w", padx=25)

        elif operation in ("not", "and", "or", "xor"):
            self._build_boolean_controls(self.control_content)

        elif operation == "binary":
            self._add_info_card(
                "Binary Image",
                "Menghasilkan citra biner berukuran 100 × 100 piksel. "
                "Nilai 0 merepresentasikan hitam dan 255 merepresentasikan putih."
            )

        elif operation == "rgb":
            self._add_info_card(
                "RGB Adjustment",
                "Atur intensitas kanal Red, Green, dan Blue pada gambar "
                "yang diunggah. Rentang pengaturan setiap kanal adalah "
                "-255 hingga +255."
            )
            self._build_rgb_controls(self.control_content)

        elif operation == "hsv":
            self._add_info_card(
                "HSV Color Space",
                "Mengonversi citra RGB ke ruang warna HSV "
                "(Hue, Saturation, Value) dan menampilkan "
                "kanal warna yang dipilih."
            )

            self._build_hsv_controls(self.control_content)

        elif operation in ("add", "subtract", "multiply", "divide"):
            default_value = (
                "2" if operation in ("multiply", "divide") else "50"
            )

            self.scalar_value.set(default_value)
            self._build_arithmetic_controls(self.control_content)

        elif operation == "pseudo":
            self._build_pseudo_color_controls(self.control_content)

        elif operation == "thresholding":
            self._add_info_card(
                "Image Thresholding",
                "Mengubah citra grayscale menjadi citra biner "
                "berdasarkan nilai ambang antara 0 sampai 255."
            )
            self._build_thresholding_controls(self.control_content)

        elif operation == "convolution":
            self._add_info_card(
                "Convolution",
                "Menerapkan kernel untuk memproses citra."
            )
            self._build_convolution_controls(self.control_content)

        elif operation == "fourier_transform":
            self._add_info_card(
                "Fourier Transform",
                "Mengubah citra dari domain spasial ke domain frekuensi "
                "menggunakan Discrete Fourier Transform (DFT)."
            )

        else:
            self._add_info_card(
                "Fitur belum diimplementasikan",
                "Struktur menu sudah tersedia. Algoritma untuk operasi "
                "ini akan diintegrasikan setelah menu selesai dirapikan."
            )

        self.apply_button_operation = operation

    def _add_info_card(self, title, description):
        card = tk.Frame(self.control_content, bg=C.PANEL,
                        highlightthickness=1,
                        highlightbackground=C.BORDER)
        card.pack(fill="x", padx=20, pady=(0, 12))
        tk.Label(card, text=title, bg=C.PANEL, fg=C.TEXT,
                 font=F(10, "bold")).pack(anchor="w", padx=14, pady=(12, 5))
        tk.Label(card, text=description, bg=C.PANEL, fg=C.MUTED,
                 font=F(9), wraplength=300, justify="left").pack(
                     anchor="w", padx=14, pady=(0, 12)
                 )

    def _add_menu_action(self, label, command):
        FlatButton(self.control_content, label, command,
                   bg=C.WHITE, fg=C.TEXT, hover=C.HOVER).pack(
                       fill="x", padx=20, pady=4
                   )

# Algoritma

    def _build_flipping_controls(self, parent):
        card = tk.Frame(parent, bg=C.PANEL,
                        highlightthickness=1,
                        highlightbackground=C.BORDER)
        card.pack(fill="x", padx=20, pady=(0, 14))

        tk.Label(card, text="ARAH PEMBALIKAN", bg=C.PANEL,
                 fg=C.TEXT, font=F(9, "bold")).pack(
                     anchor="w", padx=14, pady=(12, 8)
                 )

        options = [
            ("Horizontal (kiri ↔ kanan)", "flip_horizontal"),
            ("Vertikal (atas ↕ bawah)", "flip_vertical"),
            ("Horizontal + Vertikal", "flip_both"),
        ]
        for label, value in options:
            tk.Radiobutton(
                card,
                text=label,
                variable=self.selected_operation,
                value=value,
                bg=C.PANEL,
                fg=C.TEXT,
                activebackground=C.PANEL,
                font=F(9),
                anchor="w",
                selectcolor=C.WHITE
            ).pack(fill="x", padx=14, pady=4)

        tk.Label(card, text="Pilih arah pembalikan, lalu tekan Terapkan Operasi.",
                 bg=C.PANEL, fg=C.MUTED, font=F(8),
                 wraplength=300, justify="left").pack(
                     anchor="w", padx=14, pady=(6, 12)
                 )

    
    def _build_geometric_controls(self, operation, parent):
        """Membuat kontrol parameter operasi geometris."""

        self.geometric_values = {}

        if operation == "translation":
            title = "Translation Parameters"
            description = "Atur pergeseran citra pada sumbu X dan Y."
            fields = [
                ("X Translation", "tx", "50"),
                ("Y Translation", "ty", "30"),
            ]

        elif operation == "rotation":
            title = "Rotation Parameters"
            description = "Tentukan sudut rotasi citra dalam derajat."
            fields = [
                ("Rotation Angle (°)", "angle", "70"),
            ]

        elif operation == "zooming":
            title = "Zooming Parameters"
            description = "Atur faktor pembesaran atau pengecilan citra."
            fields = [
                ("Scale X", "scale_x", "3.0"),
                ("Scale Y", "scale_y", "2.0"),
            ]

        elif operation == "cropping":
            title = "Cropping Parameters"
            description = (
                "Tentukan area pemotongan berdasarkan persentase "
                "ukuran citra (0–100%)."
            )
            fields = [
                ("X1 (%)", "x1", "25"),
                ("Y1 (%)", "y1", "25"),
                ("X2 (%)", "x2", "75"),
                ("Y2 (%)", "y2", "75"),
            ]

        else:
            return

        self._add_info_card(title, description)

        for label_text, key, default_value in fields:
            tk.Label(
                parent,
                text=label_text,
                bg=C.WHITE,
                fg=C.TEXT,
                font=F(9, "bold")
            ).pack(anchor="w", padx=20, pady=(8, 3))

            variable = tk.StringVar(value=default_value)
            self.geometric_values[key] = variable

            tk.Entry(
                parent,
                textvariable=variable,
                font=F(10),
                relief="solid",
                bd=1
            ).pack(fill="x", padx=20, pady=(0, 5))


    def _build_rgb_controls(self, parent):
        """Membuat kontrol pengaturan kanal RGB."""

        self.rgb_red = tk.IntVar(value=0)
        self.rgb_green = tk.IntVar(value=0)
        self.rgb_blue = tk.IntVar(value=0)

        channels = [
            ("Red (R)", self.rgb_red, "#E74C3C"),
            ("Green (G)", self.rgb_green, "#27AE60"),
            ("Blue (B)", self.rgb_blue, "#3498DB"),
        ]

        self.rgb_value_labels = {}

        for name, variable, color in channels:
            frame = tk.Frame(parent, bg=C.WHITE)
            frame.pack(fill="x", padx=20, pady=(8, 12))

            tk.Label(
                frame,
                text=name,
                bg=C.WHITE,
                fg=C.TEXT,
                font=F(10, "bold")
            ).pack(anchor="w")

            value_label = tk.Label(
                frame,
                text="0",
                bg=C.WHITE,
                fg=color,
                font=F(9, "bold")
            )
            value_label.pack(anchor="e")

            self.rgb_value_labels[name] = value_label

            scale = tk.Scale(
                frame,
                from_=-255,
                to=255,
                orient="horizontal",
                variable=variable,
                bg=C.WHITE,
                fg=C.TEXT,
                troughcolor=C.BORDER,
                activebackground=color,
                highlightthickness=0,
                showvalue=False,
                resolution=1,
                command=lambda value, label=value_label: label.config(
                    text=f"{int(float(value)):+d}"
                )
            )
            scale.pack(fill="x")

        tk.Button(
            parent,
            text="Reset Nilai RGB",
            command=lambda: self._reset_rgb_values(),
            bg=C.WHITE,
            fg=C.TEXT,
            font=F(9),
            relief="solid",
            bd=1,
            cursor="hand2"
        ).pack(fill="x", padx=20, pady=(5, 10))

    def _reset_rgb_values(self):
        self.rgb_red.set(0)
        self.rgb_green.set(0)
        self.rgb_blue.set(0)

        for label in self.rgb_value_labels.values():
            label.config(text="0")

    def _build_hsv_controls(self, parent):
        self.hsv_channel = tk.StringVar(value="HSV")

        tk.Label(
            parent,
            text="HSV Channel",
            bg=C.WHITE,
            fg=C.TEXT,
            font=F(10, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 8))

        channel_menu = ttk.Combobox(
            parent,
            textvariable=self.hsv_channel,
            values=["HSV", "H - Hue", "S - Saturation", "V - Value"],
            state="readonly"
        )
        channel_menu.pack(fill="x", padx=20)

        tk.Button(
            parent,
            text="Reset Channel",
            command=lambda: self.hsv_channel.set("HSV"),
            bg=C.WHITE,
            fg=C.TEXT,
            font=F(9),
            relief="solid",
            bd=1,
            cursor="hand2"
        ).pack(fill="x", padx=20, pady=15)

    def _build_pseudo_color_controls(self):
        self._add_info_card(
            "Pseudo Color",
            "Mengubah citra grayscale menjadi citra berwarna "
            "menggunakan pemetaan intensitas."
        )

        self.pseudo_colormap = tk.StringVar(value="JET")

        ttk.Label(
            self.control_frame,
            text="Color Map"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        colormap_options = ["JET", "HOT", "OCEAN", "RAINBOW"]

        colormap_menu = ttk.Combobox(
            self.control_frame,
            textvariable=self.pseudo_colormap,
            values=colormap_options,
            state="readonly"
        )
        colormap_menu.pack(fill="x", padx=15)

        ttk.Button(
            self.control_frame,
            text="Reset",
            command=lambda: self.pseudo_colormap.set("JET")
        ).pack(fill="x", padx=15, pady=10)

    def _build_pseudo_color_controls(self, parent):
        """Membuat kontrol pemilihan colormap Pseudo Color."""

        self.pseudo_colormap = tk.StringVar(value="JET")

        tk.Label(
            parent,
            text="Color Map",
            bg=C.WHITE,
            fg=C.TEXT,
            font=F(10, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 8))

        colormap_menu = ttk.Combobox(
            parent,
            textvariable=self.pseudo_colormap,
            values=["JET", "HOT", "OCEAN", "RAINBOW"],
            state="readonly"
        )
        colormap_menu.pack(fill="x", padx=20)

        tk.Button(
            parent,
            text="Reset Colormap",
            command=lambda: self.pseudo_colormap.set("JET"),
            bg=C.WHITE,
            fg=C.TEXT,
            font=F(9),
            relief="solid",
            bd=1,
            cursor="hand2"
        ).pack(fill="x", padx=20, pady=15)

    def _build_arithmetic_controls(self, parent):
        """Membangun kontrol untuk operasi Arithmetic."""

        card = tk.Frame(parent, bg=C.PANEL,
                        highlightthickness=1,
                        highlightbackground=C.BORDER)
        card.pack(fill="x", padx=20, pady=(0, 14))

        tk.Label(card, text="MODE OPERASI", bg=C.PANEL,
                 fg=C.TEXT, font=F(9, "bold")).pack(
                     anchor="w", padx=14, pady=(12, 8)
                 )

        tk.Radiobutton(
            card,
            text="Scalar Arithmetic (Satu Citra)",
            variable=self.arithmetic_mode,
            value="scalar",
            command=self._toggle_arithmetic_mode,
            bg=C.PANEL,
            fg=C.TEXT,
            activebackground=C.PANEL,
            selectcolor=C.WHITE,
            font=F(9),
            anchor="w"
        ).pack(fill="x", padx=14, pady=4)

        tk.Radiobutton(
            card,
            text="Image Arithmetic (Dua Citra)",
            variable=self.arithmetic_mode,
            value="images",
            command=self._toggle_arithmetic_mode,
            bg=C.PANEL,
            fg=C.TEXT,
            activebackground=C.PANEL,
            selectcolor=C.WHITE,
            font=F(9),
            anchor="w"
        ).pack(fill="x", padx=14, pady=4)

        # Pengaturan Scalar Arithmetic
        self.arithmetic_scalar_frame = tk.Frame(card, bg=C.PANEL)

        tk.Label(self.arithmetic_scalar_frame, text="Nilai Skalar (k)",
                 bg=C.PANEL, fg=C.TEXT, font=F(9, "bold")).pack(
                     anchor="w", padx=14, pady=(12, 5)
                 )

        tk.Entry(
            self.arithmetic_scalar_frame,
            textvariable=self.scalar_value,
            font=F(10),
            relief="solid",
            bd=1
        ).pack(fill="x", padx=14, pady=(0, 12), ipady=5)

        # Pengaturan Image Arithmetic
        self.arithmetic_image_frame = tk.Frame(card, bg=C.PANEL)

        tk.Label(self.arithmetic_image_frame, text="Citra 1",
                 bg=C.PANEL, fg=C.TEXT, font=F(9, "bold")).pack(
                     anchor="w", padx=14, pady=(12, 3)
                 )

        tk.Label(
            self.arithmetic_image_frame,
            text="Menggunakan citra yang sedang aktif.",
            bg=C.PANEL,
            fg=C.MUTED,
            font=F(8),
            wraplength=290,
            justify="left"
        ).pack(anchor="w", padx=14)

        tk.Label(self.arithmetic_image_frame, text="Citra 2",
                 bg=C.PANEL, fg=C.TEXT, font=F(9, "bold")).pack(
                     anchor="w", padx=14, pady=(12, 5)
                 )

        self.second_image_label = tk.Label(
            self.arithmetic_image_frame,
            text="Belum ada citra kedua",
            bg=C.WHITE,
            fg=C.MUTED,
            font=F(8),
            anchor="w",
            padx=10,
            pady=9
        )
        self.second_image_label.pack(fill="x", padx=14, pady=(0, 8))

        FlatButton(
            self.arithmetic_image_frame,
            "＋  Pilih Citra Kedua",
            self._choose_second_image,
            bg=C.WHITE,
            fg=C.PRIMARY,
            hover=C.PRIMARY_SOFT
        ).pack(fill="x", padx=14, pady=(0, 12))

        self._toggle_arithmetic_mode()

    def _toggle_arithmetic_mode(self):
        """Menampilkan pengaturan sesuai mode Arithmetic."""

        self.arithmetic_scalar_frame.pack_forget()
        self.arithmetic_image_frame.pack_forget()

        if self.arithmetic_mode.get() == "scalar":
            self.arithmetic_scalar_frame.pack(fill="x", pady=(4, 0))
        else:
            self.arithmetic_image_frame.pack(fill="x", pady=(4, 0))

    
    def _build_boolean_controls(self, parent):
        """Membuat kontrol untuk operasi Boolean."""

        if self.active_operation == "not":
            self.boolean_image2 = None

            self._add_info_card(
                "Boolean NOT",
                "Membalik nilai piksel citra utama menggunakan "
                "operasi bitwise NOT."
            )
            return

        self.boolean_image2 = None

        self._add_info_card(
            "Boolean Operation",
            "Pilih citra kedua untuk melakukan operasi "
            "Boolean terhadap citra utama."
        )

        self.boolean_image2_label = tk.Label(
            parent,
            text="Belum ada citra kedua",
            anchor="w"
        )
        self.boolean_image2_label.pack(
            fill="x",
            padx=10,
            pady=5
        )

        tk.Button(
            parent,
            text="Pilih Citra Kedua",
            command=self._load_boolean_image2
        ).pack(
            fill="x",
            padx=10,
            pady=5
        )


    def _load_boolean_image2(self):
        """Memuat citra kedua untuk operasi Boolean."""

        path = filedialog.askopenfilename(
            title="Pilih Citra Kedua",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
            ]
        )

        if not path:
            return

        try:
            self.boolean_image2 = Image.open(path).convert("RGB")

            self.boolean_image2_label.config(
                text=f"Citra kedua: {path.split('/')[-1]}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Gagal membuka citra:\n{e}"
            )

    def _build_convolution_controls(self, parent):
        self.convolution_kernel = tk.StringVar(value="sharpen")

        tk.Label(
            parent,
            text="Pilih Kernel",
            font=F(10, "bold"),
            bg=C.WHITE,
            fg=C.TEXT
        ).pack(anchor="w", padx=20, pady=(5, 8))

        kernel_options = [
            ("Identity", "identity"),
            ("Blur", "blur"),
            ("Sharpen", "sharpen"),
            ("Edge Detection", "edge"),
            ("Emboss", "emboss")
        ]

        for label, value in kernel_options:
            tk.Radiobutton(
                parent,
                text=label,
                variable=self.convolution_kernel,
                value=value,
                bg=C.WHITE,
                fg=C.TEXT,
                selectcolor=C.PANEL,
                activebackground=C.WHITE,
                activeforeground=C.TEXT,
                font=F(9)
            ).pack(anchor="w", padx=25, pady=3)
    
    def _build_thresholding_controls(self, parent):
        self.threshold_value = tk.IntVar(value=127)

        tk.Label(
            parent,
            text="Threshold Value",
            bg=C.WHITE,
            fg=C.TEXT,
            font=F(10, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        self.threshold_value_label = tk.Label(
            parent,
            text="127",
            bg=C.WHITE,
            fg=C.PRIMARY,
            font=F(11, "bold")
        )
        self.threshold_value_label.pack(anchor="w", padx=20)

        tk.Scale(
            parent,
            from_=0,
            to=255,
            orient="horizontal",
            variable=self.threshold_value,
            command=lambda value: self.threshold_value_label.config(
                text=str(int(float(value)))
            ),
            bg=C.WHITE,
            fg=C.TEXT,
            highlightthickness=0,
            troughcolor=C.BORDER
        ).pack(fill="x", padx=20, pady=5)

        tk.Button(
            parent,
            text="Reset Threshold",
            command=lambda: self.threshold_value.set(127)
        ).pack(fill="x", padx=20, pady=10)



    def _choose_second_image(self):
        """Memilih citra kedua untuk Image Arithmetic."""

        if not PIL_OK:
            messagebox.showerror(
                "Pillow belum terpasang",
                "Jalankan perintah: pip install pillow"
            )
            return

        path = filedialog.askopenfilename(
            title="Pilih Citra Kedua",
            filetypes=[
                ("Gambar", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
                ("Semua file", "*.*"),
            ]
        )
        if not path:
            return

        try:
            image = Image.open(path).convert("RGB")
            self.second_image = image.copy()
            self.second_image_path = path

            if self.second_image_label is not None:
                self.second_image_label.config(
                    text=os.path.basename(path),
                    fg=C.TEXT
                )
        except Exception as exc:
            messagebox.showerror("Gagal membuka citra kedua", str(exc))

    # --------------------------------------------------------
    # OPERASI CITRA
    # --------------------------------------------------------
    def upload_image(self):
        if not PIL_OK:
            messagebox.showerror(
                "Pillow belum terpasang",
                "Jalankan perintah: pip install pillow"
            )
            return

        path = filedialog.askopenfilename(
            title="Pilih citra",
            filetypes=[
                ("Gambar", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
                ("Semua file", "*.*"),
            ]
        )
        if not path:
            return

        try:
            image = Image.open(path).convert("RGB")
            self.original_image = image.copy()
            self.current_image = image.copy()
            self.history.clear()
            self.second_image = None
            self.second_image_path = None
            if self.second_image_label is not None:
                self.second_image_label.config(
                    text="Belum ada citra kedua", fg=C.MUTED
                )
            self.panel_before.show_image(self.original_image)
            self.panel_after.show_image(None)
        except Exception as exc:
            messagebox.showerror("Gagal membuka gambar", str(exc))

    def apply_operation(self):

        # Binary dan Grayscale Gradient tidak membutuhkan gambar awal.
        no_image_required = (
            self.active_operation == "binary"
            or (
                self.active_operation == "grayscale"
                and self.grayscale_mode.get() == "gradient"
            )
        )

        if self.current_image is None and not no_image_required:
            messagebox.showwarning(
                "Tidak ada gambar",
                "Silakan unggah gambar terlebih dahulu."
            )
            return

        try:

            if self.active_operation == "rgb":
                result = rgb_adjustment(
                    self.current_image,
                    red=self.rgb_red.get(),
                    green=self.rgb_green.get(),
                    blue=self.rgb_blue.get()
                )

            elif self.active_operation == "binary":
                result = binary_image()

            elif self.active_operation == "negative":
                result = image_negative(self.current_image)

            elif self.active_operation == "pseudo":
                result = pseudo_color(
                    self.current_image,
                    colormap=self.pseudo_colormap.get()
                )
            elif self.active_operation == "hsv":
                channel = self.hsv_channel.get()

                if channel == "HSV":
                    selected_channel = "HSV"
                else:
                    selected_channel = channel[0]

                result = hsv_conversion(
                    self.current_image,
                    channel=selected_channel
                )

            elif self.active_operation == "flipping":
                operation = self.selected_operation.get()

                if operation == "flip_horizontal":
                    result = flip_horizontal(self.current_image)

                elif operation == "flip_vertical":
                    result = flip_vertical(self.current_image)

                elif operation == "flip_both":
                    result = flip_both(self.current_image)

                else:
                    messagebox.showwarning(
                        "Operasi tidak dikenal",
                        "Pilihan flipping tidak valid."
                    )
                    return

            elif self.active_operation == "grayscale":
                mode = self.grayscale_mode.get()

                if mode == "conversion":
                    result = grayscale_conversion(self.current_image)

                elif mode == "gradient":
                    result = grayscale_gradient(256, 256)

                else:
                    return

            elif self.active_operation == "thresholding":
                threshold_value = self.threshold_value.get()

                result = thresholding(
                    self.current_image,
                    threshold_value=threshold_value
                )

            elif self.active_operation == "convolution":
                kernel_type = self.convolution_kernel.get()
                result = convolution(
                    self.current_image,
                    kernel_type=kernel_type
                )

            elif self.active_operation == "not":
                result = boolean_not(self.current_image)

            elif self.active_operation == "and":
                if self.boolean_image2 is None:
                    messagebox.showwarning(
                        "Boolean AND",
                        "Silakan pilih citra kedua terlebih dahulu."
                    )
                    return

                result = boolean_and(
                    self.current_image,
                    self.boolean_image2
                )

            elif self.active_operation == "or":
                if self.boolean_image2 is None:
                    messagebox.showwarning(
                        "Boolean OR",
                        "Silakan pilih citra kedua terlebih dahulu."
                    )
                    return

                result = boolean_or(
                    self.current_image,
                    self.boolean_image2
                )

            elif self.active_operation == "xor":
                if self.boolean_image2 is None:
                    messagebox.showwarning(
                        "Boolean XOR",
                        "Silakan pilih citra kedua terlebih dahulu."
                    )
                    return

                result = boolean_xor(
                    self.current_image,
                    self.boolean_image2
                )

            
            elif self.active_operation == "translation":
                try:
                    tx = float(self.geometric_values["tx"].get())
                    ty = float(self.geometric_values["ty"].get())
                except ValueError:
                    messagebox.showwarning(
                        "Parameter Tidak Valid",
                        "Masukkan nilai translasi berupa angka."
                    )
                    return

                result = translation(
                    self.current_image,
                    tx=tx,
                    ty=ty
                )

            elif self.active_operation == "rotation":
                try:
                    angle = float(self.geometric_values["angle"].get())
                except ValueError:
                    messagebox.showwarning(
                        "Parameter Tidak Valid",
                        "Masukkan sudut rotasi berupa angka."
                    )
                    return

                result = rotation(
                    self.current_image,
                    angle=angle
                )

            elif self.active_operation == "zooming":
                try:
                    scale_x = float(self.geometric_values["scale_x"].get())
                    scale_y = float(self.geometric_values["scale_y"].get())
                except ValueError:
                    messagebox.showwarning(
                        "Parameter Tidak Valid",
                        "Masukkan faktor skala berupa angka."
                    )
                    return

                if scale_x <= 0 or scale_y <= 0:
                    messagebox.showwarning(
                        "Parameter Tidak Valid",
                        "Faktor skala harus lebih besar dari 0."
                    )
                    return

                result = zooming(
                    self.current_image,
                    scale_x=scale_x,
                    scale_y=scale_y
                )

            elif self.active_operation == "cropping":
                try:
                    x1 = int(self.geometric_values["x1"].get())
                    y1 = int(self.geometric_values["y1"].get())
                    x2 = int(self.geometric_values["x2"].get())
                    y2 = int(self.geometric_values["y2"].get())
                except ValueError:
                    messagebox.showwarning(
                        "Parameter Tidak Valid",
                        "Koordinat cropping harus berupa bilangan bulat."
                    )
                    return

                if not (0 <= x1 < x2 <= 100):
                    messagebox.showwarning(
                        "Koordinat Tidak Valid",
                        "Pastikan 0 <= X1 < X2 <= 100."
                    )
                    return

                if not (0 <= y1 < y2 <= 100):
                    messagebox.showwarning(
                        "Koordinat Tidak Valid",
                        "Pastikan 0 <= Y1 < Y2 <= 100."
                    )
                    return

                result = cropping(
                    self.current_image,
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2
                )

            elif self.active_operation == "fourier_transform":
                result = fourier_transform(self.current_image)

            elif self.active_operation in (
                "add", "subtract", "multiply", "divide"
            ):
                operation = self.active_operation
                mode = self.arithmetic_mode.get()

                if mode == "scalar":
                    try:
                        value = float(self.scalar_value.get())
                    except ValueError:
                        messagebox.showwarning(
                            "Nilai Tidak Valid",
                            "Masukkan nilai skalar berupa angka."
                        )
                        return

                    if operation == "divide" and value == 0:
                        messagebox.showwarning(
                            "Nilai Tidak Valid",
                            "Nilai pembagi tidak boleh nol."
                        )
                        return

                    scalar_functions = {
                        "add": add_scalar,
                        "subtract": subtract_scalar,
                        "multiply": multiply_scalar,
                        "divide": divide_scalar,
                    }

                    result = scalar_functions[operation](
                        self.current_image,
                        value
                    )

                else:
                    if self.second_image is None:
                        messagebox.showwarning(
                            "Citra Kedua Belum Dipilih",
                            "Silakan pilih citra kedua terlebih dahulu."
                        )
                        return

                    image_functions = {
                        "add": add_images,
                        "subtract": subtract_images,
                        "multiply": multiply_images,
                        "divide": divide_images,
                    }

                    result = image_functions[operation](
                        self.current_image,
                        self.second_image
                    )


            else:
                messagebox.showinfo(
                    "Fitur Belum Tersedia",
                    "Operasi yang dipilih belum memiliki algoritma."
                )
                return

            # Konversi hasil operasi menjadi gambar RGB Pillow.
            result_image = Image.fromarray(
                np.asarray(result, dtype=np.uint8)
            ).convert("RGB")

            # Simpan kondisi sebelumnya untuk Undo.
            if self.current_image is not None:
                self.history.append(self.current_image.copy())

            # Perbarui gambar hasil.
            self.current_image = result_image
            self.panel_after.show_image(self.current_image)

        except Exception as exc:
            messagebox.showerror(
                "Gagal memproses gambar",
                str(exc)
            )

    def undo(self):
        if not self.history:
            messagebox.showinfo("Undo", "Belum ada operasi yang dapat dibatalkan.")
            return
        self.current_image = self.history.pop()
        self.panel_after.show_image(self.current_image)

    def reset_image(self):
        if self.original_image is None:
            messagebox.showwarning("Reset", "Belum ada citra yang diunggah.")
            return
        self.current_image = self.original_image.copy()
        self.history.clear()
        self.panel_after.show_image(None)

    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Simpan", "Belum ada hasil citra untuk disimpan.")
            return
        self.save_image_as()

    def save_image_as(self):
        if self.current_image is None:
            messagebox.showwarning("Simpan", "Belum ada hasil citra untuk disimpan.")
            return
        path = filedialog.asksaveasfilename(
            title="Simpan hasil citra",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
            ]
        )
        if not path:
            return
        try:
            self.current_image.save(path)
            messagebox.showinfo("Berhasil", "Citra hasil berhasil disimpan.")
        except Exception as exc:
            messagebox.showerror("Gagal menyimpan citra", str(exc))

    def show_code_info(self):
        messagebox.showinfo(
            "Kode Python",
            "Kode algoritma operasi akan ditampilkan di sini pada tahap pengembangan berikutnya."
        )


if __name__ == "__main__":
    app = PicLabApp()
    app.mainloop()
