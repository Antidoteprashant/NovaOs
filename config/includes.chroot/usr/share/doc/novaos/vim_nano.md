# Vim and Nano Cheatsheet

Terminal-based text editors are essential for remote servers and quick file editing. NovaOS includes both `nano` (easier for beginners) and `vim` (powerful, but has a learning curve).

## Nano Basics
Nano is straightforward. You use `Ctrl` (`^`) keys to perform actions.

- **Open/Create a file:** `nano filename.txt`
- **Save changes:** `Ctrl + O` (Write Out), then press `Enter`
- **Exit Nano:** `Ctrl + X` (It will prompt you to save if you have unsaved changes)
- **Cut line:** `Ctrl + K`
- **Paste line:** `Ctrl + U`
- **Search (Where Is):** `Ctrl + W`

## Vim Basics
Vim operates in different "modes". It starts in **Command Mode**. You must switch to **Insert Mode** to type text.

- **Open/Create a file:** `vim filename.txt`

### Modes
- **Insert Mode (for typing):** Press `i`. (Press `Esc` to return to Command Mode)
- **Command Mode (for saving/exiting):** Press `Esc`.

### Saving and Exiting (in Command Mode)
- **Save (Write):** `:w` then `Enter`
- **Exit (Quit):** `:q` then `Enter`
- **Save and Exit:** `:wq` or `:x` then `Enter`
- **Exit without saving:** `:q!` then `Enter`

### Navigation and Editing (in Command Mode)
- **Undo:** `u`
- **Redo:** `Ctrl + R`
- **Copy line (Yank):** `yy`
- **Cut line (Delete):** `dd`
- **Paste (Put):** `p`
- **Search:** `/word` then `Enter` (Press `n` for next result)
