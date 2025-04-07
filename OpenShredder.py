import os
import sys
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import platform
import subprocess
import webbrowser

# Cross-platform admin check
def is_admin():
    if platform.system() == "Windows":
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        # On Linux/macOS, check if the user is root (uid 0)
        return os.geteuid() == 0 if platform.system() != "Windows" else False

# Cross-platform run as admin
def run_as_admin():
    if not is_admin():
        if platform.system() == "Windows":
            script_path = os.path.abspath(__file__)
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}" --elevated', None, 1)
            sys.exit()
        else:
            # On Linux/macOS, use sudo to relaunch the script
            script_path = os.path.abspath(__file__)
            subprocess.run(["sudo", sys.executable, script_path, "--elevated"])
            sys.exit()

# File shredding functions with logging
def zerofill(path, cycles=1, log_callback=None):
    default_passes = 1  # Zerofill: 1 pass per cycle by default
    total_passes = default_passes * cycles
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if log_callback:
                log_callback(f"Starting shredding of {path} with Zerofill ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                with open(path, 'r+b') as f:
                    for i in range(default_passes):
                        f.seek(0)
                        f.write(b'\x00' * file_size)
                        if log_callback:
                            log_callback(f"Pass {i+1}/{default_passes} completed (cycle {cycle+1})")
            return True, f"File {path} shredded with Zerofill ({total_passes} total passes, {cycles} cycles)."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with Zerofill ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        with open(file_path, 'r+b') as f:
                            for i in range(default_passes):
                                f.seek(0)
                                f.write(b'\x00' * file_size)
                                if log_callback:
                                    log_callback(f"Pass {i+1}/{default_passes} completed (cycle {cycle+1})")
            return True, f"Directory {path} shredded with Zerofill ({total_passes} total passes, {cycles} cycles)."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with Zerofill: {e}"

def gutmann(path, cycles=1, log_callback=None):
    default_passes = 35  # Gutmann: 35 passes per cycle by default
    total_passes = default_passes * cycles
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if log_callback:
                log_callback(f"Starting shredding of {path} with Gutmann ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                with open(path, 'r+b') as f:
                    for i in range(min(4, default_passes)):
                        f.seek(0)
                        f.write(os.urandom(file_size))
                        if log_callback:
                            log_callback(f"Random pass {i+1}/{min(4, default_passes)} completed (cycle {cycle+1})")
                    patterns = [b'\x55', b'\xAA', b'\x92\x49\x24']
                    for i in range(min(3, max(0, default_passes-4))):
                        f.seek(0)
                        f.write(patterns[i % len(patterns)] * file_size)
                        if log_callback:
                            log_callback(f"Pattern pass {i+1}/{min(3, max(0, default_passes-4))} completed (cycle {cycle+1})")
                    for i in range(max(0, default_passes-7)):
                        f.seek(0)
                        f.write(os.urandom(file_size))
                        if log_callback:
                            log_callback(f"Additional random pass {i+1}/{max(0, default_passes-7)} completed (cycle {cycle+1})")
            return True, f"File {path} shredded with Gutmann ({total_passes} total passes, {cycles} cycles)."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with Gutmann ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        with open(file_path, 'r+b') as f:
                            for i in range(min(4, default_passes)):
                                f.seek(0)
                                f.write(os.urandom(file_size))
                                if log_callback:
                                    log_callback(f"Random pass {i+1}/{min(4, default_passes)} completed (cycle {cycle+1})")
                            patterns = [b'\x55', b'\xAA', b'\x92\x49\x24']
                            for i in range(min(3, max(0, default_passes-4))):
                                f.seek(0)
                                f.write(patterns[i % len(patterns)] * file_size)
                                if log_callback:
                                    log_callback(f"Pattern pass {i+1}/{min(3, max(0, default_passes-4))} completed (cycle {cycle+1})")
                            for i in range(max(0, default_passes-7)):
                                f.seek(0)
                                f.write(os.urandom(file_size))
                                if log_callback:
                                    log_callback(f"Additional random pass {i+1}/{max(0, default_passes-7)} completed (cycle {cycle+1})")
            return True, f"Directory {path} shredded with Gutmann ({total_passes} total passes, {cycles} cycles)."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with Gutmann: {e}"

def dod_5220(path, cycles=1, log_callback=None):
    default_passes = 3  # DoD: 3 passes per cycle by default
    total_passes = default_passes * cycles
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if log_callback:
                log_callback(f"Starting shredding of {path} with DoD 5220.22-M ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                with open(path, 'r+b') as f:
                    f.seek(0)
                    f.write(b'\x00' * file_size)
                    if log_callback:
                        log_callback(f"Pass 1/3 (zeros) completed (cycle {cycle+1})")
                    f.seek(0)
                    f.write(b'\xFF' * file_size)
                    if log_callback:
                        log_callback(f"Pass 2/3 (ones) completed (cycle {cycle+1})")
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    if log_callback:
                        log_callback(f"Pass 3/3 (random) completed (cycle {cycle+1})")
            return True, f"File {path} shredded with DoD 5220.22-M ({total_passes} total passes, {cycles} cycles)."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with DoD 5220.22-M ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        with open(file_path, 'r+b') as f:
                            f.seek(0)
                            f.write(b'\x00' * file_size)
                            if log_callback:
                                log_callback(f"Pass 1/3 (zeros) completed (cycle {cycle+1})")
                            f.seek(0)
                            f.write(b'\xFF' * file_size)
                            if log_callback:
                                log_callback(f"Pass 2/3 (ones) completed (cycle {cycle+1})")
                            f.seek(0)
                            f.write(os.urandom(file_size))
                            if log_callback:
                                log_callback(f"Pass 3/3 (random) completed (cycle {cycle+1})")
            return True, f"Directory {path} shredded with DoD 5220.22-M ({total_passes} total passes, {cycles} cycles)."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with DoD 5220.22-M: {e}"

def random_data(path, cycles=1, log_callback=None):
    default_passes = 1  # Random Data: 1 pass per cycle by default
    total_passes = default_passes * cycles
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if log_callback:
                log_callback(f"Starting shredding of {path} with Random Data ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                with open(path, 'r+b') as f:
                    for i in range(default_passes):
                        f.seek(0)
                        f.write(os.urandom(file_size))
                        if log_callback:
                            log_callback(f"Pass {i+1}/{default_passes} completed (cycle {cycle+1})")
            return True, f"File {path} shredded with Random Data ({total_passes} total passes, {cycles} cycles)."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with Random Data ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        with open(file_path, 'r+b') as f:
                            for i in range(default_passes):
                                f.seek(0)
                                f.write(os.urandom(file_size))
                                if log_callback:
                                    log_callback(f"Pass {i+1}/{default_passes} completed (cycle {cycle+1})")
            return True, f"Directory {path} shredded with Random Data ({total_passes} total passes, {cycles} cycles)."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with Random Data: {e}"

def ff_00(path, cycles=1, log_callback=None):
    default_passes = 2  # 0xFF 0x00: 2 passes per cycle by default (1 for 0xFF, 1 for 0x00)
    total_passes = default_passes * cycles
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if log_callback:
                log_callback(f"Starting shredding of {path} with 0xFF 0x00 ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                with open(path, 'r+b') as f:
                    f.seek(0)
                    f.write(b'\xFF' * file_size)
                    if log_callback:
                        log_callback(f"Pass 1/2 (ones) completed (cycle {cycle+1})")
                    f.seek(0)
                    f.write(b'\x00' * file_size)
                    if log_callback:
                        log_callback(f"Pass 2/2 (zeros) completed (cycle {cycle+1})")
            return True, f"File {path} shredded with 0xFF 0x00 ({total_passes} total passes, {cycles} cycles)."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with 0xFF 0x00 ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        with open(file_path, 'r+b') as f:
                            f.seek(0)
                            f.write(b'\xFF' * file_size)
                            if log_callback:
                                log_callback(f"Pass 1/2 (ones) completed (cycle {cycle+1})")
                            f.seek(0)
                            f.write(b'\x00' * file_size)
                            if log_callback:
                                log_callback(f"Pass 2/2 (zeros) completed (cycle {cycle+1})")
            return True, f"Directory {path} shredded with 0xFF 0x00 ({total_passes} total passes, {cycles} cycles)."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with 0xFF 0x00: {e}"

def nzsit_402(path, cycles=1, log_callback=None):
    default_passes = 3  # NZSIT 402: 3 passes per cycle by default
    total_passes = default_passes * cycles
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if log_callback:
                log_callback(f"Starting shredding of {path} with NZSIT 402 ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                with open(path, 'r+b') as f:
                    f.seek(0)
                    f.write(b'\x00' * file_size)
                    if log_callback:
                        log_callback(f"Pass 1/3 (zeros) completed (cycle {cycle+1})")
                    f.seek(0)
                    f.write(b'\xFF' * file_size)
                    if log_callback:
                        log_callback(f"Pass 2/3 (ones) completed (cycle {cycle+1})")
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    if log_callback:
                        log_callback(f"Pass 3/3 (random) completed (cycle {cycle+1})")
            return True, f"File {path} shredded with NZSIT 402 ({total_passes} total passes, {cycles} cycles)."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with NZSIT 402 ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        with open(file_path, 'r+b') as f:
                            f.seek(0)
                            f.write(b'\x00' * file_size)
                            if log_callback:
                                log_callback(f"Pass 1/3 (zeros) completed (cycle {cycle+1})")
                            f.seek(0)
                            f.write(b'\xFF' * file_size)
                            if log_callback:
                                log_callback(f"Pass 2/3 (ones) completed (cycle {cycle+1})")
                            f.seek(0)
                            f.write(os.urandom(file_size))
                            if log_callback:
                                log_callback(f"Pass 3/3 (random) completed (cycle {cycle+1})")
            return True, f"Directory {path} shredded with NZSIT 402 ({total_passes} total passes, {cycles} cycles)."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with NZSIT 402: {e}"

def nato_standard(path, cycles=1, log_callback=None):
    default_passes = 7  # NATO Standard: 7 passes per cycle by default
    total_passes = default_passes * cycles
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if log_callback:
                log_callback(f"Starting shredding of {path} with NATO Standard ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                with open(path, 'r+b') as f:
                    for i in range(3):
                        f.seek(0)
                        f.write(b'\x00' * file_size)
                        if log_callback:
                            log_callback(f"Pass {i*2+1}/7 (zeros) completed (cycle {cycle+1})")
                        f.seek(0)
                        f.write(b'\xFF' * file_size)
                        if log_callback:
                            log_callback(f"Pass {i*2+2}/7 (ones) completed (cycle {cycle+1})")
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    if log_callback:
                        log_callback(f"Pass 7/7 (random) completed (cycle {cycle+1})")
            return True, f"File {path} shredded with NATO Standard ({total_passes} total passes, {cycles} cycles)."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with NATO Standard ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        with open(file_path, 'r+b') as f:
                            for i in range(3):
                                f.seek(0)
                                f.write(b'\x00' * file_size)
                                if log_callback:
                                    log_callback(f"Pass {i*2+1}/7 (zeros) completed (cycle {cycle+1})")
                                f.seek(0)
                                f.write(b'\xFF' * file_size)
                                if log_callback:
                                    log_callback(f"Pass {i*2+2}/7 (ones) completed (cycle {cycle+1})")
                            f.seek(0)
                            f.write(os.urandom(file_size))
                            if log_callback:
                                log_callback(f"Pass 7/7 (random) completed (cycle {cycle+1})")
            return True, f"Directory {path} shredded with NATO Standard ({total_passes} total passes, {cycles} cycles)."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with NATO Standard: {e}"

def schneier(path, cycles=1, log_callback=None):
    default_passes = 7  # Bruce Schneier: 7 passes per cycle by default
    total_passes = default_passes * cycles
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if log_callback:
                log_callback(f"Starting shredding of {path} with Bruce Schneier's Algorithm ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                with open(path, 'r+b') as f:
                    f.seek(0)
                    f.write(b'\x00' * file_size)
                    if log_callback:
                        log_callback(f"Pass 1/7 (zeros) completed (cycle {cycle+1})")
                    f.seek(0)
                    f.write(b'\xFF' * file_size)
                    if log_callback:
                        log_callback(f"Pass 2/7 (ones) completed (cycle {cycle+1})")
                    for i in range(5):
                        f.seek(0)
                        f.write(os.urandom(file_size))
                        if log_callback:
                            log_callback(f"Pass {i+3}/7 (random) completed (cycle {cycle+1})")
            return True, f"File {path} shredded with Bruce Schneier's Algorithm ({total_passes} total passes, {cycles} cycles)."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with Bruce Schneier's Algorithm ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        with open(file_path, 'r+b') as f:
                            f.seek(0)
                            f.write(b'\x00' * file_size)
                            if log_callback:
                                log_callback(f"Pass 1/7 (zeros) completed (cycle {cycle+1})")
                            f.seek(0)
                            f.write(b'\xFF' * file_size)
                            if log_callback:
                                log_callback(f"Pass 2/7 (ones) completed (cycle {cycle+1})")
                            for i in range(5):
                                f.seek(0)
                                f.write(os.urandom(file_size))
                                if log_callback:
                                    log_callback(f"Pass {i+3}/7 (random) completed (cycle {cycle+1})")
            return True, f"Directory {path} shredded with Bruce Schneier's Algorithm ({total_passes} total passes, {cycles} cycles)."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with Bruce Schneier's Algorithm: {e}"

def combine_all(path, cycles=1, log_callback=None):
    methods = [
        (zerofill, 1),  # Zerofill: 1 pass per default
        (gutmann, 35),  # Gutmann: 35 passes per default
        (dod_5220, 3),  # DoD: 3 passes per default
        (random_data, 1),  # Random Data: 1 pass per default
        (ff_00, 2),  # 0xFF 0x00: 2 passes per default
        (nzsit_402, 3),  # NZSIT 402: 3 passes per default
        (nato_standard, 7),  # NATO Standard: 7 passes per default
        (schneier, 7)  # Bruce Schneier: 7 passes per default
    ]
    total_passes = sum(default_passes for _, default_passes in methods) * cycles
    try:
        if os.path.isfile(path):
            if log_callback:
                log_callback(f"Starting shredding of {path} with Combine All ({total_passes} total passes, {cycles} cycles)")
            for cycle in range(cycles):
                if log_callback:
                    log_callback(f"Cycle {cycle+1}/{cycles}")
                for method, default_passes in methods:
                    success, message = method(path, 1, log_callback)  # 1 cycle at a time, repeated by the outer loop
                    if not success:
                        return False, message
            os.remove(path)  # Deletion after all methods
            if log_callback:
                log_callback(f"File {path} deleted")
            return True, f"File {path} shredded with all methods ({total_passes} total passes, {cycles} cycles) and deleted."
        elif os.path.isdir(path):
            if log_callback:
                log_callback(f"Starting shredding of directory {path} with Combine All ({total_passes} total passes, {cycles} cycles)")
            for root, _, files in os.walk(path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    if log_callback:
                        log_callback(f"Shredding {file_path}")
                    for cycle in range(cycles):
                        if log_callback:
                            log_callback(f"Cycle {cycle+1}/{cycles}")
                        for method, default_passes in methods:
                            success, message = method(file_path, 1, log_callback)
                            if not success:
                                return False, message
                    os.remove(file_path)  # Deletion after all methods for this file
                    if log_callback:
                        log_callback(f"File {file_path} deleted")
                os.rmdir(root)  # Deletion of directories after processing files
                if log_callback:
                    log_callback(f"Directory {root} deleted")
            return True, f"Directory {path} shredded with all methods ({total_passes} total passes, {cycles} cycles) and deleted."
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {e}")
        return False, f"Error during shredding with all methods: {e}"

# Check if the context menu option exists (Windows only)
def check_context_menu():
    if platform.system() != "Windows":
        return False
    try:
        import winreg as reg
        key = reg.OpenKey(reg.HKEY_CLASSES_ROOT, r"*\shell", 0, reg.KEY_READ)
        reg.OpenKey(key, "Shred with OpenShredder")
        reg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error checking context menu: {e}")
        return False

# Add the option to the context menu (Windows only)
def add_to_context_menu(log_callback=None):
    if platform.system() != "Windows":
        if log_callback:
            log_callback("Context menu integration is only supported on Windows.")
        return False, "Context menu integration is only supported on Windows."
    try:
        import winreg as reg
        script_path = os.path.abspath(__file__)
        python_path = sys.executable
        command = f'"{python_path}" "{script_path}" "%1"'
        icon_path = r"C:\OpenShredder\shredder.ico"  # Replace with the actual path to your icon
        
        key = reg.OpenKey(reg.HKEY_CLASSES_ROOT, r"*\shell", 0, reg.KEY_SET_VALUE)
        subkey = reg.CreateKey(key, "Shred with OpenShredder")
        reg.SetValue(subkey, "", reg.REG_SZ, "Shred with OpenShredder")
        reg.SetValueEx(subkey, "Icon", 0, reg.REG_SZ, icon_path)
        reg.CreateKey(subkey, "command")
        reg.SetValue(subkey, "command", reg.REG_SZ, command)
        reg.CloseKey(subkey)
        reg.CloseKey(key)
        if log_callback:
            log_callback("Option 'Shred with OpenShredder' added to context menu with icon.")
        return True, "Option added to context menu successfully."
    except Exception as e:
        if log_callback:
            log_callback(f"Error adding to context menu: {e}")
        return False, f"Error adding to context menu: {e}"

# Remove the option from the context menu (Windows only)
def remove_from_context_menu(log_callback=None):
    if platform.system() != "Windows":
        if log_callback:
            log_callback("Context menu integration is only supported on Windows.")
        return False, "Context menu integration is only supported on Windows."
    try:
        import winreg as reg
        key = reg.OpenKey(reg.HKEY_CLASSES_ROOT, r"*\shell", 0, reg.KEY_SET_VALUE)
        reg.DeleteKey(key, r"Shred with OpenShredder\command")
        reg.DeleteKey(key, "Shred with OpenShredder")
        reg.CloseKey(key)
        if log_callback:
            log_callback("Option 'Shred with OpenShredder' removed from context menu.")
        return True, "Option removed from context menu successfully."
    except FileNotFoundError:
        if log_callback:
            log_callback("Option 'Shred with OpenShredder' does not exist in the context menu.")
        return True, "Option did not exist in the context menu."
    except Exception as e:
        if log_callback:
            log_callback(f"Error removing from context menu: {e}")
        return False, f"Error removing from context menu: {e}"

# GUI with classic theme
def create_gui(file_path=None):
    def log(message):
        debug_console.configure(state='normal')
        debug_console.insert(tk.END, message + "\n")
        debug_console.see(tk.END)
        debug_console.configure(state='disabled')

    def select_path():
        path = filedialog.askopenfilename() if file_var.get() == "File" else filedialog.askdirectory()
        if path:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, path)

    def shred():
        path = path_entry.get()
        method = method_var.get()
        cycles = cycles_var.get()
        if not path:
            messagebox.showerror("Error", "Please select a file or directory.")
            return
        if not os.path.exists(path):
            messagebox.showerror("Error", "The specified path does not exist.")
            return
        
        log(f"Starting operation on {path}")
        if method == "zerofill":
            success, message = zerofill(path, cycles, log)
            if success:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"File {path} deleted")
                    message += " and deleted."
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            log(f"File {file_path} deleted")
                        os.rmdir(root)
                        log(f"Directory {root} deleted")
                    message += " and deleted."
        elif method == "gutmann":
            success, message = gutmann(path, cycles, log)
            if success:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"File {path} deleted")
                    message += " and deleted."
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            log(f"File {file_path} deleted")
                        os.rmdir(root)
                        log(f"Directory {root} deleted")
                    message += " and deleted."
        elif method == "dod":
            success, message = dod_5220(path, cycles, log)
            if success:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"File {path} deleted")
                    message += " and deleted."
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            log(f"File {file_path} deleted")
                        os.rmdir(root)
                        log(f"Directory {root} deleted")
                    message += " and deleted."
        elif method == "random":
            success, message = random_data(path, cycles, log)
            if success:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"File {path} deleted")
                    message += " and deleted."
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            log(f"File {file_path} deleted")
                        os.rmdir(root)
                        log(f"Directory {root} deleted")
                    message += " and deleted."
        elif method == "ff_00":
            success, message = ff_00(path, cycles, log)
            if success:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"File {path} deleted")
                    message += " and deleted."
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            log(f"File {file_path} deleted")
                        os.rmdir(root)
                        log(f"Directory {root} deleted")
                    message += " and deleted."
        elif method == "nzsit":
            success, message = nzsit_402(path, cycles, log)
            if success:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"File {path} deleted")
                    message += " and deleted."
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            log(f"File {file_path} deleted")
                        os.rmdir(root)
                        log(f"Directory {root} deleted")
                    message += " and deleted."
        elif method == "nato":
            success, message = nato_standard(path, cycles, log)
            if success:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"File {path} deleted")
                    message += " and deleted."
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            log(f"File {file_path} deleted")
                        os.rmdir(root)
                        log(f"Directory {root} deleted")
                    message += " and deleted."
        elif method == "schneier":
            success, message = schneier(path, cycles, log)
            if success:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"File {path} deleted")
                    message += " and deleted."
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            log(f"File {file_path} deleted")
                        os.rmdir(root)
                        log(f"Directory {root} deleted")
                    message += " and deleted."
        elif method == "combine":
            success, message = combine_all(path, cycles, log)
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def toggle_context_menu():
        if not is_admin():
            log("Requesting elevated privileges to modify context menu...")
            run_as_admin()
        else:
            if check_context_menu():
                success, message = remove_from_context_menu(log)
                if success:
                    toggle_button.config(text="Add to Context Menu")
            else:
                success, message = add_to_context_menu(log)
                if success:
                    toggle_button.config(text="Remove from Context Menu")

    def show_about():
        about_window = tk.Toplevel(root)
        about_window.title("About OpenShredder")
        about_window.geometry("300x150")
        about_window.resizable(False, False)

        ttk.Label(about_window, text="OpenShredder", font=("Helvetica", 12, "bold")).pack(pady=5)
        ttk.Label(about_window, text="Version 0.1").pack()

        # Clickable label for "Made with <3 by TrackingIsEvil"
        made_by_label = ttk.Label(about_window, text="Made with <3 by TrackingIsEvil", foreground="blue", cursor="hand2")
        made_by_label.pack(pady=5)
        made_by_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/TrackingIsEvil"))

        ttk.Label(about_window, text="If you like our program, please consider to donate even a small amount <3", wraplength=250).pack(pady=5)

    root = tk.Tk()
    root.title("OpenShredder")
    root.geometry("500x900")
    root.resizable(False, False)

    # Use default Tkinter theme (classic)
    style = ttk.Style()

    # Title
    ttk.Label(root, text="OpenShredder", font=("Helvetica", 14, "bold")).pack(pady=10)
    
    # Target type
    ttk.Label(root, text="Target Type:").pack(pady=5)
    file_var = tk.StringVar(value="File")
    ttk.Radiobutton(root, text="File", variable=file_var, value="File").pack()
    ttk.Radiobutton(root, text="Directory", variable=file_var, value="Directory").pack()

    # Path
    ttk.Label(root, text="Path:").pack(pady=5)
    path_entry = ttk.Entry(root, width=50)
    path_entry.pack()
    if file_path:
        path_entry.insert(0, file_path)
    ttk.Button(root, text="Browse", command=select_path).pack(pady=5)

    # Shredding method
    ttk.Label(root, text="Shredding Method:").pack(pady=5)
    method_var = tk.StringVar(value="zerofill")

    zerofill_frame = ttk.Frame(root)
    zerofill_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(zerofill_frame, text="", variable=method_var, value="zerofill").pack(side="left")
    ttk.Label(zerofill_frame, text="Zerofill (1 pass per cycle)").pack(side="left")

    gutmann_frame = ttk.Frame(root)
    gutmann_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(gutmann_frame, text="", variable=method_var, value="gutmann").pack(side="left")
    ttk.Label(gutmann_frame, text="Gutmann (35 passes per cycle)").pack(side="left")

    dod_frame = ttk.Frame(root)
    dod_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(dod_frame, text="", variable=method_var, value="dod").pack(side="left")
    ttk.Label(dod_frame, text="DoD 5220.22-M (3 passes per cycle)").pack(side="left")

    random_frame = ttk.Frame(root)
    random_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(random_frame, text="", variable=method_var, value="random").pack(side="left")
    ttk.Label(random_frame, text="Random Data (1 pass per cycle)").pack(side="left")

    ff_00_frame = ttk.Frame(root)
    ff_00_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(ff_00_frame, text="", variable=method_var, value="ff_00").pack(side="left")
    ttk.Label(ff_00_frame, text="0xFF 0x00 (2 passes per cycle)").pack(side="left")

    nzsit_frame = ttk.Frame(root)
    nzsit_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(nzsit_frame, text="", variable=method_var, value="nzsit").pack(side="left")
    ttk.Label(nzsit_frame, text="NZSIT 402 (3 passes per cycle)").pack(side="left")

    nato_frame = ttk.Frame(root)
    nato_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(nato_frame, text="", variable=method_var, value="nato").pack(side="left")
    ttk.Label(nato_frame, text="NATO Standard (7 passes per cycle)").pack(side="left")

    schneier_frame = ttk.Frame(root)
    schneier_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(schneier_frame, text="", variable=method_var, value="schneier").pack(side="left")
    ttk.Label(schneier_frame, text="Bruce Schneier's Algorithm (7 passes per cycle)").pack(side="left")

    combine_frame = ttk.Frame(root)
    combine_frame.pack(fill="x", padx=20)
    ttk.Radiobutton(combine_frame, text="", variable=method_var, value="combine").pack(side="left")
    ttk.Label(combine_frame, text="Combine All (59 passes per cycle, Maximum Security)").pack(side="left")

    # Number of cycles
    ttk.Label(root, text="Number of Cycles:").pack(pady=5)
    cycles_var = tk.IntVar(value=1)
    for c in [1, 3, 7, 33]:
        ttk.Radiobutton(root, text=str(c), variable=cycles_var, value=c).pack()

    # Shred button (classic style)
    shred_button = ttk.Button(root, text="Shred and Delete", command=shred)
    shred_button.pack(pady=10)

    # Context menu toggle button (classic style)
    toggle_button_text = "Remove from Context Menu" if check_context_menu() else "Add to Context Menu"
    toggle_button = ttk.Button(root, text=toggle_button_text, command=toggle_context_menu)
    toggle_button.pack(pady=5)

    # About button (classic style)
    about_button = ttk.Button(root, text="About", command=show_about)
    about_button.pack(pady=5)

    # Debug console
    ttk.Label(root, text="Debug Console:").pack(pady=5)
    debug_console = scrolledtext.ScrolledText(root, width=60, height=10, state='disabled')
    debug_console.pack(pady=5)

    if check_context_menu():
        log("Option 'Shred with OpenShredder' is already present in the context menu.")
    else:
        log("Option 'Shred with OpenShredder' is not in the context menu.")

    root.mainloop()

if __name__ == "__main__":
    if "--elevated" in sys.argv:
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        create_gui(file_path)
    else:
        file_path = sys.argv[1] if len(sys.argv) > 1 else None
        create_gui(file_path)