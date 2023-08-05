import tensorflow as tf
from abc import ABC


class Model(ABC):
    """
    Abstraction of the model (neural network) for gtrain learning process
    """
    def build(self):
        """
        method that build whole model in a Tensorflow environment
        """
        pass

    def get_loss(self):
        """
        :return: a tf variable that represents the loss function
        """
        pass

    def get_hits(self):
        """
        :return: a tf variable that represents correctly classified samples
        """
        pass

    def get_count(self):
        """
        :return: a tf variable that represents the number of samples
        """
        pass

    def get_train_summaries(self):
        """
        :return: additional summaries that are computed on the training data at each step of the gtrain training cycle
        """
        pass

    def get_dev_summaries(self):
        """
        :return: additional summaries that are computed on the testing data at each step of the gtrain training cycle
        """
        pass

    def get_placeholders(self):
        """
        :return: a tf placeholders of the input and output of the model
        """
        pass

    def train_ended(self, session):
        """
        a method that is called after the training of the model ended
        - you can for example save the trained weights of the model
        """
        pass

    def name(self):
        """
        :return: a name of the model with the particular settings
        """
        pass


class FCNet(Model):
    """
    Implementation of a multi layer perceptron
    """

    def __init__(self, layer_sizes, activation_function=tf.nn.sigmoid, use_cross_entropy=True, class_weights=None):
        """
        Constructor
        :param layer_sizes: a list of sizes of the layers, it begins with the input size and ends with number of classes
        :param activation_function: tf operator that is used as activation function
        :param use_cross_entropy: a flag if the cross entropy should be used
        :param class_weights: weights of the classes if is defined the model balance the gradient contribution of each class
        """
        self.input_size = layer_sizes[0]
        self.num_classes = layer_sizes[-1]
        self.layer_sizes = layer_sizes
        self.cross_entropy = use_cross_entropy
        self.activation_function=activation_function
        self.class_weights = class_weights

    def build(self):
        with tf.name_scope("Input"):
            self.x = tf.placeholder(tf.float32,shape=[None, self.input_size], name="Input...")
        with tf.name_scope("Target"):
            self.t = tf.placeholder(tf.float32,shape=[None, self.num_classes], name="Target_output")
            tc = tf.argmax(self.t,1,name="Target_classes")
        with tf.name_scope("FC_net"):
            flowing_x = self.x
            self.W = list()
            self.b = list()
            ls = self.layer_sizes
            for i in range(len(ls)-1):
                with tf.name_scope("layer_{}".format(i)):
                    W = tf.get_variable(shape=[ls[i], ls[i+1]], name="Weights_{}".format(i), initializer=tf.contrib.layers.xavier_initializer())
                    b = tf.get_variable(shape= [ ls[i+1]], name="Biases_{}".format(i), initializer=tf.contrib.layers.xavier_initializer())
                    self.W.append(W)
                    self.b.append(b)
                    flowing_x = self.activation_function(tf.nn.xw_plus_b(flowing_x, W, b))

            y = flowing_x

            with tf.name_scope("Output"):
                self.out = tf.nn.softmax(y)
            with tf.name_scope("Loss"):
                if self.cross_entropy:
                    if self.class_weights is not None:
                        class_weights = tf.constant(tf.cast(self.class_weights, dtype=tf.float32))
                        logits = tf.multiply(y, class_weights)
                    else:
                        logits = y
                    self.loss = tf.reduce_mean(
                        tf.losses.softmax_cross_entropy(logits=logits, onehot_labels=self.t))
                else:
                    self.loss = tf.reduce_mean(
                        tf.nn.l2_loss(self.out-self.t))
            with tf.name_scope("Accuracy"):
                hits_list = tf.cast(tf.equal(tf.argmax(y, 1), tc), tf.float32)
                self.hits = tf.reduce_sum(hits_list)
                self.count = tf.cast(tf.size(hits_list), tf.float32)
        
    def get_loss(self):
        return self.loss

    def get_out(self):
        return self.out
    
    def get_hits(self):
        return self.hits

    def get_count(self):
        return self.count

    def get_train_summaries(self):
        return []

    def get_dev_summaries(self):
        return []

    def get_placeholders(self):
        return self.x, self.t

    def name(self):
        return "FC_net_{}".format("-".join([str(ls) for ls in self.layer_sizes]))

    def train_ended(self, session):
        self.trained_W = session.run(self.W)
        self.trained_b = session.run(self.b)


