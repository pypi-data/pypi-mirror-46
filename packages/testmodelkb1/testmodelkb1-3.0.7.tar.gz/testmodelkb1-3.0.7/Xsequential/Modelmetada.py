# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:31:18 2019

@author: Siri
"""
from keras.utils import plot_model
import matplotlib.pyplot as plt
import matplotlib.pyplot as plot
import itertools
import numpy as np


class Modelmetadata():

    def plot_classification_report(cr, title='Classification report ', with_avg_total=False, cmap=plot.cm.Blues):

        lines = cr.split('\n')
        lines = list(filter(None, lines))
        classes = []
        plotMat = []
        for line in lines[2: (len(lines) - 3)]:
            # print(line)
            t = line.split()
            # print(t)
            classes.append(t[0])
            v = [float(x) for x in t[1: len(t) - 1]]
            # print(v)
            plotMat.append(v)

        if with_avg_total:
            aveTotal = lines[len(lines) - 1].split()
            classes.append('avg/total')
            vAveTotal = [float(x) for x in t[1:len(aveTotal) - 1]]
            plotMat.append(vAveTotal)

        plot.imshow(plotMat, interpolation='nearest', cmap=cmap)
        plot.title(title)
        plot.colorbar()
        x_tick_marks = np.arange(3)
        y_tick_marks = np.arange(len(classes))
        plot.xticks(x_tick_marks, ['precision', 'recall', 'f1-score'], rotation=45)
        plot.yticks(y_tick_marks, classes)
        plot.tight_layout()
        plot.ylabel('Classes')
        plot.xlabel('Measures')

        # To plot the confusion matrix

    def plot_confusion_matrix(cm, classes,
                              normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues):
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            # print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        # print(cm)

        plt.figure(figsize=(7, 7))
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     fontsize=10,
                     color="white" if cm[i, j] > thresh else "black")

        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()

    # For extracting the model_metadata
    def extract_model_metadata(self, model_metadata):

        if (self):
            model_metadata['layersCount'] = len(self.layers)
            model_metadata['InputTensors'] = self.input_shape
            model_metadata['OutputTensor'] = self.output_shape
            model_metadata['Optimizer'] = self.optimizer.__class__.__name__
            model_metadata['LossFunction'] = self.loss

            return model_metadata

    # Visualization of metadata
    def visualize_model_metadata(self, folder_name, project_name, history):

        # Plot training & validation accuracy values
        plt.plot(history.history['acc'])
        # plt.plot(history.history['val_acc'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train'], loc='upper left')
        plt.savefig(folder_name + '/' + project_name + '/' + project_name + '_accuracy.png')

        # Plot training & validation loss values
        plt.plot(history.history['loss'])
        # plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train'], loc='upper left')
        plt.savefig(folder_name + '/' + project_name + '/' + project_name + '_loss.png')

    # Saving the model
    def save_model(self, folder_name, project_name):
        self.save(folder_name + '/' + project_name + '/' + project_name + '_model.h5')

    # Plotting model architecture
    def plot_model(model, folder_name, project_name):
        plot_model(model, folder_name + '/' + project_name + '/' + project_name + '_architecture.png')



