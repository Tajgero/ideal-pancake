# %%
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import tensorflow as tf
import numpy as np

# %%
# Load the dataset from a text file
data = np.loadtxt('data/ml_course/data_w3_ex2.csv', delimiter=',')

# Split the inputs and outputs into separate arrays
x_bc = data[:,:-1]
y_bc = data[:,-1]
y_bc = np.expand_dims(y_bc, axis=1)

print(f"the shape of the inputs x is: {x_bc.shape}")
print(f"the shape of the targets y is: {y_bc.shape}")

# %%
# Split data
X_train, X_val, y_train, y_val = train_test_split(x_bc, y_bc, train_size=0.6, random_state=2025)
X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=0.5, random_state=2025)

# %%
# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# %%
# Build the models
model_1 = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(25, activation = 'relu'),
        tf.keras.layers.Dense(15, activation = 'relu'),
        tf.keras.layers.Dense(1, activation = 'linear')
    ],
    name='model_1'
)
model_2 = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(20, activation = 'relu'),
        tf.keras.layers.Dense(12, activation = 'relu'),
        tf.keras.layers.Dense(12, activation = 'relu'),
        tf.keras.layers.Dense(20, activation = 'relu'),
        tf.keras.layers.Dense(1, activation = 'linear')
    ],
    name='model_2'
)
model_3 = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(32, activation = 'relu'),
        tf.keras.layers.Dense(16, activation = 'relu'),
        tf.keras.layers.Dense(8, activation = 'relu'),
        tf.keras.layers.Dense(4, activation = 'relu'),
        tf.keras.layers.Dense(12, activation = 'relu'),
        tf.keras.layers.Dense(1, activation = 'linear')
    ],
    name='model_3'
)
nn_models = [model_1, model_2, model_3]

# %%
# Initialize lists that will contain the errors for each model
nn_train_error = []
nn_val_error = []
history = []

# Loop over the the models
for model in nn_models:
    
    # Setup the loss and optimizer
    model.compile(
    loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
    metrics=['mae']
    )
    print(f"Training {model.name}...")
    
    # Train the model
    result = model.fit(
        X_train_scaled, y_train,
        epochs=200,
        verbose=0
    )
    history.append(result)
    
    print("Done!\n")
    
    # Set the threshold for classification
    threshold = 0.5
    
    # Record the fraction of misclassified examples for the training set
    yhat = model.predict(X_train_scaled)
    yhat = tf.math.sigmoid(yhat)
    yhat = np.where(yhat >= threshold, 1, 0)
    train_error = np.mean(yhat != y_train)
    nn_train_error.append(train_error)

    # Record the fraction of misclassified examples for the cross validation set
    yhat = model.predict(X_val_scaled)
    yhat = tf.math.sigmoid(yhat)
    yhat = np.where(yhat >= threshold, 1, 0)
    val_error = np.mean(yhat != y_val)
    nn_val_error.append(val_error)

# Print the result
for model_num in range(len(nn_train_error)):
    print(
        f"Model {model_num+1}: Training Set Classification Error: {nn_train_error[model_num]:.5f}, " +
        f"CV Set Classification Error: {nn_val_error[model_num]:.5f}"
        )

# %%
# Select the model with the lowest error
model_num = np.argmin(nn_val_error) + 1

# Compute the test error
yhat = nn_models[model_num-1].predict(X_test_scaled)
yhat = tf.math.sigmoid(yhat)
yhat = np.where(yhat >= threshold, 1, 0)
nn_test_error = np.mean(yhat != y_test)

print(f"Selected Model: {model_num}")
print(f"Training Set Classification Error: {nn_train_error[model_num-1]:.4f}")
print(f"CV Set Classification Error: {nn_val_error[model_num-1]:.4f}")
print(f"Test Set Classification Error: {nn_test_error:.4f}")
