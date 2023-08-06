from keras.models import load_model

from Xsequential.custompr import Xsequential


def performpredict(modelpath, classpath, inputfilepath):
    results = dict()
    currentresult = {}

    outputclass = Xsequential.xpredict(modelpath, classpath, inputfilepath)
    currentresult.update({'classname': outputclass})
    results["one"] = currentresult
    return results

def performpredictdummy(modelpath, classpath, inputfilepath):

    currentresult = {}

    currentresult.update({'accuracy': "99"})

    outputclass = Xsequential.xpredict(modelpath, classpath, inputfilepath)
    currentresult.update({'classname': "sample"})

    return currentresult