'''
 Example integration code of C++ functions with Python,
 using standard ctypes library.

 
 sparse_vector_dot_cpp
 '''

import ctypes
import time

class ProcessingPipeline():
    ''' Example processing pipeline 
        to demonstrate ctypes usage
    '''
    def __init__(self):
        self.cpp_lib = ctypes.CDLL('optimized_code.dll')

    def execute_pipeline_python_only(self):
        '''Executes the  pipeline 
            without utilizing optimized C++ sections.

            The pipeline only job here is to calculate dot product of two sparse vectors.
        '''

        # Initizalize two sparse vectors 
        vector_a, vector_b = self.get_sparse_vectors()
        # Calculate dot product of these two sparse vectors
        result = self.sparse_vector_dot(vector_a, vector_b)
        return result

    def execute_pipeline(self):
        '''Executes the pipeline 
            utilizing optimized C++ sections

            The pipeline only job here is to calculate dot product of two sparse vectors.
        '''
        # Initizalize two sparse vectors  
        vector_a, vector_b = self.get_sparse_vectors()
        # Calculate dot product of these two sparse vectors
        result = self.sparse_vector_dot_cpp(vector_a, vector_b)

        return result

    def get_sparse_vectors(self):
        '''Initizalize two sparse vectors 
            Representation format: 
                Choosen to support extremelly large vectors
                where most of the values are zeroes

                [[index_1, value_1], ... [index_n, value_n]]
                The first value is position index, 
                The second value is its value  
                E.g. [[1, 5], ... [3, 7]]
        '''
        vector_a = [(x*2, x) for x in range(10)]
        vector_b = [(x*3, x*3) for x in range(10)]
        
        return (vector_a, vector_b)

    def benchmark(self):
        '''Compares the performance of C++ implementation 
            with Python implementation
        '''
        n = 1000 # set execution count

        vector_a, vector_b = self.get_sparse_vectors()
        
        # Measure Python implementation
        start = time.perf_counter()
        for i in range(n):
            self.sparse_vector_dot(vector_a, vector_b)
        print(f"Execution time of Python implementation \
            {time.perf_counter()-start} seconds")

        # Measure C++ implementation called from Python
        start = time.perf_counter()
        for i in range(n):
            self.sparse_vector_dot_cpp(vector_a, vector_b)
        print(f"Execution time of C++ implementation \
            {time.perf_counter()-start} seconds)")

    def sparse_vector_dot(self, vector_a: [()], vector_b: [()]):
        '''
         Time Complexity: O(n + m)
            where m if size on vector_a and n is size of vector_b
         Space Complexity:

         The algorithms and vector representation is chosen 
        '''
        dot_product = 0
        idx_a = 0
        idx_b = 0

        while idx_a < len(vector_a) and idx_b < len(vector_b):
            if vector_a[idx_a][0] == vector_b[idx_b][0]:
                dot_product += vector_a[idx_b][1] * vector_b[idx_b][1]
                idx_a += 1
                idx_b += 1
            elif vector_a[idx_a] > vector_b[idx_b]:
                idx_b += 1
            else:
                idx_a += 1

        return dot_product

    def sparse_vector_dot_cpp(self, vector_a: [()], vector_b: [()]):
        pass
        '''
        dot_cpp = self.cpp_lib.sparse_vector_dot
        dot_cpp.argtypes =(ctypes.POINTER(ctypes.int), ctypes.c_uint64,ctypes.POINTER(ctypes.int), ctypes.c_uint64)
        
        seq = ctypes.c_uint64 * len(vector_a)(*vector_a)
        arr = seq(*pyarr)

        return dot_cpp(vector_a, len(vector_a), vector_b, len(vector_b))
        '''
        
    '''
    Wrappers to call optimized C++ functions
    '''

    def calculate_sqrt_cpp(self, value):
        sqrt_cpp = self.cpp_lib.calculate_sqrt
        return sqrt_cpp(value)

    def calculate_add_cpp(self, a, b):
        #return 2.2
        sqrt_add = self.cpp_lib.calculate_add
        sqrt_add.restype = ctypes.c_float
        sqrt_add.argtypes = [ctypes.c_float, ctypes.c_float]

        return sqrt_add(a, b)

    '''
    def get_message_cpp(self):
        get_message = self.cpp_lib.get_message
        get_message.restype = ctypes.c_wchar_p
        return get_message()
    '''

if __name__ == '__main__':
    pipeline = ProcessingPipeline()
    pipeline.benchmark()




