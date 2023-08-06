import numpy as np
import os
import urllib.request
import gzip
import subprocess
import sys

try:
    import idx2numpy
except ImportError:
    print('installing idx2numpy...')
    subprocess.call([sys.executable, "-m", "pip", "install", 'idx2numpy'])


class NeuralNetwork:

    def sigmoid(x):
        """ Activation function used in neural network. """
        return 1/(1+np.exp(-x))
    
    def __init__(
            self, design, 
            weights=None, step_size=0.01, 
            activation_function=sigmoid, bias=False):
        """ Set up basic attributes of neural network.

        Args: 
            design (list): List containing the number of nodes in each layer.
                Can have any length (above 1). E.g., [784, 20, 10].
            weights (list): List containing numpy arrays with desired weights.
                Defaults to None. If no weights are specified, random ones 
                are generated.
            step_size (float): Step size used for backpropagation. 
                Defaults to 0.01
            activation_function (string): Specifies activation function of
                neural network. Only a sigmoid function is given, but others,
                e.g., ReLU, could be added.
            bias (boolean): Should bias node be added to neural network?
                Defaults to None.

        """

        self.design = design
        self.weights = weights
        self.step_size = step_size
        self.activation_function = activation_function
        self.bias = bias
        self.activation = []

        # Create random weights
        if self.weights is None:
            self.weights = [np.zeros(0)]
            for i in np.arange(len(self.design) - 1):
                self.weights.append(np.random.uniform(-1, 1, 
                    [self.design[i+1], self.design[i]+self.bias]))

        # Function check    
        if self.weights[1].shape == (self.design[1], self.design[0]+self.bias):
            print('Network created successfully')
        else:
            print('Network creation failed')        
    
    def train(self, input_data, target_data, epochs=1):
        """ Loop for backpropagation function (see below).
        
        Args:
            input_data (array): 3-dimensional numpy array containing
                input data (see pre_processing function for exact format).
            target_data (array): 2-dimensional numpy array containing
                target data in one-hot representation.
            epochs (int): Number of times the training algorithms 
                iterates through the *entire* dataset.
                Defaults to 1.

        """

        print('Training...')
        for epoch in np.arange(epochs):
            print('Epoch: ' + str(epoch + 1) + ' (of ' + str(epochs) + ')')
            for i in np.arange(len(input_data)):
                self.one_training(input_data[i], target_data[i])
        
        # Function check
        if i == len(input_data) - 1:
            print('Data trained successfully')
        else:
            print('Training failed')
    
    def one_training(self, input_data, target_data):
        """ Backpropagation algorithm to train neural network.
        
        Args:
            input_data (array): 2-dimensional numpy array containing
                a single input. Passed by train function (see above).
            target_data (array): 2-dimensional numpy array containing
                a single target. Passed by train function (see above).

        """
        
        # Convert data into coumn vectors
        input_vector = np.array(input_data.flatten(), ndmin=2).T
        if self.bias:
            input_vector = np.array(np.append(1, input_vector), ndmin=2).T
        target_vector = np.array(target_data, ndmin=2).T
        
        # Forward propagation to compute activation
        self.activation = []
        self.activation.append(input_vector)
        for i in np.arange(len(self.design)-1):
            self.activation.append(self.activation_function(
                self.weights[i+1] @ self.activation[i]))
            if self.bias:
                self.activation[i+1] = np.array(
                    np.append(1, self.activation[i+1]), ndmin=2).T
            
        # Compute error
        error = target_vector - self.activation[-1][self.bias:]
        
        # Backpropagation to update weights
        for i in np.arange(len(self.design) - 1, 0, -1):
            gradient = (error * self.activation[i][self.bias:] 
                * (1.0 - self.activation[i][self.bias:])) @ self.activation[i-1].T
            correction = self.step_size * gradient
            self.weights[i] += correction
            error = self.weights[i].T @ error
            error = error[self.bias:]
    
    def run(self, input_data):
        """ Forward propagation algorithm.

        Computes output of neural network for a single input.
        
        Args:
            input_data (array): 2-dimensional numpy array containing
                a single input.

        """
        
        # Convert data into column vector
        input_vector = np.array(input_data.flatten(), ndmin=2).T
        if self.bias:
            input_vector = np.array(np.append(1, input_vector), ndmin=2).T
        
        # Compute layer outputs/activations
        self.activation = []
        self.activation.append(input_vector)
        for i in np.arange(len(self.design)-1):
            self.activation.append(self.activation_function(
                self.weights[i+1] @ self.activation[i]))
            if self.bias and i != len(self.design) - 2:
                self.activation[i+1] = np.array(
                    np.append(1, self.activation[i+1]), ndmin=2).T
        return self.activation[-1]
    
    def evaluate(self, input_data, target_data):
        """ Evaluates performance of neural network.

        Computes accuracy of neural network, as well as recall and precision 
        for each class using a confusion matrix. Results are printed to the
        console, but also defined as attributes of the neural network.

        Note: Use independent test data!
        
        Args:
            input_data (array): 3-dimensional numpy array containing
                test input data.
            target_data (array): 2-dimensional numpy array containing
                test target data in one-hot representation.

        """

        self.confusion_matrix = np.zeros(
            [target_data.shape[-1], target_data.shape[-1]])
        
        # Compute confusion matrix (one data point at a time)
        for i in np.arange(len(input_data)):
            output = self.run(input_data[i])
            true_label = np.array(target_data[i], ndmin=2).T
        
            # Compute result and add to confusion matrix 
            # (true label in rows, prediction in columns)
            confusion_result = true_label @ output.T
            confusion_result[confusion_result == np.max(confusion_result)] = 1
            confusion_result[confusion_result != 1] = 0
            self.confusion_matrix += confusion_result
        
        total_predictions = np.sum(self.confusion_matrix)
        correct_predictions = np.sum(np.diag(self.confusion_matrix))
        false_predictions = total_predictions - correct_predictions
        
        # Accuracy
        self.accuracy = correct_predictions / total_predictions
        
        # Recall (per class)
        self.recall = np.array([])
        for i in np.arange(target_data.shape[-1]):
            self.recall = np.append(
                self.recall, 
                self.confusion_matrix[i,i] / np.sum(self.confusion_matrix[i,:]),
                )
        
        # Precision (per class)
        self.precision = np.array([])
        for i in np.arange(target_data.shape[-1]):
            self.precision = np.append(
                self.precision, 
                self.confusion_matrix[i,i] / np.sum(self.confusion_matrix[:,i]),
                )
        
        # Print accuracy measures
        print('Accuracy: ' + str('%.2f' % (self.accuracy * 100)) + '%')
        for i in np.arange(target_data.shape[-1]):    
            print('Recall for ' + str(i) + ': ' 
                + str('%.2f' % (self.recall[i] * 100)) + '%')
            print('Precision for ' + str(i) + ': ' 
                + str('%.2f' % (self.precision[i] * 100)) + '%')

    def save(self, file_name):
        np.save(file_name + '.npy', np.asarray(self.weights))
        if os.path.isfile(file_name + '.npy'):
            print('Network saved successfully as ' + file_name + '.npy')
        else:
            print('Saving failed')

