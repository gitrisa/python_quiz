import numpy as np
from PIL import Image
from ai_edge_litert.interpreter import Interpreter


interpreter = Interpreter(
    model_path="model/model.tflite"
)

interpreter.allocate_tensors()


input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


with open("model/labels.txt", "r") as file:
    labels = file.read().splitlines()



def predict_image(filepath):

    image = Image.open(filepath)

    image = image.resize((224,224))

    image = np.array(image)

    image = np.expand_dims(image, axis=0)

    image = image.astype(np.float32)

    image = image / 255.0


    interpreter.set_tensor(
        input_details[0]["index"],
        image
    )


    interpreter.invoke()


    output = interpreter.get_tensor(
        output_details[0]["index"]
    )


    prediction_index = np.argmax(output)


    prediction = labels[prediction_index]


    confidence = output[0][prediction_index] * 100


    return prediction, confidence