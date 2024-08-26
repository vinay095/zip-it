import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
from cryptography.fernet import Fernet
import os

class CompressionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Compression Tool")

        # Load or generate a key
        self.key = self.load_key()
        self.cipher = Fernet(self.key)

        self.compress_button = tk.Button(root, text="Compress and Encrypt File", command=self.compress_file)
        self.compress_button.pack(pady=10)

        self.decompress_button = tk.Button(root, text="Decrypt and Decompress File", command=self.decompress_file)
        self.decompress_button.pack(pady=10)

    def load_key(self):
        key_file = 'secret.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key

    def compress_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to compress")
        if not file_path:
            return

        zip_file_path = file_path + '.zip'
        encrypted_zip_file_path = zip_file_path + '.enc'

        try:
            # Create a ZIP file
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(file_path, os.path.basename(file_path))

            # Encrypt the ZIP file
            with open(zip_file_path, 'rb') as f:
                zip_data = f.read()
            encrypted_data = self.cipher.encrypt(zip_data)

            with open(encrypted_zip_file_path, 'wb') as f:
                f.write(encrypted_data)

            os.remove(zip_file_path)  # Remove the unencrypted ZIP file

            messagebox.showinfo("Success", f"File compressed and encrypted successfully!\nSaved as: {encrypted_zip_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def decompress_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to decrypt and decompress", filetypes=[("Encrypted ZIP files", "*.zip.enc")])
        if not file_path:
            return

        decrypted_zip_file_path = file_path.replace('.enc', '')
        decompressed_file_path = decrypted_zip_file_path.replace('.zip', '')

        try:
            # Decrypt the encrypted ZIP file
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            zip_data = self.cipher.decrypt(encrypted_data)

            with open(decrypted_zip_file_path, 'wb') as f:
                f.write(zip_data)

            # Extract the ZIP file
            with zipfile.ZipFile(decrypted_zip_file_path, 'r') as zipf:
                zipf.extractall(os.path.dirname(decompressed_file_path))

            os.remove(decrypted_zip_file_path)  # Remove the decrypted ZIP file

            messagebox.showinfo("Success", f"File decrypted and decompressed successfully!\nSaved as: {decompressed_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompressionTool(root)
    root.mainloop()
