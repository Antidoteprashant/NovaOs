# Linux Basics Cheatsheet

Welcome to the Linux command line! Here are some essential commands you will need for your coursework.

## File Navigation & Management
- `pwd`: Print Working Directory (shows where you are)
- `ls`: List files in the current directory
  - `ls -l`: List in long format (permissions, size, owner)
  - `ls -a`: List all files, including hidden ones (starting with `.`)
- `cd [directory]`: Change directory
  - `cd ..`: Go up one directory level
  - `cd ~`: Go to your home directory
- `mkdir [name]`: Create a new directory
- `rm [file]`: Remove a file
  - `rm -r [directory]`: Remove a directory and its contents recursively
- `cp [source] [destination]`: Copy a file
  - `cp -r [src_dir] [dest_dir]`: Copy a directory
- `mv [source] [destination]`: Move or rename a file

## Process Management
- `top` or `htop`: View active processes and system resource usage
- `ps aux`: List all running processes
- `kill [PID]`: Terminate a process with the given Process ID
- `killall [process_name]`: Terminate all processes with the given name

## File Permissions
- `chmod [permissions] [file]`: Change file permissions
  - Example: `chmod +x script.sh` (make script executable)
- `chown [owner]:[group] [file]`: Change file owner

## Getting Help
- `man [command]`: Open the manual page for a command
- `[command] --help`: Show a brief help message for a command

> **Tip:** You can use the `novaai` command for quick explanations right in your terminal!
