import numpy as np
import os
import urllib.request
import gzip
import subprocess
import sys
import tkinter as tk
from PIL import Image, ImageDraw, ImageOps

try:
    import idx2numpy
except ImportError:
    print('installing idx2numpy...')
    subprocess.call([sys.executable, "-m", "pip", "install", 'idx2numpy'])

class NeuralNetwork:
    """ Defines functions necessary to install neural network. """

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

def install_network(design=[784,200,100,10], bias=True, epochs=3, file_name='my_network'):
    """ Sets up neural network by running the functions defined above. 
    
    Design, bias, and number of epochs are given but can be changed.
    """

    # Import data
    train_images, train_labels, test_images, test_labels = pre_processing()

    # Build neural network (with two hidden layers of 200/100 nodes respectively)
    neural_network = NeuralNetwork(design, bias=bias)
    neural_network.train(train_images, train_labels, epochs=epochs)
    neural_network.evaluate(test_images, test_labels)

    # Export neural network
    os.chdir('DR_Data')
    neural_network.save(file_name)
    os.chdir('..')


class Gui:
    """ Defines functions necessary for GUI. """
    
    def __init__(self, master):
        """ Set up layout and basic functionality of interface.

        Creates window with input and feedback frame. The input frame contains
        two drawing applications: One from tkinter that is used to display the 
        number that is drawn in the interface and one from PIL that is passed 
        to the neural network. The feedback frame contains three fields that 
        display various outputs of the neural network.

        Args:
            master: Window where the interface is created.

        """
        
        # Build neural network
        os.chdir('DR_Data')
        self.weights = np.load('my_network.npy').tolist()
        os.chdir('..')
        self.neural_network = NeuralNetwork(
            [784,200,100,10], 
            weights=self.weights, 
            bias=True,
            )
        
        # Layout and frames
        self.master = master
        self.master.title('Digit Recognition')
        self.master.geometry('450x330')
        border_color='white' # Not visible, just for development purposes
        input_frame = tk.Frame(master, 
            highlightbackground=border_color, highlightthickness=2)
        input_frame.grid(row=2, column=0)
        feedback_frame = tk.Frame(master, 
            highlightbackground=border_color, highlightthickness=2)
        feedback_frame.grid(row=2, column=2)
        
        # Empty frames/labels for layout
        empty_frame_1 = tk.Frame(master, 
            highlightbackground=border_color, highlightthickness=2)
        empty_frame_1.grid(row=2, column=1)
        empty_label_1 = tk.Label(empty_frame_1, 
            text=' ', font=("Helvetica", 30))
        empty_label_1.pack()
        
        # Buttons
        self.button_reset = tk.Button(input_frame, 
            text='Reset', width=10, command=self.reset)
        self.button_reset.pack(side=tk.BOTTOM)
        self.button_recognize = tk.Button(input_frame, 
            text='Recognize!', width=10, command=self.run_nn)
        self.button_recognize.pack(side=tk.BOTTOM)

        # Drawing field
        heading_1 = tk.Label(input_frame, 
            text='Write your digit!', font=("Helvetica", 15))
        heading_1.pack(side=tk.TOP)
        self.drawing_field = tk.Canvas(input_frame, 
            height=250, width=250, cursor='cross', 
            highlightbackground="black", highlightthickness=2)
        self.drawing_field.pack() 
        self.drawing_field.bind("<Motion>", self.previous_position)
        self.drawing_field.bind("<B1-Motion>", self.draw)

        # Indication where to draw the digit
        self.drawing_field.create_rectangle(70,40, 180,210, 
            fill='light grey', outline='light grey')
        
        # Feedback field
        heading_2 = tk.Label(feedback_frame, 
            text='Recognized as...', font=("Helvetica", 15))
        heading_2.pack(side=tk.TOP)
        self.prediction_field = tk.Text(feedback_frame, 
            height=1, width=1, font=("Helvetica", 50), bg='light grey', 
            state='disabled')
        self.prediction_field.pack(side=tk.TOP)
        
        heading_3 = tk.Label(feedback_frame, 
            text='Confidence...', font=("Helvetica", 15))
        heading_3.pack(side=tk.TOP)
        self.confidence_field = tk.Text(feedback_frame, 
            height=1, width=5, font=("Helvetica", 50), bg='light grey',
            state='disabled')
        self.confidence_field.pack(side=tk.TOP)
        
        heading_4 = tk.Label(feedback_frame, 
            text='Alternative...', font=("Helvetica", 15))
        heading_4.pack(side=tk.TOP)
        self.alternative_field = tk.Text(feedback_frame, 
            height=1, width=1, font=("Helvetica", 50), bg='light grey',
            state='disabled')
        self.alternative_field.pack(side=tk.TOP)
        
        # PIL drawing field
        self.PIL_drawing = Image.new("RGB",(250,250),(255,255,255))
        self.PIL_draw = ImageDraw.Draw(self.PIL_drawing)

    def previous_position(self, event):
        """ Saves last position of the mouse. 

        (no matter if mouse button has been pressed or not) 

        Args:
            event: Mouse input
        
        """

        self.previous_x = event.x
        self.previous_y = event.y

    def draw(self, event):
        """ Draws line when mouse button 1 is pressed.

        Connects previous mouse position to current mouse position in both
        the tkinter image and the PIL image.

        Args:
            event: Mouse input

        """

        # Get current position
        self.x = event.x
        self.y = event.y

        # Connect previous and current position
        self.drawing_field.create_polygon(self.previous_x, self.previous_y, 
            self.x, self.y, 
            width=20, outline='black')
        self.PIL_draw.line(((self.previous_x, self.previous_y),
            (self.x, self.y)),
            (1,1,1), width=20)

        # Save as previous position
        self.previous_x = self.x
        self.previous_y = self.y

    def run_nn(self):
        """ Feeds image to neural network and retreives output. """

        # Convert PIL image to appropriate matrix representation
        img_inverted = ImageOps.invert(self.PIL_drawing)
        img_resized = img_inverted.resize((28,28), Image.ANTIALIAS)
        self.input_image = np.asarray(img_resized)[:,:,0] * (0.99/255) + 0.01

        if self.input_image.sum() > 0.01*784: # drawing not empty
            # Forward propagation of neural network
            output = self.neural_network.run(self.input_image).T[0]
            linear_output = np.log(output/(1-output))
            softmax_output = np.exp(linear_output) / np.sum(np.exp(linear_output), axis=0)

            # Extract output from neural network
            self.prediction = np.argmax(output)
            self.confidence = np.max(softmax_output)
            self.alternative = np.argsort(output)[-2]

            # Display output
            self.prediction_field.configure(state='normal')
            self.prediction_field.insert(tk.END, str(self.prediction))
            self.prediction_field.configure(state='disabled') # don't allow input
            self.confidence_field.configure(state='normal')
            self.confidence_field.insert(tk.END, '%.0f%%' %(self.confidence*100))
            self.confidence_field.configure(state='disabled')
            self.alternative_field.configure(state='normal')
            if self.confidence < 0.8:
                self.alternative_field.insert(tk.END, str(self.alternative))
            else:
                self.alternative_field.insert(tk.END, '/')
            self.alternative_field.configure(state='disabled')
        
    def reset(self):
        """ Empties drawing and feedback fields. """

        # Reset tkinter
        self.prediction_field.configure(state='normal')
        self.confidence_field.configure(state='normal')
        self.alternative_field.configure(state='normal')
        self.prediction_field.delete(1.0,tk.END)
        self.confidence_field.delete(1.0,tk.END)
        self.alternative_field.delete(1.0,tk.END)
        self.prediction_field.configure(state='disabled')
        self.confidence_field.configure(state='disabled')
        self.alternative_field.configure(state='disabled')
        self.drawing_field.delete('all')
        self.drawing_field.create_rectangle(70,40, 180,210, 
            fill='light grey', outline='light grey')

        # Reset PIL
        self.PIL_drawing=Image.new("RGB",(250,250),(255,255,255))
        self.PIL_draw=ImageDraw.Draw(self.PIL_drawing)

def digit_recognition():
    """ Runs gui (defined above) in infinite loop. """

    root = tk.Tk()
    a = Gui(root)
    root.mainloop()