import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import sys
import datetime
import subprocess

# --- 1. FFI Wrapper Logic ---

SHARED_LIB_NAME = 'libgeometry.so'
LIB_GEOMETRY = None

def find_library_path(lib_name):

    # 1. Check current directory (Development)
    if os.path.exists(lib_name):
        return os.path.abspath(lib_name)

    # 2. Check PyInstaller temp path (Packaged App)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_path = os.path.join(sys._MEIPASS, lib_name)
        if os.path.exists(bundle_path):
            return bundle_path

    return None

def load_c_kernel():
    """Loads the pre-compiled C shared library."""
    global LIB_GEOMETRY
    lib_path = find_library_path(SHARED_LIB_NAME)

    if not lib_path:
        return f"[ERROR] Shared library '{SHARED_LIB_NAME}' not found. Please compile it first or ensure it is bundled correctly."

    try:
        # Load the compiled library
        LIB_GEOMETRY = ctypes.CDLL(lib_path)
        
        # Define the C function's prototype for ctypes
        LIB_GEOMETRY.generate_shape.argtypes = [
            ctypes.c_int,  # shape_id
            ctypes.c_char_p # (const char*)
        ]
        LIB_GEOMETRY.generate_shape.restype = ctypes.c_int # (0 for success)
        
        return f"[SUCCESS] C kernel loaded from: {lib_path}"
    except Exception as e:
        LIB_GEOMETRY = None
        return f"[FATAL] Failed to load C library: {e}"

def generate_3d_model(shape_id: int, output_file: str) -> bool:
    """Invokes the C kernel to generate the geometry."""
    if not LIB_GEOMETRY:
        return False
        
    print(f"[FFI Wrapper] Invoking C kernel to generate: {output_file}")
    
    try:
        result = LIB_GEOMETRY.generate_shape(
            shape_id, 
            output_file.encode('utf-8') # Python string to C char* (bytes)
        )
        return result == 0
    except Exception as e:
        print(f"[FFI Error] Call to C function failed: {e}")
        return False

# --- 2. ML Inference Simulator ---

def ml_inference_simulator(prompt: str) -> int:

    prompt = prompt.lower()
    
    if "cube" in prompt or "box" in prompt or "square" in prompt:
        return 1
    elif "sphere" in prompt or "ball" in prompt or "round" in prompt:
        return 2
    else:
        return 0

# --- 3. GUI (Tkinter) ---

class TextTo3DApp:
    def __init__(self, master):
        self.master = master
        master.title("Text-to-3D Model Generator")
        
        # Load the C kernel and update status immediately
        self.kernel_status = load_c_kernel()

        self.setup_ui()
        self.update_status(self.kernel_status, "blue")

    def setup_ui(self):
        self.master.configure(bg='#f0f4f8')
        
        # Configure grid for responsiveness
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Main frame
        main_frame = tk.Frame(self.master, padx=30, pady=30, bg='#f0f4f8')
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Title Label
        title_label = tk.Label(main_frame, text="Generate Solid Object", font=("Inter", 20, "bold"), bg='#f0f4f8', fg='#333333')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Prompt Label
        prompt_label = tk.Label(main_frame, text="Enter Text Prompt (e.g., 'A round ball', 'A wooden box'):", font=("Inter", 12), bg='#f0f4f8', fg='#555555')
        prompt_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 5))

        # Prompt Entry
        self.prompt_entry = tk.Entry(main_frame, width=50, font=("Inter", 14), bd=2, relief=tk.FLAT)
        self.prompt_entry.grid(row=2, column=0, columnspan=2, sticky="ew", ipady=8)
        self.prompt_entry.insert(0, "A standard cube")
        
        # Generate Button
        self.generate_button = tk.Button(main_frame, text="Generate OBJ Model", command=self.run_pipeline, 
                                         font=("Inter", 14, "bold"), bg='#4CAF50', fg='white', 
                                         activebackground='#45A049', activeforeground='white',
                                         bd=0, relief=tk.RAISED, cursor="hand2")
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=(25, 10), sticky="ew", ipady=10)
        self.generate_button.bind("<Enter>", lambda e: self.generate_button.config(bg='#45A049'))
        self.generate_button.bind("<Leave>", lambda e: self.generate_button.config(bg='#4CAF50'))

        # Status Label
        status_frame = tk.Frame(main_frame, bg='white', padx=10, pady=10, bd=1, relief=tk.SUNKEN)
        status_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(20, 0))

        self.status_label = tk.Label(status_frame, text="Ready.", font=("Inter", 10), bg='white', justify=tk.LEFT, anchor='w')
        self.status_label.pack(fill='x', expand=True)

    def update_status(self, message, color='black'):
        """Updates the status bar message."""
        self.status_label.config(text=message, fg=color)
        self.master.update()

    def run_pipeline(self):
        """Main pipeline execution when the button is clicked."""
        prompt = self.prompt_entry.get().strip()

        if not prompt:
            self.update_status("Please enter a text prompt.", "orange")
            return

        if not LIB_GEOMETRY:
            self.update_status(self.kernel_status, "red")
            messagebox.showerror("Kernel Error", self.kernel_status)
            return

        self.update_status(f"Analyzing prompt: '{prompt}'...", "gray")
        
        # 1. Simulate ML Inference
        shape_id = ml_inference_simulator(prompt)

        if shape_id == 0:
            self.update_status("Could not determine shape. Try 'cube' or 'sphere'.", "orange")
            return

        # 2. Define Output
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shape_name = "cube" if shape_id == 1 else "sphere_sim"
        output_filename = f"{shape_name}_model_{timestamp}.obj"

        desktop_path = os.path.expanduser("~/Desktop") 
        output_path = os.path.join(desktop_path, output_filename)
        
        self.update_status(f"Generating model... Target: {output_filename}", "blue")

        # 3. High-Performance Geometry Generation (C via FFI)
        success = generate_3d_model(shape_id, output_path)
        
        # 4. Final Report
        if success:
            self.update_status(f"✅ SUCCESS! File saved to: {output_path}", "green")
            messagebox.showinfo("Success", f"3D Model generated!\nFile saved to:\n{output_path}\n\nUse a 3D viewer (like Blender or MeshLab) to inspect the .obj file.")
        else:
            self.update_status("❌ FAILED to generate 3D model. Check console for C errors.", "red")
            messagebox.showerror("Failure", "Failed to generate 3D model. Check your system console for specific C library errors.")

# --- Main Execution ---

if __name__ == '__main__':
    root = tk.Tk()
    app = TextTo3DApp(root)
    root.mainloop()
