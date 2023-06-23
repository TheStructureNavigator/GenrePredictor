#Dependencies
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

from sklearn.model_selection import train_test_split
import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras import layers
import keras_tuner

pd.set_option('display.max_rows', None)


#Data
hiphop = pd.read_csv('HipHop.csv')
pop = pd.read_csv('Pop.csv')
rock = pd.read_csv('Rock.csv')

genres = [hiphop, pop, rock]

df = pd.concat(genres, ignore_index = True).set_index('Track URI') #concatenate tracklists

#Columns
floats = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
category = ['key', 'mode', 'time_signature']

#Normalize objects
scaler = MinMaxScaler()
encoder = LabelEncoder()

#Normalizing floats
floats_normalized = scaler.fit_transform(df[floats].values)
normalized_df = pd.DataFrame(floats_normalized, columns = floats)

#Reset the indexes of the DataFrames before concatenation
normalized_df.reset_index(drop=True, inplace=True)
df.reset_index(drop=True, inplace=True)

#Concatenate to samples
samples = pd.concat([normalized_df, df[category]], axis = 1).values #input samples to an nn
samples_df = pd.concat([normalized_df, df[category]], axis = 1) # samples dataframe

#Target
target = encoder.fit_transform(df['genres'].values) #target encoding to values
target_df = pd.DataFrame(target, columns = ['genres']) #target dataframe

#Target dictionary
encoded_target = encoder.inverse_transform(target) #target decoding to string
target_dict = dict(zip(encoded_target, target)) #target encoding dictionary

#Dataframe representation
nn_dataframe = pd.concat([samples_df, target_df], axis = 1)

#Data split
X_train, X_test, y_train, y_test = train_test_split(samples, target)

#Model
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape = (13, 1)),
    tf.keras.layers.Dense(32, activation = 'relu'),
    #tf.keras.layers.Dense(32, activation= 'relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3, activation = 'softmax')
])
#Compiler
loss_func = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer = 'adam',
              loss = loss_func,
              metrics = ['accuracy'])

#Training
trained_model = model.fit(X_train, y_train, batch_size = 32, epochs = 100, verbose = 0, validation_split = 0.1)

#Evaluating to check performance
model.evaluate(X_test, y_test, verbose = 2)

plt.style.use('dark_background')  # plot style

# Plot training and validation loss
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13, 4))

axes[0].plot(trained_model.history['loss'], label='Training Loss')
axes[0].plot(trained_model.history['val_loss'], label='Validation Loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].legend()

# Plot training and validation accuracy
axes[1].plot(trained_model.history['accuracy'], label='Training Accuracy')
axes[1].plot(trained_model.history['val_accuracy'], label='Validation Accuracy')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].legend()

plt.tight_layout()  # Adjust the spacing between subplots
plt.show()

#Sample prediction
print('Model Prediction:', model(X_test)[6])
print('Genre', y_test[6])

#Prediction accuracy using predict method
predictions = model.predict(X_test)
predicted_labels = np.argmax(predictions, axis=1)
accuracy = np.mean(predicted_labels == y_test)
print(accuracy)