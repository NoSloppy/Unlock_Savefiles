#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class ProffieSafe:
    def __init__(self, filename):
        self.valid = False
        try:
            self.f = open(filename, "rb")
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"{filename} not found")
            return

        if self.read_uint32() != 0xFF1E5AFE:
            messagebox.showerror("Error", f"{filename}: wrong magic number")
            return

        checksum = self.read_uint32()
        iteration = self.read_uint32()
        length = self.read_uint32()

        if self.read_uint32() != 0xFF1E5AFE:
            messagebox.showerror("Error", f"{filename}: wrong magic number in second header")
            return

        if self.read_uint32() != checksum:
            messagebox.showerror("Error", f"{filename}: second header doesn't match (checksum)")
            return
        if self.read_uint32() != iteration:
            messagebox.showerror("Error", f"{filename}: second header doesn't match (iteration)")
            return
        if self.read_uint32() != length:
            messagebox.showerror("Error", f"{filename}: second header doesn't match (length)")
            return

        self.f.seek(512)
        c = 0
        for x in range(0, length):
            c = (c * 997 + self.read_uint8()) & 0xFFFFFFFF
        if c != checksum:
            messagebox.showerror("Error", f"{filename}: Checksum doesn't match content. {c} != {checksum}")
            return

        self.valid = True
        self.checksum = checksum
        self.iteration = iteration
        self.length = length


    def read_uint8(self):
        return ord(self.f.read(1))

    def read_uint16(self):
        a = self.read_uint8()
        b = self.read_uint8()
        return a + (b << 8)

    def read_uint32(self):
        a = self.read_uint16()
        b = self.read_uint16()
        return a + (b << 16)

    def read(self):
        self.f.seek(512)
        return self.f.read(self.length)

    def close(self):
        self.f.close()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    ini_full_path = filedialog.askopenfilename(
        title="Select INI File",
        filetypes=[("INI Files", "*.ini")]
    )

    if not ini_full_path:
        messagebox.showinfo("No File", "No file provided.")
        return

    file_dir = os.path.dirname(ini_full_path)
    ini_filename = os.path.basename(ini_full_path)
    tmp_filename = os.path.splitext(ini_filename)[0] + '.tmp'

    tmp_full_path = os.path.join(file_dir, tmp_filename)

    ini = ProffieSafe(ini_full_path)
    tmp = ProffieSafe(tmp_full_path)
    best = ini
    if tmp.valid:
        if not ini.valid or tmp.iteration > ini.iteration:
            best = tmp

    data = best.read()
    ini.close()
    tmp.close()

    bak_filename = ini_filename + ".bak"
    old_filename = tmp_filename + ".old"

    bak_full_path = os.path.join(file_dir, bak_filename)
    old_full_path = os.path.join(file_dir, old_filename)

    # Rename original .ini and .tmp files
    os.rename(ini_full_path, bak_full_path)
    if os.path.exists(tmp_full_path):
        os.rename(tmp_full_path, old_full_path)

    # Write best data back to .ini file
    open(ini_full_path, "wb").write(data)

if __name__ == "__main__":
    main()
