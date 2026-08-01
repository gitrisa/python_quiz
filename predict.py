import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps

# Load SavedModel
model = tf.saved_model.load("model/model.savedmodel")

# Ambil fungsi inferensi
infer = model.signatures["serving_default"]

# Load label
with open("model/labels.txt", "r") as file:
    labels = file.readlines()


def predict_image(image_path):

    image = Image.open(image_path).convert("RGB")

    image = ImageOps.fit(
        image,
        (224, 224),
        Image.Resampling.LANCZOS
    )

    image_array = np.asarray(image)

    image_array = (
        image_array.astype(np.float32) / 127.5
    ) - 1

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    tensor = tf.convert_to_tensor(
        image_array
    )

    output = infer(tensor)

    prediction = list(
        output.values()
    )[0].numpy()

    index = np.argmax(prediction)

    confidence = float(
        prediction[0][index]
    ) * 100

    label = labels[index].strip()

    label = label.split(" ", 1)[1]

    return label, round(confidence, 2)