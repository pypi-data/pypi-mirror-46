import numpy as np
import os
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


def get_loss_and_accuracy(save_dir):
    """
    loads scalars from training procedure saved in summaries created by gtrain
    :param save_dir: same as save_dir in gtrain method
    :return: dict with
        "val_acc": vector of validation accuracies
        "val_loss": vector of loss
        "val_stem": step in which the record was made
        "val_timestamp": time in which the record was made
        "train_acc": vector of validation accuracies
        "train_loss": vector of loss
        "train_stem": step in which the record was made
        "train_timestamp": time in which the record was made
    """
    def scallarEvent_list_2_dict(sel):
        wall_time = list()
        step = list()
        value = list()
        for se in sel:
            wall_time.append(se.wall_time)
            step.append(se.step)
            value.append(se.value)
        return {
            "wall_time": wall_time,
            "step": step,
            "value": value,
        }

    event_acc = EventAccumulator(os.path.join(save_dir, "summaries", "train"))
    event_acc.Reload()
    train_loss = scallarEvent_list_2_dict(event_acc.Scalars("loss"))
    train_acc = scallarEvent_list_2_dict(event_acc.Scalars("accuracy"))

    event_acc = EventAccumulator(os.path.join(save_dir, "summaries", "dev"))
    event_acc.Reload()
    val_loss = scallarEvent_list_2_dict(event_acc.Scalars("loss"))
    val_acc = scallarEvent_list_2_dict(event_acc.Scalars("accuracy"))
    return {
        "train_loss": train_loss["value"],
        "train_acc": train_acc["value"],
        "train_step": train_loss["step"],
        "train_timestamp": train_loss["wall_time"],
        "val_loss": val_loss["value"],
        "val_acc": val_acc["value"],
        "val_step": val_loss["step"],
        "val_timestamp": val_loss["wall_time"],
    }


def confmat(y0, y1, num_classes=None):
    """
    compute confusion matrix for y1 and y2 does not meter if either of them is in vector or integer form
    :param y0: list of - labels or vector of probabilities
    :param y1: list of - labels or vector of probabilities
    :param num_classes: number of classes if is not defined takes maximal value in labels as the highest class
    :return: confusion matrix
    """
    if not isinstance(y0[0], (int, float, np.int, np.int32, np.int64, np.float, np.float32, np.float64)):
        y0 = np.argmax(y0, axis=1)
    elif isinstance(y0, list):
        y0 = np.array(y0)
    if not isinstance(y1[0], (int, float, np.int, np.int32, np.int64, np.float, np.float32, np.float64)):
        y1 = np.argmax(y1, axis=1)
    elif isinstance(y1, list):
        y1 = np.array(y1)
    labels_num = max(max(y0), max(y1)) + 1 if num_classes is None else num_classes
    out = np.zeros((labels_num, labels_num))
    for i in range(labels_num):
        for j in range(labels_num):
            out[i, j] = np.sum(y1[y0==i]==j)
    return out


def accuracy(y0, y1):
    """
    compute accuracy for y1 and y2 does not meter if either of them is in vector or integer form
    :param y0: list of - labels or vector of probabilities
    :param y1: list of - labels or vector of probabilities
    :return: accuracy
    """
    if not isinstance(y0[0], (int, float, np.int, np.int32, np.int64, np.float, np.float32, np.float64)):
        y0 = np.argmax(y0, axis=1)
    elif isinstance(y0, list):
        y0 = np.array(y0)
    if not isinstance(y1[0], (int, float, np.int, np.int32, np.int64, np.float, np.float32, np.float64)):
        y1 = np.argmax(y1, axis=1)
    elif isinstance(y1, list):
        y1 = np.array(y1)

    out = np.sum(y0==y1)/len(y0)
    return out


def labels2probabilities(labels):
    """
    transforms labels into the 1-hod encoded vectors
    :param labels: list of integer values 0..(number_of_classes - 1), size n
    :return: matrix size (n, num_of_classes), ones are on the indexes defined by param labels
    """
    num_of_classes = max(labels)+1
    return np.apply_along_axis(lambda x: np.eye(num_of_classes)[x], 0, labels)


def save_weights(list_of_numpy_arrays, file_name):
    """
    saves list of numpy arrays into the file
    if the file have other than npz extension or no extension at all the .npz is added at the end of file_name
    (uses nympy function savez_compressed)
    :param list_of_numpy_arrays: list of numpy arrays
    :param file_name: filename with format npz
    """
    if os.path.dirname(file_name):
        check_dir(os.path.dirname(file_name))
    if not str(file_name).endswith(".npz"):
        file_name = file_name + ".npz"

    np.savez_compressed(file_name, *list_of_numpy_arrays)


def load_weights(file_name):
    """
    loads weights saved by save_weights, so the extension npz of the file is necessary
    :param file_name: filename with format npz
    :return: list of loaded numpy arrays
    """
    if not str(file_name).endswith(".npz"):
        raise IOError("file_name has bad format use .npz file insted.")
    l = np.load(file_name)
    files = l.files
    output = list()
    for file in files:
        output += [l[file]]
    return output


def check_dir(directory):
    """
    Checks if the path exists and if not it creates all missing folders
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def join_weights_and_biases(weights, biases):
    """
    joins two arrays into one
    :param weights: list of numpy arrays.
    :param biases: list of numpy arrays with same length as weights.
    :return: list of list with two numpy arrays for weights and biases, respectively.
        - the first index is defines layer and the second weight (0) or bias (1)
    """
    out = list()
    for i, _ in enumerate(weights):
        out.append([weights[i], biases[i]])
    return out


def get_class_vs_others_indexes(class_index, labels, return_new_labels=False):
    """
    Generate a indexes that contains the same number of samples from the specified class (class_index) and
    other remaining classes. It also can return new labels, i.e., 0 for samples with class_index and 1 for the others.
    The returned indexes are randomly shuffled.
    :param class_index: index of the base class
    :param labels: list of labels for given dataset
    :param return_new_labels: a flag
    :return: indexes of samples with all samples from the class (class_index) and the same number of other classes
        - if return_new_labels is True then also new labels are returned
    """
    ar = np.arange(len(labels))
    indexes0 = ar[labels==class_index]
    indexes1 = np.random.choice(ar[labels!=class_index], len(indexes0))
    out = indexes0 + indexes1
    out_lables = np.zeros((2*len(indexes0)), dtype=np.int)
    out_lables[-len(indexes0):] = 1
    rp = np.random.permutation(len(out))
    if return_new_labels:
        return out[rp], out_lables[rp]
    else:
        return out[rp]

