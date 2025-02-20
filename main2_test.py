import main_params as mp
import model_functions as model_funcs

import tensorflow as tf
import tensorflow_addons as tfa
from matplotlib import pyplot as plt
import random
import numpy as np

from pathlib import Path
import pickle

# --- ----

models_dir_path = Path(mp.TRAINED_MODELS_DIRECTORY)

# ---

model_file_paths = [sub_file for sub_file in models_dir_path.iterdir() if sub_file.is_file() and sub_file.suffix == '.hdf5']
number_of_models = len(model_file_paths)

print('Detected ' + str(number_of_models) + ' models in directory:')
for i,model_file_path in enumerate(model_file_paths):
    print('(' + str(i) + ') ' + str(model_file_path))

model_index = int(input('\nWhich model will be evaluated? [0-' + str(number_of_models - 1) + ']: '))

# ---

chosen_model = model_file_paths[model_index]

# ---

test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    mp.TEST_DATASET_DIRECTORY,
    shuffle = True,
            
    labels = "inferred",
    label_mode = "int",
    class_names = mp.label_names,
     
    image_size = (mp.img_HEIGHT, mp.img_WIDTH),
    batch_size = mp.BATCH_SIZE
).prefetch(
    buffer_size = tf.data.experimental.AUTOTUNE
)

# ---

test_model = mp.create_model()
test_model.load_weights(chosen_model)

test_model.summary()

# ---

results = test_model.evaluate(
    test_dataset,
    verbose=2
)

pickle.dump(results, open(
    str(Path(mp.TESTING_RESULTS_DIRECTORY)
        / (str(Path(chosen_model).stem) + '__results.obj')
    ), 'wb')
)
