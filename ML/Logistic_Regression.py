import numpy as np


def sigmoid(value: float):
    """Turns any value to probability range"""
    return 1 / (1 + np.exp(-value))
    

def loss_log(target: float, pred: float):
    """Returns logistic cost for value and its prediction"""
    return -target * np.log(pred) - (1 - target) * np.log(1 - pred)


def compute_model_output(X, w, b):
    """Predicts output"""
    m = X.shape[0] # number of training examples
    
    f_wb = np.zeros(m)
    for i in range(m):
        f_wb[i] = sigmoid(np.dot(w, X[i]) + b)
        
    return f_wb


def compute_cost_log(X, y, w, b):
    """Cost function for logistic regression"""
    m = X.shape[0]

    cost_sum = 0
    for i in range(m):
        f_wb = sigmoid(np.dot(w, X[i]) + b)
        cost = loss_log(y[i], f_wb)
        cost_sum += cost

    return cost_sum / m


def compute_gradient_log(X, y, w, b):
    """Computes gradients for weight and bias in logistic regression"""
    m, n = X.shape # m - parameters, n - features
    
    # X[i] - vector across all features
    # X[i, j] - scalar number in "j" feature
    # w - initiate vector of weights
    # b - scalar number of bias
    
    dj_db = 0
    dj_dw = np.zeros(n)
    
    for i in range(m): # For each example
        f_wb = sigmoid(np.dot(w, X[i]) + b) # Prediction
        error = f_wb - y[i] # Simple error: prediction - target
        dj_db += error
        for j in range(n): # For each feature
            dj_dw[j] += error * X[i, j]

    return (dj_dw / m, dj_db / m)


def gradient_descent_log(X, y, w_in, b_in, alpha=0.01, num_iters=10000, erg_eval=1e-3):
    """
    Performs batch gradient descent
    
    Args:
        X (ndarray_like)  : Input train data array
        y (array_like)    : Input train target data
        w_in (array_like) : Initialize weights at start
        b_in (int)        : Initialize bias at start
        alpha (float, optional)     : Learning rate
        num_iters (int, optional)   : Number of iterations to run gradient descent
        erg_eval (float, optional)  : Minimum error improvement

    Returns:
        w (ndarray)       : Updated values of parameters
        b (int)           : Updated value of parameter
        J_history (list)  : List of cost evaluations
    """
    from copy import deepcopy
    # Hyperparameters
    a = alpha
    w = deepcopy(w_in)
    b = b_in
    error = np.inf

    # History
    J_history = []
    
    # Finding weight and bias
    for i in range(num_iters):
        dj_dw, dj_db = compute_gradient_log(X_train, y_train, w, b)
        
        # Updates hyperparameters
        w = w - a * dj_dw
        b = b - a * dj_db
    
        new_error = compute_cost_log(X_train, y_train, w, b)
        
        # Save cost J at each iteration
        if i % 10 == 0: # prevent resource exhaustion 
            J_history.append((i, new_error))
        
        if error - new_error < erg_eval: #or new_error > error:
            print(f"Converged after {i+1} iterations.")
            break
        error = new_error
    else:
        print("Max iterations reached")
    
    return w, b, J_history


if __name__ == '__main__':
    """For some points it calculates best logistic regression"""
    
    # Initialize a max iterations and minimum change to converge
    iters = 40000
    erg_eval = 1e-6
    
    # Data
    X_train = np.array([[0.5, 1.5], [1,1], [1.5, 0.5], [3, 0.5], [2, 2], [1, 2.5]])
    y_train = np.array([0, 0, 0, 1, 1, 1])
    
    # Parameters
    a = 0.1
    w = np.zeros_like(X_train[0])
    b = 0
    
    w, b, history = gradient_descent_log(X_train, y_train, w, b, a, iters, erg_eval)
    
    # Predict
    print(f"Cost: {compute_cost_log(X_train, y_train, w, b):.3f}")
    print(f"Weights: {w.round(2)}")
    print(f"Bias: {b:.2f}")
    
    # Solution
    w_print = [str(i) + '(x' + str(j) + ')' for j, i in enumerate(np.round(w, 3))]
    print(f"Regression: f(x) = {' + '.join(w_print)} + {b:.3f}")
    
    
    # Show learning curve
    from matplotlib import pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13,6))
    
    Jx = [x[0] for x in history]
    Jy = [y[1] for y in history]

    # Cost plot
    ax1.set_title("Cost vs iterations")   
    ax1.set_xlabel("Iterations")
    ax1.set_ylabel("Cost")
    ax1.plot(Jx, Jy)
    
    
    # Filter the data
    X_class_0 = X_train[y_train == 0]
    X_class_1 = X_train[y_train == 1]
    
    # Scatter data
    ax2.set_title("Classification")   
    ax2.set_xlabel("x1")
    ax2.set_ylabel("x2")
    ax2.scatter(X_class_0[:,0], X_class_0[:,1], s=120, marker='o')
    ax2.scatter(X_class_1[:,0], X_class_1[:,1], s=120, marker='X')
    
    # Points for line
    x0 = -b/w[0]
    x1 = -b/w[1]
    
    # Boundary line
    ax2.plot([0,x0], [x1,0], c='green', lw=3)
    ax2.fill_between()
    
    plt.show()
    
    
    
