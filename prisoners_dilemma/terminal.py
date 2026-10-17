"""Small ASCII/ANSI helpers; no external terminal package is required."""

from enum import Enum
import os
import re
import shutil
import sys
import textwrap


class Color(str, Enum):
    CYAN = "96"
    GREEN = "92"
    RED = "91"
    YELLOW = "93"
    MAGENTA = "95"
    DIM = "2"
    BOLD = "1"


_color_enabled = False
_ansi = re.compile(r"\x1b\[[0-9;]*m")


def _enable_windows_ansi() -> bool:
    """Ask a Windows console to process ANSI; unsupported consoles stay plain."""
    import ctypes
    from ctypes import wintypes

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetStdHandle.argtypes = [wintypes.DWORD]
    kernel.GetStdHandle.restype = wintypes.HANDLE
    kernel.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel.GetConsoleMode.restype = wintypes.BOOL
    kernel.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.SetConsoleMode.restype = wintypes.BOOL
    handle = kernel.GetStdHandle(-11 & 0xFFFFFFFF)  # STD_OUTPUT_HANDLE
    mode = wintypes.DWORD()
    if not kernel.GetConsoleMode(handle, ctypes.byref(mode)):
        return False
    return bool(kernel.SetConsoleMode(handle, mode.value | 0x0004))


def configure_color(mode: str = "auto") -> None:
    global _color_enabled
    if mode not in {"auto", "always", "never"}:
        raise ValueError("Color mode must be auto, always or never.")
    _color_enabled = False
    if mode == "never":
        return
    if mode == "auto" and (
        not sys.stdout.isatty() or "NO_COLOR" in os.environ
        or os.environ.get("TERM") == "dumb"
    ):
        return
    supported = os.name != "nt" or _enable_windows_ansi()
    _color_enabled = mode == "always" or supported


def paint(text: str, color: Color) -> str:
    return f"\033[{color.value}m{text}\033[0m" if _color_enabled else text


def plain(text: str) -> str:
    return _ansi.sub("", text)


def pad(text: str, width: int) -> str:
    """Pad using printed characters, so ANSI codes cannot shift table borders."""
    return text + " " * max(0, width - len(plain(text)))


def panel(title: str, lines: tuple[str, ...] = (), color: Color = Color.CYAN) -> None:
    width = max(28, min(72, shutil.get_terminal_size((80, 24)).columns - 4))
    border = "+" + "-" * (width + 2) + "+"
    print(paint(border, color))
    for line in textwrap.wrap(title, width=width) or [""]:
        print(paint("| " + line.center(width) + " |", color))
    if lines:
        print(paint(border, color))
        for line in lines:
            for part in textwrap.wrap(line, width=width, replace_whitespace=False) or [""]:
                print(paint("|", color) + " " + part.ljust(width) + " " + paint("|", color))
    print(paint(border, color))


def notice(text: str, color: Color = Color.YELLOW) -> None:
    print(paint(f"[!] {text}", color))
