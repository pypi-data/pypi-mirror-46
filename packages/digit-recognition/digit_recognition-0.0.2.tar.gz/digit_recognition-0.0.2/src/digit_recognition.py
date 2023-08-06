import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageDraw, ImageOps

from nn_functions import NeuralNetwork


class Gui:
    
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
        self.weights = np.load('my_network.npy').tolist()
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

if __name__ == "__main__":
    """ Runs gui (defined above) in infinite loop. """

    root = tk.Tk()
    a = Gui(root)
    root.mainloop()