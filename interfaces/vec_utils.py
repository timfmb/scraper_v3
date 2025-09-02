from bson.binary import Binary, BinaryVectorDtype
import numpy as np


def normalize_to_int8(vector):
    """
    Normalize a vector of floats to int8 range (-128 to 127) for BSON conversion.

    Parameters:
    - vector: List or numpy array of floats.

    Returns:
    - A numpy array of int8 integers in the range [-128, 127].
    """
    # Convert input to numpy array for efficient computation
    vector = np.array(vector, dtype=float)

    # Compute the minimum and maximum values of the vector
    x_min = vector.min()
    x_max = vector.max()

    # Handle the case where all values are the same
    if x_max == x_min:
        # Map all values to zero (or any value within the range)
        int8_vector = np.full_like(vector, 0, dtype=np.int8)
    else:
        # Scale and shift the vector to fit into the range [-128, 127]
        normalized_vector = (vector - x_min) / (x_max - x_min)  # Scale to [0, 1]
        scaled_vector = normalized_vector * 255 - 128           # Scale to [-128, 127]
        int8_vector = np.round(scaled_vector).astype(np.int8)   # Round and convert to int8
    return int8_vector



def generate_bson_vector(vector, vector_dtype=BinaryVectorDtype.INT8):
   return Binary.from_vector(vector, vector_dtype)
