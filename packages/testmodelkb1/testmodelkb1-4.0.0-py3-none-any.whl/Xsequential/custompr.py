
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 14:31:05 2019

@author: Siri
"""
import pickle

from keras.models import Sequential
import numpy as np
from keras.preprocessing import image
from keras.utils import plot_model
import matplotlib.pyplot as plt
from keras.models import load_model
from keras import backend as K
import time
import os
import json


class Xsequential(Sequential):
    metadata = {}

    def get_projectname(self):
        return self.__project_name

    def set_projectname(self, project_name):
        self.__project_name = project_name

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
        plt.show()

        # Plot training & validation loss values
        plt.plot(history.history['loss'])
        # plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train'], loc='upper left')
        plt.savefig(folder_name + '/' + project_name + '/' + project_name + '_loss.png')
        plt.show()

        # For localImages prediction

    def xpredict(modelPath, classesPath, imagePath, project_name):
        K.clear_session()
        model = load_model(modelPath)
        if(project_name == "CNN"):
            import numpy as np
            from keras.preprocessing import image
            test_image = image.load_img(imagePath, target_size=(64, 64))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            result = model.predict(test_image)
            if result[0][0] == 1:
                prediction = 'dog'
            else:
                prediction = 'cat'

        if(project_name == "FashionMnist"):


            return prediction



    def xfit_generator(self, generator,
                       steps_per_epoch=None,
                       epochs=1,
                       verbose=1,
                       callbacks=None,
                       validation_data=None,
                       validation_steps=None,
                       class_weight=None,
                       max_queue_size=10,
                       workers=1,
                       use_multiprocessing=False,
                       shuffle=True,
                       initial_epoch=0):
        history = self.fit_generator(generator,
                                     steps_per_epoch=steps_per_epoch,
                                     epochs=epochs,
                                     verbose=verbose,
                                     callbacks=callbacks,
                                     validation_data=validation_data,
                                     validation_steps=validation_steps,
                                     class_weight=class_weight,
                                     max_queue_size=max_queue_size,
                                     workers=workers,
                                     use_multiprocessing=use_multiprocessing,
                                     shuffle=shuffle,
                                     initial_epoch=initial_epoch)

        Xsequential.set_projectname(Xsequential, 'siri')

        project_name = Xsequential.get_projectname(Xsequential)

        folder_name = Xsequential.get_projectname(Xsequential)

        try:
            os.makedirs(project_name)
        except OSError:
            print("Creation of the directory %s failed" % folder_name)
        else:
            print("Successfully created the directory %s" % folder_name)

        project_name += time.strftime("%m%d%y-%H%M%S")

        try:
            os.makedirs(folder_name + '/' + project_name)
        except OSError:
            print("Creation of the directory %s failed" % folder_name)
        else:
            print("Successfully created the directory %s" % folder_name)

        # model saving.
        self.save(folder_name + '/' + project_name + '/' + project_name + '_model.h5')

        # size of the model.
        statinfo = os.stat(folder_name + '/' + project_name + '/' + project_name + '_model.h5')
        size = statinfo.st_size

        # loading model.
        model = load_model(folder_name + '/' + project_name + '/' + project_name + '_model.h5')

        # converting model in json format
        model_json = model.to_json()
        version = json.loads(model_json)

        # model architecture.
        plot_model(model, folder_name + '/' + project_name + '/' + project_name + '_architecture.png')

        # framework
        framework = str(model.__class__)
        index = framework.find('keras')

        # storing class-indices
        Xsequential.generator = generator
        Xsequential.input_shape = ()
        Xsequential.input_shape = model.input_shape[1:]

        # metadata.
        historyLen = len(history.history['acc']) - 1
        Xsequential.metadata['model_name'] = project_name
        if index != -1:
            Xsequential.metadata['framework'] = framework[index:13] + ' ' + version['keras_version']
        Xsequential.metadata['size'] = str(size / 1000) + ' kilobytes'
        Xsequential.metadata['epochs'] = epochs
        model_metadata = Xsequential.extract_model_metadata(self, Xsequential.metadata)
        Xsequential.metadata['AccuracyValue'] = round((history.history['acc'][historyLen]), 3)
        Xsequential.metadata['LossValue'] = round((history.history['loss'][historyLen]), 3)
        model_metadata = Xsequential.metadata

        # plotting graph of loss and accuracy.
        Xsequential.visualize_model_metadata(Xsequential, folder_name, project_name, history)

        # saving metadata in a text file.
        with open(folder_name + '/' + project_name + '/' + project_name + '_metadata.txt', 'w') as f:
            for key, value in model_metadata.items():
                f.write('%s:%s\n' % (key, value))

        return history

        # fit function

    def xfit(self,
             x=None,
             y=None,
             batch_size=None,
             epochs=1,
             verbose=1,
             callbacks=None,
             validation_split=0.,
             validation_data=None,
             shuffle=True,
             class_weight=None,
             sample_weight=None,
             initial_epoch=0,
             steps_per_epoch=None,
             validation_steps=None,

             **kwargs):

        # Returns history of the model
        history = self.fit(x,
                           y,
                           batch_size=batch_size,
                           epochs=epochs,
                           verbose=verbose,
                           callbacks=callbacks,
                           validation_split=validation_split,
                           validation_data=validation_data,
                           shuffle=shuffle,
                           class_weight=class_weight,
                           sample_weight=sample_weight,
                           initial_epoch=initial_epoch,
                           steps_per_epoch=steps_per_epoch,
                           validation_steps=validation_steps,
                           **kwargs)

        Xsequential.set_projectname(Xsequential, 'siri')

        project_name = Xsequential.get_projectname(Xsequential)

        folder_name = Xsequential.get_projectname(Xsequential)

        try:
            os.makedirs(project_name)
        except OSError:
            print("Creation of the directory %s failed" % folder_name)
        else:
            print("Successfully created the directory %s" % folder_name)

        project_name += '_'
        project_name += time.strftime("%m%d%y-%H%M%S")

        try:
            os.makedirs(folder_name + '/' + project_name)
        except OSError:
            print("Creation of the directory %s failed" % folder_name)
        else:
            print("Successfully created the directory %s" % folder_name)

        # model saving.
        self.save(folder_name + '/' + project_name + '/' + project_name + '_model.h5')

        # size of the model.
        statinfo = os.stat(folder_name + '/' + project_name + '/' + project_name + '_model.h5')
        size = statinfo.st_size

        # loading model.
        model = load_model(folder_name + '/' + project_name + '/' + project_name + '_model.h5')

        # converting model in json format
        model_json = model.to_json()
        version = json.loads(model_json)

        # model architecture.
        plot_model(model, folder_name + '/' + project_name + '/' + project_name + '_architecture.png')

        # framework
        framework = str(model.__class__)
        index = framework.find('keras')

        # input_shape
        Xsequential.input_shape = ()
        Xsequential.input_shape = model.input_shape[1:]

        # metadata.
        historyLen = len(history.history['acc']) - 1
        Xsequential.metadata['model_name'] = project_name
        if index != -1:
            Xsequential.metadata['framework'] = framework[index:13] + ' ' + version["keras_version"]
        Xsequential.metadata['size'] = str(size / 1000) + ' kilobytes'
        Xsequential.metadata['epochs'] = epochs
        model_metadata = Xsequential.extract_model_metadata(self, Xsequential.metadata)
        Xsequential.metadata['AccuracyValue'] = round((history.history['acc'][historyLen]), 3)
        Xsequential.metadata['LossValue'] = round((history.history['loss'][historyLen]), 3)
        model_metadata = Xsequential.metadata

        # plotting graph of loss and accuracy.
        Xsequential.visualize_model_metadata(Xsequential, folder_name, project_name, history)

        # saving metadata in a text file.
        with open(folder_name + '/' + project_name + '/' + project_name + '_metadata.txt', 'w') as f:
            for key, value in model_metadata.items():
                f.write('%s:%s\n' % (key, value))

        return history

    Sequential.xfit_generator = xfit_generator
    Sequential.xfit = xfit
    Sequential.xpredict = xpredict