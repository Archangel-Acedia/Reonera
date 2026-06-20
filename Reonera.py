# -*- coding: utf-8 -*-
# --- START OF FILE text/x-python ---
# REONERA v1.0.0 
# Expert High-Fidelity PyQt6 + OpenGL Hardware-Accelerated Architecture.
# Thread-safe UI, Cryptographic Security, Frameless Mutations, Data-Driven Companions.

import os
import sys
import subprocess
import time
import json
import random
import threading
import math
import winsound
import struct
import re

print("DEBUG: Script starting...")

APP_VERSION = "1.0.0"

def _subprocess_no_window():
    return 0  # Force this to 0 to show the console errors for debugging
    # if os.name == 'nt':
    #    return subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0x08000000
    # return 0

def _show_fatal_error(message):
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, str(message), "REONERA — Startup Error", 0x10)
        except Exception:
            pass
    else:
        print(message, file=sys.stderr)

def _relaunch_self(use_pythonw=False):
    """Restart this script. Uses subprocess on Windows so paths with spaces work."""
    exe = sys.executable
    if use_pythonw and os.name == 'nt':
        pythonw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        if os.path.isfile(pythonw):
            exe = pythonw
    if os.name == 'nt':
        flags = _subprocess_no_window()
        subprocess.Popen([exe] + sys.argv, creationflags=flags)
        sys.exit(0)
    os.execv(exe, [exe] + sys.argv)

def _detach_console_on_windows():
    """Re-launch under pythonw.exe so no CMD window appears for GUI flows."""
    # Completely disabled to prevent startup issues
    return

# _detach_console_on_windows()  # Commented out to prevent relaunch

# ==========================================
# 0. SILENT PYQT6 BOOTSTRAP (If Missing)
# ==========================================
try:
    from PyQt6.QtWidgets import QApplication
except ImportError:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "PyQt6", "PyOpenGL"],
            creationflags=_subprocess_no_window(),
        )
        _relaunch_self()
    except Exception as e:
        _show_fatal_error(f"Critical Bootstrap Failure:\n{e}")
        sys.exit(1)

# ==========================================
# POST-BOOTSTRAP IMPORTS
# ==========================================
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, 
                             QCheckBox, QTextEdit, QLineEdit, QDialog,
                             QTabWidget, QGridLayout, QFileDialog, QSystemTrayIcon, 
                             QMenu, QMessageBox, QSizeGrip, QButtonGroup,
                             QFormLayout, QScrollArea, QGroupBox, QFrame, QSizePolicy)
from PyQt6.QtCore import (Qt, QTimer, QThread, pyqtSignal, QPoint, QRect, QSize, QEvent)
from PyQt6.QtGui import (QColor, QPainter, QPen, QFont, QIcon, QAction, QPixmap, QImage, QPainterPath)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram, QOpenGLTexture, QOpenGLFramebufferObject

# ==========================================
# PYTABLERICONS INTEGRATION FOR HIGH-END UI VECTORS
# ==========================================
try:
    from pytablericons import TablerIcon
    PYTABLER_AVAILABLE = True
except ImportError:
    PYTABLER_AVAILABLE = False

class IconRenderer:
    """Elite vector icon renderer with theme adaptation and graceful fallback."""
    
    ICON_MAP = {
        'refresh': 'REFRESH',
        'zone': 'BOX_MARGIN',
        'target': 'CROSSHAIR',
        'exclude': 'CIRCLE_X',
        'lock': 'LOCK',
        'clear': 'TRASH',
        'settings': 'SETTINGS',
        'about': 'INFO_CIRCLE',
        'compact': 'MINIMIZE',
        'close': 'X',
        'start': 'PLAY',
        'stop': 'SQUARE',
        'new': 'PLUS',
        'bake': 'BOLT',
        'deploy': 'DESKTOP',
        'test': 'PULSE',
        'save': 'DEVICE_FLOPPY',
    }
    
    default_theme_color = "#FFD700"
    
    @classmethod
    def render_icon(cls, icon_name, size=24, theme_color=None):
        """Render a vector icon with theme color adaptation."""
        if theme_color is None:
            theme_color = cls.default_theme_color
        
        if PYTABLER_AVAILABLE:
            try:
                icon_attr = cls.ICON_MAP.get(icon_name, icon_name.upper())
                icon = getattr(TablerIcon, icon_attr, None)
                if icon is not None:
                    pixmap = icon.render(size, size, theme_color)
                    return QIcon(pixmap)
            except AttributeError:
                pass
        
        # Fallback to geometric shapes
        return cls._render_fallback_icon(icon_name, size, theme_color)
    
    @classmethod
    def _render_fallback_icon(cls, icon_name, size, color):
        """Render geometric fallback icon using QPainter."""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(color), 2)
        painter.setPen(pen)
        
        center = size / 2
        margin = 4
        
        if icon_name == 'refresh':
            painter.drawEllipse(int(margin), int(margin), int(size-2*margin), int(size-2*margin))
            painter.drawLine(int(center), int(margin), int(center), int(size-margin))
            painter.drawLine(int(margin), int(center), int(size-margin), int(center))
        elif icon_name == 'zone':
            painter.drawRect(int(margin), int(margin), int(size-2*margin), int(size-2*margin))
        elif icon_name == 'target':
            painter.drawLine(int(margin), int(center), int(size-margin), int(center))
            painter.drawLine(int(center), int(margin), int(center), int(size-margin))
            painter.drawEllipse(int(center-3), int(center-3), 6, 6)
        elif icon_name == 'exclude':
            painter.drawEllipse(int(margin), int(margin), int(size-2*margin), int(size-2*margin))
            painter.drawLine(int(margin), int(margin), int(size-margin), int(size-margin))
            painter.drawLine(int(size-margin), int(margin), int(margin), int(size-margin))
        elif icon_name == 'lock':
            painter.drawRect(int(center-4), int(center), 8, 8)
            painter.drawArc(int(center-4), int(margin), 8, 8, 0, 180*16)
        elif icon_name == 'clear':
            painter.drawRect(int(margin), int(margin), int(size-2*margin), int(size-2*margin))
            painter.drawLine(int(margin), int(margin), int(size-margin), int(size-margin))
        elif icon_name == 'settings':
            painter.drawEllipse(int(center-6), int(center-6), 12, 12)
            painter.drawEllipse(int(center-3), int(center-3), 6, 6)
        elif icon_name == 'about':
            painter.drawEllipse(int(center-6), int(center-6), 12, 12)
            painter.drawText(int(margin), int(size-margin), "i")
        elif icon_name == 'compact':
            painter.drawLine(int(margin), int(center), int(size-margin), int(center))
        elif icon_name == 'close':
            painter.drawLine(int(margin), int(margin), int(size-margin), int(size-margin))
            painter.drawLine(int(size-margin), int(margin), int(margin), int(size-margin))
        elif icon_name == 'start':
            path = QPainterPath()
            path.moveTo(int(margin), int(margin))
            path.lineTo(int(size-margin), int(center))
            path.lineTo(int(margin), int(size-margin))
            path.closeSubpath()
            painter.drawPath(path)
        elif icon_name == 'stop':
            painter.drawRect(int(margin), int(margin), int(size-2*margin), int(size-2*margin))
        elif icon_name == 'new':
            painter.drawLine(int(center), int(margin), int(center), int(size-margin))
            painter.drawLine(int(margin), int(center), int(size-margin), int(center))
        elif icon_name == 'bake':
            painter.drawEllipse(int(center-4), int(center-4), 8, 8)
            painter.drawLine(int(center), int(margin), int(center), int(size-margin))
        elif icon_name == 'deploy':
            painter.drawRect(int(margin), int(center-2), int(size-2*margin), 4)
            painter.drawLine(int(center), int(center-2), int(center), int(margin))
        elif icon_name == 'test':
            painter.drawEllipse(int(center-3), int(center-3), 6, 6)
            painter.drawEllipse(int(margin), int(margin), 4, 4)
            painter.drawEllipse(int(size-margin-4), int(size-margin-4), 4, 4)
        elif icon_name == 'save':
            painter.drawRect(int(margin), int(center-2), int(size-2*margin), 8)
            painter.drawRect(int(center-2), int(margin), 4, 4)
        
        painter.end()
        return QIcon(pixmap)
    
    @classmethod
    def set_theme_color(cls, color):
        """Set the default theme color for icon rendering."""
        cls.default_theme_color = color

# ==========================================
# 0.5 BRAND ICONS & WINDOWS APP IDENTITY
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.argv[0]))
_WINDOWS_APP_ID_SET = False

def _ensure_windows_app_id():
    global _WINDOWS_APP_ID_SET
    if _WINDOWS_APP_ID_SET or os.name != 'nt':
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("reonera.engine.v1")
        _WINDOWS_APP_ID_SET = True
    except Exception:
        pass

def _brand_logo_path():
    return os.path.join(ASSETS_DIR, 'logo.png')

def _brand_ico_path():
    return os.path.join(ASSETS_DIR, 'icon.ico')

def load_brand_pixmap(size):
    logo_path = _brand_logo_path()
    if not os.path.exists(logo_path):
        print(f"WARNING: Brand logo not found at {logo_path}. Using fallback.")
        fallback = QPixmap(size, size)
        fallback.fill(Qt.GlobalColor.transparent)
        return fallback
    pixmap = QPixmap(logo_path)
    if pixmap.isNull():
        print(f"WARNING: Failed to load brand logo from {logo_path}. Using fallback.")
        fallback = QPixmap(size, size)
        fallback.fill(Qt.GlobalColor.transparent)
        return fallback
    return pixmap.scaled(
        size, size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )

def load_brand_icon():
    ico_path = _brand_ico_path()
    if os.path.exists(ico_path):
        icon = QIcon(ico_path)
        if not icon.isNull():
            return icon
    logo_path = _brand_logo_path()
    if not os.path.exists(logo_path):
        print(f"WARNING: Brand icon not found at {ico_path}. Using transparent fallback.")
        return QIcon()
    icon = QIcon()
    for size in (16, 24, 32, 48, 64, 128, 256):
        pixmap = load_brand_pixmap(size)
        if not pixmap.isNull():
            icon.addPixmap(pixmap)
    if icon.isNull():
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            icon = QIcon(pixmap)
    return icon

def apply_brand_icon_to_window(window):
    """Re-apply brand icon after native handle changes (frameless flag updates on Windows)."""
    icon = load_brand_icon()
    window.setWindowIcon(icon)
    app = QApplication.instance()
    if app:
        app.setWindowIcon(icon)

def load_tray_icon():
    icon = QIcon()
    for size in (16, 32):
        icon.addPixmap(load_brand_pixmap(size))
    return icon

def _center_on_screen(widget):
    screen = QApplication.primaryScreen()
    if not screen:
        return
    geo = screen.availableGeometry()
    widget.move(
        geo.center().x() - widget.width() // 2,
        geo.center().y() - widget.height() // 2,
    )

PKG_ESTIMATE_MB = {
    'pyautogui': 0.3, 'pillow': 12, 'requests': 1, 'pygetwindow': 0.1, 'pywin32': 15,
    'opencv-python': 45, 'numpy': 20, 'scikit-image': 30, 'plyer': 0.5, 'cryptography': 5,
    'pystray': 0.2, 'PyQt6': 25, 'PyOpenGL': 1,
}

def _format_bytes(num_bytes):
    if num_bytes >= 1024 ** 3:
        return f"{num_bytes / (1024 ** 3):.1f} GB"
    if num_bytes >= 1024 ** 2:
        return f"{num_bytes / (1024 ** 2):.1f} MB"
    return f"{max(1, num_bytes / 1024):.0f} KB"

def _static_size_estimate(packages):
    return int(sum(PKG_ESTIMATE_MB.get(pkg, 5) for pkg in packages) * 1024 * 1024)

def _parse_pip_download_size(output):
    total = 0
    for match in re.finditer(r'\(([\d.]+)\s*(MB|KB|GB|kB|mb|gb)\)', output, re.IGNORECASE):
        val = float(match.group(1))
        unit = match.group(2).upper()
        if unit in ('KB', 'KIB'):
            total += int(val * 1024)
        elif unit in ('MB', 'MIB'):
            total += int(val * 1024 * 1024)
        elif unit in ('GB', 'GIB'):
            total += int(val * 1024 * 1024 * 1024)
    return total

_ensure_windows_app_id()

# ==========================================
# 1. THE ASSET ENGINE & AUTOMATED MIGRATION
# ==========================================
WORKSPACE = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.argv[0]))
REONERA_DIR = os.path.join(WORKSPACE, "reonera")
ASSETS_DIR = os.path.join(REONERA_DIR, "assets")
COMPANION_DIR = os.path.join(ASSETS_DIR, "companion")
BG_DIR = os.path.join(ASSETS_DIR, "background")
BS_FILE = os.path.join(REONERA_DIR, ".bootstrapped")

THEMES = {
    "The Eternal Ouroboros": {"bg": "#05050A", "fg": "#FFD700", "warn": "#00FF87", "btn": "#0F0E17", "text_bg": "#0A0A0F", "font": "Arial", "shader": 0},
    "The Shattered Basalt Crags": {"bg": "#242526", "fg": "#8A95A5", "warn": "#FFD700", "btn": "#1A1B1C", "text_bg": "#1E1F20", "font": "Arial", "shader": 1},
    "The Cyberpunk Glitch Matrix": {"bg": "#000000", "fg": "#00F0FF", "warn": "#FF007F", "btn": "#111111", "text_bg": "#0A0A0A", "font": "Consolas", "shader": 2},
    "The Ethereal Stratus Clouds": {"bg": "#FAF9F6", "fg": "#A0C4FF", "warn": "#FFB000", "btn": "#E8F0FE", "text_bg": "#FFFFFF", "font": "Segoe UI", "shader": 3},
    "Volcanic Magma": {"bg": "#1A0F0F", "fg": "#FF4500", "warn": "#FFD700", "btn": "#3E1300", "text_bg": "#0D0404", "font": "Arial", "shader": 4},
    "Aquatic Abyssal": {"bg": "#020B14", "fg": "#00F0FF", "warn": "#00FFaa", "btn": "#04203A", "text_bg": "#01050A", "font": "Verdana", "shader": 5},
    "Robotic Futuristic": {"bg": "#2A2E33", "fg": "#FFA500", "warn": "#FF4500", "btn": "#414751", "text_bg": "#1D1F23", "font": "Impact", "shader": 6},
    "Bio-Sustained Nature": {"bg": "#1B3B2B", "fg": "#8FBC8F", "warn": "#FFD700", "btn": "#2C5C43", "text_bg": "#11261B", "font": "Georgia", "shader": 7},
    "The Deep Space Nebula": {"bg": "#020208", "fg": "#A124FF", "warn": "#FF007F", "btn": "#0C071A", "text_bg": "#06030F", "font": "Segoe UI", "shader": 8},
    "Steampunk Brass Gauge": {"bg": "#2B1E13", "fg": "#D4AF37", "warn": "#FF8C00", "btn": "#4A3525", "text_bg": "#1A120A", "font": "Times New Roman", "shader": 9},
}

def generate_qss(colors, theme_name=None):
    """Recursive Stylsheet Core Cascading Matrix with Dynamic Theme Asset Support"""
    # Check for theme-specific UI assets
    border_corner = ""
    button_normal = ""
    button_hover = ""
    button_disabled = ""
    input_border = ""
    
    if theme_name:
        theme_folder = "".join(x for x in theme_name if x.isalnum() or x in " -_")
        ui_dir = os.path.join(BG_DIR, theme_folder, "ui")
        
        if os.path.exists(ui_dir):
            corner_path = os.path.join(ui_dir, "border_corner.png")
            btn_norm_path = os.path.join(ui_dir, "button_normal.png")
            btn_hover_path = os.path.join(ui_dir, "button_hover.png")
            btn_disabled_path = os.path.join(ui_dir, "button_disabled.png")
            input_border_path = os.path.join(ui_dir, "input_border.png")
            
            if os.path.exists(corner_path):
                border_corner = f"border-image: url({corner_path});"
            if os.path.exists(btn_norm_path):
                button_normal = f"background-image: url({btn_norm_path}); background-repeat: no-repeat; background-position: center;"
            if os.path.exists(btn_hover_path):
                button_hover = f"background-image: url({btn_hover_path}); background-repeat: no-repeat; background-position: center;"
            if os.path.exists(btn_disabled_path):
                button_disabled = f"background-image: url({btn_disabled_path}); background-repeat: no-repeat; background-position: center;"
            if os.path.exists(input_border_path):
                input_border = f"border-image: url({input_border_path});"
    
    # Build QSS with asset fallbacks
    return f"""
    * {{ font-family: '{colors['font']}'; color: {colors['fg']}; outline: none; }}
    QWidget {{ background-color: transparent; }}
    QMainWindow, QDialog, QMessageBox {{ background-color: {colors['bg']}; border: 2px solid {colors['fg']}; {border_corner} }}
    QComboBox {{
        background-color: {colors['text_bg']};
        border: 2px solid {colors['fg']};
        padding: 6px 36px 6px 12px;
        color: {colors['fg']};
        border-radius: 6px;
        min-height: 32px;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 28px;
        border-left: 1px solid {colors['fg']};
    }}
    QComboBox QAbstractItemView {{
        background-color: {colors['text_bg']};
        color: {colors['fg']};
        selection-background-color: {colors['warn']};
        selection-color: #000000;
        border: 1px solid {colors['fg']};
        outline: none;
        padding: 4px;
    }}
    QTextEdit, QLineEdit {{ background-color: {colors['text_bg']}; border: 2px solid {colors['fg']}; {input_border} padding: 8px; color: {colors['fg']}; border-radius: 6px; }}
    QPushButton {{ background-color: {colors['btn']}; border: 2px solid {colors['fg']}; border-radius: 8px; padding: 10px 16px; font-weight: bold; color: {colors['fg']}; {button_normal} }}
    QPushButton:hover {{ background-color: {colors['warn']}; color: #000000; {button_hover} }}
    QPushButton:disabled {{ background-color: #555555; color: #888888; border: 2px solid #555555; {button_disabled} }}
    QProgressBar {{ border: 2px solid {colors['fg']}; text-align: center; color: white; background-color: {colors['text_bg']}; border-radius: 6px; }}
    QProgressBar::chunk {{ background-color: {colors['warn']}; }}
    QTabWidget::pane {{ border: 2px solid {colors['fg']}; background: {colors['bg']}; border-radius: 8px; }}
    QTabBar::tab {{ background: {colors['btn']}; color: {colors['fg']}; padding: 10px 16px; border: 2px solid {colors['fg']}; margin-right: 4px; border-radius: 6px 6px 0 0; }}
    QTabBar::tab:selected {{ background: {colors['warn']}; color: #000; }}
    QLabel {{ padding: 4px; }}
    QGroupBox {{
        border: 1px solid {colors['fg']};
        border-radius: 8px;
        margin-top: 10px;
        padding: 12px 10px 10px 10px;
        font-weight: bold;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 6px;
        color: {colors['fg']};
    }}
    """

# Prepare Directory Scaffolding & Demo Manifests
for d in [REONERA_DIR, ASSETS_DIR, COMPANION_DIR, BG_DIR]:
    os.makedirs(d, exist_ok=True)
for t_name in THEMES.keys():
    theme_folder = "".join(x for x in t_name if x.isalnum() or x in " -_")
    theme_path = os.path.join(BG_DIR, theme_folder)
    ui_path = os.path.join(theme_path, "ui")
    os.makedirs(theme_path, exist_ok=True)
    os.makedirs(ui_path, exist_ok=True)

# ==========================================
# 1.5 AUTO-MANIFEST COMPILER THREAD
# ==========================================
def get_png_dimensions(filepath):
    """Extremely fast, zero-dependency PNG Header Sniper via struct byte extraction."""
    try:
        with open(filepath, 'rb') as f:
            signature = f.read(8)
            if signature != b'\x89PNG\r\n\x1a\n':
                return None, None
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    break
                length, chunk_type = struct.unpack('>I4s', chunk_header)
                if chunk_type == b'IHDR':
                    data = f.read(13)
                    width, height = struct.unpack('>II', data[:8])
                    return width, height
                else:
                    f.seek(length + 4, 1) # Skip data + CRC
    except Exception:
        return None, None
    return None, None

