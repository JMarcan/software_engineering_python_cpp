# include <iostream>
# include <string>

using namespace std;

#ifndef OPTIMIZED_CODE_H
#define OPTIMIZED_CODE_H

#define LIBRARY_API __declspec( dllexport )

extern "C" {
    LIBRARY_API int sparse_vector_dot(int **vector_a, int vector_a_size, int **vector_b, int vector_b_size);
    LIBRARY_API int calculate_sqrt(int value);
    LIBRARY_API float calculate_add(float a, float b);
    LIBRARY_API string get_message(void);
}

#endif /* MY_CLASS_H */