#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * @brief 
 *
 * @param shape_id
 * @param output_filepath
 * @return 
 */
int generate_shape(int shape_id, const char* output_filepath) {
    FILE *file = fopen(output_filepath, "w");
    if (file == NULL) {
        fprintf(stderr, "[C Kernel ERROR] Could not open file: %s\n", output_filepath);
        return -1;
    }

    fprintf(stdout, "[C Kernel] Generating geometry for shape ID %d into %s...\n", shape_id, output_filepath);

    if (shape_id == 1) { // Cube
        // Cube vertices
        fprintf(file, "v -1.0 -1.0 -1.0\n"); // 1
        fprintf(file, "v -1.0 -1.0 1.0\n");  // 2
        fprintf(file, "v -1.0 1.0 1.0\n");   // 3
        fprintf(file, "v -1.0 1.0 -1.0\n");  // 4
        fprintf(file, "v 1.0 -1.0 -1.0\n");  // 5
        fprintf(file, "v 1.0 -1.0 1.0\n");   // 6
        fprintf(file, "v 1.0 1.0 1.0\n");    // 7
        fprintf(file, "v 1.0 1.0 -1.0\n");   // 8

        // Cube faces (counter-clockwise winding)
        // Back
        fprintf(file, "f 5 8 4 1\n");
        // Front
        fprintf(file, "f 2 3 7 6\n");
        // Left
        fprintf(file, "f 1 4 3 2\n");
        // Right
        fprintf(file, "f 6 7 8 5\n");
        // Top
        fprintf(file, "f 4 8 7 3\n");
        // Bottom
        fprintf(file, "f 5 1 2 6\n");

        fprintf(stdout, "[C Kernel] Cube OBJ data written successfully.\n");

    } else if (shape_id == 2) {
        
        float r = 1.5;
        fprintf(file, "v %f %f %f\n", 0.0, r, 0.0);       // Top (1)
        fprintf(file, "v %f %f %f\n", -r, -r, -r);       // Bottom-left-back (2)
        fprintf(file, "v %f %f %f\n", r, -r, -r);        // Bottom-right-back (3)
        fprintf(file, "v %f %f %f\n", 0.0, -r, 2 * r);   // Bottom-front (4)

        // Faces
        fprintf(file, "f 1 2 3\n"); // Back
        fprintf(file, "f 1 3 4\n"); // Right-front
        fprintf(file, "f 1 4 2\n"); // Left-front
        fprintf(file, "f 2 4 3\n"); // Bottom

        fprintf(stdout, "[C Kernel] Tetrahedron (Sphere simulation) OBJ data written successfully.\n");

    } else {
        fprintf(stderr, "[C Kernel ERROR] Invalid shape ID: %d\n", shape_id);
        fclose(file);
        return -1;
    }

    fclose(file);
    return 0;
}
