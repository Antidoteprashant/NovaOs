#!/usr/bin/env python3
"""NovaOS Welcome — first-login app for NovaOS students.

A lightweight PyQt5 GUI with:
  - Welcome / tour (first-run only)
  - Quick links to docs, dev setup, student toolkit
  - A "Don't show again" toggle

Run as `novaos-welcome` (installed by install-branding.sh into /usr/bin/)
or as `python3 welcome.py --first-run` to force the tour.

Memory: ~30-40 MB while open. Closes entirely on window close.
"""
from __future__ import annotations

import os
import sys
import subprocess
import argparse
from pathlib import Path
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QIcon, QFont, QDesktopServices, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QCheckBox, QSpacerItem,
    QSizePolicy, QGridLayout, QToolButton
)

# -- Asset paths (configured at install time by install-branding.sh) ----
ASSETS = Path("/usr/share/novaos")
LOGO_PATH = ASSETS / "icons" / "novaos-logo.svg"
WALLPAPER_PATH = ASSETS / "wallpaper" / "novaos-wallpaper.png"
CONFIG_DIR = Path.home() / ".config" / "novaos"

# -- Design tokens (mirror docs/design-tokens.txt) ----------------------
BG_DEEP = "#0E1620"
BG_SURFACE = "#161E2A"
BG_ELEVATED = "#1E2A3A"
BORDER = "#2A3A50"
FG = "#E6EDF3"
FG_MUTED = "#8B9BB0"
FG_DIM = "#5C6B80"
ACCENT = "#1FB8C1"
ACCENT_HOVER = "#2BD4DE"
SUCCESS = "#4ADE80"

# ------------------------------------------------------------------------
# QSS — single stylesheet applied to the whole app
# ------------------------------------------------------------------------
QSS = f"""
QMainWindow, QWidget#centralWidget {{
    background-color: {BG_DEEP};
    color: {FG};
}}

QFrame#sidebar {{
    background-color: {BG_SURFACE};
    border-right: 1px solid {BORDER};
}}

QFrame#card {{
    background-color: {BG_SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px;
}}

QPushButton#navButton {{
    background-color: transparent;
    color: {FG_MUTED};
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    text-align: left;
    font-size: 10pt;
}}

QPushButton#navButton:hover {{
    background-color: {BG_ELEVATED};
    color: {FG};
}}

QPushButton#navButton:checked {{
    background-color: {BG_ELEVATED};
    color: {ACCENT};
    border-left: 3px solid {ACCENT};
}}

QToolButton#quickLink {{
    background-color: {BG_SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 16px;
    font-size: 10pt;
    color: {FG};
    min-width: 180px;
    max-width: 240px;
    min-height: 80px;
    text-align: left;
}}

QToolButton#quickLink:hover {{
    border-color: {ACCENT};
    background-color: {BG_ELEVATED};
}}

QToolButton#quickLink QLabel#linkTitle {{
    color: {ACCENT};
    font-weight: bold;
    font-size: 11pt;
}}

QToolButton#quickLink QLabel#linkDesc {{
    color: {FG_MUTED};
    font-size: 9pt;
}}

QPushButton#primaryButton {{
    background-color: {ACCENT};
    color: {BG_DEEP};
    border: none;
    border-radius: 6px;
    padding: 10px 24px;
    font-weight: bold;
    font-size: 10pt;
}}

QPushButton#primaryButton:hover {{
    background-color: {ACCENT_HOVER};
}}

QPushButton#secondaryButton {{
    background-color: transparent;
    color: {FG_MUTED};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 9pt;
}}

QPushButton#secondaryButton:hover {{
    color: {FG};
    border-color: {ACCENT};
}}

QLabel#title {{
    color: {FG};
    font-size: 22pt;
    font-weight: bold;
}}

QLabel#subtitle {{
    color: {FG_MUTED};
    font-size: 11pt;
}}

QLabel#cardTitle {{
    color: {ACCENT};
    font-size: 13pt;
    font-weight: bold;
}}

QLabel#cardBody {{
    color: {FG};
    font-size: 10pt;
}}

QLabel#codeBlock {{
    background-color: {BG_DEEP};
    color: {FG};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 12px;
    font-family: "JetBrains Mono", "DejaVu Sans Mono", monospace;
    font-size: 9pt;
}}

QCheckBox {{
    color: {FG_MUTED};
    font-size: 9pt;
    spacing: 6px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    background-color: {BG_ELEVATED};
    border: 1px solid {BORDER};
    border-radius: 3px;
}}

QCheckBox::indicator:checked {{
    background-color: {ACCENT};
    border-color: {ACCENT};
}}
"""