def pre_processing():
    """ Downloads, imports and preprocess data for digit recognition.

    Data is downloaded from the MNIST database. Consists of 70.000
    handwritten digits of 28x28 pixels. Each with a corresponding,
    manually added label. Data is split into 60.000 instances for 
    training and 10.000 instances for testing.

    Uses the idx2numpy module.

    Returns:
        Matrix representations of digits and correspondings 
        labels in a format optimized for the neural network.

    """

    # Download data (to 'DR_Data' folder)
    downloaded = os.path.exists('DR_Data')

    if not downloaded:

        os.mkdir('DR_Data')
        print('Downloading dataset...')
        url = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
        urllib.request.urlretrieve(url, 'DR_Data/train-images-idx3-ubyte.gz')
        url = 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'  
        urllib.request.urlretrieve(url, 'DR_Data/train-labels-idx1-ubyte.gz')
        url = 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'  
        urllib.request.urlretrieve(url, 'DR_Data/t10k-images-idx3-ubyte.gz')
        url = 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'  
        urllib.request.urlretrieve(url, 'DR_Data/t10k-labels-idx1-ubyte.gz')

        # Check download
        if os.path.isfile('DR_Data/train-images-idx3-ubyte.gz') and os.path.isfile('DR_Data/train-labels-idx1-ubyte.gz') and os.path.isfile('DR_Data/t10k-images-idx3-ubyte.gz') and os.path.isfile('DR_Data/t10k-labels-idx1-ubyte.gz'):
            print('Downloaded data successfully')
        else:
            print('Download failed')
    else:
        print('Data has been downloaded')
    

    # Load data and convert data to numpy arrays
    os.chdir('DR_Data')
    train_images = idx2numpy.convert_from_file(gzip.open('train-images-idx3-ubyte.gz','r'))
    train_labels = idx2numpy.convert_from_file(gzip.open('train-labels-idx1-ubyte.gz','r'))
    test_images = idx2numpy.convert_from_file(gzip.open('t10k-images-idx3-ubyte.gz','r'))
    test_labels = idx2numpy.convert_from_file(gzip.open('t10k-labels-idx1-ubyte.gz','r'))
    os.chdir('..')

    # Re-scale input values from intervals [0,255] to [0.01,1] 
    # (necessary for optimal performance of NN)
    train_images = train_images * (0.99/255) + 0.01
    test_images = test_images * (0.99/255) + 0.01

    # Convert label data to one-hot representation with either 0.01 or 0.99 
    # (also necessary for optimal performance of NN 
    # and to compute confusion matrix)
    train_labels = np.asfarray(train_labels)
    test_labels = np.asfarray(test_labels)
    train_labels = np.array(train_labels, ndmin=2).T
    test_labels = np.array(test_labels, ndmin=2).T
    train_labels = (np.arange(10) == train_labels).astype(np.float)
    test_labels = (np.arange(10) == test_labels).astype(np.float)
    train_labels[train_labels == 1] = 0.99
    test_labels[test_labels == 1] = 0.99
    train_labels[train_labels == 0] = 0.01
    test_labels[test_labels == 0] = 0.01

    # Function check
    if train_images.shape == (60000, 28, 28) and train_labels.shape == (60000, 10):
        print('Data preprocessed successfully')
    else:
        print('Preprocessing failed')
    
    return train_images, train_labels, test_images, test_labels

def install_network():
    # Import data
    train_images, train_labels, test_images, test_labels = pre_processing()

    # Build neural network (with two hidden layers of 200/100 nodes respectively)
    neural_network = NeuralNetwork([784,200,100,10], bias=True)
    neural_network.train(train_images, train_labels, epochs=3)
    neural_network.evaluate(test_images, test_labels)

    # Export neural network
    os.chdir('DR_Data')
    neural_network.save('my_network')
    os.chdir('..')