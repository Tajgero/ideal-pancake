# %%
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import tensorflow as tf
import numpy as np

# %%
def standard_scaler(data):
    mean = np.mean(data, axis=0) # For columns
    std = np.std(data, axis=0) # For columns
    return (data - mean) / std

# %%
# Load the dataset from the text file
data = np.loadtxt('./data/ml_course/data_w3_ex1.csv', delimiter=',')
x = data[:,0]
y = data[:,1]

# Convert 1-D arrays into 2-D
X = np.expand_dims(x, axis=1); print(f"the shape of the inputs x is: {x.shape}")
y = np.expand_dims(y, axis=1); print(f"the shape of the targets y is: {y.shape}")

# %%
"""
# Get 60% of the dataset as the training set. 
# Put the remaining 40% in dev set.
# Split the 40% dev set above into halfs.
"""
X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.60, random_state=2025)
X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=0.50, random_state=2025)

# %%
# Compute the mean and standard deviation of the training set
scaler_linear = StandardScaler()
X_train_scaled = scaler_linear.fit_transform(X_train)

# Train the model
linear_model = LinearRegression()
linear_model.fit(X_train_scaled, y_train)

# Feed the scaled training set and get the predictions
prediction_train = linear_model.predict(X_train_scaled)

# Calculate MSE
J_train = mean_squared_error(y_train, prediction_train) / 2
print(f"MSE_train: {J_train}")

# Transform dev set, not fit: It was fitted on training data and kept that way!
X_val_scaled = scaler_linear.transform(X_val)
prediction_val = linear_model.predict(X_val_scaled)
J_val = mean_squared_error(y_val, prediction_val) / 2
print(f"MSE_val: {J_val}")

# %%
# =============================================================================
# Polynomial features
# =============================================================================
# Loop n times over to create different polynomial models

# Initialize lists to save the errors, models, and feature transforms
train_mses = []
val_mses = []
models = []
polys = []
scalers = []
n = 10 # Max Polynomial Models increasing by 1 each time

for degree in range(1, n+1):

    # Compute the number of features and transform the training set
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_mapped = poly.fit_transform(X_train)
    polys.append(poly)
    
    # Scale mapped training set
    scaler_poly = StandardScaler()
    X_train_mapped_scaled = scaler_poly.fit_transform(X_train_mapped)
    scalers.append(scaler_poly)
    
    # Create and train model
    model = LinearRegression()
    model.fit(X_train_mapped_scaled, y_train)
    models.append(model)
    
    # Compute the training MSE
    prediction = model.predict(X_train_mapped_scaled)
    J_train = mean_squared_error(y_train, prediction) / 2
    train_mses.append(J_train)
    
    # Add the polynomial features to the cross validation set
    X_val_mapped = poly.transform(X_val)
    X_val_mapped_scaled = scaler_poly.transform(X_val_mapped)
    prediction = model.predict(X_val_mapped_scaled)
    J_val = mean_squared_error(y_val, prediction) / 2
    val_mses.append(J_val)

# %%
# Plot evaluation
from matplotlib import pyplot as plt
plt.figure()
plt.ylabel("MSE")
plt.xlabel("degree")
# Downward arrows
head = (np.argmin(train_mses) + 1, np.min(train_mses) + 10)
plt.annotate(
    f"Training best MSE {np.min(train_mses):.2f}",
    xy=head, # Arrowhead position
    xytext=(head[0], head[1] + 100), # Text and arrow tail position
    arrowprops=dict(facecolor='blue', shrink=0.05),
    horizontalalignment='center'
)
head = (np.argmin(val_mses) + 1, np.min(val_mses) + 10)
plt.annotate(
    f"Validation best MSE {np.min(val_mses):.2f}",
    xy=head, # Arrowhead position
    xytext=(head[0], head[1] + 100), # Text and arrow tail position
    arrowprops=dict(facecolor='green', shrink=0.05),
    horizontalalignment='center'
)
plt.plot(np.arange(1, n+1), train_mses, marker="o", c="blue", label="training")
plt.plot(np.arange(1, n+1), val_mses, marker="o", c="green", label="validation")
plt.legend()

# %%
"""
# Because best validation is 2 degree model, best training is 10 degree model
# to not overfit model we choose model with 2 degree, because it best generalize
# new data while checking which model to choose
"""
degree = np.argmin(val_mses) + 1

# Choose final model and check generalization on test set
X_test_mapped = polys[degree - 1].transform(X_test)
X_test_mapped_scaled = scalers[degree - 1].transform(X_test_mapped)
prediction_test = models[degree - 1].predict(X_test_mapped_scaled)
J_test = mean_squared_error(y_test, prediction_test) / 2
print(f"Training MSE: {train_mses[degree-1]:.2f}")
print(f"Cross Validation MSE: {val_mses[degree-1]:.2f}")
print(f"Test MSE: {J_test:.2f}")

# %%
# =============================================================================
# Neural Networks
# =============================================================================
# Add polynomial features
degree = 1
poly = PolynomialFeatures(degree, include_bias=False)
X_train_mapped = poly.fit_transform(X_train)
X_val_mapped = poly.transform(X_val)
X_test_mapped = poly.transform(X_test)

# %%
# Scale the features using the z-score
scaler = StandardScaler()
X_train_mapped_scaled = scaler.fit_transform(X_train_mapped)
X_val_mapped_scaled = scaler.transform(X_val_mapped)
X_test_mapped_scaled = scaler.transform(X_test_mapped)

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
nn_train_mses = []
nn_val_mses = []
history = []

# Loop over the the models
for model in nn_models:
    
    # Setup the loss and optimizer
    model.compile(
    loss='mse',
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
    metrics=['mae']
    )

    print(f"Training {model.name}...")
    
    # Train the model
    result = model.fit(
        X_train_mapped_scaled, y_train,
        epochs=300,
        verbose=0
    )
    history.append(result)
    
    print("Done!\n")
    
    # Record the training MSEs
    pred = model.predict(X_train_mapped_scaled)
    train_mse = mean_squared_error(y_train, pred) / 2
    nn_train_mses.append(train_mse)
    
    # Record the cross validation MSEs 
    pred = model.predict(X_val_mapped_scaled)
    val_mse = mean_squared_error(y_val, pred) / 2
    nn_val_mses.append(val_mse)
    
# print results
print("RESULTS:")
for model_num in range(len(nn_train_mses)):
    print(
        f"Model {model_num+1}: Training MSE: {nn_train_mses[model_num]:.2f}, " +
        f"Val MSE: {nn_val_mses[model_num]:.2f}"
        )

# %%
# Select the model with the lowest val MSE
model_num = np.argmin(nn_val_mses) + 1

# Compute the test MSE
test_mse, test_mae = nn_models[model_num - 1].evaluate(X_test_mapped_scaled, y_test, verbose=0)
test_mse /= 2

print(f"Selected Model: {model_num}")
print(f"Training MSE: {nn_train_mses[model_num-1]:.2f}")
print(f"Cross Validation MSE: {nn_val_mses[model_num-1]:.2f}")
print(f"Test MSE: {test_mse:.2f}")
