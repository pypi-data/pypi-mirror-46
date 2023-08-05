
import torch.nn as nn

activation_dict = {'relu' : nn.ReLU(), 'linear' : None}

def Dense(no_of_neurons,activation= 'linear'):
    return no_of_neurons, activation_dict[activation]





