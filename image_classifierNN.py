import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import cv2
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from keras import layers as Layers

class_names = ["buildings", "forest", "glacier", "mountain", "sea", "street"]
class_names_label = {"buildings": 0,
                     "forest": 1,
                     "glacier": 2,
                     "mountain": 3,
                     "sea": 4,
                     "street": 5
                     }

#Getting data

def load_data():
    data_sets = ["seg_train/seg_train", "seg_test/seg_test"]
    size = (150, 150)
    output = []
    for dataset in data_sets:
        directory = "Data/" + dataset
        X = []
        y = []
        for folder in os.listdir(directory):
            curr_label = class_names_label[folder]
            for file in os.listdir(directory + "/" + folder):
                img_path = directory + "/" + folder + "/" + file
                curr_img = cv2.imread(img_path)
                curr_img = cv2.resize(curr_img, size)
                X.append(curr_img)
                y.append(curr_label)
        X, y = shuffle(X, y)
        X = np.array(X, dtype="float32")
        y = np.array(y, dtype="int32")

        output.append((X, y))
    return output

(train_images, train_labels), (test_images, test_labels) = load_data()

#Scale data
train_images = train_images / 255.0
test_images = test_images / 255.0


model = keras.Sequential([keras.layers.Conv2D(200, (3, 3), activation="relu", input_shape=(150, 150, 3)),
                          keras.layers.Conv2D(180, (3,3), activation='relu'),
                          keras.layers.MaxPooling2D(pool_size=(5, 5)),
                          keras.layers.Conv2D(180, (3, 3), activation="relu"),
                          keras.layers.Conv2D(140, (3, 3), activation="relu"),
                          keras.layers.Conv2D(100, (3, 3), activation="relu"),
                          keras.layers.Conv2D(50, (3, 3), activation="relu"),
                          keras.layers.MaxPooling2D(pool_size=(5, 5)),
                          keras.layers.Flatten(),
                          keras.layers.Dense(180, activation="relu"),
                          keras.layers.Dense(100, activation="relu"),
                          keras.layers.Dense(50, activation="relu"),
                          keras.layers.Dense(6, activation="softmax")
                          ])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(train_images, train_labels, epochs=30)

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print("Test accuracy: {}".format(test_acc))
predictions = model.predict(test_images)

for i in range(10):
    print("Image #{}".format(i))
    print("Prediction: {}".format(class_names[np.argmax(predictions[i])]))
    print("Actual Image: {}\n".format(class_names[test_labels[i]]))
