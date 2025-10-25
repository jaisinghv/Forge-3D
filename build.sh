
C_SOURCE="geometry_kernel.c"
SHARED_LIB="libgeometry.so"

# Check if the source file exists
if [ ! -f "$C_SOURCE" ]; then
    echo "Error: C source file ($C_SOURCE) not found in the current directory."
    exit 1
fi

echo "--- Compiling C Geometry Kernel for macOS ---"


gcc -shared -fPIC -arch arm64 -o "$SHARED_LIB" "$C_SOURCE"

if [ $? -eq 0 ]; then
    echo "✅ SUCCESS! Compiled shared library created: $SHARED_LIB"
    echo "You can now proceed to package the application with PyInstaller."
else
    echo "❌ ERROR: C compilation failed. Ensure 'gcc' is installed (via Xcode Command Line Tools)."
fi
