/*
 Example C++ dll library 
 which functions we call from Python with its ctypes library
*/

# include <iostream>
# include <string>
# include "optimized_code.h"

using namespace std;

/* Library API
    The Section with exposed functions
    Specifying C interface with extern "C" 
    is necessary as Python library ctypes
    supports calling external C functions, 
    instead of directly C++
*/
extern "C"
{
    LIBRARY_API int sparse_vector_dot(const uint64_t **vector_a, const uint64_t vector_a_size, const uint64_t **vector_b, const uint64_t vector_b_size) {
        long dot_product = 0;

        int idx_a = 0;
        int idx_b = 0;

        while (idx_a < vector_a_size && idx_b < vector_b_size){
            int index_a = vector_a[0][0];
            int index_b = vector_b[0][0];
            if (index_a == index_b) {
                int value_a = vector_a[0][1];
                int value_b = vector_b[0][1];
                dot_product += value_a * value_b;
                idx_a += 1;
                idx_b += 1;
            }
            else if (index_a < index_b) {
                index_a += 1;
            }
            else {
                index_b += 1;
            }
        }
        return dot_product;
    }
    // Example code to demonstrate ctypes mapping to variety of datatypes
    LIBRARY_API int calculate_sqrt(int value) {
        return value * value;
    }

    LIBRARY_API float calculate_add(float a, float b) {
        return a + b;
    }

    /*
     fix implementation, so it's C compatible
    LIBRARY_API string get_message(void) {
        string msg = "Message from C++ function";
        return msg;
    }
    */
}