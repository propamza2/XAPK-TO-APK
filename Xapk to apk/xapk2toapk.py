import zipfile
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def extract_xapk(xapk_path, log_widget):
    if not zipfile.is_zipfile(xapk_path):
        log_widget.insert(tk.END, f"❌ Not a valid XAPK: {xapk_path}\n")
        return

    base_dir = os.path.dirname(xapk_path)
    out_dir = os.path.join(base_dir, os.path.splitext(os.path.basename(xapk_path))[0])
    os.makedirs(out_dir, exist_ok=True)

    with zipfile.ZipFile(xapk_path, 'r') as z:
        # APK dosyaları
        apk_files = [f for f in z.namelist() if f.endswith(".apk")]
        if not apk_files:
            log_widget.insert(tk.END, f"❌ No APK found in {xapk_path}\n")
            return

        for apk_file in apk_files:
            apk_name = os.path.basename(apk_file)
            output_path = os.path.join(out_dir, apk_name)
            with z.open(apk_file) as source, open(output_path, "wb") as target:
                target.write(source.read())
            log_widget.insert(tk.END, f"✅ Extracted APK: {output_path}\n")

        # OBB dosyaları
        obb_files = [f for f in z.namelist() if f.startswith("Android/obb/")]
        if obb_files:
            log_widget.insert(tk.END, "📂 Extracting OBB files...\n")
            for f in obb_files:
                z.extract(f, out_dir)
            log_widget.insert(tk.END, f"✅ OBB extracted to: {os.path.join(out_dir, 'Android/obb')}\n")
        else:
            log_widget.insert(tk.END, "ℹ️ No OBB found.\n")

    log_widget.insert(tk.END, "🎉 Done!\n\n")
    log_widget.see(tk.END)

def select_file(log_widget):
    filetypes = [("XAPK Files", "*.xapk"), ("All files", "*.*")]
    paths = filedialog.askopenfilenames(title="Select XAPK file(s)", filetypes=filetypes)
    for path in paths:
        extract_xapk(path, log_widget)

def on_drop(event, log_widget):
    paths = event.data.strip().split()
    for path in paths:
        extract_xapk(path.strip("{}"), log_widget)

def main():
    root = tk.Tk()
    root.title("XAPK → APK Extractor")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    lbl = tk.Label(frame, text="Drag & Drop .xapk files here\nor click 'Select File'")
    lbl.pack(pady=5)

    log_widget = scrolledtext.ScrolledText(frame, width=60, height=15)
    log_widget.pack(pady=5, fill=tk.BOTH, expand=True)

    btn = tk.Button(frame, text="📂 Select File", command=lambda: select_file(log_widget))
    btn.pack(pady=5)

    # Sürükle-bırak desteği için "tkdnd" gerekiyor
    try:
        import tkinterdnd2 as tkdnd
        root = tkdnd.TkinterDnD.Tk()
        lbl.drop_target_register(tkdnd.DND_FILES)
        lbl.dnd_bind("<<Drop>>", lambda e: on_drop(e, log_widget))
    except ImportError:
        log_widget.insert(tk.END, "⚠️ Drag & Drop requires 'tkinterdnd2'. Install it:\n pip install tkinterdnd2\n\n")

    root.mainloop()

if __name__ == "__main__":
    main()
