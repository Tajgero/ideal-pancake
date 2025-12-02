import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.activations import linear, relu, sigmoid
import matplotlib.pyplot as plt
import logging

# Settings
logging.getLogger("tensorflow").setLevel(logging.ERROR)
tf.autograph.set_verbosity(0)
np.set_printoptions(precision=2)


def softmax(z):
    """ Softmax converts a vector of values to a probability distribution.
    Args:
      z (ndarray (N,))  : input data, N features
    Returns:
        (ndarray (N,))  : softmax of z
    """  
    return np.exp(z) / np.sum(np.exp(z))


# load dataset
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

# View letter
letter = np.random.randint(X_train.shape[0])
plt.figure()
plt.imshow(X_train[letter], cmap='gray')
print("It should be", y_train[letter])

# Build model
features = X_train.shape[1] * X_train.shape[2]
model = Sequential([
    tf.keras.Input(shape=(28, 28)), # Specify input shape
    Flatten(),
    Dense(25, activation=relu),
    Dense(15, activation=relu),
    Dense(10, activation=linear),
    
], name = "mnist_model")
model.summary()

# Examine Weights shapes
[_, layer1, layer2, layer3] = model.layers
W1,b1 = layer1.get_weights()
W2,b2 = layer2.get_weights()
W3,b3 = layer3.get_weights()
print(f"W1 shape = {W1.shape}, b1 shape = {b1.shape}")
print(f"W2 shape = {W2.shape}, b2 shape = {b2.shape}")
print(f"W3 shape = {W3.shape}, b3 shape = {b3.shape}")

# Compile - from logits
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
)
history = model.fit(X_train, y_train, epochs=5) # Educational only

# Plot loss
plt.figure()
plt.ylabel("Loss (cost)"); plt.xlabel("Epoch"); plt.grid(True)
plt.plot(history.epoch, history.history["loss"])

# Evaluate neural network performance
model.evaluate(X_test,  y_test, verbose=2)

# Predict
predictions = model.predict(X_test) # Not softmaxed
predictions = tf.nn.softmax(predictions) # Softmaxed
predictions_best = np.argmax(predictions, axis=1) # Get best prediction
correct_predictions = np.sum(predictions_best == y_test)
accuracy = correct_predictions / len(y_test)
print(f'\nAccuracy: {accuracy:.4f}')
