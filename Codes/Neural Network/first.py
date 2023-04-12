import tensorflow as tf
from tensorflow.keras import layers

# define the input shape of the images
input_shape = (40, 40, 1)  # 1 for grayscale images

# define the CNN architecture
model = tf.keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10)  # 10 classes (0-9)
])

# compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# load your data and preprocess it
# assuming your data is stored in X_train, y_train, X_test, y_test
X_train = X_train.reshape(-1, 40, 40, 1).astype('float32') / 255.0
X_test = X_test.reshape(-1, 40, 40, 1).astype('float32') / 255.0

# train the model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# evaluate the model
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print('Test accuracy:', test_acc)