def _scan_companion_png_animations(d_path):
    """Scan all PNG sprite sheets in a companion folder and build animation metadata."""
    png_files = sorted(
        f for f in os.listdir(d_path)
        if f.lower().endswith('.png') and not f.startswith('.')
    )
    if not png_files:
        return None

    animations = {}
    frame_w, frame_h = 64, 64

    for png_file in png_files:
        img_path = os.path.join(d_path, png_file)
        w, h = get_png_dimensions(img_path)
        if w is None or h is None or h <= 0:
            continue
        frames = max(1, w // h)
        fw = w // frames
        anim_key = os.path.splitext(png_file)[0].lower()
        animations[anim_key] = {
            "frames": list(range(frames)),
            "speed": 150,
            "source": png_file,
        }
        if len(animations) == 1:
            frame_w, frame_h = fw, h

    if not animations:
        return None

    return {
        "width": frame_w,
        "height": frame_h,
        "animations": animations,
    }

def rebuild_companion_manifests(force=False):
    """Regenerate companion manifest.json files from PNG sprite sheets."""
    rebuilt = 0
    if not os.path.exists(COMPANION_DIR):
        return rebuilt
    for d in os.listdir(COMPANION_DIR):
        d_path = os.path.join(COMPANION_DIR, d)
        if not os.path.isdir(d_path):
            continue
        m_path = os.path.join(d_path, 'manifest.json')
        if os.path.exists(m_path) and not force:
            continue
        try:
            scanned = _scan_companion_png_animations(d_path)
            if scanned:
                manifest = {
                    "name": d.capitalize(),
                    "width": scanned["width"],
                    "height": scanned["height"],
                    "animations": scanned["animations"],
                    "auto_generated": True,
                }
            else:
                manifest = {
                    "name": d.capitalize(),
                    "width": 64,
                    "height": 64,
                    "animations": {"idle": {"frames": [0], "speed": 150}},
                    "auto_generated": True,
                }
            with open(m_path, 'w') as f:
                json.dump(manifest, f, indent=4)
            rebuilt += 1
        except Exception:
            pass
    return rebuilt

class CompanionCompilerThread(QThread):
    companions_ready = pyqtSignal(list)
    
    def run(self):
        valid_companions = ["Off"]
        try:
            if not os.path.exists(COMPANION_DIR):
                self.companions_ready.emit(valid_companions)
                return
                
            for d in os.listdir(COMPANION_DIR):
                d_path = os.path.join(COMPANION_DIR, d)
                if not os.path.isdir(d_path):
                    continue
                
                # Preserve raw casing - do NOT force .lower() conversion
                m_path = os.path.join(d_path, 'manifest.json')

                if os.path.exists(m_path):
                    # Cache Bypass: JSON exists, skip massive PNG loads.
                    valid_companions.append(d)
                    continue

                try:
                    scanned = _scan_companion_png_animations(d_path)
                    if scanned:
                        manifest = {
                            "name": d.capitalize(),
                            "width": scanned["width"],
                            "height": scanned["height"],
                            "animations": scanned["animations"],
                            "auto_generated": True,
                        }
                    else:
                        manifest = {
                            "name": d.capitalize(),
                            "width": 64,
                            "height": 64,
                            "animations": {
                                "idle": {"frames": [0], "speed": 150}
                            },
                            "auto_generated": True,
                            "source_image": None,
                        }

                    with open(m_path, 'w') as f:
                        json.dump(manifest, f, indent=4)
                    valid_companions.append(d)
                except Exception as e:
                    try:
                        minimal_manifest = {
                            "name": d.capitalize(),
                            "width": 64,
                            "height": 64,
                            "animations": {
                                "idle": {"frames": [0], "speed": 150}
                            },
                            "auto_generated": True,
                            "generation_error": str(e),
                        }
                        with open(m_path, 'w') as f:
                            json.dump(minimal_manifest, f, indent=4)
                        valid_companions.append(d)
                    except Exception:
                        pass
        except Exception:
            pass
            
        self.companions_ready.emit(valid_companions)

# ==========================================
# 2. PRE-FLIGHT DEPENDENCY GATE
# ==========================================
ENGINE_DEPS = {
    'pyautogui': 'pyautogui', 'PIL': 'pillow', 'requests': 'requests',
    'pygetwindow': 'pygetwindow', 'win32gui': 'pywin32', 'win32com': 'pywin32',
    'cv2': 'opencv-python', 'numpy': 'numpy', 'skimage': 'scikit-image',
    'plyer': 'plyer', 'cryptography': 'cryptography', 'pystray': 'pystray',
    'pytablericons': 'pytablericons',
}

# Critical dependencies that the app cannot run without
CRITICAL_DEPS = {
    'PyQt6': 'PyQt6',
}

# Optional dependencies with fallback mechanisms
OPTIONAL_DEPS = {
    'pyautogui': 'pyautogui', 'PIL': 'pillow', 'requests': 'requests',
    'pygetwindow': 'pygetwindow', 'win32gui': 'pywin32', 'win32com': 'pywin32',
    'cv2': 'opencv-python', 'numpy': 'numpy', 'skimage': 'scikit-image',
    'plyer': 'plyer', 'cryptography': 'cryptography', 'pystray': 'pystray',
    'pytablericons': 'pytablericons',
}

class SizeEstimateWorker(QThread):
    size_ready = pyqtSignal(int)

    def __init__(self, packages):
        super().__init__()
        self.packages = packages

    def run(self):
        fallback = _static_size_estimate(self.packages)
        try:
            cmd = [sys.executable, "-m", "pip", "install", "--dry-run", "--ignore-installed"] + self.packages
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                creationflags=_subprocess_no_window(),
                timeout=180,
            )
            parsed = _parse_pip_download_size(proc.stdout + proc.stderr)
            self.size_ready.emit(parsed if parsed > 0 else fallback)
        except Exception:
            self.size_ready.emit(fallback)

class InstallWorker(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(bool)
    
    def __init__(self, packages):
        super().__init__()
        self.packages = packages
        
    def run(self):
        try:
            self.log_signal.emit(f"Installing packages: {', '.join(self.packages)}")
            # Use --only-binary :all: to prevent building from source (fixes pygame build failures)
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--only-binary", ":all:"] + self.packages
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=0,  # Show console for debugging
            )
            output_lines = []
            for line in iter(proc.stdout.readline, ''):
                if line:
                    output_lines.append(line.strip())
                    self.log_signal.emit(line.strip())
            proc.stdout.close()
            return_code = proc.wait()
            
            if return_code != 0:
                self.log_signal.emit(f"Installation failed with return code {return_code}")
                self.log_signal.emit("Last 10 lines of output:")
                for line in output_lines[-10:]:
                    self.log_signal.emit(f"  {line}")
                self.log_signal.emit("Retrying without --only-binary flag...")
                
                # Retry without --only-binary flag as fallback
                cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + self.packages
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=0,
                )
                output_lines = []
                for line in iter(proc.stdout.readline, ''):
                    if line:
                        output_lines.append(line.strip())
                        self.log_signal.emit(line.strip())
                proc.stdout.close()
                return_code = proc.wait()
                
                if return_code != 0:
                    self.log_signal.emit(f"Retry also failed with return code {return_code}")
                    self.log_signal.emit("Last 10 lines of output:")
                    for line in output_lines[-10:]:
                        self.log_signal.emit(f"  {line}")
            
            self.done_signal.emit(return_code == 0)
        except FileNotFoundError:
            self.log_signal.emit("ERROR: Python executable not found. Please check your Python installation.")
            self.done_signal.emit(False)
        except PermissionError:
            self.log_signal.emit("ERROR: Permission denied. Try running as administrator.")
            self.done_signal.emit(False)
        except Exception as e:
            self.log_signal.emit(f"Process Exception: {str(e)}")
            self.log_signal.emit(f"Error type: {type(e).__name__}")
            self.done_signal.emit(False)

class RotatingLogoLoader(QWidget):
    LOADER_SIZE = 80

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.LOADER_SIZE, self.LOADER_SIZE)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._angle = 0
        self._pixmap = load_brand_pixmap(self.LOADER_SIZE)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def _tick(self):
        self._angle = (self._angle + 6) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._angle)
        painter.drawPixmap(
            -self._pixmap.width() // 2,
            -self._pixmap.height() // 2,
            self._pixmap,
        )

    def stop(self):
        self._timer.stop()

class FramelessDraggableDialog(QDialog):
    """Frameless branded dialog that can be dragged and sent to the background."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start = None
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_start is not None and event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self._drag_start
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._drag_start = event.globalPosition().toPoint()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_start = None
        super().mouseReleaseEvent(event)

class DependencyConsentDialog(FramelessDraggableDialog):
    def __init__(self, packages, reason_text):
        super().__init__()
        self.packages = packages
        self.setWindowIcon(load_brand_icon())
        self.setFixedSize(520, 360)
        self.setStyleSheet(generate_qss(THEMES["The Eternal Ouroboros"]))

        lay = QVBoxLayout(self)
        title = QLabel("REONERA — Dependency Setup")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)

        lay.addWidget(RotatingLogoLoader(), alignment=Qt.AlignmentFlag.AlignCenter)

        self.reason_lbl = QLabel(reason_text)
        self.reason_lbl.setWordWrap(True)
        self.reason_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.reason_lbl)

        pkg_text = ", ".join(packages) if len(packages) <= 6 else ", ".join(packages[:6]) + f", +{len(packages) - 6} more"
        self.pkg_lbl = QLabel(f"Packages: {pkg_text}")
        self.pkg_lbl.setWordWrap(True)
        self.pkg_lbl.setFont(QFont("Consolas", 9))
        lay.addWidget(self.pkg_lbl)

        self.size_lbl = QLabel(
            f"Estimated download size: ~{_format_bytes(_static_size_estimate(packages))} (calculating precise size...)"
        )
        self.size_lbl.setWordWrap(True)
        self.size_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.size_lbl)

        btn_lay = QHBoxLayout()
        self.btn_install = QPushButton("Install Dependencies")
        self.btn_cancel = QPushButton("Not Now")
        self.btn_install.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        btn_lay.addWidget(self.btn_install)
        btn_lay.addWidget(self.btn_cancel)
        lay.addLayout(btn_lay)

        _center_on_screen(self)

        self._estimator = SizeEstimateWorker(packages)
        self._estimator.size_ready.connect(self._on_size_ready)
        self._estimator.start()

    def _on_size_ready(self, num_bytes):
        self.size_lbl.setText(f"Estimated download size: ~{_format_bytes(num_bytes)}")

class StartupSplash(FramelessDraggableDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(load_brand_icon())
        self.setFixedSize(400, 200)
        self.setStyleSheet(generate_qss(THEMES["The Eternal Ouroboros"]))
        
        lay = QVBoxLayout(self)
        title = QLabel("REONERA")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        lay.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.loader = RotatingLogoLoader()
        lay.addWidget(self.loader, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.status_lbl = QLabel("Initializing...")
        self.status_lbl.setFont(QFont("Consolas", 10))
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.status_lbl)

        _center_on_screen(self)
        
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_status)
        self._timer.start(100)
        self._elapsed = 0
        self._splash_duration = 5000  # 5 seconds

    def _update_status(self):
        self._elapsed += 100
        if self._elapsed < 1500:
            self.status_lbl.setText("Initializing...")
        elif self._elapsed < 3000:
            self.status_lbl.setText("Starting Reonera...")
        elif self._elapsed < 4500:
            self.status_lbl.setText("Loading engine...")
        else:
            self.status_lbl.setText("Ready")
        
        if self._elapsed >= self._splash_duration:
            self._timer.stop()
            self.loader.stop()
            self.accept()

class SplashInstaller(FramelessDraggableDialog):
    def __init__(self, packages):
        super().__init__()
        self.packages = packages
        self.setWindowIcon(load_brand_icon())
        self.setFixedSize(500, 260)
        self.setStyleSheet(generate_qss(THEMES["The Eternal Ouroboros"]))
        
        lay = QVBoxLayout(self)
        title = QLabel("REONERA Initialization & Security Update")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        lay.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.loader = RotatingLogoLoader()
        lay.addWidget(self.loader, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.log_lbl = QLabel("Preparing engine matrices...")
        self.log_lbl.setFont(QFont("Consolas", 9))
        self.log_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.log_lbl)

        _center_on_screen(self)

        self.worker = InstallWorker(self.packages)
        self.worker.log_signal.connect(lambda msg: self.log_lbl.setText(msg[-72:]))

    def start_installation(self):
        self.worker.done_signal.connect(self.on_complete)
        self.worker.start()

    def on_complete(self, success):
        self.loader.stop()
        if success:
            try:
                with open(BS_FILE, 'w') as f:
                    f.write(APP_VERSION)
                self.log_lbl.setText("Installation complete. Restarting REONERA...")
                QApplication.processEvents()
                # Delay relaunch to ensure file is written
                QTimer.singleShot(1000, _relaunch_self)
            except Exception as e:
                self.log_lbl.setText(f"Failed to write bootstrap file: {e}")
        else:
            self.log_lbl.setText("Installation failed. Check console for details. Try running as administrator.")

def run_preflight_gate():
    # Force dependency check on every launch to catch missing packages
    missing_critical = []
    missing_optional = []
    
    # Check critical dependencies
    for mod, pkg in CRITICAL_DEPS.items():
        try:
            __import__(mod)
        except ImportError:
            missing_critical.append(pkg)
    
    # Check optional dependencies
    for mod, pkg in OPTIONAL_DEPS.items():
        try:
            __import__(mod)
        except ImportError:
            missing_optional.append(pkg)

    # Handle critical dependencies - must install to run
    if missing_critical:
        _ensure_windows_app_id()
        app = QApplication.instance() or QApplication(sys.argv)
        app.setWindowIcon(load_brand_icon())

        packages = sorted(set(missing_critical))
        reason = "CRITICAL: REONERA cannot run without these core dependencies."

        consent = DependencyConsentDialog(packages, reason)
        if consent.exec() != QDialog.DialogCode.Accepted:
            QMessageBox.warning(
                None,
                "REONERA",
                "REONERA cannot start without critical dependencies.\nYou can run the application again when you are ready to install them.",
            )
            sys.exit(0)

        splash = SplashInstaller(packages)
        splash.show()
        QApplication.processEvents()
        splash.start_installation()
        splash.exec()
        sys.exit(0)
    
    # Handle optional dependencies - can run with fallbacks
    if missing_optional:
        _ensure_windows_app_id()
        app = QApplication.instance() or QApplication(sys.argv)
        app.setWindowIcon(load_brand_icon())

        packages = sorted(set(missing_optional))
        reason = "Some optional REONERA engine packages are missing. The app will run with limited functionality."

        consent = DependencyConsentDialog(packages, reason)
        if consent.exec() == QDialog.DialogCode.Accepted:
            splash = SplashInstaller(packages)
            splash.show()
            QApplication.processEvents()
            splash.start_installation()
            splash.exec()
            sys.exit(0)
        else:
            # User chose to skip optional dependencies - warn and continue
            QMessageBox.information(
                None,
                "REONERA",
                f"REONERA will run with limited functionality.\n\nMissing optional packages:\n{', '.join(packages)}\n\nSome features may not work as expected.",
            )

    # Version check for updates
    version_match = False
    if os.path.exists(BS_FILE):
        with open(BS_FILE, 'r') as f:
            if f.read().strip() == APP_VERSION:
                version_match = True

    if not version_match:
        _ensure_windows_app_id()
        app = QApplication.instance() or QApplication(sys.argv)
        app.setWindowIcon(load_brand_icon())

        packages = sorted(set(list(ENGINE_DEPS.values())))
        reason = "REONERA has been updated and needs to refresh its engine packages."

        consent = DependencyConsentDialog(packages, reason)
        if consent.exec() != QDialog.DialogCode.Accepted:
            with open(BS_FILE, 'w') as f:
                f.write(APP_VERSION)
            return

        splash = SplashInstaller(packages)
        splash.show()
        QApplication.processEvents()
        splash.start_installation()
        splash.exec()
        sys.exit(0)

run_preflight_gate()

# --- Post-Flight Heavy Imports ---
try:
    import pyautogui
    from PIL import Image
    import pygetwindow as gw
    import win32gui
    import cv2
    import numpy as np
    from skimage.metrics import structural_similarity as ssim
    from plyer import notification
    from cryptography.fernet import Fernet
    import requests
except Exception as e:
    _show_fatal_error(f"Failed to load REONERA engine modules:\n{e}\n\nRun the dependency installer or install packages manually.")
    sys.exit(1)

if os.name == 'nt':
    from ctypes import windll, byref, c_int

# ==========================================
# 3. CRYPTO CONFIGURATION ROUTING
# ==========================================
class CryptoManager:
    KEY_FILE = os.path.join(REONERA_DIR, '.reonera.key')
    _cipher = None

    @classmethod
    def get_cipher(cls):
        if cls._cipher is None:
            if not os.path.exists(cls.KEY_FILE):
                key = Fernet.generate_key()
                with open(cls.KEY_FILE, 'wb') as f: f.write(key)
                if os.name == 'nt':
                    try: subprocess.check_call(['attrib', '+h', cls.KEY_FILE], creationflags=subprocess.CREATE_NO_WINDOW)
                    except: pass
            with open(cls.KEY_FILE, 'rb') as f: key = f.read()
            cls._cipher = Fernet(key)
        return cls._cipher

    @classmethod
    def encrypt(cls, data_dict):
        json_data = json.dumps(data_dict).encode('utf-8')
        return cls.get_cipher().encrypt(json_data).decode('utf-8')
        
    @classmethod
    def decrypt(cls, encrypted_str):
        try:
            json_data = cls.get_cipher().decrypt(encrypted_str.encode('utf-8'))
            return json.loads(json_data.decode('utf-8'))
        except Exception: return {}

# ==========================================
# 4. HARDWARE ACCELERATED SHADER CANVAS
# ==========================================
VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec2 position;
out vec2 v_uv;
void main() { 
    gl_Position = vec4(position, 0.0, 1.0); 
    v_uv = position * 0.5 + 0.5;
}
"""
# Fallback fragment mapping embedded
FRAGMENT_FALLBACK = """
#version 330 core
out vec4 FragColor;
in vec2 v_uv;
uniform int u_use_tex;
uniform sampler2D u_tex;
uniform vec3 u_color;
void main() {
    if (u_use_tex == 1) { FragColor = texture(u_tex, v_uv); }
    else { FragColor = vec4(u_color, 1.0); }
}
"""

