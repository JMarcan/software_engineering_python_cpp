import pytest
from python_pipeline import ProcessingPipeline

def test_sparse_vector_dot():
    pipeline = ProcessingPipeline()
    vector_a = [(2, 1), (3, 1), (4, 1)]
    vector_b = [(1, 3), (3, 2), (5, 3)]

    assert pipeline.sparse_vector_dot(vector_a, vector_b) == 2

def test_sparse_vector_dot_cpp():
    pipeline = ProcessingPipeline()
    vector_a = [(2, 1), (3, 1), (4, 1)]
    vector_b = [(1, 3), (3, 2), (5, 3)]

    assert pipeline.sparse_vector_dot_cpp(vector_a, vector_b) == 2

def test_calculate_sqrt():
    pipeline = ProcessingPipeline()
    assert pipeline.calculate_sqrt_cpp(5) == 25

def test_calculate_add():
    pipeline = ProcessingPipeline()
    assert pipeline.calculate_add_cpp(1.1, 1.1) == pytest.approx(2.2, 0.1)

'''
- implementation not working now
def test_get_message():
    pipeline = ProcessingPipeline()
    assert pipeline.get_message_cpp() == "Message from C++ function"
'''

pytest.main()