class TextCNN(Model):
    """
    Convolutional neural network for the text classification.
    Layers are stacked as follows:
        embedding layer
        convolutional layer with defined filter (ReLu activaiton)
        max-pooling over all previous
        any number of FC layer defined by layer_sizes
    The size of the input text can be variable
    """
    def __init__(self,
                 embedding,
                 filter_shape,
                 fc_layer_sizes,
                 activation_function=tf.nn.sigmoid,
                 class_weights=None):
        """
        Constructor
        :param embedding: a list of word embeddings
        :param filter_shape: a shape of the filter
        :param fc_layer_sizes: a list of layer sizes after the convolutional layer
        :param activation_function: tf operator used as activaiton function for fully connected layers
        :param class_weights: weights of the classes if is defined the model balance the gradient contribution of each class
        :return: class instance
        """
        self.embedding = embedding
        self.filter_shape = filter_shape
        self.num_classes = fc_layer_sizes[-1]
        self.layer_sizes = fc_layer_sizes
        self.activation_function = activation_function
        self.class_weights = class_weights

    def build(self):
        with tf.name_scope("Input"):
            self.tf_emb = tf.constant(self.embedding, name="Embedding", dtype=tf.float32)
            self.x = tf.placeholder(tf.int32, shape=[None, None], name="Index_input")
        with tf.name_scope("Target"):
            self.t = tf.placeholder(tf.float32, shape=[None, self.num_classes], name="Target_output")
            tc = tf.argmax(self.t, 1, name="Target_classes")
        with tf.name_scope("CNN_for_text"):
            f = tf.get_variable(shape=self.filter_shape, name="Filter", initializer=tf.contrib.layers.xavier_initializer())
            flowing_x = tf.nn.embedding_lookup(self.tf_emb, self.x, name="Embedding_layer")
            flowing_x = tf.nn.conv1d(flowing_x, f, 1, "SAME", name="Conv_layer")
            flowing_x = tf.nn.relu(flowing_x)
            flowing_x = tf.reduce_max(flowing_x, axis=1)
            self.W = list()
            self.b = list()
            self.W.append(f)
            ls = self.layer_sizes
            for i in range(len(ls) - 1):
                with tf.name_scope("layer_{}".format(i)):
                    W = tf.get_variable(shape=[ls[i], ls[i + 1]], name="Weights_{}".format(i),
                                        initializer=tf.contrib.layers.xavier_initializer())
                    b = tf.get_variable(shape=[ls[i + 1]], name="Biases_{}".format(i),
                                        initializer=tf.contrib.layers.xavier_initializer())
                    self.W.append(W)
                    self.b.append(b)
                    flowing_x = self.activation_function(tf.nn.xw_plus_b(flowing_x, W, b))
            y = flowing_x

            with tf.name_scope("Output"):
                self.out = tf.nn.softmax(y)
            with tf.name_scope("Loss"):
                if self.class_weights is not None:
                    class_weights = tf.constant(tf.cast(self.class_weights, dtype=tf.float32))
                    logits = tf.multiply(y, class_weights)
                else:
                    logits = y
                self.loss = tf.reduce_mean(
                    tf.losses.softmax_cross_entropy(logits=logits, onehot_labels=self.t))
            with tf.name_scope("Accuracy"):
                hits_list = tf.cast(tf.equal(tf.argmax(y, 1), tc), tf.float32)
                self.hits = tf.reduce_sum(hits_list)
                self.count = tf.cast(tf.size(hits_list), tf.float32)

    def get_loss(self):
        return self.loss

    def get_out(self):
        return self.out

    def get_hits(self):
        return self.hits

    def get_count(self):
        return self.count

    def get_train_summaries(self):
        return []

    def get_dev_summaries(self):
        return []

    def get_placeholders(self):
        return self.x, self.t

    def name(self):
        return "FC_net_{}".format("-".join([str(ls) for ls in self.layer_sizes]))

    def train_ended(self, session):
        self.trained_W = session.run(self.W)
        self.trained_b = session.run(self.b)

