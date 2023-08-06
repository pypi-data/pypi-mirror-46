import numpy as np
from preprocessing_utils import generate_images_arrays
from misc_utils import my_import
def max_occ_position(lst):
    return lst[np.argmax(np.array([lst.count(i) for i in lst]))]
def severity_prediction(imgs_path, model, model_config):
    patient = generate_images_arrays(imgs_path, model.input_shape[1:3], my_import(model_config['preprocess_input_function']))
    return model.predict(patient)
def mean_severity_prediction(imgs_path, model, model_config):
    return round(np.mean(argmax_severity_prediction(imgs_path, model, model_config)))
def argmax_severity_prediction(imgs_path, model, model_config):
    return [np.argmax(pred) for pred in severity_prediction(imgs_path, model, model_config)]
def max_severity_prediction(imgs_path, model, model_config):
    lst = argmax_severity_prediction(imgs_path, model, model_config)
    return max_occ_position(lst)
def argmax_mean_high_score(imgs_path, model, model_config):
    a =  severity_prediction(imgs_path, model, model_config)
    argmax_arr = np.array([arr.argmax() for arr in a])
#     print('argmax array ',argmax_arr)
    severity = max_occ_position(argmax_arr.tolist())
#     print('severity',severity)
    c_arr = np.array([arr for arr in a if arr.argmax() == severity ]).reshape(-1,5)
#     print('Arrays that corresponds to argmax Class ',c_arr,'with shape :',c_arr.shape)
    c_arr_mean = []
    for i in range(5) :
        c_arr_mean.extend([np.mean(c_arr[:,i])])
    score=np.sum(c_arr_mean[0:3])
    return float(score)

def mean_severity_score_prediction(imgs_path, model, model_config):
    return np.mean(severity_prediction(imgs_path, model, model_config))

def mean_ctr_score_prediction_by_label(imgs_path, model, label_i, model_config):
    return np.mean(severity_prediction(imgs_path, model, model_config))

def mean_ctr_score_prediction_by_label(imgs_path, model, label_i, model_config):
    return np.mean(severity_prediction(imgs_path, model, model_config)[label_i])