class ShaderBackground(QOpenGLWidget):
    error_signal = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.program = None
        self.u_time = 0.0
        self.theme_id = -1
        self.particles_enabled = 1
        self.use_tex = 0
        self.texture = None
        self.fallback_color = [0.0, 0.0, 0.0]
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.pending_reload = False
        self.theme_dir = None
        self.variant_filename = None
        
        # Multi-pass rendering infrastructure
        self.shader_passes = {}  # Stores compiled shader programs for each pass
        self.buffer_fbos = {}    # Stores QOpenGLFramebufferObject for each buffer pass
        self.common_code = ""    # Common code to prepend to all passes
        self.render_passes = []  # Ordered list of render passes from JSON
        self.using_json_shader = False  # Flag to indicate if using JSON multi-pass shader
        self.channel_types = {}  # iChannel index -> sampler kind
        self.channel_textures = {}  # iChannelN placeholder textures
        self.buffer_output_ids = {}  # buffer pass name -> output id
        self._init_vertices()

    def _init_vertices(self):
        self.vertices = np.array(
            [[-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0], [1.0, 1.0]],
            dtype=np.float32,
        )

    def _image_pass_key(self):
        if "Image" in self.shader_passes:
            return "Image"
        for pass_data in self.render_passes:
            pass_name = pass_data.get("name", "")
            if pass_name == "Image" or pass_data.get("type") == "image":
                key = pass_name or "Image"
                if key in self.shader_passes:
                    return key
        if len(self.shader_passes) == 1:
            return next(iter(self.shader_passes))
        return None

    def _surface_size(self):
        dpr = max(self.devicePixelRatioF(), 1.0)
        return max(int(self.width() * dpr), 1), max(int(self.height() * dpr), 1)

    def initializeGL(self):
        import OpenGL.GL as gl
        gl.glClearColor(*self.fallback_color, 1.0)
        self.reload_assets()

    def set_custom_assets(self, theme_dir, hex_bg, variant_filename=None):
        self.theme_dir = theme_dir
        self.variant_filename = variant_filename
        self.fallback_color = [int(hex_bg[i:i+2], 16)/255.0 for i in (1, 3, 5)]
        self.pending_reload = True
        self.update()

    def cleanup_shaders(self):
        """Clean up existing shader programs and framebuffers."""
        for program in self.shader_passes.values():
            if program:
                program.release()
        self.shader_passes.clear()
        
        for fbo in self.buffer_fbos.values():
            if fbo:
                del fbo
        self.buffer_fbos.clear()

        for texture in self.channel_textures.values():
            if texture:
                texture.destroy()
        self.channel_textures.clear()
        
        self.render_passes = []
        self.common_code = ""
        self.using_json_shader = False
        self.channel_types = {}
        self.buffer_output_ids = {}

    def load_json_shader(self, json_path):
        """Load and parse JSON shader file with multi-pass support."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract renderpass array - handle both structures
            renderpass = data.get("Shader", {}).get("renderpass", [])
            if not renderpass:
                # Try direct renderpass key (Shadertoy format)
                renderpass = data.get("renderpass", [])
            
            if not renderpass:
                raise ValueError("No renderpass array found in JSON")
            
            self.render_passes = renderpass
            self._parse_channel_types()
            
            # Extract common code if present
            for pass_data in renderpass:
                if pass_data.get("name") == "Common":
                    self.common_code = pass_data.get("code", "")
                    break
            
            return True
        except Exception as e:
            self.error_signal.emit(f"[JSON ERROR] Failed to load shader JSON: {e}")
            return False

    def _parse_channel_types(self):
        """Map Shadertoy iChannel indices to sampler kinds from JSON inputs."""
        self.channel_types = {}
        self.buffer_output_ids = {}
        for pass_data in self.render_passes:
            pass_name = pass_data.get("name", "")
            for output in pass_data.get("outputs", []):
                out_id = output.get("id")
                if pass_name.startswith("Buffer") and out_id:
                    self.buffer_output_ids[pass_name] = out_id
            pass_type = pass_data.get("type", "")
            if pass_name == "Image" or pass_type == "image" or (not pass_name and len(self.render_passes) == 1):
                for inp in pass_data.get("inputs", []):
                    ch = inp.get("channel", 0)
                    inp_type = inp.get("type", "texture")
                    if inp_type == "cubemap":
                        self.channel_types[ch] = "cubemap"
                    elif inp_type == "buffer":
                        self.channel_types[ch] = "buffer"
                    else:
                        self.channel_types[ch] = "2d"

    def _channel_uniform_line(self, channel_idx, channel_kind):
        if channel_kind == "cubemap":
            return f"uniform samplerCube iChannel{channel_idx};\n"
        return f"uniform sampler2D iChannel{channel_idx};\n"

    def _create_placeholder_2d(self, color):
        img = QImage(64, 64, QImage.Format.Format_RGB888)
        img.fill(QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
        texture = QOpenGLTexture(img.mirrored(False, True))
        texture.setMinificationFilter(QOpenGLTexture.Filter.Linear)
        texture.setMagnificationFilter(QOpenGLTexture.Filter.Linear)
        texture.setWrapMode(QOpenGLTexture.WrapMode.Repeat)
        return texture

    def _create_placeholder_cubemap(self, color):
        img = QImage(8, 8, QImage.Format.Format_RGB888)
        img.fill(QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
        texture = QOpenGLTexture(QOpenGLTexture.Target.TargetCubeMap)
        texture.setSize(8, 8)
        texture.setFormat(QOpenGLTexture.TextureFormat.RGB8_UNorm)
        texture.allocateStorage()
        faces = (
            QOpenGLTexture.CubeMapFace.CubeMapPositiveX,
            QOpenGLTexture.CubeMapFace.CubeMapNegativeX,
            QOpenGLTexture.CubeMapFace.CubeMapPositiveY,
            QOpenGLTexture.CubeMapFace.CubeMapNegativeY,
            QOpenGLTexture.CubeMapFace.CubeMapPositiveZ,
            QOpenGLTexture.CubeMapFace.CubeMapNegativeZ,
        )
        for face in faces:
            texture.setData(
                0, 0, face,
                QOpenGLTexture.PixelFormat.RGB,
                QOpenGLTexture.PixelType.UInt8,
                img.constBits(),
            )
        texture.setMinificationFilter(QOpenGLTexture.Filter.Linear)
        texture.setMagnificationFilter(QOpenGLTexture.Filter.Linear)
        texture.setWrapMode(QOpenGLTexture.WrapMode.ClampToEdge)
        texture.create()
        return texture

    def _prepare_channel_textures(self):
        """Create placeholder textures for external iChannel inputs declared in JSON."""
        palette = [
            (0.15, 0.35, 0.55),
            (0.35, 0.55, 0.20),
            (0.45, 0.20, 0.35),
            (0.30, 0.30, 0.30),
        ]
        for channel_idx, channel_kind in self.channel_types.items():
            if channel_kind == "buffer":
                continue
            key = f"iChannel{channel_idx}"
            if key in self.channel_textures:
                continue
            color = palette[channel_idx % len(palette)]
            try:
                if channel_kind == "cubemap":
                    self.channel_textures[key] = self._create_placeholder_cubemap(color)
                else:
                    self.channel_textures[key] = self._create_placeholder_2d(color)
            except Exception as e:
                self.error_signal.emit(f"[SHADER WARN] Channel {key} placeholder failed: {e}")

    def _bind_image_pass_channels(self, program):
        import OpenGL.GL as gl
        tex_unit = 0
        image_pass = None
        for pass_data in self.render_passes:
            if pass_data.get("name") == "Image" or pass_data.get("type") == "image":
                image_pass = pass_data
                break
        if not image_pass and len(self.render_passes) == 1:
            image_pass = self.render_passes[0]
        if not image_pass:
            return
        for inp in image_pass.get("inputs", []):
            ch = inp.get("channel", 0)
            inp_type = inp.get("type", "texture")
            inp_id = inp.get("id", "")
            uniform = f"iChannel{ch}"
            if inp_type == "buffer":
                for pass_data in self.render_passes:
                    pass_name = pass_data.get("name", "")
                    if pass_name.startswith("Buffer") and self.buffer_output_ids.get(pass_name) == inp_id:
                        fbo = self.buffer_fbos.get(pass_name)
                        if fbo:
                            gl.glActiveTexture(gl.GL_TEXTURE0 + tex_unit)
                            gl.glBindTexture(gl.GL_TEXTURE_2D, fbo.texture())
                            program.setUniformValue(uniform, tex_unit)
                            tex_unit += 1
                        break
            else:
                channel_tex = self.channel_textures.get(uniform)
                if channel_tex:
                    gl.glActiveTexture(gl.GL_TEXTURE0 + tex_unit)
                    channel_tex.bind()
                    program.setUniformValue(uniform, tex_unit)
                    tex_unit += 1
        program.setUniformValue("iMouse", 0.0, 0.0, 0.0, 0.0)

    def build_shadertoy_uniforms(self, frag_code):
        """Convert Shadertoy GLSL to compatible fragment shader with uniforms."""
        # Remove debug preprocessor directives that might be bleeding in
        frag_code = re.sub(r'#ifdef GL_KHR_blend_equation_advanced.*?#endif', '', frag_code, flags=re.DOTALL)
        frag_code = re.sub(r'#extension.*?;', '', frag_code)
        frag_code = re.sub(r'#define lowp', '', frag_code)
        frag_code = re.sub(r'#define mediump', '', frag_code)
        frag_code = re.sub(r'#define highp', '', frag_code)
        frag_code = re.sub(r'#line \d+', '', frag_code)
        
        # Replace Shadertoy uniforms with our custom uniforms (order matters: iTimeDelta before iTime)
        frag_code = re.sub(r'\biTimeDelta\b', 'u_time_delta', frag_code)
        frag_code = re.sub(r'\biTime\b', 'u_time', frag_code)
        frag_code = re.sub(r'\biFrame\b', 'u_frame', frag_code)
        frag_code = re.sub(r'\biResolution\b', '(vec3(u_resolution, 1.0))', frag_code)

        # Add Shadertoy-compatible uniforms at the top
        header = """#version 330 core
