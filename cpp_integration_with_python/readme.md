# How to integrate high-performing C++ blocks into Python 

While Python is the language to get things done fast,<br>
C and C++ is the language to make performance critical sections run fast.<br>
Let's take a look how to combine the best of both Worlds.

# Table of Contents
- [Typical scenario](#typical-scenario)
- [Options and their tradeoffs](#available-options-and-their-tradeoffs)
- [a) Ctypes](##a-ctypes)
- [b) SWIG](##b-swig)
- [c) Python C-API](##c-python-c-api)
- [d) Cython](##d-cython)
- [Summary](#summary)

# Typical scenario

The team started its new project.<br>
They used Python to produce working prototype.<br>
They faced obstacles on the way.<br> 
They had to change some assumtions and some tooling.<br>
But no big deal as Python allowed them to adjust fast.<br>

Now they got it to the production.<br>
While it works well,<br>
they identified a few performance bootlenecks,<br>
including the following function calculating dot product of two sparse vectors:
```
def sparse_vector_dot(self, vector_a: [()], vector_b: [()]):
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
```

<br>
Now the team wants to speed it up by rewritting it into C++<br>
while continue calling it from Python.<br>

# Available options and their tradeoffs

There are 4 commonly used techniques we will use here.
a) ctyoes
b) SWIG
c) Python-C-API
d) Cython


## a) ctypes
ctypes is standard Python library<br>
allowing us to call from Python C or C++ functions shared in DLLs. <br> 

With ctypes,<br>
you can call directly from your Python code <br>
compiled C++ .dll library prepared by you or by somebody else.<br>

If later a new version of C++ .dll is released,<br>
you just place it to the folder and load that new version.<br>
No need to change Python code as long as none of interfaces changed.

ctypes is great option for:
- For simple cases as loading C++ dll is about a few datatypes transitions
- For using existing C++ library where recompilation is difficult
- For situation when you want to stick with a standard Python module without need to install anything extra

ctypes disadvantages:
- Wrapping lots of code can be tedious
- If there is an error in external library, your whole Python interpreter will crash
- Debugging can become hell. Your stack is obscured by ctypes/ffi magic and finding out what cause specific variable values can get complicated

## ctypes code example

To get ctypes work with our C++ code,<br>
we need to ensure that C++ compiler will not mangle function names.<br> 
We achieve it by wrapping the the API into extern "C" section as shown below.

```
extern "C"
{
    LIBRARY_API int sparse_vector_dot(const uint64_t **vector_a, const uint64_t vector_a_size, const uint64_t **vector_b, const uint64_t vector_b_size) {
        long dot_product = 0;

        int idx_a = 0;
        int idx_b = 0;
        // ....
        return dot_product
    }
}
```
C is strongly type language, so we need to specify for each variable its data types.
Python on the other hand is a dynamically typed language, so each variable there is an object type.
So we need to specify C data type that we are passing to our C function.

List of ctypes with their C equivalent in the official documentation [Officiaul documentation](https://docs.python.org/3/library/ctypes.html#fundamental-data-types). 

## b) SWIG

SWIG is flip side of ctypes.

SWIG (Simplified Wrapper and Inrerface Generator) 
allows us to call C and C++ code from high-level languages. Except the Python, it's C#, Java, Go and others.

SWIG is a great tool if we need wrapping between multiple languages. 

## SWIG Example

## c) Python C API

Python C-Api is used to write official extension modules for Python. Example can be NumPy or TensorFlow.

I mention for Python C Api for completness,
personally I had never the need to use it,

Disadvantages:
- Effort insentive
- No forward compatibility across Python versions as C-API changes

The official documentation for Python C API can be found [here](https://docs.python.org/3/c-api/index.html). Personally, I find  the most explanatory the one provided by NumPy [here](https://numpy.org/devdocs/user/c-info.how-to-extend.html).


## Python C API code example
When extension module is compiled and installed into Python path,
the code can be imported into module.

```
import your_function_factorial

print (your_function_factorial.calculate(5))
```

Thought is looks like ordinary Python import,
the code is written in C++.


## d) Cython



# Summary



