import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import filedialog

def try_password(zip_file, password):
    try:
        with zip_file.open(zip_file.infolist()[0], 'r', pwd=password.encode('utf-8')) as file:
            file.read()
        return True
    except RuntimeError:
        return False

def brute_force(zip_path, user_combos, num_threads=4):
    with zipfile.ZipFile(zip_path) as zip_file:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(try_password, zip_file, password): password for password in user_combos}

            for future in as_completed(futures):
                password = futures[future]
                success = future.result()
                if success:
                    print(f"Password found: {password}")
                    return

    print("No password found in the provided combinations.")

def main():
    root = tk.Tk()
    root.withdraw()

    zip_path = filedialog.askopenfilename(title="Select the ZIP file", filetypes=[("ZIP files", "*.zip")])
    combos = input("Enter password combinations separated by commas: ").strip().split(',')
    num_threads = int(input("Enter the number of threads to use: ").strip())

    brute_force(zip_path, combos, num_threads)

if __name__ == "__main__":
    main()