# ------------------------------------------------------------------------
# Pages
# ------------------------------------------------------------------------
class WelcomePage(QWidget):
    """First page — greeting, intro, 'Get started' button."""
    def __init__(self, on_close):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Logo
        if LOGO_PATH.exists():
            logo = QLabel()
            logo.setPixmap(QPixmap(str(LOGO_PATH)).scaled(
                120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(logo, 0, Qt.AlignLeft)

        layout.addSpacing(8)

        title = QLabel("Welcome to NovaOS")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel(
            "A custom Linux distribution built for Computer Science and IT students."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Intro card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        card_title = QLabel("What now?")
        card_title.setObjectName("cardTitle")
        card_layout.addWidget(card_title)

        card_body = QLabel(
            "This quick tour will show you the important parts of NovaOS:\n"
            "  • Where your development tools live\n"
            "  • How to access the student toolkit\n"
            "  • Where to find documentation and help\n\n"
            "Takes about 2 minutes. You can revisit anytime from the menu."
        )
        card_body.setObjectName("cardBody")
        card_body.setWordWrap(True)
        card_layout.addWidget(card_body)

        layout.addWidget(card)

        layout.addStretch()

        # Footer
        footer = QHBoxLayout()
        dont_show = QCheckBox("Don't show on future logins")
        dont_show.stateChanged.connect(lambda s: _set_first_run_pref(s == Qt.Checked))
        footer.addWidget(dont_show)
        footer.addStretch()
        start_btn = QPushButton("Start Tour →")
        start_btn.setObjectName("primaryButton")
        start_btn.clicked.connect(on_close)  # close for now — keep simple
        footer.addWidget(start_btn)
        layout.addLayout(footer)


class QuickLinksPage(QWidget):
    """The 'main' page — quick links for the student."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Quick Links")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel("Everything you need, one click away.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Grid of quick-link cards
        grid = QGridLayout()
        grid.setSpacing(12)

        links = [
            ("Documentation", "Browse NovaOS docs", "https://docs.novaos.local", "📖"),
            ("Dev Setup", "Configure your dev environment", None, "⚙"),
            ("Student Toolkit", "Notes, math, references", None, "🎓"),
            ("Terminal", "Open a terminal window", "qterminal", "💻"),
            ("Files", "File manager", "pcmanfm-qt", "📁"),
            ("Browser", "Open the web browser", "firefox", "🌐"),
            ("System Settings", "Customize NovaOS", "lxqt-config", "🛠"),
            ("Report a Bug", "Tell us what went wrong", "https://github.com/...", "🐛"),
        ]

        for i, (name, desc, target, icon) in enumerate(links):
            btn = QToolButton()
            btn.setObjectName("quickLink")
            btn.setIconSize(QSize(24, 24))
            btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

            # Build a tiny label-layout inside the button via its text
            # (QToolButton has limited layout — use rich text)
            btn.setText(f"  {icon}  {name}\n       {desc}")

            if target:
                if target.startswith("http"):
                    btn.clicked.connect(
                        lambda checked=False, u=target: QDesktopServices.openUrl(QUrl(u))
                    )
                else:
                    btn.clicked.connect(
                        lambda checked=False, cmd=target: subprocess.Popen([cmd])
                    )

            grid.addWidget(btn, i // 2, i % 2)

        layout.addLayout(grid)
        layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setObjectName("secondaryButton")
        close_btn.clicked.connect(self.window().close)
        layout.addWidget(close_btn, 0, Qt.AlignRight)


class DevSetupPage(QWidget):
    """Show the standard NovaOS dev setup recipe."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Development Setup")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel("Get your dev environment ready in 4 commands.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        # Card 1: Git
        card = QFrame()
        card.setObjectName("card")
        cl = QVBoxLayout(card)
        cl.setSpacing(8)
        cl.addWidget(_label("cardTitle", "1. Configure Git"))
        cl.addWidget(_label("cardBody",
            "Set your name and email so commits are correctly attributed:"))
        cl.addWidget(_label("codeBlock",
            'git config --global user.name "Your Name"\n'
            'git config --global user.email "you@school.edu"'))
        layout.addWidget(card)

        # Card 2: Python
        card2 = QFrame()
        card2.setObjectName("card")
        c2l = QVBoxLayout(card2)
        c2l.setSpacing(8)
        c2l.addWidget(_label("cardTitle", "2. Set up Python (for CS courses)"))
        c2l.addWidget(_label("cardBody", "Use a venv per project to avoid conflicts:"))
        c2l.addWidget(_label("codeBlock",
            'python3 -m venv ~/projects/myproject/venv\n'
            'source ~/projects/myproject/venv/bin/activate\n'
            'pip install <packages>'))
        layout.addWidget(card2)

        # Card 3: C/C++
        card3 = QFrame()
        card3.setObjectName("card")
        c3l = QVBoxLayout(card3)
        c3l.setSpacing(8)
        c3l.addWidget(_label("cardTitle", "3. C / C++ toolchain"))
        c3l.addWidget(_label("cardBody",
            "GCC, GDB, Make, and CMake are pre-installed. To verify:"))
        c3l.addWidget(_label("codeBlock",
            'gcc --version\n'
            'gdb --version\n'
            'make --version\n'
            'cmake --version'))
        layout.addWidget(card3)

        # Card 4: VS Code
        card4 = QFrame()
        card4.setObjectName("card")
        c4l = QVBoxLayout(card4)
        c4l.setSpacing(8)
        c4l.addWidget(_label("cardTitle", "4. Your editor"))
        c4l.addWidget(_label("cardBody",
            "Find VS Code in Programming → Editors. Press Meta+E to open from anywhere."))
        layout.addWidget(card4)

        layout.addStretch()


def _label(obj_name: str, text: str) -> QLabel:
    l = QLabel(text)
    l.setObjectName(obj_name)
    l.setWordWrap(True)
    l.setTextInteractionFlags(Qt.TextSelectableByMouse)  # copy code easily
    return l


# ------------------------------------------------------------------------
# Main window
# ------------------------------------------------------------------------
class NovaWelcome(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NovaOS Welcome")
        self.setMinimumSize(880, 560)
        self.resize(960, 640)

        # Apply stylesheet
        self.setStyleSheet(QSS)

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar nav
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sl = QVBoxLayout(sidebar)
        sl.setContentsMargins(12, 20, 12, 12)
        sl.setSpacing(4)

        # Logo
        if LOGO_PATH.exists():
            logo = QLabel()
            logo.setPixmap(QPixmap(str(LOGO_PATH)).scaled(
                48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            sl.addWidget(logo, 0, Qt.AlignHCenter)
            sl.addSpacing(8)

        # Logo text
        brand = QLabel("NovaOS")
        brand.setStyleSheet(f"color: {ACCENT}; font-weight: bold; font-size: 13pt;")
        brand.setAlignment(Qt.AlignCenter)
        sl.addWidget(brand)
        sl.addSpacing(20)

        # Nav buttons
        self.nav_buttons = []
        for i, name in enumerate(["Welcome", "Quick Links", "Dev Setup"]):
            b = QPushButton(name)
            b.setObjectName("navButton")
            b.setCheckable(True)
            b.setAutoExclusive(True)
            b.clicked.connect(lambda checked=False, idx=i: self.stack.setCurrentIndex(idx))
            sl.addWidget(b)
            self.nav_buttons.append(b)

        self.nav_buttons[0].setChecked(True)

        sl.addStretch()

        version = QLabel("v1.0 (2026-07)")
        version.setStyleSheet(f"color: {FG_DIM}; font-size: 8pt;")
        version.setAlignment(Qt.AlignCenter)
        sl.addWidget(version)

        root.addWidget(sidebar)

        # Stacked content
        self.stack = QStackedWidget()
        self.stack.addWidget(WelcomePage(on_close=self.close))
        self.stack.addWidget(QuickLinksPage())
        self.stack.addWidget(DevSetupPage())
        root.addWidget(self.stack, 1)


# ------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------
def _set_first_run_pref(suppress: bool) -> None:
    """Remember the 'Don't show again' preference."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    (CONFIG_DIR / "welcome.cfg").write_text(
        f"first_run={not suppress}\n"
    )


# ------------------------------------------------------------------------
# Entry
# ------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-run", action="store_true",
                        help="Force the welcome page on top (default behavior)")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setApplicationName("NovaOS Welcome")
    app.setApplicationDisplayName("NovaOS Welcome")
    app.setDesktopFileName("novaos-welcome")

    # Default font — Inter if installed, else system
    font = QFont()
    font.setFamily("Inter")
    font.setPointSize(10)
    if QFont("Inter").exactMatch():
        app.setFont(font)

    win = NovaWelcome()
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