out vec4 FragColor;
in vec2 v_uv;
uniform float u_time;
uniform float u_time_delta;
uniform int u_frame;
uniform vec2 u_resolution;
uniform vec3 u_color;
uniform int u_use_tex;
uniform sampler2D u_tex;
uniform vec4 iMouse;
"""
        declared_channels = set()
        for channel_idx in sorted(self.channel_types.keys()):
            channel_kind = self.channel_types[channel_idx]
            header += self._channel_uniform_line(channel_idx, channel_kind)
            declared_channels.add(channel_idx)
        for channel_idx in range(4):
            if channel_idx not in declared_channels and f"iChannel{channel_idx}" in frag_code:
                header += self._channel_uniform_line(channel_idx, "2d")
        
        # Replace Shadertoy mainImage with main
        if "void mainImage(" in frag_code:
            frag_code = frag_code.replace("void mainImage(out vec4 fragColor, in vec2 fragCoord)",
                                          "void mainImage(out vec4 fragColor, in vec2 fragCoord)")
            frag_code = frag_code.replace("mainImage(fragColor, gl_FragCoord.xy)",
                                          "mainImage(fragColor, gl_FragCoord.xy)")
            # Add main function that calls mainImage
            if "void main()" not in frag_code:
                frag_code += "\nvoid main() {\n    vec4 fragColor;\n    mainImage(fragColor, gl_FragCoord.xy);\n    FragColor = fragColor;\n}"
        else:
            # If no mainImage, wrap existing code
            if "void main()" not in frag_code:
                frag_code += "\nvoid main() {\n    FragColor = vec4(1.0);\n}"
        
        return header + frag_code

    def compile_pass_shader(self, pass_code, pass_name):
        """Compile a shader pass with common code prepended."""
        try:
            full_code = self.common_code + "\n" + pass_code
            frag_src = self.build_shadertoy_uniforms(full_code)
            
            program = QOpenGLShaderProgram()
            program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex, VERTEX_SHADER)
            
            success = program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, frag_src)
            if not success:
                err = program.log()
                raise ValueError(f"Shader compilation failed for pass '{pass_name}': {err}")
            
            program.link()
            return program
        except Exception as e:
            self.error_signal.emit(f"[SHADER ERROR] Failed to compile pass '{pass_name}': {e}")
            return None

    def reload_assets(self):
        # Clean up existing resources
        self.cleanup_shaders()
        self._init_vertices()
        
        if self.texture:
            self.texture.destroy()
            self.texture = None
        
        self.use_tex = 0
        frag_src = FRAGMENT_FALLBACK
        
        if self.theme_dir and os.path.exists(self.theme_dir):
            try:
                target_file = None
                if getattr(self, 'variant_filename', None):
                    t_path = os.path.join(self.theme_dir, self.variant_filename)
                    if os.path.exists(t_path):
                        target_file = self.variant_filename

                if target_file:
                    if target_file.endswith(('.png', '.jpg')):
                        img = QImage(os.path.join(self.theme_dir, target_file)).mirrored(False, True)
                        self.texture = QOpenGLTexture(img)
                        self.texture.setMinificationFilter(QOpenGLTexture.Filter.Linear)
                        self.use_tex = 1
                    elif target_file.endswith(('.glsl', '.txt')):
                        with open(os.path.join(self.theme_dir, target_file), 'r', encoding='utf-8') as f:
                            frag_src = f.read()
                    elif target_file.endswith('.json'):
                        # Load JSON multi-pass shader
                        json_path = os.path.join(self.theme_dir, target_file)
                        if self.load_json_shader(json_path):
                            self.using_json_shader = True
                            
                            # Create framebuffers for buffer passes
                            w, h = self._surface_size()
                            for i, pass_data in enumerate(self.render_passes):
                                pass_name = pass_data.get("name", "")
                                if pass_name.startswith("Buffer"):
                                    # Create framebuffer for this buffer
                                    fbo = QOpenGLFramebufferObject(w, h)
                                    self.buffer_fbos[pass_name] = fbo
                            
                            # Compile all shader passes
                            for pass_data in self.render_passes:
                                pass_name = pass_data.get("name", "")
                                if not pass_name and (
                                    pass_data.get("type", "image") == "image"
                                    or len(self.render_passes) == 1
                                ):
                                    pass_name = "Image"
                                pass_code = pass_data.get("code", "")
                                if pass_name != "Common" and pass_code:
                                    program = self.compile_pass_shader(pass_code, pass_name)
                                    if program:
                                        self.shader_passes[pass_name] = program

                            self._prepare_channel_textures()
                            
                            image_key = self._image_pass_key()
                            if image_key:
                                self.pending_reload = False
                                return
                            else:
                                # Fallback if Image pass compilation failed
                                self.error_signal.emit("[SHADER ERROR] Image pass compilation failed. Using fallback.")
                                self.using_json_shader = False
                                self.cleanup_shaders()
            except Exception as e:
                self.error_signal.emit(f"[GLSL ERROR] Asset load fail: {e}")
                self.using_json_shader = False
                self.cleanup_shaders()

        # Standard single-pass shader or fallback
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex, VERTEX_SHADER)
        success = self.program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, frag_src)
        
        if not success:
            err = self.program.log()
            self.error_signal.emit(f"[SHADER FATAL] Compilation Failed. Engaging Color Fallback.\n{err}")
            self.program = QOpenGLShaderProgram()
            self.program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex, VERTEX_SHADER)
            self.program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, FRAGMENT_FALLBACK)
            self.use_tex = 0
            
        self.program.link()
        self.pending_reload = False

    def paintGL(self):
        if self.pending_reload: 
            self.reload_assets()
        if not self.isVisible(): return

        import OpenGL.GL as gl
        surf_w, surf_h = self._surface_size()
        gl.glViewport(0, 0, surf_w, surf_h)
        gl.glClearColor(*self.fallback_color, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        image_key = self._image_pass_key()
        # Handle multi-pass JSON shader rendering
        if self.using_json_shader and image_key:
            try:
                # Render buffer passes first
                for i, pass_data in enumerate(self.render_passes):
                    pass_name = pass_data.get("name", "")
                    if pass_name.startswith("Buffer") and pass_name in self.shader_passes:
                        program = self.shader_passes[pass_name]
                        fbo = self.buffer_fbos.get(pass_name)
                        
                        if fbo and program:
                            fbo.bind()
                            gl.glViewport(0, 0, fbo.width(), fbo.height())
                            gl.glClearColor(0, 0, 0, 1)
                            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
                            
                            program.bind()
                            program.setUniformValue("u_time", self.u_time)
                            program.setUniformValue("u_time_delta", 0.016)
                            program.setUniformValue("u_frame", int(self.u_time * 60.0))
                            program.setUniformValue("u_resolution", float(fbo.width()), float(fbo.height()))
                            program.setUniformValue("u_color", *self.fallback_color)
                            program.setUniformValue("u_use_tex", 0)
                            
                            # Bind buffer textures as inputs
                            tex_unit = 0
                            for j, prev_pass in enumerate(self.render_passes[:i]):
                                prev_name = prev_pass.get("name", "")
                                if prev_name.startswith("Buffer") and prev_name in self.buffer_fbos:
                                    gl.glActiveTexture(gl.GL_TEXTURE0 + tex_unit)
                                    gl.glBindTexture(gl.GL_TEXTURE_2D, self.buffer_fbos[prev_name].texture())
                                    program.setUniformValue(f"iChannel{j}", tex_unit)
                                    tex_unit += 1
                            
                            program.enableAttributeArray(0)
                            program.setAttributeArray(0, self.vertices)
                            gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
                            program.disableAttributeArray(0)
                            program.release()
                            fbo.release()
                
                # Render final Image pass to screen
                image_program = self.shader_passes[image_key]
                if image_program:
                    gl.glViewport(0, 0, surf_w, surf_h)
                    image_program.bind()
                    image_program.setUniformValue("u_time", self.u_time)
                    image_program.setUniformValue("u_time_delta", 0.016)
                    image_program.setUniformValue("u_frame", int(self.u_time * 60.0))
                    image_program.setUniformValue("u_resolution", float(surf_w), float(surf_h))
                    image_program.setUniformValue("u_color", *self.fallback_color)
                    image_program.setUniformValue("u_use_tex", 0)
                    self._bind_image_pass_channels(image_program)
                    
                    image_program.enableAttributeArray(0)
                    image_program.setAttributeArray(0, self.vertices)
                    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
                    image_program.disableAttributeArray(0)
                    image_program.release()
                    
                    for texture in self.channel_textures.values():
                        texture.release()
                    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
                return
            except Exception as e:
                err_msg = str(e)
                if getattr(self, "_last_render_error", None) != err_msg:
                    self._last_render_error = err_msg
                    self.error_signal.emit(f"[RENDER ERROR] Multi-pass rendering failed: {e}. Falling back to solid color.")
                self.using_json_shader = False
                self.cleanup_shaders()
                self.pending_reload = True
                self.update()
                return
        
        # Standard single-pass rendering or fallback
        if self.program is None: return
            
        self.program.bind()
        self.program.setUniformValue("u_time", self.u_time)
        self.program.setUniformValue("u_resolution", float(surf_w), float(surf_h))
        self.program.setUniformValue("u_use_tex", self.use_tex)
        self.program.setUniformValue("u_color", *self.fallback_color)
        
        if self.use_tex and self.texture:
            self.texture.bind()
            self.program.setUniformValue("u_tex", 0) 
            
        self.program.enableAttributeArray(0)
        self.program.setAttributeArray(0, self.vertices)
        
        import OpenGL.GL as gl
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
        
        self.program.disableAttributeArray(0)
        if self.use_tex and self.texture: self.texture.release()
        self.program.release()

    def resizeGL(self, w, h):
        if self.using_json_shader:
            self.pending_reload = True

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.using_json_shader:
            self.pending_reload = True
            self.update()

    def update_time(self):
        self.u_time += 0.016
        self.update()
    
    def stop_shader_timer(self):
        """Stop the shader timer and freeze current frame."""
        if hasattr(self, 'gl_timer'):
            self.gl_timer.stop()
    
    def resume_shader_timer(self):
        """Resume the shader timer."""
        if hasattr(self, 'gl_timer'):
            fps_lock = self.parent().config.get("fps_lock", False) if hasattr(self.parent(), 'config') else False
            self.gl_timer.start(33 if fps_lock else 16)

# ==========================================
# 5. DYNAMIC COMPANION COMBAT FSM ENGINE
# ==========================================
class CompanionCombatEngine(QWidget):
    error_signal = pyqtSignal(str)
    position_changed = pyqtSignal(int, int)
    SPRITE_SCALE = 1.75
    BASE_WIDTH = 500
    BASE_HEIGHT = 280
    
    def __init__(self, app_ref=None, slot_id=0):
        super().__init__(None)
        self.app_ref = app_ref
        self.slot_id = slot_id
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.combat_mode = False
        self.allow_anim = True
        self._global_drag_origin = None
        self._window_origin = None
        self.saved_x = None
        self.saved_y = None
        
        self.e1_manifest = None; self.e1_sheets = {}
        self.e2_manifest = None; self.e2_sheets = {}
        
        self.state = "IDLE"
        self.e1_anim = "idle"; self.e1_frame = 0; self.e1_timer = 0; self.e1_reverse = False
        self.e2_anim = "idle"; self.e2_frame = 0; self.e2_timer = 0; self.e2_reverse = False
        
        self.fireball_x = -100
        
        # Animation cycling support
        self.e1_animation_list = []  # List of available animation names
        self.e1_current_anim_index = 0
        self.e1_pinned_animation = None  # User-pinned animation (if any)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(50) # 20fps logic tick

    def trigger_attack(self):
        if self.combat_mode and self.state == "IDLE":
            self.state = "ATTACK"
            self.e1_anim = "attack"; self.e1_frame = 0

    def load_entity(self, name, silent=False):
        try:
            if name == "Off":
                return None, {}, []
            d_path = os.path.join(COMPANION_DIR, name)
            m_path = os.path.join(d_path, 'manifest.json')
            if not os.path.exists(m_path):
                raise Exception("manifest.json missing")
            with open(m_path, 'r') as f:
                manifest = json.load(f)

            sheets = {}
            animations = manifest.get('animations', {})
            png_index = {
                f.lower(): f for f in os.listdir(d_path)
                if f.lower().endswith('.png') and not f.startswith('.')
            }

            for anim_name, anim_data in animations.items():
                img_path = None
                source = anim_data.get('source') if isinstance(anim_data, dict) else None
                if source:
                    candidate = os.path.join(d_path, source)
                    if os.path.exists(candidate):
                        img_path = candidate
                if not img_path:
                    for variant in (f"{anim_name}.png", f"{anim_name.replace('_', ' ')}.png"):
                        matched = png_index.get(variant.lower())
                        if matched:
                            img_path = os.path.join(d_path, matched)
                            break
                if not img_path:
                    for fname in png_index.values():
                        if os.path.splitext(fname)[0].lower() == anim_name.lower():
                            img_path = os.path.join(d_path, fname)
                            break

                if img_path:
                    sheet = QImage(img_path)
                    if not sheet.isNull():
                        if sheet.hasAlphaChannel():
                            sheet = sheet.convertToFormat(QImage.Format.Format_ARGB32)
                        sheets[anim_name] = sheet

            if not sheets:
                raise Exception("No PNG sprite sheets found in companion folder")

            animation_names = list(sheets.keys())
            return manifest, sheets, animation_names
        except Exception as e:
            if not silent:
                self.error_signal.emit(f"[WARNING] Companion '{name}' assets corrupted/missing: {e}. Bypassing.")
            return None, {}, []

    def refresh_settings(self, config, c_name=None, pinned_anim=None, saved_pos=None):
        self.combat_mode = config.get("combat_mode", False)
        self.allow_anim = config.get("allow_bg_anim", True)
        
        if not config.get("render_graphics", True) or not self.allow_anim:
            self.hide()
            return

        if c_name is None:
            c_name = config.get("companion", "Off")
        if pinned_anim is None:
            pinned_anim = config.get("companion_pinned_anim", "")
        
        if c_name == "Off":
            self.hide()
            self.e1_manifest, self.e1_sheets = None, {}
            self.e2_manifest, self.e2_sheets = None, {}
            self.e1_animation_list = []
            return

        self.e1_manifest, self.e1_sheets, self.e1_animation_list = self.load_entity(c_name)

        if self.combat_mode and self.e1_manifest:
            self.e2_manifest, self.e2_sheets, _ = self.load_entity("werewolf", silent=True)
        else:
            self.e2_manifest, self.e2_sheets = None, {}

        if self.e1_manifest:
            self.show()
            self.setFixedSize(self.BASE_WIDTH, self.BASE_HEIGHT)
            self.state = "IDLE"
            self.e1_anim = "idle" if "idle" in self.e1_sheets else next(iter(self.e1_sheets), "idle")
            self.e2_anim = "idle"
            self.e1_frame = 0
            self.e1_reverse = False
            if pinned_anim and pinned_anim not in ("", "Cycle All"):
                self.e1_pinned_animation = pinned_anim if pinned_anim in self.e1_sheets else None
                if self.e1_pinned_animation:
                    self.e1_anim = self.e1_pinned_animation
            else:
                self.e1_pinned_animation = None
                if self.e1_anim in self.e1_animation_list:
                    self.e1_current_anim_index = self.e1_animation_list.index(self.e1_anim)
                elif self.e1_animation_list:
                    self.e1_current_anim_index = 0
                    self.e1_anim = self.e1_animation_list[0]
                else:
                    self.e1_current_anim_index = 0
            if saved_pos:
                gx = saved_pos.get("gx", saved_pos.get("x"))
                gy = saved_pos.get("gy", saved_pos.get("y"))
                if gx is not None and gy is not None:
                    self.move(int(gx), int(gy))
                    self.saved_x, self.saved_y = int(gx), int(gy)
            self.raise_()
            self.show()
        else:
            self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._global_drag_origin = event.globalPosition().toPoint()
            self._window_origin = self.frameGeometry().topLeft()
            self.raise_()
            self.activateWindow()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._global_drag_origin is not None and event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self._global_drag_origin
            self.move(self._window_origin + delta)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._global_drag_origin is not None:
            self.saved_x, self.saved_y = self.x(), self.y()
            self.position_changed.emit(self.saved_x, self.saved_y)
        self._global_drag_origin = None
        self._window_origin = None
        super().mouseReleaseEvent(event)

    def get_anim_data(self, manifest, anim_name):
        if not manifest or 'animations' not in manifest: return [0], 150, False
        data = manifest['animations'].get(anim_name, manifest['animations'].get('idle', {"frames": [0], "speed": 150}))
        return data.get('frames', [0]), data.get('speed', 150), data.get('reversible', False)

    def _is_cycling_idle(self):
        return (
            self.state == "IDLE"
            and not self.combat_mode
            and self.e1_pinned_animation is None
            and len(self.e1_animation_list) > 1
        )

    def _advance_cycle_animation(self):
        self.e1_current_anim_index = (self.e1_current_anim_index + 1) % len(self.e1_animation_list)
        self.e1_anim = self.e1_animation_list[self.e1_current_anim_index]
        self.e1_frame = 0
        self.e1_reverse = False
        self.e1_timer = 0

    def _on_e1_animation_finished(self, frames, rev):
        if self._is_cycling_idle():
            if self.e1_anim == "die" and rev and not self.e1_reverse:
                self.e1_reverse = True
                self.e1_frame = max(len(frames) - 2, 0)
                return
            self._advance_cycle_animation()
            return

        if self.e1_anim == "attack":
            self.e1_anim = "idle"
            self.e1_frame = 0
            self.fireball_x = 80
        elif self.e1_anim == "die" and not rev:
            self.e1_frame = len(frames) - 1
        elif self.e1_anim == "die" and rev:
            self.e1_reverse = True
            self.e1_frame = max(len(frames) - 2, 0)
        else:
            self.e1_frame = 0

    def tick(self):
        if not self.isVisible() or not self.allow_anim: return
        dt = 50
        
        # Entity 1 Tick
        if self.e1_manifest:
            frames, speed, rev = self.get_anim_data(self.e1_manifest, self.e1_anim)
            self.e1_timer += dt
            if self.e1_timer >= speed:
                self.e1_timer = 0
                if self.e1_reverse:
                    self.e1_frame -= 1
                    if self.e1_frame < 0:
                        self.e1_reverse = False
                        if self._is_cycling_idle():
                            self._advance_cycle_animation()
                        else:
                            self.e1_anim = "idle"
                            self.e1_frame = 0
                            self.state = "IDLE"
                else:
                    self.e1_frame += 1
                    if self.e1_frame >= len(frames):
                        self._on_e1_animation_finished(frames, rev)

        # Entity 2 Tick
        if self.e2_manifest:
            frames, speed, rev = self.get_anim_data(self.e2_manifest, self.e2_anim)
            self.e2_timer += dt
            if self.e2_timer >= speed:
                self.e2_timer = 0
                if self.e2_reverse:
                    self.e2_frame -= 1
                    if self.e2_frame < 0:
                        self.e2_reverse = False
                        self.e2_anim = "idle"; self.e2_frame = 0; self.state = "IDLE"
                else:
                    self.e2_frame += 1
                    if self.e2_frame >= len(frames):
                        if self.e2_anim == "hurt":
                            self.e2_anim = "die"; self.e2_frame = 0; self.state = "DIE"
                        elif self.e2_anim == "die" and rev and self.state == "RESURRECT":
                            self.e2_reverse = True; self.e2_frame = len(frames) - 2
                        elif self.e2_anim == "die":
                            self.e2_frame = len(frames) - 1 # stay dead
                            self.state = "RESURRECT"
                        else:
                            self.e2_frame = 0

        # Fireball Combat Logic
        if self.fireball_x > 0:
            self.fireball_x += 15
            if self.fireball_x > 200:
                self.fireball_x = -100
                if self.e2_manifest:
                    self.e2_anim = "hurt"; self.e2_frame = 0; self.state = "HURT"
                    
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False) # Sharp Pixels
        
        def draw_ent(manifest, sheets, anim_name, frame_idx, x_off):
            if not manifest or not sheets:
                return
            sheet = sheets.get(anim_name)
            if sheet is None:
                sheet = sheets.get('idle') or next(iter(sheets.values()), None)
            if sheet is None:
                return
            w, h = manifest.get("width", 64), manifest.get("height", 64)
            frames, _, _ = self.get_anim_data(manifest, anim_name)
            idx = frames[frame_idx] if frame_idx < len(frames) else frames[-1]
            target = QRect(
                x_off,
                int(self.height() - (h * self.SPRITE_SCALE)),
                int(w * self.SPRITE_SCALE),
                int(h * self.SPRITE_SCALE),
            )
            source = QRect(idx * w, 0, w, h)
            painter.drawImage(target, sheet, source)

        draw_ent(self.e1_manifest, self.e1_sheets, self.e1_anim, self.e1_frame, 0)
        draw_ent(self.e2_manifest, self.e2_sheets, self.e2_anim, self.e2_frame, 200)
        
        if self.fireball_x > 0:
            painter.setBrush(QColor(255, 100, 0))
            painter.drawEllipse(self.fireball_x, 80, 16, 16)

# ==========================================
# 6. THREAD-SAFE UI WIDGETS
# ==========================================
class VisionFeedWidget(QWidget):
    """Dedicated paint surface for live vision frames."""

    def __init__(self, owner, parent=None):
        super().__init__(parent)
        self.owner = owner
        self.setFixedSize(770, 400)
        self.setStyleSheet("background-color: #141419; border: 2px solid #444;")

    def _frame_mapping(self):
        frame = self.owner.current_frame
        if not frame or frame.isNull():
            return None
        scaled = frame.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2
        return frame, scaled, x, y

    def _map_click_to_frame(self, pos):
        mapped = self._frame_mapping()
        if not mapped:
            return None
        frame, scaled, x, y = mapped
        local_x = pos.x() - x
        local_y = pos.y() - y
        if local_x < 0 or local_y < 0 or local_x > scaled.width() or local_y > scaled.height():
            return None
        src_x = int(local_x * frame.width() / max(1, scaled.width()))
        src_y = int(local_y * frame.height() / max(1, scaled.height()))
        return src_x, src_y

    def mousePressEvent(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.owner.heatmap_enabled
            and hasattr(self.owner, "add_click_point")
        ):
            point = self._map_click_to_frame(event.position().toPoint())
            if point:
                self.owner.add_click_point(*point)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.fillRect(self.rect(), QColor(20, 20, 25))
        frame = self.owner.current_frame
        if frame and not frame.isNull():
            scaled = frame.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawImage(x, y, scaled)
            if self.owner.heatmap_enabled and self.owner.click_heatmap:
                self.owner._draw_heatmap_on(painter, scaled, x, y)
            if self.owner.flash_zones_enabled:
                if self.owner.flash_zones:
                    self.owner._draw_flash_zones_on(painter, scaled, x, y)
                if hasattr(self.owner, "_draw_config_overlays"):
                    self.owner._draw_config_overlays(painter, scaled, x, y)
        else:
            painter.setPen(QColor(60, 60, 80))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "VISION FEED STANDBY")

class VisionMapWindow(QDialog):
    """Separate Vision Map Window with Heat Map and Flash Controls."""
    
    def __init__(self, parent=None):
        super().__init__(None)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowMinMaxButtonsHint
        )
        self.setWindowTitle("REONERA Vision Map")
        self.setMinimumSize(800, 650)
        self.resize(800, 650)
        
        self.current_frame = None
        self.heatmap_enabled = False
        self.flash_zones_enabled = False
        self.flash_zones = []
        self.flash_timer = 0
        self.click_heatmap = []  # Store click coordinates for heatmap
        self.monitor_mode = "target"  # "target" or "window"
        
        # Tech-bezel styling
        self.bezel_color = QColor(100, 100, 100)
        self.crosshair_color = QColor(0, 255, 0)
        
        self.setup_ui()
        self._flash_timer = QTimer(self)
        self._flash_timer.timeout.connect(self._tick_flash)
        self._flash_timer.start(50)

    def _apply_theme_styles(self):
        theme = THEMES.get(
            getattr(getattr(self, "app_ref", None), "config", {}).get("theme", "The Eternal Ouroboros"),
            THEMES["The Eternal Ouroboros"],
        )
        self.setStyleSheet(generate_qss(theme, getattr(getattr(self, "app_ref", None), "config", {}).get("theme")))

    def showEvent(self, event):
        super().showEvent(event)
        self._apply_theme_styles()
        if self.app_ref:
            self.app_ref.raise_companions()
    
    def _tick_flash(self):
        if self.flash_zones_enabled and self.flash_zones:
            for zone in self.flash_zones[:]:
                zone['timer'] -= 1
                if zone['timer'] <= 0:
                    self.flash_zones.remove(zone)
            self.vision_display.update()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Vision display area
        self.vision_display = VisionFeedWidget(self)
        layout.addWidget(self.vision_display, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_heatmap = QPushButton("Heat Map")
        self.btn_heatmap.setCheckable(True)
        self.btn_heatmap.clicked.connect(self.toggle_heatmap)
        btn_layout.addWidget(self.btn_heatmap)
        
        self.btn_flash = QPushButton("Flash Zones")
        self.btn_flash.setCheckable(True)
        self.btn_flash.clicked.connect(self.toggle_flash)
        btn_layout.addWidget(self.btn_flash)
        
        self.btn_clear_heatmap = QPushButton("Clear Heat Map")
        self.btn_clear_heatmap.clicked.connect(self.clear_heatmap)
        btn_layout.addWidget(self.btn_clear_heatmap)
        
        btn_layout.addStretch()
        
        # Monitor mode buttons
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(10)
        
        self.btn_target_mode = QPushButton("Target Monitor")
        self.btn_target_mode.setCheckable(True)
        self.btn_target_mode.setChecked(True)
        self.btn_target_mode.clicked.connect(lambda: self.set_monitor_mode("target"))
        mode_layout.addWidget(self.btn_target_mode)
        
        self.btn_window_mode = QPushButton("Window Monitor")
        self.btn_window_mode.setCheckable(True)
        self.btn_window_mode.clicked.connect(lambda: self.set_monitor_mode("window"))
        mode_layout.addWidget(self.btn_window_mode)

        self.mode_group = QButtonGroup(self)
        self.mode_group.setExclusive(True)
        self.mode_group.addButton(self.btn_target_mode)
        self.mode_group.addButton(self.btn_window_mode)
        
        layout.addLayout(btn_layout)
        layout.addLayout(mode_layout)
        
        # Status label
        self.status_label = QLabel("Vision Map Active - Target Mode")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
    
    def toggle_heatmap(self):
        self.heatmap_enabled = self.btn_heatmap.isChecked()
        if self.app_ref and hasattr(self.app_ref, "vision_field"):
            self.app_ref.vision_field.heatmap_enabled = self.heatmap_enabled
        self.vision_display.update()
    
    def toggle_flash(self):
        self.flash_zones_enabled = self.btn_flash.isChecked()
        if not self.flash_zones_enabled:
            self.flash_zones = []
        if self.app_ref and hasattr(self.app_ref, "vision_field"):
            self.app_ref.vision_field.flash_zones_enabled = self.flash_zones_enabled
            if not self.flash_zones_enabled:
                self.app_ref.vision_field.flash_zones = []
        self.vision_display.update()
    
    def clear_heatmap(self):
        self.click_heatmap = []
        self.vision_display.update()
    
    def set_monitor_mode(self, mode):
        self.monitor_mode = mode
        self.btn_target_mode.setChecked(mode == "target")
        self.btn_window_mode.setChecked(mode == "window")
        self.status_label.setText(f"Vision Map Active - {mode.capitalize()} Mode")
    
    def update_frame(self, rgb_array):
        """Update the vision feed with new frame data."""
        try:
            import numpy as np
            rgb_array = np.ascontiguousarray(rgb_array)
            h, w, ch = rgb_array.shape
            self.current_frame = QImage(
                rgb_array.data, w, h, ch * w, QImage.Format.Format_RGB888
            ).copy()
            self.vision_display.update()
        except Exception:
            pass

    def closeEvent(self, event):
        event.accept()
        self.hide()
    
    def add_click_point(self, x, y):
        """Add a click point to the heatmap."""
        self.click_heatmap.append((x, y))
        if len(self.click_heatmap) > 1000:  # Limit heatmap points
            self.click_heatmap.pop(0)
        self.vision_display.update()
    
    def trigger_flash_zone(self, bbox, zone_type="target"):
        """Trigger a flash effect for a detection zone."""
        if self.flash_zones_enabled:
            self.flash_zones.append({'bbox': bbox, 'timer': 10, 'type': zone_type})
            self.flash_timer = 10

    def _draw_heatmap_on(self, painter, scaled_frame, offset_x, offset_y):
        """Draw heatmap overlay on the vision display widget."""
        if not self.click_heatmap:
            return
        for x, y in self.click_heatmap:
            scaled_x = offset_x + int(x * scaled_frame.width() / max(1, self.current_frame.width()))
            scaled_y = offset_y + int(y * scaled_frame.height() / max(1, self.current_frame.height()))
            for r in range(20, 0, -2):
                alpha = int(255 * (1 - r / 20) * 0.3)
                color = QColor(255, 100, 0, alpha)
                painter.setPen(QPen(color, 1))
                painter.setBrush(color)
                painter.drawEllipse(scaled_x - r, scaled_y - r, r * 2, r * 2)

    def _draw_flash_zones_on(self, painter, scaled_frame, offset_x, offset_y):
        """Draw flash zones on the vision display widget."""
        for zone in self.flash_zones:
            bbox = zone['bbox']
            zone_type = zone.get('type', 'target')
            timer = zone.get('timer', 10)
            alpha = int(255 * max(0.2, min(1.0, timer / 10)))
            if zone_type == "target":
                flash_color = QColor(0, 255, 0, alpha)
            elif zone_type == "refresh":
                flash_color = QColor(0, 255, 255, alpha)
            elif zone_type == "zone":
                flash_color = QColor(255, 255, 0, alpha)
            elif zone_type == "exclude":
                flash_color = QColor(255, 0, 0, alpha)
            else:
                flash_color = QColor(255, 255, 255, alpha)
            painter.setPen(QPen(flash_color, 3))
            painter.setBrush(QColor(flash_color.red(), flash_color.green(), flash_color.blue(), alpha // 2))
            if len(bbox) == 2:
                x = offset_x + int(bbox[0] * scaled_frame.width() / max(1, self.current_frame.width()))
                y = offset_y + int(bbox[1] * scaled_frame.height() / max(1, self.current_frame.height()))
                painter.drawEllipse(x - 8, y - 8, 16, 16)
            else:
                x = offset_x + bbox[0] * scaled_frame.width() // 1920 if bbox[0] < 1000 else bbox[0]
                y = offset_y + bbox[1] * scaled_frame.height() // 1080 if bbox[1] < 1000 else bbox[1]
                w = bbox[2] * scaled_frame.width() // 1920 if bbox[2] < 1000 else bbox[2]
                h = bbox[3] * scaled_frame.height() // 1080 if bbox[3] < 1000 else bbox[3]
                painter.drawRect(x, y, w, h)

    def _draw_config_overlays(self, painter, scaled_frame, offset_x, offset_y):
        """Draw configured mask regions while flash mode is active."""
        if not self.app_ref or not self.current_frame:
            return
        cfg = self.app_ref.config
        fw, fh = scaled_frame.width(), scaled_frame.height()
        sw, sh = self.current_frame.width(), self.current_frame.height()
        overlays = [
            (cfg.get("zone_rel"), "zone"),
            (cfg.get("target_bounds"), "target"),
        ]
        for rel, zone_type in overlays:
            if not rel:
                continue
            if len(rel) == 4:
                x = offset_x + int(rel[0] * fw / max(1, sw))
                y = offset_y + int(rel[1] * fh / max(1, sh))
                w = int(rel[2] * fw / max(1, sw))
                h = int(rel[3] * fh / max(1, sh))
                color = {
                    "zone": QColor(255, 255, 0, 90),
                    "target": QColor(0, 255, 0, 90),
                }.get(zone_type, QColor(255, 255, 255, 90))
                painter.setPen(QPen(color, 2, Qt.PenStyle.DashLine))
                painter.setBrush(QColor(color.red(), color.green(), color.blue(), 40))
                painter.drawRect(x, y, w, h)
        refresh = cfg.get("refresh_rel")
        if refresh and len(refresh) >= 2:
            x = offset_x + int(refresh[0] * fw / max(1, sw))
            y = offset_y + int(refresh[1] * fh / max(1, sh))
            painter.setPen(QPen(QColor(0, 255, 255, 180), 2))
            painter.setBrush(QColor(0, 255, 255, 80))
            painter.drawEllipse(x - 6, y - 6, 12, 12)

class AdvancedVisionField(QWidget):
    """Isolated Vision Field Widget with Heatmap & Flash Zone Detection."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(320, 240)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.current_frame = None
        self.heatmap_enabled = False
        self.flash_zones_enabled = False
        self.flash_zones = []
        self.flash_timer = 0
        self.detection_threshold = 0.85
        self.app_ref = None
        
        # Tech-bezel styling
        self.bezel_color = QColor(100, 100, 100)
        self.crosshair_color = QColor(0, 255, 0)
        
        # Vision map window reference
        self.vision_map_window = None
    
    def mousePressEvent(self, event):
        """Open vision map window when clicked."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.vision_map_window is None:
                self.vision_map_window = VisionMapWindow()
                self.vision_map_window.app_ref = self.app_ref
            if not self.vision_map_window.isVisible():
                if self.current_frame:
                    self.vision_map_window.current_frame = self.current_frame
                    self.vision_map_window.vision_display.update()
                self.vision_map_window.show()
                self.vision_map_window.raise_()
                self.vision_map_window.activateWindow()
            else:
                self.vision_map_window.raise_()
                self.vision_map_window.activateWindow()
            if self.app_ref:
                self.app_ref.raise_companions()
        super().mousePressEvent(event)
    
    def closeEvent(self, event):
        """Close vision map window when this widget is closed."""
        if self.vision_map_window and self.vision_map_window.isVisible():
            self.vision_map_window.close()
        super().closeEvent(event)
    
    def update_frame(self, rgb_array):
        """Update the vision feed with new frame data."""
        try:
            import numpy as np
            rgb_array = np.ascontiguousarray(rgb_array)
            h, w, ch = rgb_array.shape
            self.current_frame = QImage(
                rgb_array.data, w, h, ch * w, QImage.Format.Format_RGB888
            ).copy()
            self.update()
            if self.vision_map_window and self.vision_map_window.isVisible():
                self.vision_map_window.update_frame(rgb_array)
        except Exception:
            pass
    
    def set_heatmap_enabled(self, enabled):
        self.heatmap_enabled = enabled
        self.update()
    
    def set_flash_zones_enabled(self, enabled):
        self.flash_zones_enabled = enabled
        if not enabled:
            self.flash_zones = []
        self.update()
    
    def trigger_flash_zone(self, bbox):
        """Trigger a flash effect for a detection zone."""
        if self.flash_zones_enabled:
            self.flash_zones.append({'bbox': bbox, 'timer': 10})
            self.flash_timer = 10
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), QColor(20, 20, 30))
        
        # Draw current frame or placeholder
        if self.current_frame:
            scaled_frame = self.current_frame.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x = (self.width() - scaled_frame.width()) // 2
            y = (self.height() - scaled_frame.height()) // 2
            painter.drawImage(x, y, scaled_frame)
            if self.heatmap_enabled:
                self._draw_heatmap(painter, scaled_frame, x, y)
        else:
            # Draw placeholder
            painter.setPen(QColor(60, 60, 80))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "VISION FEED STANDBY")
        
        # Draw tech-bezel borders
        self._draw_tech_bezel(painter)
        
        # Draw flash zones
        if self.flash_zones_enabled and self.flash_zones:
            self._draw_flash_zones(painter)
    
    def _draw_heatmap(self, painter, scaled_frame, offset_x, offset_y):
        """Draw optional heatmap overlay on top of the live frame."""
        if not self.current_frame:
            return
        heatmap_overlay = QPixmap(scaled_frame.size())
        heatmap_overlay.fill(Qt.GlobalColor.transparent)
        overlay_painter = QPainter(heatmap_overlay)
        overlay_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for i in range(0, scaled_frame.width(), 20):
            for j in range(0, scaled_frame.height(), 20):
                variance = (math.sin(i * 0.1 + time.time()) * math.cos(j * 0.1 + time.time()) + 1) / 2
                if variance < 0.33:
                    color = QColor(0, int(100 + variance * 300), 255, 80)
                elif variance < 0.66:
                    color = QColor(int(255 * (variance - 0.33) * 3), 255, 0, 90)
                else:
                    color = QColor(255, int(255 * (1 - variance) * 3), 0, 100)
                overlay_painter.fillRect(i, j, 20, 20, color)
        overlay_painter.end()
        painter.drawPixmap(offset_x, offset_y, heatmap_overlay)
    
    def _draw_tech_bezel(self, painter):
        """Draw tech-bezel borders with geometric crosshair tick marks."""
        w, h = self.width(), self.height()
        margin = 10
        tick_size = 8
        
        # Draw main border
        painter.setPen(QPen(self.bezel_color, 2))
        painter.drawRect(margin, margin, w - 2*margin, h - 2*margin)
        
        # Draw corner crosshairs
        painter.setPen(QPen(self.crosshair_color, 1))
        
        # Top-left
        painter.drawLine(margin, margin + tick_size, margin, margin)
        painter.drawLine(margin, margin, margin + tick_size, margin)
        
        # Top-right
        painter.drawLine(w - margin - tick_size, margin, w - margin, margin)
        painter.drawLine(w - margin, margin, w - margin, margin + tick_size)
        
        # Bottom-left
        painter.drawLine(margin, h - margin - tick_size, margin, h - margin)
        painter.drawLine(margin, h - margin, margin + tick_size, h - margin)
        
        # Bottom-right
        painter.drawLine(w - margin - tick_size, h - margin, w - margin, h - margin)
        painter.drawLine(w - margin, h - margin, w - margin, h - margin - tick_size)
        
        # Draw coordinate tick marks along edges
        for i in range(margin + 20, w - margin, 20):
            painter.drawLine(i, margin, i, margin + 3)
            painter.drawLine(i, h - margin, i, h - margin - 3)
        
        for j in range(margin + 20, h - margin, 20):
            painter.drawLine(margin, j, margin + 3, j)
            painter.drawLine(w - margin, j, w - margin - 3, j)
    
    def _draw_flash_zones(self, painter):
        """Draw flashing detection zones."""
        if self.flash_timer > 0:
            self.flash_timer -= 1
            
            for zone in self.flash_zones[:]:
                zone['timer'] -= 1
                if zone['timer'] <= 0:
                    self.flash_zones.remove(zone)
                    continue
                
                bbox = zone['bbox']
                alpha = int(255 * (zone['timer'] / 10))
                
                # Flash effect with high-visibility strobe
                flash_color = QColor(255, 255, 0, alpha)
                painter.setPen(QPen(flash_color, 3))
                painter.setBrush(QColor(255, 255, 0, alpha // 2))
                
                # Scale bbox to widget coordinates
                x = bbox[0] * self.width() // 1920 if bbox[0] < 1000 else bbox[0]
                y = bbox[1] * self.height() // 1080 if bbox[1] < 1000 else bbox[1]
                w = bbox[2] * self.width() // 1920 if bbox[2] < 1000 else bbox[2]
                h = bbox[3] * self.height() // 1080 if bbox[3] < 1000 else bbox[3]
                
                painter.drawRect(x, y, w, h)
        
        if self.flash_timer == 0:
            self.flash_zones = []

class TechWaveVisualizer(QWidget):
    """Theme-Adaptive Tech Wave Synthesizer Visualizer."""
    
    THEME_COLOR_MAP = {
        "Volcanic Magma": {
            "bg": QColor(26, 15, 15),
            "wave1": QColor(255, 69, 0),
            "wave2": QColor(255, 140, 0),
            "wave3": QColor(255, 215, 0),
            "intensity": 1.0
        },
        "The Cyberpunk Glitch Matrix": {
            "bg": QColor(0, 0, 0),
            "wave1": QColor(0, 240, 255),
            "wave2": QColor(255, 0, 127),
            "wave3": QColor(0, 255, 127),
            "intensity": 1.2
        },
        "Bio-Sustained Nature": {
            "bg": QColor(27, 59, 43, 200),
            "wave1": QColor(143, 188, 143),
            "wave2": QColor(34, 139, 34),
            "wave3": QColor(255, 215, 0),
            "intensity": 0.8
        },
        "The Eternal Ouroboros": {
            "bg": QColor(5, 5, 10, 180),
            "wave1": QColor(255, 215, 0),
            "wave2": QColor(0, 255, 135),
            "wave3": QColor(255, 0, 255),
            "intensity": 0.9
        },
        "The Shattered Basalt Crags": {
            "bg": QColor(36, 37, 38, 180),
            "wave1": QColor(138, 149, 165),
            "wave2": QColor(255, 215, 0),
            "wave3": QColor(100, 149, 237),
            "intensity": 0.7
        },
        "The Ethereal Stratus Clouds": {
            "bg": QColor(250, 249, 246, 200),
            "wave1": QColor(160, 196, 255),
            "wave2": QColor(255, 176, 0),
            "wave3": QColor(135, 206, 250),
            "intensity": 0.6
        },
        "Aquatic Abyssal": {
            "bg": QColor(2, 11, 20, 180),
            "wave1": QColor(0, 240, 255),
            "wave2": QColor(0, 255, 170),
            "wave3": QColor(65, 105, 225),
            "intensity": 1.0
        },
        "Robotic Futuristic": {
            "bg": QColor(42, 46, 51, 180),
            "wave1": QColor(255, 165, 0),
            "wave2": QColor(255, 69, 0),
            "wave3": QColor(0, 255, 127),
            "intensity": 1.1
        },
        "The Deep Space Nebula": {
            "bg": QColor(2, 2, 8, 180),
            "wave1": QColor(161, 36, 255),
            "wave2": QColor(255, 0, 127),
            "wave3": QColor(0, 191, 255),
            "intensity": 1.0
        },
        "Steampunk Brass Gauge": {
            "bg": QColor(43, 30, 19, 180),
            "wave1": QColor(212, 175, 55),
            "wave2": QColor(255, 140, 0),
            "wave3": QColor(139, 69, 19),
            "intensity": 0.8
        }
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.current_theme = "The Eternal Ouroboros"
        self.time_offset = 0.0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_wave)
        self.timer.start(33)  # ~30 FPS
    
    def set_theme(self, theme_name):
        self.current_theme = theme_name
        self.update()
    
    def _update_wave(self):
        self.time_offset += 0.05
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get theme colors
        colors = self.THEME_COLOR_MAP.get(self.current_theme, self.THEME_COLOR_MAP["The Eternal Ouroboros"])
        
        # Draw background
        painter.fillRect(self.rect(), colors["bg"])
        
        # Draw multi-layered intersecting sine/cosine waves
        w, h = self.width(), self.height()
        intensity = colors["intensity"]
        
        # Wave 1 - Primary
        self._draw_wave(painter, colors["wave1"], w, h, self.time_offset, 1.0, intensity)
        
        # Wave 2 - Secondary (phase shifted)
        self._draw_wave(painter, colors["wave2"], w, h, self.time_offset + 2.0, 0.8, intensity * 0.8)
        
        # Wave 3 - Tertiary (different frequency)
        self._draw_wave(painter, colors["wave3"], w, h, self.time_offset + 4.0, 1.2, intensity * 0.6)
    
    def _draw_wave(self, painter, color, w, h, time_offset, frequency, intensity):
        """Draw a single wave layer."""
        path = QPainterPath()
        
        points = []
        for x in range(0, w, 2):
            # Multi-layered intersecting sine/cosine waves
            y = h / 2 + (
                math.sin((x * frequency * 0.02) + time_offset) * 15 * intensity +
                math.cos((x * frequency * 0.01) + time_offset * 1.5) * 10 * intensity +
                math.sin((x * frequency * 0.03) - time_offset * 0.5) * 5 * intensity
            )
            points.append((x, y))
        
        if points:
            path.moveTo(points[0][0], points[0][1])
            for x, y in points[1:]:
                path.lineTo(x, y)
        
        # Draw wave with glow effect
        pen = QPen(color, 2)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Add glow overlay
        glow_color = QColor(color)
        glow_color.setAlpha(50)
        painter.setPen(QPen(glow_color, 4))
        painter.drawPath(path)

class TelemetryChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.delays = []
        self.line_color = QColor("#00FF00")
        self.setMinimumHeight(40)

    def update_data(self, delay):
        self.delays.append(delay)
        if len(self.delays) > 10: self.delays.pop(0)
        self.update()

    def set_color(self, hex_color):
        self.line_color = QColor(hex_color)
        self.update()

    def paintEvent(self, event):
        if not self.delays: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.line_color, 2))
        
        w, h = self.width(), self.height()
        max_val = max(self.delays) or 1
        step = w / max(1, len(self.delays) - 1)
        
        pts = [QPoint(int(i * step), int(h - (val / max_val * h))) for i, val in enumerate(self.delays)]
        for i in range(len(pts) - 1): painter.drawLine(pts[i], pts[i+1])

class SelectorOverlay(QWidget):
    def __init__(self, callback, mode="point", color="#FF0000"):
        super().__init__()
        self.callback = callback
        self.mode = mode
        self.color = QColor(color)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.showFullScreen()
        self.start_pos = None; self.current_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        if self.mode == "rect" and self.start_pos and self.current_pos:
            painter.setPen(QPen(self.color, 3))
            painter.drawRect(QRect(self.start_pos, self.current_pos))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.mode == "rect" and self.start_pos:
            self.current_pos = event.globalPosition().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            end_pos = event.globalPosition().toPoint()
            self.hide()
            QTimer.singleShot(150, lambda: self.process_capture(end_pos))

    def process_capture(self, end_pos):
        abs_x, abs_y = end_pos.x(), end_pos.y()
        if self.mode == "point":
            win = gw.getWindowsAt(abs_x, abs_y)
            title = win[0].title if win else "Desktop"
            rel_x = abs_x - (win[0].left if win else 0)
            rel_y = abs_y - (win[0].top if win else 0)
            self.callback(title, rel_x, rel_y, abs_x, abs_y)
        else:
            x1, x2 = sorted([self.start_pos.x(), end_pos.x()])
            y1, y2 = sorted([self.start_pos.y(), end_pos.y()])
            win = gw.getWindowsAt(x1, y1)
            title = win[0].title if win else "Desktop"
            rel_bounds = (x1 - (win[0].left if win else 0), y1 - (win[0].top if win else 0), x2 - x1, y2 - y1)
            if (x2 - x1) > 2 and (y2 - y1) > 2:
                self.callback(title, rel_bounds, (x1, y1, x2, y2))
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

# ==========================================
# 7. BACKGROUND VISION & MONITORING QTHREAD
# ==========================================
class MonitorThread(QThread):
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str, str)
    shift_signal = pyqtSignal(str)
    telemetry_signal = pyqtSignal(float)
    alert_signal = pyqtSignal(str)
    match_preview_signal = pyqtSignal(object) 
    finished_signal = pyqtSignal()
    combat_trigger_signal = pyqtSignal()
    vision_flash_signal = pyqtSignal(str, object)
    vision_click_signal = pyqtSignal(int, int)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.is_running = True
        self.shift_start_time = time.time()
        self.target_shift_duration = random.randint(1200, 1800)
        self.last_circadian_break = time.time()
        self.consecutive_failures = 0

    def get_abs(self, rel_coords, bounds=False):
        try:
            win = gw.getWindowsWithTitle(self.config["window_title"])[0]
            if bounds: return win.left + rel_coords[0], win.top + rel_coords[1], rel_coords[2], rel_coords[3]
            else: return win.left + rel_coords[0], win.top + rel_coords[1]
        except IndexError: return None

    def human_click(self, target_x, target_y, is_decoy=False):
        if not self.is_running: return
        current_fw = win32gui.GetForegroundWindow()
        if self.config.get("browser_spoofing"):
            windows = gw.getWindowsWithTitle(self.config["window_title"])
            if windows:
                try: win32gui.SetForegroundWindow(windows[0]._hWnd)
                except: pass
                
        start_x, start_y = pyautogui.position()
        dist = math.hypot(target_x - start_x, target_y - start_y)
        dur = max(0.15, min(0.4, dist / 3000.0 + random.uniform(0.05, 0.15)))
        tx, ty = target_x + random.randint(-2, 2), target_y + random.randint(-2, 2)

        if dist > 100:
            pyautogui.moveTo((start_x + tx)/2 + random.randint(-50,50), (start_y + ty)/2 + random.randint(-50,50), duration=dur*0.4, tween=pyautogui.easeInQuad)
            pyautogui.moveTo(tx, ty, duration=dur*0.6, tween=pyautogui.easeOutQuad)
        else:
            pyautogui.moveTo(tx, ty, duration=dur, tween=pyautogui.easeInOutQuad)

        if random.random() > 0.85:
            pyautogui.moveTo(tx + random.randint(-3, 3), ty + random.randint(-3, 3), duration=0.08)
            pyautogui.moveTo(tx, ty, duration=0.08)

        self.sleep_check(random.uniform(0.1, 0.4))
        
        if is_decoy:
            pyautogui.move(random.randint(-2, 2), random.randint(-2, 2), 0.1)
            self.sleep_check(0.05)

        pyautogui.click()
        self.sleep_check(random.uniform(0.02, 0.08))
        self.vision_click_signal.emit(tx, ty)
        self.vision_flash_signal.emit("zone" if is_decoy else "refresh", (tx, ty))
        if self.config.get("browser_spoofing") and current_fw:
            try: win32gui.SetForegroundWindow(current_fw)
            except: pass

    def match_vision(self):
        abs_bounds = self.get_abs(self.config["target_bounds"], bounds=True)
        if not abs_bounds:
            self.log_signal.emit("⚠️ Vision Warning: Target bounds resolution failed. Check coordinate configuration.")
            return True
        
        screen_np = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        x, y, w, h = abs_bounds
        
        if y < 0 or x < 0 or w <= 0 or h <= 0:
            self.log_signal.emit(f"⚠️ Vision Warning: Invalid target bounds detected (x={x}, y={y}, w={w}, h={h}). Skipping vision check.")
            return True
        
        if y+h > screen_np.shape[0] or x+w > screen_np.shape[1]:
            self.log_signal.emit(f"⚠️ Vision Warning: Target bounds ({x}, {y}, {w}, {h}) exceed screen dimensions ({screen_np.shape[1]}, {screen_np.shape[0]}). Skipping vision check.")
            return True
        
        try:
            screen_crop = screen_np[y:y+h, x:x+w]
        except Exception as e:
            self.log_signal.emit(f"⚠️ Vision Warning: Screen crop failed with bounds ({x}, {y}, {w}, {h}): {e}")
            return True
        
        tpath = os.path.join(REONERA_DIR, 'target_state.png')
        try:
            target_bgr = cv2.imread(tpath)
            if target_bgr is None:
                self.log_signal.emit("⚠️ Vision Warning: Target state image not found or corrupted. Skipping vision check.")
                return True
        except Exception as e:
            self.log_signal.emit(f"⚠️ Vision Warning: Failed to load target state image: {e}")
            return True

        for ex in self.config.get("exclusion_zones", []):
            ex_abs = self.get_abs(ex, bounds=True)
            if ex_abs:
                cx, cy = ex_abs[0] - x, ex_abs[1] - y
                cv2.rectangle(screen_crop, (cx, cy), (cx+ex_abs[2], cy+ex_abs[3]), (0,0,0), -1)
                cv2.rectangle(target_bgr, (cx, cy), (cx+ex_abs[2], cy+ex_abs[3]), (0,0,0), -1)

        self.match_preview_signal.emit(cv2.cvtColor(screen_crop, cv2.COLOR_BGR2RGB).copy())

        try:
            if np.max(cv2.matchTemplate(screen_crop, target_bgr, cv2.TM_CCOEFF_NORMED)) >= 0.85: return True
        except Exception as e:
            self.log_signal.emit(f"⚠️ Vision Warning: Template matching failed: {e}")

        try:
            target_gray = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2GRAY)
            screen_gray = cv2.cvtColor(screen_crop, cv2.COLOR_BGR2GRAY)
            if target_gray.shape != screen_gray.shape: screen_gray = cv2.resize(screen_gray, (target_gray.shape[1], target_gray.shape[0]))
            if ssim(target_gray, screen_gray, full=True)[0] >= 0.80: return True
        except Exception as e:
            self.log_signal.emit(f"⚠️ Vision Warning: SSIM comparison failed: {e}")
        return False

    def sleep_check(self, duration):
        start = time.time()
        while time.time() - start < duration:
            if not self.is_running: return False
            time.sleep(0.1)
        return True

    def execute_break(self, minutes):
        self.status_signal.emit(f"ON BREAK ({minutes}m)", "purple")
        self.log_signal.emit(f"☕ Initiating organic break: {minutes} minutes.")
        pyautogui.moveTo(random.choice([10, pyautogui.size()[0]-10]), random.choice([10, pyautogui.size()[1]-10]), duration=random.uniform(1.0, 2.0), tween=pyautogui.easeOutQuad)
        
        start = time.time()
        while time.time() - start < minutes * 60:
            if not self.is_running: return False
            rm, rs = divmod(int((minutes * 60) - (time.time() - start)), 60)
            self.shift_signal.emit(f"Taking Break: {rm}m {rs}s remaining")
            time.sleep(1)
        self.status_signal.emit("ACTIVE SCANNING", "red")
        return True

    def run(self):
        self.log_signal.emit("Engine initialized & Ballistic locks engaged.")
        self.status_signal.emit("ACTIVE SCANNING", "red")
        
        while self.is_running:
            try:
                if self.config.get("circadian_engine") and random.random() < 0.05 and time.time() - self.last_circadian_break > 10800:
                    if not self.execute_break(random.randint(30, 45)): break
                    self.last_circadian_break = time.time()

                if time.time() - self.shift_start_time >= self.target_shift_duration:
                    if not self.execute_break(random.randint(3, 8)): break
                    self.shift_start_time, self.target_shift_duration = time.time(), random.randint(1200, 1800)
                    
                lpath = os.path.join(REONERA_DIR, 'login_wall.png')
                if os.path.exists(lpath) and pyautogui.locateOnScreen(lpath, confidence=0.85):
                    self.log_signal.emit("🚨 EMERGENCY: Login wall detected! Halting engine.")
                    self.alert_signal.emit("EMERGENCY: Login Wall Detected. Engine Locked.")
                    break

                windows = gw.getWindowsWithTitle(self.config["window_title"])
                if not windows or not windows[0].isActive:
                    if windows: 
                        try: windows[0].activate()
                        except: windows[0].minimize(); windows[0].restore()
                    else:
                        self.log_signal.emit("Target window missing. Waiting...")
                        if not self.sleep_check(5): break
                        continue

                abs_ref = self.get_abs(self.config["refresh_rel"])
                if not abs_ref: continue
                self.human_click(abs_ref[0], abs_ref[1], is_decoy=False)
                self.log_signal.emit("🔄 Page Refresh Fired.")
                
                wait_start = time.time()
                while time.time() - wait_start < 10.0:
                    if not self.is_running: break
                    cx, cy = pyautogui.position()
                    if abs(cx - abs_ref[0]) > 20 or abs(cy - abs_ref[1]) > 20: raise Exception("User Interventions Caught")
                    time.sleep(0.5)
                
                if not self.is_running: break
                
                if not self.match_vision():
                    self.log_signal.emit("🎉 TASK FOUND! Vision map altered.")
                    self.status_signal.emit("TASK FOUND! 🎉", "#00FF00")
                    self.alert_signal.emit("REONERA: Project Added!")
                    self.combat_trigger_signal.emit()
                    break
                else:
                    self.consecutive_failures = 0
                    abs_zone = self.get_abs(self.config["zone_rel"], bounds=True)
                    if abs_zone and random.choice([True, False]):
                        for _ in range(random.randint(1, 2)):
                            if not self.is_running: break
                            self.human_click(random.randint(abs_zone[0], abs_zone[0]+abs_zone[2]), random.randint(abs_zone[1], abs_zone[1]+abs_zone[3]), is_decoy=True)
                            self.sleep_check(random.uniform(1.0, 2.0))
                    
                    delay = random.randint(300, 900) + random.uniform(0.001, 0.999)
                    self.telemetry_signal.emit(delay)
                    m, s = divmod(int(delay), 60)
                    self.log_signal.emit(f"Clear. Sleeping {m}m {s}s...")
                    
                    start_sleep = time.time()
                    while time.time() - start_sleep < delay:
                        if not self.is_running: break
                        rm, rs = divmod(int(delay - (time.time() - start_sleep)), 60)
                        self.shift_signal.emit(f"Shift Active - Wait: {rm}m {rs}s")
                        time.sleep(0.5)

            except Exception as e:
                if "User Interventions" in str(e):
                    self.log_signal.emit("🛑 Manual user override caught. Engine Standby.")
                    break
                    
                self.consecutive_failures += 1
                self.log_signal.emit(f"⚠️ Internal Error ({self.consecutive_failures}/3): {e}")
                if self.consecutive_failures >= 3:
                    self.alert_signal.emit("CRITICAL: Script crashed 3 times. Suspended.")
                    break
                self.sleep_check(10)
                
        self.finished_signal.emit()

# ==========================================
# 8. PRIMARY CONFIGURATION MATRICES
# ==========================================
class SettingsDialog(QDialog):
    def __init__(self, app_ref):
        super().__init__(app_ref)
        self.app = app_ref
        self.setWindowTitle("REONERA Configuration Matrix")
        self.setFixedSize(580, 780)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        
        layout = QVBoxLayout(self)
        tb_lay = QHBoxLayout(); tb_lay.addWidget(QLabel("Settings Matrix")); tb_lay.addStretch()
        cb = QPushButton("✖"); cb.clicked.connect(self.reject); tb_lay.addWidget(cb)
        layout.addLayout(tb_lay)

        tabs = QTabWidget(); layout.addWidget(tabs)
        c = self.app.config

        # Tab 1: Engine Flags (RESTORED)
        t1 = QWidget()
        l1 = QVBoxLayout(t1)
        self.browser_spoof = QCheckBox("Browser Focus Spoofing (Window Depth Manipulation)")
        self.circadian = QCheckBox("Asymmetric Sleep Schedules (Circadian Engine)")
        self.tray = QCheckBox("Minimize to Tray on Close")
        self.autorun = QCheckBox("Auto-Run Engine on Launch")
        self.always_on_top = QCheckBox("Keep Console Window Always on Top")
        
        self.browser_spoof.setChecked(c.get("browser_spoofing", True))
        self.circadian.setChecked(c.get("circadian_engine", True))
        self.tray.setChecked(c.get("minimize_to_tray", True))
        self.autorun.setChecked(c.get("auto_run", False))
        self.always_on_top.setChecked(c.get("always_on_top", False))
        
        for w in [self.browser_spoof, self.circadian, self.tray, self.autorun, self.always_on_top]: l1.addWidget(w)
        l1.addStretch()
        tabs.addTab(t1, "Engine Flags")

        # Tab 2: External Alerts Tab (Crypto protected)
        t2 = QWidget(); l2 = QGridLayout(t2)
        self.audio = QCheckBox("Enable Local Audio Alerts")
        self.audio.setChecked(c.get("audio_alert", True))
        l2.addWidget(self.audio, 0, 0, 1, 3)

        self.audio_path = QLineEdit(c.get("audio_path", ""))
        btn_browse = QPushButton("Browse .wav")
        btn_browse.clicked.connect(lambda: self.audio_path.setText(QFileDialog.getOpenFileName(self, "Select Audio", "", "WAV Audio (*.wav)")[0] or self.audio_path.text()))
        l2.addWidget(QLabel("Custom Audio:"), 1, 0)
        l2.addWidget(self.audio_path, 1, 1)
        l2.addWidget(btn_browse, 1, 2)

        self.toast = QCheckBox("Native OS Windows Toast Notifications")
        self.toast.setChecked(c.get("os_toast", True))
        l2.addWidget(self.toast, 2, 0, 1, 3)

        l2.addWidget(QLabel("Discord Webhook:"), 3, 0)
        self.discord = QLineEdit(c.get("discord", "")); self.discord.setEchoMode(QLineEdit.EchoMode.Password)
        l2.addWidget(self.discord, 3, 1, 1, 2)
        
        l2.addWidget(QLabel("Telegram Token:"), 4, 0)
        self.tele_token = QLineEdit(c.get("tele_token", "")); self.tele_token.setEchoMode(QLineEdit.EchoMode.Password)
        l2.addWidget(self.tele_token, 4, 1, 1, 2)
        
        l2.addWidget(QLabel("Telegram Chat ID:"), 5, 0)
        self.tele_chat = QLineEdit(c.get("tele_chat", ""))
        l2.addWidget(self.tele_chat, 5, 1, 1, 2)

        l2.addWidget(QLabel("Slack Webhook:"), 6, 0)
        self.slack = QLineEdit(c.get("slack", "")); self.slack.setEchoMode(QLineEdit.EchoMode.Password)
        l2.addWidget(self.slack, 6, 1, 1, 2)

        # Test Button for Webhook Diagnostics
        self.btn_test_alerts = QPushButton("Run Connection Diagnostics")
        self.btn_test_alerts.setIcon(IconRenderer.render_icon('test', 18, self.app.current_theme_color))
        self.btn_test_alerts.clicked.connect(self.test_webhook_connections)
        l2.addWidget(self.btn_test_alerts, 7, 0, 1, 3)
        tabs.addTab(t2, "Alerts & Routing")

        # Tab 3: Cosmetics & Switches Tab
        cosmetics_scroll = QScrollArea()
        cosmetics_scroll.setWidgetResizable(True)
        cosmetics_scroll.setFrameShape(QFrame.Shape.NoFrame)
        t3 = QWidget()
        l3 = QVBoxLayout(t3)
        l3.setSpacing(14)
        l3.setContentsMargins(8, 8, 8, 8)

        env_group = QGroupBox("Immersive Environment")
        env_form = QFormLayout(env_group)
        env_form.setSpacing(10)
        env_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        env_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()))
        self.theme_combo.setCurrentText(c.get("theme", "The Eternal Ouroboros"))

        self.variant_combo = QComboBox()
        self.variant_filename_map = {}
        self.theme_combo.currentTextChanged.connect(self.populate_variants)
        self.populate_variants(self.theme_combo.currentText())
        var_text = c.get("variant", "")
        if var_text:
            idx = self.variant_combo.findText(var_text)
            if idx >= 0:
                self.variant_combo.setCurrentIndex(idx)
            else:
                for display_name, filename in self.variant_filename_map.items():
                    if filename == var_text:
                        idx = self.variant_combo.findText(display_name)
                        if idx >= 0:
                            self.variant_combo.setCurrentIndex(idx)
                            break

        env_form.addRow("Theme:", self.theme_combo)
        env_form.addRow("Background:", self.variant_combo)
        l3.addWidget(env_group)

        companion_group = QGroupBox("Desktop Companions")
        companion_form = QFormLayout(companion_group)
        companion_form.setSpacing(10)
        companion_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        companion_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        anim_modes = c.get("companion_anim_modes", [])
        legacy_anim = c.get("companion_pinned_anim", "Cycle All")

        self.companion_combo = QComboBox()
        self.companion_combo.addItems(self.app.available_companions)
        self.companion_combo.setCurrentText(c.get("companion", "Off"))
        self.companion_anim_combo = self._make_anim_combo()
        self.companion_extra1 = QComboBox()
        self.companion_extra1_anim = self._make_anim_combo()
        self.companion_extra2 = QComboBox()
        self.companion_extra2_anim = self._make_anim_combo()
        for cb in (self.companion_extra1, self.companion_extra2):
            cb.addItems(self.app.available_companions)

        extras = c.get("companion_extras", [])
        if len(extras) > 0:
            self.companion_extra1.setCurrentText(extras[0])
        if len(extras) > 1:
            self.companion_extra2.setCurrentText(extras[1])

        self.companion_combo.currentTextChanged.connect(
            lambda name: self._populate_anim_combo(self.companion_anim_combo, name, anim_modes[0] if len(anim_modes) > 0 else legacy_anim)
        )
        self.companion_extra1.currentTextChanged.connect(
            lambda name: self._populate_anim_combo(self.companion_extra1_anim, name, anim_modes[1] if len(anim_modes) > 1 else legacy_anim)
        )
        self.companion_extra2.currentTextChanged.connect(
            lambda name: self._populate_anim_combo(self.companion_extra2_anim, name, anim_modes[2] if len(anim_modes) > 2 else legacy_anim)
        )
        self.app.companions_updated.connect(self.update_companions)

        self._populate_anim_combo(self.companion_anim_combo, self.companion_combo.currentText(), anim_modes[0] if len(anim_modes) > 0 else legacy_anim)
        self._populate_anim_combo(self.companion_extra1_anim, self.companion_extra1.currentText(), anim_modes[1] if len(anim_modes) > 1 else legacy_anim)
        self._populate_anim_combo(self.companion_extra2_anim, self.companion_extra2.currentText(), anim_modes[2] if len(anim_modes) > 2 else legacy_anim)

        companion_form.addRow("Companion 1:", self.companion_combo)
        companion_form.addRow("Animation 1:", self.companion_anim_combo)
        companion_form.addRow("Companion 2:", self.companion_extra1)
        companion_form.addRow("Animation 2:", self.companion_extra1_anim)
        companion_form.addRow("Companion 3:", self.companion_extra2)
        companion_form.addRow("Animation 3:", self.companion_extra2_anim)
        l3.addWidget(companion_group)

        tip = QLabel(
            "Each companion can cycle all animations or lock to one. "
            "Drag companions anywhere — positions save to your profile."
        )
        tip.setWordWrap(True)
        tip.setStyleSheet("padding: 6px 4px; font-size: 11px;")
        l3.addWidget(tip)

        render_group = QGroupBox("Rendering & Performance")
        render_layout = QVBoxLayout(render_group)
        render_layout.setSpacing(8)
        self.r_graphics = QCheckBox("Render Immersive Canvas Graphics")
        self.r_graphics.setChecked(c.get("render_graphics", True))
        self.allow_anim = QCheckBox("Allow Background Animations")
        self.allow_anim.setChecked(c.get("allow_bg_anim", True))
        self.fps_lock = QCheckBox("Economy Mode (Lock to 30 FPS)")
        self.fps_lock.setChecked(c.get("fps_lock", False))
        self.combat_mode = QCheckBox("Engage Companion Interactive Combat Mode")
        self.combat_mode.setChecked(c.get("combat_mode", False))
        self.disable_canvas_bg = QCheckBox("Completely Disable Background Canvas Rendering")
        self.disable_canvas_bg.setChecked(c.get("disable_canvas_bg", False))
        for w in [self.r_graphics, self.allow_anim, self.fps_lock, self.combat_mode, self.disable_canvas_bg]:
            render_layout.addWidget(w)
        l3.addWidget(render_group)
        l3.addStretch()

        cosmetics_scroll.setWidget(t3)
        tabs.addTab(cosmetics_scroll, "Cosmetics")

        # Tab 4: Dev Tab (RESTORED COMPILE BUTTON)
        t4 = QWidget(); l4 = QVBoxLayout(t4)
        btn_bake = QPushButton("Bake Code into Standalone .EXE")
        btn_bake.setIcon(IconRenderer.render_icon('bake', 18, self.app.current_theme_color))
        btn_bake.clicked.connect(self.app.bake_executable)
        l4.addWidget(btn_bake)
        
        btn_sc = QPushButton("Deploy Desktop/Start Menu Shortcuts")
        btn_sc.setIcon(IconRenderer.render_icon('deploy', 18, self.app.current_theme_color))
        btn_sc.clicked.connect(self.app.deploy_shortcuts)
        l4.addWidget(btn_sc)

        btn_rebuild = QPushButton("Rebuild Companion Manifests")
        btn_rebuild.setIcon(IconRenderer.render_icon('refresh', 18, self.app.current_theme_color))
        btn_rebuild.clicked.connect(self.rebuild_companion_manifests)
        l4.addWidget(btn_rebuild)
        l4.addStretch()
        tabs.addTab(t4, "Developer")

        btn_save = QPushButton("Apply Engine Matrix")
        btn_save.setIcon(IconRenderer.render_icon('save', 18, self.app.current_theme_color))
        btn_save.clicked.connect(self.save)
        layout.addWidget(btn_save)

    def populate_variants(self, theme_name):
        self.variant_combo.clear()
        # Preserve raw casing - do NOT force .lower() conversion
        theme_dir = os.path.join(BG_DIR, "".join(x for x in theme_name if x.isalnum() or x in " -_"))
        if os.path.exists(theme_dir):
            variant_map = {}  # Maps display name to actual filename
            
            try:
                # Scan for .json files first (multi-pass shaders)
                for f in os.listdir(theme_dir):
                    if f.endswith('.json'):
                        json_path = os.path.join(theme_dir, f)
                        try:
                            with open(json_path, 'r', encoding='utf-8') as json_file:
                                data = json.load(json_file)
                                # Extract display name from Shader -> info -> name
                                display_name = (
                                    data.get("Shader", {}).get("info", {}).get("name")
                                    or data.get("info", {}).get("name")
                                    or f
                                )
                                variant_map[display_name] = f
                        except Exception as e:
                            # If JSON is corrupted, use filename as display name
                            variant_map[f] = f
            except Exception:
                pass
            
            # Also scan for legacy file types (.glsl, .txt, .png, .jpg)
            try:
                for f in os.listdir(theme_dir):
                    if f.endswith(('.glsl', '.txt', '.png', '.jpg')) and f not in variant_map.values():
                        variant_map[f] = f
            except Exception:
                pass
            
            # Add items to combo box using display names
            if variant_map:
                # Store the mapping for later retrieval
                self.variant_filename_map = variant_map
                self.variant_combo.addItems(sorted(variant_map.keys()))
            else:
                # Fallback to empty list
                self.variant_filename_map = {}

    def _make_anim_combo(self):
        combo = QComboBox()
        combo.setMinimumHeight(32)
        combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        combo.addItem("Cycle All")
        return combo

    def _populate_anim_combo(self, combo, companion_name, preferred="Cycle All"):
        if combo is None:
            return
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("Cycle All")
        if companion_name and companion_name != "Off":
            m_path = os.path.join(COMPANION_DIR, companion_name, "manifest.json")
            if os.path.exists(m_path):
                try:
                    with open(m_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    for anim in sorted(manifest.get("animations", {}).keys()):
                        combo.addItem(anim)
                except Exception:
                    pass
        idx = combo.findText(preferred)
        combo.setCurrentIndex(idx if idx >= 0 else 0)
        combo.blockSignals(False)

    def update_companions(self, theme_name):
        curr = self.companion_combo.currentText()
        self.companion_combo.blockSignals(True)
        self.companion_combo.clear()
        self.companion_combo.addItems(companions)
        idx = self.companion_combo.findText(curr)
        self.companion_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self.companion_combo.blockSignals(False)
        for cb in (getattr(self, "companion_extra1", None), getattr(self, "companion_extra2", None)):
            if cb is None:
                continue
            saved = cb.currentText()
            cb.blockSignals(True)
            cb.clear()
            cb.addItems(companions)
            eidx = cb.findText(saved)
            cb.setCurrentIndex(eidx if eidx >= 0 else 0)
            cb.blockSignals(False)
        if hasattr(self, "companion_anim_combo"):
            self._populate_anim_combo(self.companion_anim_combo, self.companion_combo.currentText(), self.companion_anim_combo.currentText())
        if hasattr(self, "companion_extra1_anim"):
            self._populate_anim_combo(self.companion_extra1_anim, self.companion_extra1.currentText(), self.companion_extra1_anim.currentText())
        if hasattr(self, "companion_extra2_anim"):
            self._populate_anim_combo(self.companion_extra2_anim, self.companion_extra2.currentText(), self.companion_extra2_anim.currentText())

    def rebuild_companion_manifests(self):
        count = rebuild_companion_manifests(force=True)
        companions = ["Off"]
        if os.path.exists(COMPANION_DIR):
            for d in os.listdir(COMPANION_DIR):
                d_path = os.path.join(COMPANION_DIR, d)
                if os.path.isdir(d_path):
                    companions.append(d)
        self.app.available_companions = companions
        self.app.companions_updated.emit(companions)
        self.update_companions(companions)
        self.app.apply_theme()
        QMessageBox.information(
            self,
            "Manifests Rebuilt",
            f"Rebuilt {count} companion manifest(s) from PNG sprite sheets.",
        )

    def save(self):
        c = self.app.config
        # Update restored toggles
        c["browser_spoofing"] = self.browser_spoof.isChecked()
        c["circadian_engine"] = self.circadian.isChecked()
        c["minimize_to_tray"] = self.tray.isChecked()
        c["auto_run"] = self.autorun.isChecked()
        c["always_on_top"] = self.always_on_top.isChecked()
        c["audio_alert"] = self.audio.isChecked()
        c["audio_path"] = self.audio_path.text()
        c["os_toast"] = self.toast.isChecked()
        
        c["discord"] = self.discord.text()
        c["tele_token"] = self.tele_token.text()
        c["tele_chat"] = self.tele_chat.text()
        c["slack"] = self.slack.text()
        c["theme"] = self.theme_combo.currentText()
        # Get actual filename from display name using the map
        display_name = self.variant_combo.currentText()
        c["variant"] = self.variant_filename_map.get(display_name, display_name)
        c["companion"] = self.companion_combo.currentText()
        c["companion_anim_modes"] = [
            self.companion_anim_combo.currentText(),
            self.companion_extra1_anim.currentText(),
            self.companion_extra2_anim.currentText(),
        ]
        c["companion_pinned_anim"] = c["companion_anim_modes"][0]
        extras = []
        for cb in (self.companion_extra1, self.companion_extra2):
            name = cb.currentText()
            if name and name != "Off":
                extras.append(name)
        c["companion_extras"] = extras
        c["render_graphics"] = self.r_graphics.isChecked()
        c["allow_bg_anim"] = self.allow_anim.isChecked()
        c["fps_lock"] = self.fps_lock.isChecked()
        c["combat_mode"] = self.combat_mode.isChecked()
        c["disable_canvas_bg"] = self.disable_canvas_bg.isChecked()
        
        self.app.save_config()
        self.app.apply_theme()
        self.app.apply_window_flags()
        self.app.register_startup(c["auto_run"])
        self.accept()

    def test_webhook_connections(self):
        """Test webhook connections in a background thread"""
        discord_url = self.discord.text()
        tele_token = self.tele_token.text()
        tele_chat = self.tele_chat.text()
        slack_url = self.slack.text()
        
        def test_worker():
            errors = []
            success_count = 0
            
            test_message = "🔔 REONERA: Interface Link Secured. Pipeline Diagnostics [SUCCESS]."
            
            # Test Discord
            if discord_url:
                try:
                    response = requests.post(discord_url, json={"content": test_message}, timeout=5)
                    if response.status_code in [200, 204]:
                        success_count += 1
                    else:
                        errors.append(f"Discord: HTTP {response.status_code}")
                except Exception as e:
                    errors.append(f"Discord: {str(e)}")
            
            # Test Slack
            if slack_url:
                try:
                    response = requests.post(slack_url, json={"text": test_message}, timeout=5)
                    if response.status_code == 200:
                        success_count += 1
                    else:
                        errors.append(f"Slack: HTTP {response.status_code}")
                except Exception as e:
                    errors.append(f"Slack: {str(e)}")
            
            # Test Telegram
            if tele_token and tele_chat:
                try:
                    response = requests.post(
                        f"https://api.telegram.org/bot{tele_token}/sendMessage",
                        data={"chat_id": tele_chat, "text": test_message},
                        timeout=5
                    )
                    if response.status_code == 200:
                        success_count += 1
                    else:
                        errors.append(f"Telegram: HTTP {response.status_code}")
                except Exception as e:
                    errors.append(f"Telegram: {str(e)}")
            
            # Show results on UI thread
            QTimer.singleShot(0, lambda: self.show_test_results(success_count, errors))
        
        threading.Thread(target=test_worker, daemon=True).start()

    def show_test_results(self, success_count, errors):
        """Display test results in message box"""
        if not errors and success_count > 0:
            QMessageBox.information(self, "Diagnostics Complete", f"✅ All webhook connections are green!\n\nSuccessfully connected to {success_count} service(s).")
        elif not errors and success_count == 0:
            QMessageBox.warning(self, "Diagnostics Complete", "⚠️ No webhook URLs configured.\n\nPlease configure at least one webhook service (Discord, Slack, or Telegram) to test connections.")
        else:
            error_text = "\n".join(errors)
            QMessageBox.critical(self, "Diagnostics Failed", f"❌ Connection errors detected:\n\n{error_text}\n\nPlease check your webhook URLs and tokens.")

# ==========================================
# 9. MASTER APPLICATION CONTROLLER
# ==========================================
class REONERA_App(QMainWindow):
    companions_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.setWindowIcon(load_brand_icon())
        self.current_profile = os.path.join(REONERA_DIR, 'default.reonera_profile')
        if len(sys.argv) > 1 and sys.argv[1].lower().endswith('.reonera_profile'):
            ext = os.path.abspath(sys.argv[1])
            if os.path.exists(ext):
                self.current_profile = ext
        self.config = {
            "window_title": None, "refresh_rel": None, "zone_rel": None, "target_bounds": None,
            "exclusion_zones": [],
            "theme": "The Eternal Ouroboros", "variant": "", "companion": "Off",
            "companion_pinned_anim": "Cycle All",
            "companion_anim_modes": ["Cycle All", "Cycle All", "Cycle All"],
            "companion_extras": [],
            "companion_positions": {},
            "render_graphics": True, "allow_bg_anim": True, "fps_lock": False, "combat_mode": False,
            "discord": "", "tele_token": "", "tele_chat": "", "slack": "",
            "audio_alert": True, "audio_path": "", "os_toast": True,
            "browser_spoofing": True, "circadian_engine": True, "minimize_to_tray": True, "auto_run": False,
            "always_on_top": False, "disable_canvas_bg": False
        }
        self.monitor_thread = None
        self._start_pos = None
        self.compact_mode = False
        
        # Async Auto-Compiler Dispatch
        self.available_companions = ["Off"]
        self.compiler_thread = CompanionCompilerThread()
        self.compiler_thread.companions_ready.connect(self.on_companions_ready)
        self.compiler_thread.start()
        
        self.load_config()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.Window)
        self.setMinimumSize(500, 600)
        self.resize(850, 820)
        self._resize_edge = None
        self._resize_start_geo = None
        self._resize_start_pos = None
        self._resize_margin = 12
        self._header_drag_height = 52

        self.build_ui()
        apply_brand_icon_to_window(self)
        self.apply_theme()
        self.apply_window_flags()
        self.register_context_menu()
        
        # Create system tray icon at startup
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(load_tray_icon())
        
        menu = QMenu()
        restore_act = QAction("Show REONERA Console", self)
        restore_act.triggered.connect(self.showNormal)
        quit_act = QAction("Force Terminate Engine", self)
        quit_act.triggered.connect(QApplication.instance().quit)
        
        menu.addAction(restore_act)
        menu.addAction(quit_act)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
        
        if self.config.get("auto_run"):
            QTimer.singleShot(500, self._maybe_auto_start)

    def raise_companions(self):
        for comp in getattr(self, "companions", []):
            if comp.isVisible():
                comp.raise_()
                comp.show()

    def open_settings(self):
        SettingsDialog(self).exec()
        self.raise_companions()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.ActivationChange and self.isActiveWindow():
            self.raise_companions()

    def on_companions_ready(self, companions):
        self.available_companions = companions
        self.companions_updated.emit(companions)

    def build_ui(self):
        self.gl_widget = ShaderBackground(self)
        self.gl_widget.setGeometry(0, 0, self.width(), self.height())
        self.gl_widget.lower()
        self.gl_widget.error_signal.connect(self.log)

        self.gl_timer = QTimer(self)
        self.gl_timer.timeout.connect(self.gl_widget.update_time)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize IconRenderer with current theme
        self.current_theme_color = THEMES.get(self.config.get("theme", "The Eternal Ouroboros"), {}).get("fg", "#FFD700")
        
        # Header (Now functions cleanly as a unified Title Bar)
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(10, 8, 10, 8)
        
        # Add app icon beside title
        icon_label = QLabel()
        icon_label.setPixmap(load_brand_pixmap(24))
        h_layout.addWidget(icon_label)
        
        title_label = QLabel("REONERA Engine")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        h_layout.addWidget(title_label)
        h_layout.addStretch()
        
        btn_set = QPushButton("Settings")
        btn_set.setIcon(IconRenderer.render_icon('settings', 20, self.current_theme_color))
        btn_set.clicked.connect(self.open_settings)
        btn_abt = QPushButton("About")
        btn_abt.setIcon(IconRenderer.render_icon('about', 20, self.current_theme_color))
        btn_abt.clicked.connect(self.show_about)
        btn_cmp = QPushButton("Compact")
        btn_cmp.setIcon(IconRenderer.render_icon('compact', 20, self.current_theme_color))
        btn_cmp.clicked.connect(self.toggle_compact)
        
        # FIX: Restored native Title Bar minimize feature
        btn_min = QPushButton("—")
        btn_min.clicked.connect(self.showMinimized)
        
        btn_close = QPushButton("")
        btn_close.setIcon(IconRenderer.render_icon('close', 20, self.current_theme_color))
        btn_close.clicked.connect(self.close)
        
        for b in [btn_set, btn_abt, btn_cmp, btn_min, btn_close]:
            h_layout.addWidget(b)
        main_layout.addLayout(h_layout)

        self.content_container = QWidget()
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(12)

        prof_lay = QHBoxLayout()
        prof_lay.setSpacing(8)
        prof_lay.addWidget(QLabel("Profile:"))
        self.profile_combo = QComboBox()
        self.profile_combo.activated.connect(self.switch_profile)
        prof_lay.addWidget(self.profile_combo, 1)
        btn_new_prof = QPushButton("New")
        btn_new_prof.setIcon(IconRenderer.render_icon('new', 16, self.current_theme_color))
        btn_new_prof.clicked.connect(self.create_profile)
        prof_lay.addWidget(btn_new_prof)
        content_layout.addLayout(prof_lay)
        self.refresh_profile_list()

        # Status
        self.status_lbl = QLabel("Status: SETUP REQUIRED")
        self.status_lbl.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        content_layout.addWidget(self.status_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.ref_lbl = QLabel("❌ Refresh: NOT SET")
        self.zone_lbl = QLabel("❌ Safe Zone: NOT SET")
        self.tgt_lbl = QLabel("❌ Vision Target: NOT SET")
        self.shift_lbl = QLabel("Shift Engine: STANDBY")
        for l in [self.ref_lbl, self.zone_lbl, self.tgt_lbl]:
            l.setCursor(Qt.CursorShape.PointingHandCursor)
            content_layout.addWidget(l, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.shift_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        # Telemetry with AdvancedVisionField
        tel_lay = QHBoxLayout()
        self.chart = TelemetryChart()
        tel_lay.addWidget(self.chart, 1)
        
        # TechWaveVisualizer - Theme-Adaptive Wave Synthesizer (moved lower)
        self.wave_visualizer = TechWaveVisualizer(self)
        tel_lay.addWidget(self.wave_visualizer)
        content_layout.addLayout(tel_lay)

        # Vision preview — top-right, directly above the log panel
        vision_row = QHBoxLayout()
        vision_row.addStretch(1)
        self.vision_field = AdvancedVisionField(self)
        self.vision_field.app_ref = self
        vision_row.addWidget(self.vision_field)
        content_layout.addLayout(vision_row)

        # Live vision map polling timer (10 FPS)
        self.preview_timer = QTimer(self)
        self.preview_timer.timeout.connect(self.poll_vision_feed)
        self.preview_timer.start(100)

        # Logger
        self.log_txt = QTextEdit()
        self.log_txt.setReadOnly(True)
        self.log_txt.setFixedHeight(150)
        content_layout.addWidget(self.log_txt)

        # Config Buttons with IconRenderer
        s_lay = QHBoxLayout()
        s_lay.setSpacing(8)
        btn_ref = QPushButton("Mark Refresh")
        btn_ref.setIcon(IconRenderer.render_icon('refresh', 18, self.current_theme_color))
        btn_ref.clicked.connect(self.show_ref_overlay)
        btn_zone = QPushButton("Drag Safe Zone")
        btn_zone.setIcon(IconRenderer.render_icon('zone', 18, self.current_theme_color))
        btn_zone.clicked.connect(self.show_zone_overlay)
        btn_tgt = QPushButton("Snip Target")
        btn_tgt.setIcon(IconRenderer.render_icon('target', 18, self.current_theme_color))
        btn_tgt.clicked.connect(self.show_tgt_overlay)
        btn_exc = QPushButton("Mask Exclude")
        btn_exc.setIcon(IconRenderer.render_icon('exclude', 18, self.current_theme_color))
        btn_exc.clicked.connect(self.show_exc_overlay)
        for b in [btn_ref, btn_zone, btn_tgt, btn_exc]: s_lay.addWidget(b)
        content_layout.addLayout(s_lay)

        adv_lay = QHBoxLayout()
        adv_lay.setSpacing(8)
        btn_login = QPushButton("Snip Login Wall")
        btn_login.setIcon(IconRenderer.render_icon('lock', 18, self.current_theme_color))
        btn_login.clicked.connect(self.show_login_overlay)
        btn_clear = QPushButton("Clear Masks")
        btn_clear.setIcon(IconRenderer.render_icon('clear', 18, self.current_theme_color))
        btn_clear.clicked.connect(self.clear_exclusion_masks)
        adv_lay.addWidget(btn_login)
        adv_lay.addWidget(btn_clear)
        content_layout.addLayout(adv_lay)

        # Run Buttons with IconRenderer
        self.btn_start = QPushButton("START ENGINE")
        self.btn_start.setFixedHeight(45)
        self.btn_start.setIcon(IconRenderer.render_icon('start', 24, self.current_theme_color))
        self.btn_start.clicked.connect(self.start_monitoring)
        self.btn_stop = QPushButton("STOP ENGINE")
        self.btn_stop.setFixedHeight(45)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setIcon(IconRenderer.render_icon('stop', 24, self.current_theme_color))
        self.btn_stop.clicked.connect(self.stop_monitoring)
        c_lay = QHBoxLayout(); c_lay.setSpacing(8); c_lay.addWidget(self.btn_start); c_lay.addWidget(self.btn_stop)
        content_layout.addLayout(c_lay)

        main_layout.addWidget(self.content_container, 1)

        self.compact_container = QWidget()
        cmp_lay = QVBoxLayout(self.compact_container)
        self.cmp_status = QLabel("STANDBY")
        self.cmp_status.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        cmp_lay.addWidget(self.cmp_status, alignment=Qt.AlignmentFlag.AlignCenter)
        cmp_b_lay = QHBoxLayout()
        b_c_start = QPushButton("Start")
        b_c_start.setIcon(IconRenderer.render_icon('start', 18, self.current_theme_color))
        b_c_start.clicked.connect(self.start_monitoring)
        b_c_stop = QPushButton("Stop")
        b_c_stop.setIcon(IconRenderer.render_icon('stop', 18, self.current_theme_color))
        b_c_stop.clicked.connect(self.stop_monitoring)
        b_c_exp = QPushButton("Expand")
        b_c_exp.setIcon(IconRenderer.render_icon('compact', 18, self.current_theme_color))
        b_c_exp.clicked.connect(self.toggle_compact)
        for b in [b_c_start, b_c_stop, b_c_exp]: cmp_b_lay.addWidget(b)
        cmp_lay.addLayout(cmp_b_lay)
        self.compact_container.hide()
        main_layout.addWidget(self.compact_container)

        # Companions — draggable layer over content
        self.companions = []
        self.companion = None  # primary reference for combat triggers

        # Bottom-right resize grip for frameless window
        self.size_grip = QSizeGrip(self.central_widget)
        
        self.check_readiness()
        QTimer.singleShot(0, self.refresh_companions)

    def refresh_companions(self):
        """Build or refresh all companion widgets from config."""
        c = self.config
        for comp in self.companions:
            comp.hide()
            comp.deleteLater()
        self.companions = []
        self.companion = None

        if not c.get("render_graphics", True) or not c.get("allow_bg_anim", True):
            return

        positions = c.get("companion_positions", {})
        anim_modes = c.get("companion_anim_modes", [])
        legacy_anim = c.get("companion_pinned_anim", "Cycle All")
        names = []
        primary = c.get("companion", "Off")
        if primary and primary != "Off":
            names.append(primary)
        for extra in c.get("companion_extras", []):
            if extra and extra != "Off" and extra not in names:
                names.append(extra)

        for idx, name in enumerate(names):
            slot_key = str(idx)
            saved = positions.get(slot_key, positions.get(name, {}))
            comp = CompanionCombatEngine(self, slot_id=idx)
            comp.error_signal.connect(self.log)
            comp.position_changed.connect(lambda x, y, i=idx: self._save_companion_position(i, x, y))
            pinned = anim_modes[idx] if idx < len(anim_modes) else legacy_anim
            comp.refresh_settings(c, c_name=name, pinned_anim=pinned, saved_pos=saved)
            if comp.isVisible():
                self.companions.append(comp)
                if idx == 0:
                    self.companion = comp
        self.position_companions()

    def _save_companion_position(self, slot_id, x, y):
        positions = self.config.setdefault("companion_positions", {})
        positions[str(slot_id)] = {"gx": x, "gy": y, "x": x, "y": y}
        self.save_config()

    def position_companions(self):
        """Default-position companions that have no saved coordinates."""
        if not self.companions:
            return
        anchor = self.log_txt.mapToGlobal(QPoint(0, 0))
        default_y = anchor.y() - self.companions[0].height() - 8
        for idx, comp in enumerate(self.companions):
            if comp.saved_x is None or comp.saved_y is None:
                comp.move(anchor.x() + 10 + idx * 30, default_y - idx * 20)
            comp.raise_()
            comp.show()

    def _vision_coords_to_frame(self, x, y):
        tb = self.config.get("target_bounds")
        if tb and len(tb) == 4:
            rel_x = x - tb[0]
            rel_y = y - tb[1]
            if 0 <= rel_x <= tb[2] and 0 <= rel_y <= tb[3]:
                return rel_x, rel_y
        return x, y

    def on_vision_click(self, x, y):
        vm = getattr(self.vision_field, "vision_map_window", None)
        if not vm or not vm.isVisible() or not vm.heatmap_enabled:
            return
        fx, fy = self._vision_coords_to_frame(x, y)
        vm.add_click_point(fx, fy)

    def on_vision_flash(self, zone_type, point):
        vm = getattr(self.vision_field, "vision_map_window", None)
        if not vm or not vm.isVisible() or not vm.flash_zones_enabled:
            return
        fx, fy = self._vision_coords_to_frame(*point)
        vm.trigger_flash_zone((fx, fy), zone_type)

    def poll_vision_feed(self):
        """Live vision map polling at 10 FPS."""
        try:
            import pyautogui
            import numpy as np
            monitor_mode = "target"
            vm = getattr(self.vision_field, "vision_map_window", None)
            if vm and vm.isVisible():
                monitor_mode = vm.monitor_mode
            if monitor_mode == "window":
                geo = self.geometry()
                screenshot = pyautogui.screenshot(region=(geo.x(), geo.y(), geo.width(), geo.height()))
            elif self.config.get("target_bounds"):
                screenshot = pyautogui.screenshot(region=self.config["target_bounds"])
            else:
                return
            frame_array = np.array(screenshot)
            self.vision_field.update_frame(frame_array)
        except Exception:
            pass

    def show_ref_overlay(self):
        self.ref_overlay = SelectorOverlay(self.save_ref, "point")
        self.ref_overlay.show()

    def show_zone_overlay(self):
        self.zone_overlay = SelectorOverlay(self.save_zone, "rect", "blue")
        self.zone_overlay.show()

    def show_tgt_overlay(self):
        self.tgt_overlay = SelectorOverlay(self.save_tgt, "rect", "green")
        self.tgt_overlay.show()

    def show_exc_overlay(self):
        self.exc_overlay = SelectorOverlay(self.save_exclusion, "rect", "orange")
        self.exc_overlay.show()

    def show_login_overlay(self):
        self.login_overlay = SelectorOverlay(self.save_login_wall, "rect", "purple")
        self.login_overlay.show()

    def _hit_resize_edge(self, pos):
        m = self._resize_margin
        w, h = self.width(), self.height()
        on_right = pos.x() >= w - m
        on_bottom = pos.y() >= h - m
        if on_right and on_bottom:
            return "corner"
        if on_right:
            return "right"
        if on_bottom:
            return "bottom"
        return None

    def _update_resize_cursor(self, edge):
        if edge == "corner":
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in ("right", "left"):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge in ("bottom", "top"):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            edge = self._hit_resize_edge(pos)
            if edge:
                self._resize_edge = edge
                self._resize_start_geo = self.geometry()
                self._resize_start_pos = event.globalPosition().toPoint()
                self._start_pos = None
            elif pos.y() <= self._header_drag_height:
                self._start_pos = event.globalPosition().toPoint()
                self._resize_edge = None
            else:
                self._start_pos = None
                self._resize_edge = None
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        if self._resize_edge and self._resize_start_geo and self._resize_start_pos is not None:
            delta = event.globalPosition().toPoint() - self._resize_start_pos
            geo = QRect(self._resize_start_geo)
            min_w, min_h = self.minimumWidth(), self.minimumHeight()
            if self._resize_edge in ("right", "corner"):
                geo.setWidth(max(min_w, self._resize_start_geo.width() + delta.x()))
            if self._resize_edge in ("bottom", "corner"):
                geo.setHeight(max(min_h, self._resize_start_geo.height() + delta.y()))
            self.setGeometry(geo)
        elif self._start_pos is not None:
            delta = event.globalPosition().toPoint() - self._start_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._start_pos = event.globalPosition().toPoint()
        else:
            self._update_resize_cursor(self._hit_resize_edge(pos))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._start_pos = None
        self._resize_edge = None
        self._resize_start_geo = None
        self._resize_start_pos = None
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        apply_brand_icon_to_window(self)
        self.gl_widget.setGeometry(0, 0, self.width(), self.height())
        self.gl_widget.lower()
        self.central_widget.raise_()
        QTimer.singleShot(0, self.position_companions)
        for comp in getattr(self, "companions", []):
            if comp.e1_manifest:
                comp.show()
                comp.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.gl_widget.setGeometry(0, 0, self.width(), self.height())
        self.gl_widget.lower()
        self.central_widget.raise_()
        self.position_companions()
        if hasattr(self, 'size_grip') and hasattr(self, 'central_widget'):
            self.size_grip.move(
                self.central_widget.width() - self.size_grip.width(),
                self.central_widget.height() - self.size_grip.height(),
            )
            self.size_grip.raise_()

    # FIX: Hijack the close button to minimize to the Windows System Tray
    def closeEvent(self, event):
        if not self.config.get("minimize_to_tray", True):
            QApplication.instance().quit()
            return
            
        event.ignore()
        self.hide()
        for comp in getattr(self, "companions", []):
            comp.hide()
        self.log("Engine minimized to System Tray. Still monitoring.")

    def apply_window_flags(self):
        if self.config.get("always_on_top", False):
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.Window)
        self.show()
        apply_brand_icon_to_window(self)

    def apply_theme(self):
        c = self.config
        t_name = c.get("theme", "The Eternal Ouroboros")
        theme = THEMES.get(t_name)

        # Global Cascading QSS with theme name for asset checking
        QApplication.instance().setStyleSheet(generate_qss(theme, t_name))

        # Graphics Toggles with proper shader fallback
        if c.get("disable_canvas_bg", False):
            self.gl_timer.stop()
            self.gl_widget.hide()
            self.setStyleSheet("")
            # Set solid background color on central widget as fallback
            self.central_widget.setStyleSheet(f"background-color: {theme['bg']};")
        elif c.get("render_graphics", True):
            self.gl_widget.show()
            self.setStyleSheet("")
            self.central_widget.setStyleSheet("")
            theme_dir = os.path.join(BG_DIR, "".join(x for x in t_name if x.isalnum() or x in " -_"))
            variant = c.get("variant", "")
            self.gl_widget.set_custom_assets(theme_dir, theme["bg"], variant)
            
            if c.get("allow_bg_anim", True):
                self.gl_timer.start(33 if c.get("fps_lock", False) else 16)
            else:
                self.gl_timer.stop()
                # Freeze shader on current frame instead of making transparent
                self.gl_widget.update()
        else:
            self.gl_timer.stop()
            self.gl_widget.hide()
            self.setStyleSheet("")
            # Set solid background color as fallback
            self.central_widget.setStyleSheet(f"background-color: {theme['bg']};")

        self.chart.set_color(theme["warn"])
        self.refresh_companions()
        
        # Update TechWaveVisualizer theme if it exists
        if hasattr(self, 'wave_visualizer'):
            self.wave_visualizer.set_theme(t_name)
        
        # Update IconRenderer theme color and refresh all button icons
        self.current_theme_color = theme["fg"]
        IconRenderer.set_theme_color(theme["fg"])
        self._refresh_button_icons()
    
    def _refresh_button_icons(self):
        """Refresh all button icons with the current theme color."""
        # Header buttons
        if hasattr(self, 'content_container'):
            for widget in self.content_container.findChildren(QPushButton):
                if widget.text():
                    icon_name = self._get_icon_name_for_button(widget.text())
                    if icon_name:
                        widget.setIcon(IconRenderer.render_icon(icon_name, 18, self.current_theme_color))
        
        # Compact container buttons
        if hasattr(self, 'compact_container'):
            for widget in self.compact_container.findChildren(QPushButton):
                if widget.text():
                    icon_name = self._get_icon_name_for_button(widget.text())
                    if icon_name:
                        widget.setIcon(IconRenderer.render_icon(icon_name, 18, self.current_theme_color))
    
    def _get_icon_name_for_button(self, button_text):
        """Map button text to icon name."""
        text_lower = button_text.lower()
        if 'settings' in text_lower:
            return 'settings'
        elif 'about' in text_lower:
            return 'about'
        elif 'compact' in text_lower or 'expand' in text_lower:
            return 'compact'
        elif 'refresh' in text_lower:
            return 'refresh'
        elif 'zone' in text_lower:
            return 'zone'
        elif 'target' in text_lower or 'snip' in text_lower:
            return 'target'
        elif 'exclude' in text_lower or 'mask' in text_lower:
            return 'exclude'
        elif 'login' in text_lower or 'wall' in text_lower:
            return 'lock'
        elif 'clear' in text_lower:
            return 'clear'
        elif 'start' in text_lower:
            return 'start'
        elif 'stop' in text_lower:
            return 'stop'
        elif 'new' in text_lower:
            return 'new'
        elif 'bake' in text_lower:
            return 'bake'
        elif 'deploy' in text_lower:
            return 'deploy'
        elif 'test' in text_lower:
            return 'test'
        elif 'save' in text_lower or 'apply' in text_lower:
            return 'save'
        return None

    def log(self, msg):
        if not hasattr(self, 'log_txt'): return
        self.log_txt.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        if self.log_txt.document().blockCount() > 200:
            cursor = self.log_txt.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            cursor.select(cursor.SelectionType.BlockUnderCursor)
            cursor.removeSelectedText()

    def load_config(self):
        try:
            if os.path.exists(self.current_profile):
                with open(self.current_profile, 'r') as f:
                    self.config.update(CryptoManager.decrypt(f.read()))
        except Exception as e: print(f"Profile error: {e}")

    def save_config(self):
        try:
            with open(self.current_profile, 'w') as f:
                f.write(CryptoManager.encrypt(self.config))
        except Exception as e: self.log(f"Save error: {e}")

    def save_ref(self, title, rel_x, rel_y, ax, ay):
        self.config["window_title"] = title; self.config["refresh_rel"] = (rel_x, rel_y)
        self.save_config(); self.check_readiness()

    def save_zone(self, title, rb, ab):
        self.config["window_title"] = title; self.config["zone_rel"] = rb
        self.save_config(); self.check_readiness()

    def save_tgt(self, title, rb, ab):
        try:
            pyautogui.screenshot().crop(ab).save(os.path.join(REONERA_DIR, 'target_state.png'))
            self.config["window_title"] = title; self.config["target_bounds"] = rb
            self.save_config(); self.check_readiness()
        except Exception as e: self.log(f"Capture error: {e}")

    def save_exclusion(self, title, rb, ab):
        self.config.setdefault("exclusion_zones", []).append(rb)
        self.save_config(); self.log(f"Mask added. Total: {len(self.config['exclusion_zones'])}")

    def clear_exclusion_masks(self):
        count = len(self.config.get("exclusion_zones", []))
        self.config["exclusion_zones"] = []
        self.save_config()
        self.log(f"Cleared {count} exclusion mask(s).")

    def save_login_wall(self, title, rb, ab):
        try:
            pyautogui.screenshot().crop(ab).save(os.path.join(REONERA_DIR, 'login_wall.png'))
            self.log("Login wall reference captured. Engine will halt if detected.")
        except Exception as e:
            self.log(f"Login wall capture error: {e}")

    def refresh_profile_list(self):
        if not hasattr(self, 'profile_combo'): return
        current = os.path.basename(self.current_profile)
        profiles = sorted(f for f in os.listdir(REONERA_DIR) if f.endswith('.reonera_profile'))
        if not profiles:
            profiles = [current]
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        self.profile_combo.addItems(profiles)
        idx = self.profile_combo.findText(current)
        self.profile_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self.profile_combo.blockSignals(False)

    def switch_profile(self, index):
        name = self.profile_combo.itemText(index)
        path = os.path.join(REONERA_DIR, name)
        if not os.path.exists(path): return
        if self.monitor_thread and self.monitor_thread.isRunning():
            self.stop_monitoring()
        self.current_profile = path
        self.load_config()
        self.apply_theme()
        self.check_readiness()
        self.log(f"Profile loaded: {name}")

    def create_profile(self):
        base, n = "profile", 1
        while os.path.exists(os.path.join(REONERA_DIR, f"{base}_{n}.reonera_profile")):
            n += 1
        self.current_profile = os.path.join(REONERA_DIR, f"{base}_{n}.reonera_profile")
        self.save_config()
        self.refresh_profile_list()
        self.log(f"Created profile: {os.path.basename(self.current_profile)}")

    def check_readiness(self):
        if all([self.config.get(k) for k in ["refresh_rel", "zone_rel", "target_bounds"]]):
            self.btn_start.setEnabled(True)
            self.status_lbl.setText("Status: SYSTEM READY")
            self.ref_lbl.setText(f"✅ Refresh: {self.config['refresh_rel']}")
            self.zone_lbl.setText(f"✅ Zone: {self.config['zone_rel']}")
            self.tgt_lbl.setText("✅ Target Map Locked")
        else: self.btn_start.setEnabled(False)

    def toggle_compact(self):
        if not self.compact_mode:
            self.content_container.hide()
            self.compact_container.show()
            self.resize(300, 120)
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.compact_mode = True
        else:
            self.compact_container.hide()
            self.content_container.show()
            self.resize(850, 820)
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
            self.compact_mode = False
        self.show()

    def _maybe_auto_start(self):
        if all([self.config.get(k) for k in ["refresh_rel", "zone_rel", "target_bounds"]]):
            self.start_monitoring()

    def start_monitoring(self):
        if self.monitor_thread and self.monitor_thread.isRunning():
            self.log("Engine already active.")
            return
        self.btn_start.setEnabled(False); self.btn_stop.setEnabled(True)
        self.monitor_thread = MonitorThread(self.config)
        self.monitor_thread.log_signal.connect(self.log)
        self.monitor_thread.status_signal.connect(lambda t, c: (self.status_lbl.setText(f"Status: {t}"), self.cmp_status.setText(t)))
        self.monitor_thread.shift_signal.connect(self.shift_lbl.setText)
        self.monitor_thread.telemetry_signal.connect(self.chart.update_data)
        self.monitor_thread.alert_signal.connect(self.trigger_alerts)
        self.monitor_thread.match_preview_signal.connect(self.update_preview)
        self.monitor_thread.combat_trigger_signal.connect(
            lambda: self.companion.trigger_attack() if self.companion else None
        )
        self.monitor_thread.vision_click_signal.connect(self.on_vision_click)
        self.monitor_thread.vision_flash_signal.connect(self.on_vision_flash)
        self.monitor_thread.finished_signal.connect(self.stop_monitoring)
        self.monitor_thread.start()

    def stop_monitoring(self):
        if self.monitor_thread: self.monitor_thread.is_running = False
        self.check_readiness()
        self.btn_stop.setEnabled(False)
        self.status_lbl.setText("Status: IDLE")
        self.cmp_status.setText("STANDBY")
        self.shift_lbl.setText("Shift Engine: STANDBY")
        self.log("Engine suspended.")

    def update_preview(self, rgb_arr):
        try:
            # Update the AdvancedVisionField widget instead of the simple preview label
            self.vision_field.update_frame(rgb_arr)
        except Exception as e: self.log(f"Preview Frame Drop: {e}")

    # FIX: Safely route exceptions and enable Local Audio Alerts
    def trigger_alerts(self, message):
        c = self.config

        if c.get("audio_alert", True):
            try:
                if c.get("audio_path") and os.path.exists(c.get("audio_path")):
                    winsound.PlaySound(c["audio_path"], winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except: pass

        if c.get("os_toast", True):
            try:
                notification.notify(title="REONERA Alert", message=message, timeout=5)
            except: pass

        def net_worker():
            pl = {"content": f"🔔 **REONERA:** {message}"}
            try:
                if c.get("discord"): requests.post(c["discord"], json=pl, timeout=5)
                if c.get("slack"): requests.post(c["slack"], json={"text": pl["content"]}, timeout=5)
                if c.get("tele_token") and c.get("tele_chat"):
                    requests.post(f"https://api.telegram.org/bot{c['tele_token']}/sendMessage", data={"chat_id": c["tele_chat"], "text": message}, timeout=5)
            except Exception as e:
                print(f"Alert Dispatch Failed: {e}")

        threading.Thread(target=net_worker, daemon=True).start()

    # FIX: Restore Auto-Run Windows Registry Integration
    def register_startup(self, enable):
        try:
            import winreg
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
            if enable: winreg.SetValueEx(k, 'REONERA', 0, winreg.REG_SZ, sys.argv[0])
            else:
                try: winreg.DeleteValue(k, 'REONERA')
                except: pass
            winreg.CloseKey(k)
        except: pass

    # FIX: Restore Exe Build Pipeline
    def bake_executable(self):
        def worker():
            self.log("🚀 Booting PyInstaller Build Pipeline...")
            try:
                icon_ico = _brand_ico_path()
                logo_png = _brand_logo_path()
                add_sep = ";" if os.name == 'nt' else ":"
                subprocess.check_call([
                    "pyinstaller", "--noconsole", "--onefile",
                    f"--icon={icon_ico}",
                    f"--add-data={logo_png}{add_sep}assets",
                    f"--add-data={icon_ico}{add_sep}assets",
                    sys.argv[0],
                ])
                self.log("✅ Compilation successful! Executable in 'dist'.")
                os.startfile("dist")
            except Exception as e: self.log(f"❌ Compilation failed: {e}")
        threading.Thread(target=worker, daemon=True).start()

    def deploy_shortcuts(self):
        ans = QMessageBox.question(self, "Authorize Deployment", "Deploy shortcuts to Desktop and Start Menu?")
        if ans == QMessageBox.StandardButton.Yes:
            try:
                import win32com.client
                desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
                start = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs")
                exe = os.path.abspath(sys.argv[0])
                for d in [desktop, start]:
                    shell = win32com.client.Dispatch('WScript.Shell')
                    sc = shell.CreateShortCut(os.path.join(d, "REONERA.lnk"))
                    sc.Targetpath = exe; sc.WorkingDirectory = os.path.dirname(exe)
                    sc.Description = "REONERA Automation Platform"; sc.save()
                QMessageBox.information(self, "Success", "Shortcuts deployed securely.")
            except Exception as e:
                self.log(f"Deployment Error: {e}")

    def register_context_menu(self):
        try:
            import winreg
            winreg.SetValue(winreg.HKEY_CURRENT_USER, r"Software\Classes\.reonera_profile", winreg.REG_SZ, "ReoneraProfile")
            k = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"Software\Classes\ReoneraProfile\shell\Launch with REONERA\command", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(k, "", 0, winreg.REG_SZ, f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}" "%1"')
            winreg.CloseKey(k)
        except: pass

    def show_about(self):
        d = QDialog(self)
        d.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        d.setFixedSize(400, 300)
        l = QVBoxLayout(d)
        lbl1 = QLabel("REONERA")
        lbl1.setFont(QFont("Arial", 14, QFont.Weight.Bold)); lbl1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl2 = QLabel(f"Expert High-Fidelity Automation Platform\nCopyright © 2026. Version {APP_VERSION}")
        lbl2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setText("MIT License + The Commons Clause\n\nPermission is hereby granted...\n\n\"Commons Clause\" License Condition v1.0\nWithout limiting other conditions in the License, the grant of rights under the License will not include, and the License does not grant to you, the right to Sell the Software.")
        btn = QPushButton("Close"); btn.clicked.connect(d.reject)
        for w in [lbl1, lbl2, txt, btn]: l.addWidget(w)
        d.exec()

if __name__ == "__main__":
    try:
        print("DEBUG: Main entry point reached")
        _ensure_windows_app_id()
        print("DEBUG: Windows app ID ensured")
        app = QApplication.instance()
        if not app:
            print("DEBUG: Creating new QApplication")
            app = QApplication(sys.argv)
        app.setWindowIcon(load_brand_icon())
        print("DEBUG: Window icon set")
        
        # Integrate 5-second startup splash screen
        splash = StartupSplash()
        if splash.exec() == QDialog.DialogCode.Accepted:
            window = REONERA_App()
            print("DEBUG: Window created")
            apply_brand_icon_to_window(window)
            window.show()
            apply_brand_icon_to_window(window)
            print("DEBUG: Window shown")
            sys.exit(app.exec())
        else:
            sys.exit(0)
    except Exception as e:
        print(f"DEBUG: Exception in main: {e}")
        import traceback
        traceback.print_exc()
        _show_fatal_error(f"REONERA failed to start:\n{e}")
        sys.exit(1)
# --- END OF FILE text/x-python ---
