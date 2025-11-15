from Linear_Regression_multiple_var import *
from Logistic_Regression import sigmoid
from dataclasses import dataclass

@dataclass
class Neuron():
    X_train: object
    y_train: object
    w_in: float = 0.0
    b_in: float = 0.0
    alpha: float = 1e-3
    max_iters: int = 100_000
    min_erg: float = 1e-6
    lambda_: float = 0.0
    
    def __post_init__(self):
        """Sets w_in if not specified"""
        if not self.w_in:
            self.w_in = np.zeros_like(self.X_train[0])
    
    def run_gradient(self):
        self.w, self.b, self.history = gradient_descent(
            self.X_train, self.y_train, self.w_in, self.b_in, self.alpha, 
            self.max_iters, self.min_erg, self.lambda_
        )


def dense_loop(a_in, W, b, activation='sigmoid'):
    """
    Make layer in Neural Network from neurons
    n - features per unit, j - units
       
    Args:
        a_in (ndarray (n, )) : Data, 1 example 
        W    (ndarray (n,j)) : Weights matrix
        b    (ndarray (j, )) : Bias vector for this layer
    Returns:
        a_out (ndarray (j, )) : Output vector
    """
    match activation:
        case 'sigmoid': g = sigmoid
        case _: raise NotImplementedError
    
    units = W.shape[1]
    a_out = np.zeros(units)
    
    # For each unit calculates output for g() activation function
    for j in range(units):
        w = W[:, j]
        z = np.dot(w, a_in) + b[j]
        a_out[j] = g(z)
        
    return a_out


def my_dense(A_in, W, B, activation='sigmoid'):
    """
    Make layer in Neural Network from neurons
    Vectorized approach
    """
    match activation:
        case 'sigmoid': g = sigmoid
        case _: raise NotImplementedError
        
    Z = np.matmul(A_in, W) + B
    
    return g(Z)


def my_sequential(x, W1, b1, W2, b2, W3, b3):
    a1 = my_dense(x,  W1, b1, sigmoid)
    a2 = my_dense(a1, W2, b2, sigmoid)
    a3 = my_dense(a2, W3, b3, sigmoid)
    
    return(a3)


if __name__ == "__main__":
    X_train = np.array([[2104, 5, 1, 45], [1416, 3, 2, 40], [852, 2, 1, 35]])
    y_train = np.array([460, 232, 178])
    
    unit1 = Neuron(X_train, y_train, alpha=1e-7, min_erg=1e-3)
    unit1.run_gradient()

