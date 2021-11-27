import numpy as np
import pandas as pd
from preprocess import PatternTokenizer
from tensorflow.keras.preprocessing import sequence
import tensorflow as tf
interpreter = tf.lite.Interpreter(model_path="final_model_quant.tflite")
interpreter.allocate_tensors()
input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]
maxlen=150
import pickle
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
tokenizer_2 = PatternTokenizer()

def predictions(message):
 test = [[message]]
 data = pd.DataFrame(test)
 data[0] = tokenizer_2 .process_ds(data[0]).str.join(sep=" ")
 data = data[0].str.lower()
 data = tokenizer.texts_to_sequences(data)
 data = sequence.pad_sequences(data, maxlen=maxlen)
 interpreter.set_tensor(input_index, data.astype(np.float32))
 interpreter.invoke()
 predictions = interpreter.get_tensor(output_index)
 category = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
 mask=np.array([0.3,0.3,0.3,0.3,0.3,0.3])
 if(np.greater(predictions,mask).any()):
     result_1 = category[predictions.argmax()]
     category.pop(predictions.argmax())
     predictions = np.delete(predictions, predictions.argmax())
     result_2 = category[predictions.argmax()]
     return (result_1,result_2)
 else:
     return(None,None)

