import torch.nn as nn, numpy as np, matplotlib.pyplot as plt
import torch
from .initializers import initializers_dict


loss_dict = {'mse':nn.MSELoss()}

##### functions to implement
# fit, predict, compile (necessary?), save_weights, load_weights

class Sequential():
    """
    Sequential model class.
    """

    def __init__(self):
        """
        init function
        """
        self.model = nn.Sequential()
        self.last_layers_units = 0
        self.layer_iter = 0
        self.is_compiled = False

    def add(self,layer, input_shape = None, layer_name  = None):
        "adds a layer to the model"

        # if first layer, define input shape
        if self.layer_iter == 0:

            if input_shape == None:
                # ValueError should not be used
                raise ValueError("Please Specify Input shape for first layer!")

            else:
                self.last_layers_units = input_shape[0]


        # if name not specifed, specify your own name which is the iteration number of layer
        if layer_name == None:
            layer_name = str(self.layer_iter)

        # extract activation and layer params
        layer_type, current_layer_param, activation = layer[0], layer[1]

        # currently only for Dense and Dropout!!!!
        if layer_type == 'Dense':
            nn_layer = nn.Linear(self.last_layers_units, current_layer_param)
            self.last_layers_units = current_layer_param
        elif layer_type =='Dropout':
            nn_layer = nn.Dropout(current_layer_param)

        self.model.add_module(layer_name,nn_layer)

        # if activation is None, it will be treated as linear activation and no module will be added for activation!
        if activation != None:
            self.model.add_module(layer_name+'_activation',activation)

        # updating
        self.layer_iter = self.layer_iter + 1


    def compile(self,loss,optimizer):
        """
        compiles the model with given loss function and optimizer
        :param loss: given loss function (str)
        :param optimizer: given optimizer (k_torch.optimizers)
        :return:
        """
        self.optimizer = optimizer[0](self.model.parameters(),lr = optimizer[1],weight_decay = optimizer[2])
        self.loss = loss_dict[loss]
        self.is_compiled = True

    def fit(self,X_train,y_train,epochs,verbose = False,validation_data = None, should_plot_history = False):
        """
        trains the model based on given data. Will show progress based on given parameters

        :param X_train:
        :param y_train:
        :param nb_epochs:
        :param verbose:
        :param validation_data:
        :param should_plot_history:
        :return:
        """

        if self.is_compiled == False:
            raise ValueError("Model is not compiled! Please compile first") # change this value error

        # converting X_train and y_train to np.float64 dtype
        X_train = X_train.astype(np.float64)
        y_train = y_train.astype(np.float64)

        # converting to Tensors
        X_train, y_train = map(torch.Tensor,[X_train,y_train])

        criterion = self.loss

        if validation_data != None:
            X_test = validation_data[0]
            y_test = validation_data[0]
            X_test, y_test = map(torch.Tensor, [X_test, y_test])

        training_losses, val_losses = [], []

        # training
        for epoch in range(epochs):
            # Forward Propagation for training loss
            y_pred = self.model(X_train)

            train_loss = criterion(y_pred, y_train)
            training_losses.append(train_loss)

            if validation_data != None:
                y_val = self.model(X_test)  # for validation
                val_loss = criterion(y_val, y_test)
                val_losses.append(val_loss)

            # print verbose if selected
            if verbose:
                if validation_data == None:
                    print('epoch: ', epoch, 'train_loss: ', train_loss.item())
                else:
                    print('epoch: ', epoch, 'train_loss: ', train_loss.item(), 'val_loss: ', val_loss.item())

            # Zero the gradients
            self.optimizer.zero_grad()

            # perform a backward pass (backpropagation)
            train_loss.backward()

            # Update the parameters
            self.optimizer.step()

        if should_plot_history:
            plt.plot(training_losses, label='training_loss')
            if validation_data!=None:
                plt.plot(val_losses, label='validation_loss')
            plt.ylabel('loss')
            plt.xlabel('number of epochs')
            plt.title('Loss History Visualization')
            plt.legend()
            plt.show()


    def predict(self,X_test):
        """
        makes predictions
        :param X_test:
        :return:
        """

        X_test = torch.Tensor(X_test)
        predictions = self.model(X_test).detach().numpy()

        return predictions

    def save_weights(self,path):
        """
        saves weights to a .dat file
        """
        torch.save(self.model.state_dict(), path)

    def load_weights(self,path):
        """
        loads weights from a .dat file
        """
        self.model.load_state_dict(torch.load(path))

    def initialize_weights(self, initialization = 'xavier'):
        """
        initializes weights with the given initialization
        """
        self.model.apply(initializers_dict[initialization])