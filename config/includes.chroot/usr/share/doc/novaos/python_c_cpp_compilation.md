# Compiling and Running Code in NovaOS

NovaOS comes pre-configured with essential compilers and interpreters. Here is how you can use them from the terminal.

## C Programming
NovaOS uses `gcc` (GNU Compiler Collection) for C programming.

1. **Write your code:** `nano hello.c`
2. **Compile the code:** 
   ```bash
   gcc hello.c -o hello
   ```
   *(This creates an executable file named `hello`)*
3. **Run the executable:**
   ```bash
   ./hello
   ```

## C++ Programming
NovaOS uses `g++` for C++ programming.

1. **Write your code:** `nano hello.cpp`
2. **Compile the code:** 
   ```bash
   g++ hello.cpp -o hello
   ```
3. **Run the executable:**
   ```bash
   ./hello
   ```

## Python Programming
Python 3 is installed by default. You don't need to compile Python code; you just run it.

1. **Write your code:** `nano script.py`
2. **Run the script:**
   ```bash
   python3 script.py
   ```
3. **Interactive Mode:** Simply type `python3` in the terminal to open the Python interactive shell. Type `exit()` or press `Ctrl+D` to leave.

## Java Programming
Java Development Kit (JDK) is included.

1. **Write your code:** `nano HelloWorld.java` *(Note: Class name must match file name)*
2. **Compile the code:**
   ```bash
   javac HelloWorld.java
   ```
   *(This creates a `HelloWorld.class` file)*
3. **Run the program:**
   ```bash
   java HelloWorld
   ```
