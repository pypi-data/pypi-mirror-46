
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 14:31:05 2019

@author: Siri
"""

from keras.models import Sequential
import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.metrics import confusion_matrix
import pickle
import time
import os
import json
from sklearn.metrics import classification_report
from Xsequential.Modelmetada import Modelmetadata
from Xsequential import app


class Xsequential(Sequential):

    metadata = {}
    #setters and getters for user_name
    def get_user_name(self):
        return self.user_name

    def set_user_name(self, user_name):
        self.user_name = user_name

    #setters and getters for project_name
    def get_project_name(self):
        return self.project_name

    def set_project_name(self, project_name):
        self.project_name = project_name

    #setters and getters for dataset link
    def get_dataset_link(self):
        return self.dataset_link

    def set_dataset_link(self, dataset_link):
        self.dateset_link = dataset_link

    #setters and getters for projectlink
    def get_sourcecode_link(self):
        return self.sourcecode_link

    def set_sourcecode_link(self, sourcecode_link):
        self.sourcecode_link = sourcecode_link

    #for defining the project_details
    def start_experiment(self, user_name, project_name, dataset_link, sourcecode_link):
        Xsequential.set_user_name(self,user_name)
        Xsequential.set_project_name(self,project_name)
        Xsequential.set_dataset_link(self,dataset_link)
        Xsequential.set_sourcecode_link(self,sourcecode_link)

    # For models using fit_generator
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

        project_name = Xsequential.get_project_name(self) + '_'

        folder_name = os.path.dirname(os.path.abspath(__file__)) + '/' + 'rawdata'

        try:
            os.makedirs(folder_name)
        except OSError:
            """print ("Creation of the directory %s failed" % folder_name)"""
        else:
            """print ("Successfully created the directory %s" % folder_name)"""

        project_name += time.strftime("%m%d%y-%H%M%S")

        try:
            os.makedirs(folder_name + '/' + project_name)
            os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '/' + 'testdata')
        except OSError:
            """print ("Creation of the directory %s failed" % folder_name)"""
        else:
            """print ("Successfully created the directory %s" % folder_name)"""

        try:
            os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '/' + 'testdata' + '/' + Xsequential.get_project_name(self))
        except OSError:
            """print ("Creation of the directory %s failed" % folder_name)"""
        else:
            """print ("Successfully created the directory %s" % folder_name)"""

        # model saving.
        Modelmetadata.save_model(self, folder_name, project_name)

        # size of the model.
        statinfo = os.stat(folder_name + '/' + project_name + '/' + project_name + '_model.h5')
        size = statinfo.st_size

        # loading model.
        model = load_model(folder_name + '/' + project_name + '/' + project_name + '_model.h5')

        # converting model in json format
        model_json = model.to_json()
        version = json.loads(model_json)

        # model architecture.
        # Modelmetadata.plot_model(model, folder_name, project_name)

        # framework
        framework = str(model.__class__)
        index = framework.find('keras')

        # storing class-indices
        Xsequential.generator = generator
        Xsequential.input_shape = ()
        Xsequential.input_shape = model.input_shape[1:]

        # metadata.
        historyLen = len(history.history['acc']) - 1
        Xsequential.metadata['owner'] = Xsequential.get_user_name(self)
        Xsequential.metadata['model_name'] = project_name
        if index != -1:
            Xsequential.metadata['framework'] = framework[index:13] + ' ' + version['keras_version']
        Xsequential.metadata['size'] = str(size / 1000) + ' kilobytes'
        Xsequential.metadata['epochs'] = epochs
        model_metadata = Modelmetadata.extract_model_metadata(self, Xsequential.metadata)
        Xsequential.metadata['AccuracyValue'] = round((history.history['acc'][historyLen]), 3)
        Xsequential.metadata['LossValue'] = round((history.history['loss'][historyLen]), 3)
        model_metadata = Xsequential.metadata

        # plotting graph of loss and accuracy.
        Modelmetadata.visualize_model_metadata(Xsequential, folder_name, project_name, history)

        # confusion matrix
        class_names = ["cat", "dog"]
        predicted_values = model.predict_generator(generator)
        confusionmatrix = confusion_matrix(generator.classes, predicted_values.round())
        Modelmetadata.plot_confusion_matrix(confusionmatrix, classes=class_names,
                                            title='Confusion matrix')
        plt.savefig(folder_name + '/' + project_name + '/' + project_name + '_confusion_matrix.png')

        # save classes metadata
        classes_dict = Xsequential.generator.class_indices

        pickle_out = open(folder_name + '/' + project_name + '/' + project_name + "_classes.pickle", "wb")
        pickle.dump(classes_dict, pickle_out)
        pickle_out.close()

        # saving metadata in a text file.
        with open(folder_name + '/' + project_name + '/' + project_name + '_metadata.txt', 'w') as f:
            for key, value in model_metadata.items():
                f.write('%s:%s\n' % (key, value))

        app.activate()
        return history

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

        # Opened File
        file = open('temp.py', 'w')

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

        project_name = Xsequential.get_project_name(self) + '_'

        print(os.path.dirname(os.path.abspath(__file__)))
        folder_name = os.path.dirname(os.path.abspath(__file__)) + '/' + 'rawdata'

        try:
            os.makedirs(folder_name)
        except OSError:
            """print ("Creation of the directory %s failed" % folder_name)"""
        else:
            """ print ("Successfully created the directory %s" % folder_name)"""

        project_name += time.strftime("%m%d%y-%H%M%S")

        try:
            os.makedirs(folder_name + '/' + project_name)
            os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '/' + 'testdata')

        except OSError:
            """print ("Creation of the directory %s failed" % folder_name)"""
        else:
            """print ("Successfully created the directory %s" % folder_name)"""

        try:
            os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '/' + 'testdata' + '/' + Xsequential.get_project_name(self))
        except OSError:
            """print ("Creation of the directory %s failed" % folder_name)"""
        else:
            """print ("Successfully created the directory %s" % folder_name)"""

        # model saving.
        Modelmetadata.save_model(self, folder_name, project_name)

        # size of the model.
        statinfo = os.stat(folder_name + '/' + project_name + '/' + project_name + '_model.h5')
        size = statinfo.st_size

        # loading model.
        model = load_model(folder_name + '/' + project_name + '/' + project_name + '_model.h5')

        # converting model in json format
        model_json = model.to_json()
        version = json.loads(model_json)

        # model architecture.
        # Modelmetadata.plot_model(model, folder_name, project_name)

        # framework
        framework = str(model.__class__)
        index = framework.find('keras')

        # input_shape
        Xsequential.input_shape = ()
        Xsequential.input_shape = model.input_shape[1:]

        # metadata.
        historyLen = len(history.history['acc']) - 1
        Xsequential.metadata['owner'] = Xsequential.get_user_name(self)
        Xsequential.metadata['model_name'] = project_name
        if index != -1:
            Xsequential.metadata['framework'] = framework[index:13] + ' ' + version["keras_version"]
        Xsequential.metadata['size'] = str(size / 1000) + ' kilobytes'
        Xsequential.metadata['epochs'] = epochs
        model_metadata = Modelmetadata.extract_model_metadata(self, Xsequential.metadata)
        Xsequential.metadata['AccuracyValue'] = round((history.history['acc'][historyLen]), 3)
        Xsequential.metadata['LossValue'] = round((history.history['loss'][historyLen]), 3)
        model_metadata = Xsequential.metadata

        # plotting graph of loss and accuracy.
        Modelmetadata.visualize_model_metadata(Xsequential, folder_name, project_name, history)

        class_names = ['0','1']

        # confusion matrix
        y_pred = model.predict_classes(x)
        confusionmatrix = confusion_matrix(y, y_pred)
        Modelmetadata.plot_confusion_matrix(confusionmatrix, classes=class_names,
                                            title='Confusion matrix')
        plt.savefig(folder_name + '/' + project_name + '/' + project_name + '_confusion_matrix.png')

        # Recall & Precision
        # print(classification_report(y, y_pred, target_names=class_names))
        # classificationreport = classification_report(y, y_pred, target_names=class_names)
        # Modelmetadata.plot_classification_report(classificationreport)

        # saving metadata in a text file.
        with open(folder_name + '/' + project_name + '/' + project_name + '_metadata.txt', 'a') as file:
            for key, value in model_metadata.items():
                print(value)
                file.write('%s:%s\n' % (key, value))
            file.close()

        app.activate()
        return history



    # Setting properties to Sequential so that data scientist can call xfit instead of fit.
    Sequential.xfit_generator = xfit_generator
    Sequential.xfit = xfit
    Sequential.start_experiment = start_experiment
