# gtrain

**Before you start using this package, please, read a part of README with heading Usage**


Project that using abstraction of a model and data to define structures that can be used for learning. Model can bee learned by gtrain function to fit the data properly. By model, I mean an arbitrary neural network or some other structure that can be represented in TensorFlow. 

This abstraction allows to implement almost everything you want without need to reimplementing learning algorithm all the time.

For example, it can easily handle various input lengths witch is not common in other implementations.

However, it is necessary to define model from scratch in TensorFlow framework. On the other hand, this process is inevitable when you want to use some uncommon architecture.


## Usage

Below, crucial concepts used by functions *gtrain* and *stran* are presented. Some of 

Model and Data describe methods of the classes that have to be overridden by their subclass.

Finally, algorithm descriptions shows how the functions operate and use some of their parameters.

### Model

**build()**  The method that creates model's representation in TensorFlow. It also stores some placeholders that are returned by other methods of the model.

**get_loss()**  Returns placeholder for a loss function.

**get_placeholders()** Returns a list of placeholders for the input and output.

**train_ended(session)** Executes after the training stops with session in which tre training was done.

**name()** Returns a specific name for given object.

Following methods are specific for the classification task, so in other cases, they can be implemented as some dummy functions, e.g., returning 1 all the time.

**get_hits()**  Returns placeholder for a number of correctly classified samples.

**get_counts()**  Returns placeholder for a number of samples passed into the model.

If you are familiar with TensorFlow sumarries then functions **get_train_summaries()** and **get_dev_summaries** allow you to add summaries into the training and validation steps, respectively.

### Data

**set_placeholders(placeholders_list)** It is called with an output from the method Model.get_placeholders() before training starts.

**train_ended()**  Executes after the training stops.

**get_dev_batches()** In validation stage, it returns a generator returning feed dictionaries for the tf.Session.run function. Each dictionary should have a value for each of previously obtained placeholders.

**get_batches()** Similar to get_dev_batches but in the training stage.


### *gtrain* - algorithm description

Below, a short description of the *gtrain* function is presented. The description aims to understanding of the synchronisation of the *gtrain* function and descendants of the Model and Data with respect to parameters *num_steps* and *evaluate_every*.  

For simplicity, the text between \*\*\* describes what is happening in the place where it is located without using Python syntax.

~~~
def gtrain(model, data, num_steps, evaluate_every):
    model.build() # build model in newly created TF session
    data.set_placeholders(model.get_placeholders())
    for training_step in range(num_steps):
        # train step
        for feed_dict in data.get_batches():
            ***Accumulate gradients, loss, and accuracy***
        ***Apply gradients to the model by selected optimizer***
        if training_step % evaluate_every == 0:
            # evaluation step
            for feed_dict in data.get_dev_batches():
                ***Accumulate loss and accuracy***
            ***Log validation loss and accuracy***
            if ***Loss increses***:
                ***Increment fails counter***
    data.train_ended()
    model.train_ended(***current session***)
~~~

The accumulating procedure helps with memory requirements for large datasets. In addition, it allows the application of variable input size. It the such case, get batches functions returns a part of the batch with different sizes.

Please, be aware that parameter `num_steps` refers to the sum of application of optimizeri, i.e., how many times the weights are changed. So, if the data contains `batch_count` batches then training algorithm with `epoch` epochs has `num_steps = 100 * batch_count * epochs` and `evaluate_every = batch_count * epoch`.

### *strain* - algorithm description

~~~
def strain(model, data, num_steps, session=None):
    if session is not None:
        session = tf.Session()
        with session.as_default()
            model.build()
            session.run(tf.global_variable_initializer())
    
    data.set_placeholders(model.get_placeholders())
    
    for _ in range(num_steps):
        for feed_dict in data.get_batches():
            ***Applie gradients with respect to data in feed_dict***
    data.train_ended()
    model.train_ended(session)
    return session
~~~


## Examples

There are implemented examples of the subclasses of Model:

* **FCNet** is representation of the multilayer perceptron.

* **TextCNN** is convolutional nerual network for a text classification. Architecture of a type: convolution, over-all max pooling, additional fully connected layers.

There are also implementation of the subcasses of Data:

* **AllData** in which the gradient is computed on all training samples each time.

* **BatchData** in which the gradient application is conduct separately on subsets of training samples with specified size.

Examples of applications gtrain function are included in a folder *example* in the github repository.

Artificial dataset is used in the file **random_data_FC_net.py**. The gradient is computed on the whole data because the AllData subcalass of Data is used. The architecture of applied multilayer perceptron (MLP) is 2-3-3. The MLP is set to use MSE as loss function by setting 

The second example located in the file **mnist_batch_data_FC_net.py**. This example applies data with batches that have a size 32 and teh architecture of applied NN is 784-30-20-10.

## Module *utils*

The module *utils* presents some function that comes handy when applying trying procedure on classification task.
Following list provide a short description of included functions for more informations see documentation.

* **get_loss_and_accuracy** - retreave a loss and accuracy measures that were coomputed during the training and saved as a TensorFlow summary

* **confmat** - computes confusion matrix of given two labels in either one-hot encoding representation or plain integer labels

* **accuracy** - similar to confmat, but it computes accuracy.

* **labels2probabilities** - transforms list of integer labels into one-hot encoding representation.

* **save_weights** - saves list of numpy arrays

* **load_weights** - loads list of numpy arrays saved by save_weights

* **check_dir** - creates the whole directory path if not exists

* **join_weights_and_biases** - joins two list of numpy arrays into one.

* **get_class_vs_others_indexes** - generates indexes of given samples that contains samples with the same numbers from given class and all the others.


## Module *statutils*

Rigorous statistical comparison of classifiers is complex task, because if more than two classifiers are present, more than one hypothesis is tested at the same time.
Procedure of performance of statistical tests is described in an article with name "Statistical comparisons of classifiers over multiple data sets" published by Janez Demšar in 2006. Function *compere_classifiers* copies the process describe in this article.

WARNING: This module requires to imoprt *scipy.stats*.

**WARNING: Function *compere_classifiers* may require user input if it requires to find and input certain value in the statistical tables** 

Example for the usage of the function is presented in file *compere_classifiers.py* in example directory of the repository.