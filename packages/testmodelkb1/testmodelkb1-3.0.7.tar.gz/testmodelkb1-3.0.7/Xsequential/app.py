import datetime
import errno
import os, json
import netron

from flask import Flask, render_template, request, send_from_directory, send_file
from werkzeug.utils import secure_filename

from Xsequential.custompredict import performpredict, performpredictdummy

app = Flask(__name__)

data = ''
metadata = dict()
dirs = dict()
IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "\\rawdata"
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "\\testdata"
ALLOWED_EXTENSIONS = set(['h5', 'HDF5', 'pdf', 'doc', 'md', 'docx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
dir_path = os.path.dirname(os.path.abspath(__file__))
def xFit():
    # sample data to be sent to View

    model_name = 'Gharib'
    metadata = {'epochs': 20, 'Hidden Layers': 2}

    #dirs = json.dumps(make_tree(dir_path + "/FashionMnist/"), indent=2, sort_keys=True)
    dirs = make_tree(dir_path + "\\rawdata\\")
    # pass data to FLask
    sendData(model_name, metadata, dirs)

def sendData(x, y, z):
    global data, metadata, dirs
    data = x
    metadata = y
    dirs = z

@app.route('/')
def hello_world():
    x = data
    y = metadata
    z = dirs
    return render_template('home.html', x=x, y=y, z=z)

@app.route('/view')
def viewproject():
    id = request.values.get("project")
    x = data
    y = metadata
    z = {}
    #for proj, projdetails in dir.items():
    z[id] = dirs[id]
    exp = dict()
    dir_path = os.path.dirname(os.path.abspath(__file__)) + "\\testdata\\" + id + '\\'
    try: lst = os.listdir(dir_path)
    except OSError:
        return render_template('viewproject.html', x=x, y=y, z=z, t=exp, id=id)

    for name in lst:
        try:
            lstin = os.listdir(dir_path + '/' + name)
        except OSError:
            pass  # ignore errors
        contents = {}
        for namein in lstin:
            contents.update({'testtimestamp': name})
            contents.update({'testinput': namein})
        exp[name] = contents

    return render_template('viewproject.html', x=x, y=y, z=z, t=exp, id=id)

@app.route('/upload')
def upload_file():
    proj = request.values.get("project")
    expt = request.values.get("experiment")
    m = dict()
    return render_template('uploadtest.html', f=proj, m=m, e=expt)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        project = request.values.get("project")
        experiment = request.values.get("experiment")

        filename1 = experiment + "\\" + experiment + "_model.h5"
        filenameclasses = experiment + "\\" + experiment + "_classes.pickle"

        model_path = os.path.dirname(os.path.abspath(__file__)) + "\\FashionMnist\\" + filename1
        filenameclassespath = os.path.dirname(os.path.abspath(__file__)) + "\\FashionMnist\\" + filenameclasses

        f = request.files['file']
        filename = secure_filename(f.filename)
        directory = app.config['UPLOAD_FOLDER'] + "\\" + project
        if not os.path.exists(directory):
            os.makedirs(directory)

        now = datetime.datetime.now()
        dt = str(now.month).zfill(2) + str(now.day).zfill(2) + str(now.year).zfill(2) + "-" + str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(2)

        director1y = app.config['UPLOAD_FOLDER'] + "\\" + project + "\\" + project + "--" + dt
        foldername = project + "--" + dt
        filenameforview = project + "--" + dt
        if not os.path.exists(director1y):
            os.makedirs(director1y)

        #f.save(os.path.join('C:/code/umkcmodel/testdata', filename))
        f.save(os.path.join(director1y, filename))
        filepath = director1y + "\\" + filename
        testpredict = performpredict(model_path, filenameclassespath, filepath)

        testpredicttext = ""
        for key, value in testpredict.items():
            for keyi, valuei in value.items():
                testpredicttext = testpredicttext + " " + valuei

        testpredicttext = "uploaded successfully. and categorized as shown in table."
        return render_template('uploadtest.html', f=project, m=testpredict, filename=filename, foldername=foldername, uploadstatues=testpredicttext)

@app.route('/image')
def get_image():
    experiment = request.values.get("experiment")
    image = request.values.get("type")
    project = experiment.split("_")[0]
    filename = IMAGE_FOLDER + "\\" + experiment + "\\" + experiment + "_" + image + ".png"

    filename1 = experiment + "\\" + experiment + "_model.h5"

    return send_file(filename, mimetype='image/jpg')

@app.route('/testimage')
def get_testimage():
    project = request.values.get("project")
    timestamp = request.values.get("timestamp")
    testimage = request.values.get("testimage")

    filename = UPLOAD_FOLDER + "\\" + project + "\\" + timestamp + "\\" + testimage

    return send_file(filename, mimetype='image/jpg')
@app.route('/downloadh5')
def get_h5():
    experiment = request.values.get("experiment")
    project = experiment.split("_")[0]
    filename1 = IMAGE_FOLDER + "\\" + experiment + "\\" + experiment + "_model.h5"
    fname = experiment + "_model.h5"
    return send_file(filename1, mimetype='application/octet-stream', attachment_filename=fname, as_attachment=True)
@app.route('/viewexperiment')
def viewexperiment():
    experiment = request.values.get("experiment")
    x = experiment
    ttext = experiment.split("_")[1]
    objDate = datetime.datetime.strptime(ttext, '%m%d%y-%H%M%S')
    ttext = datetime.datetime.strftime(objDate, '%b %d, %Y %H:%M')

    project = experiment.split("_")[0]
    y = project
    z = {}
    #for proj, projdetails in dir.items():
    z[project] = dirs[project]

    filename1 = experiment + "\\" + experiment + "_model.h5"
    filenameclasses = experiment + "\\" + experiment + "_classes.pickle"
    zt = True
    zf = False
    zp = 5005
    zl = 'localhost'
    model_path = os.path.dirname(os.path.abspath(__file__)) + "\\rawdata\\" + filename1
    filenameclassespath = os.path.dirname(os.path.abspath(__file__)) + "\\rawdata\\" + filenameclasses
    dir_path = os.path.dirname(os.path.abspath(__file__)) + "\\testdata\\" + project + ''
    lst = os.listdir(dir_path)
    exp = dict()

    for name in lst:
        lstin = os.listdir(dir_path + '/' + name)
        contents = {}
        for namein in lstin:
            contents.update({'testtimestamp': name})
            contents.update({'testinput': namein})
            filepath = os.path.dirname(os.path.abspath(__file__)) + "\\testdata\\" + project + "\\" + name + "\\" + namein
            testpredict = performpredictdummy(model_path, filenameclassespath, filepath)

            for classnamevalue, accuracyvalue in testpredict.items():

                contents.update({'classname': classnamevalue})
                contents.update({'accuracy': accuracyvalue})
        exp[name] = contents

    netron.start(model_path, zf, zf, zp, zl)

    return render_template('viewexperiment.html', x=x, ttext=ttext, y=y, z=z, t=exp)

@app.route('/viewchart')
def viewchart():
    x = data
    y = metadata
    z = dirs
    return render_template('viewchart.html', x=x, y=y, z=z)

@app.route('/projects')
def viewprojects():
    x = data
    y = metadata
    z = dirs
    return render_template('projects.html', x=x, y=y, z=z)

@app.route('/experiments')
def viewexperiments():
    x = data
    y = metadata
    z = dirs
    return render_template('experiments.html', x=x, y=y, z=z)

def activate():
    xFit()
    app.run()



def path_hierarchy(path):


    hierarchy = {
        'type': 'folder',
        'name': os.path.basename(path),
        'path': path,
    }

    try:
        hierarchy['children'] = [
            path_hierarchy(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        hierarchy['type'] = 'file'

    return hierarchy

def make_tree(path):
    tree = {}
    exp = {}
    currentproject = ""
    project = {}
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        currentproject = ""
        project = {}
        for name in lst:

            splits = name.split("_")
            projname = splits[0]
            runtimestamp = splits[1]
            datafile = projname + "_" + runtimestamp + "_metadata.txt"

            if currentproject == "":
                exp = dict()

            if currentproject != projname and currentproject != "":

                exp = dict()
                tree[currentproject] = project
                currentproject = projname
                project = {
                    'type': 'folder',
                    'name': projname,
                    'path': path,
                    'history': exp
                }

                if projname == 'LSTM':
                    project.update({'application': 'Image Classification'})
                    project.update({'expcount': 8})
                    project.update({'owner': 'John W.'})
                if projname == 'ImageCaptioning':
                    project.update({'application': 'Image Classification'})
                    project.update({'expcount': 8})
                    project.update({'owner': 'John W.'})
                if projname == 'FashionMnist':
                    project.update({'application': 'Image Recognition'})
                    project.update({'expcount': 7})
                    project.update({'owner': 'John W.'})
                if projname == 'CNN':
                    project.update({'application': 'Text Generation'})
                    project.update({'expcount': 1})
                    project.update({'owner': 'John W.'})
                if projname == 'siri':
                    project.update({'application': 'Text Generation'})
                    project.update({'expcount': 1})
                    project.update({'owner': 'John W.'})

            else:
                #exp = dict(name=runtimestamp, children=[])
                currentproject = projname
                project = {
                    'type': 'folder',
                    'name': projname,
                    'path': path,
                    'history': exp
                }

                if projname == 'LSTM':
                    project.update({'application': 'Image Classification'})
                    project.update({'expcount': 8})
                    project.update({'owner': 'John W.'})
                if projname == 'ImageCaptioning':
                    project.update({'application': 'Image Classification'})
                    project.update({'expcount': 8})
                    project.update({'owner': 'John W.'})
                if projname == 'FashionMnist':
                    project.update({'application': 'Image Recognition'})
                    project.update({'expcount': 7})
                    project.update({'owner': 'John W.'})
                if projname == 'CNN':
                    project.update({'application': 'Text Generation'})
                    project.update({'expcount': 1})
                    project.update({'owner': 'John W.'})
                if projname == 'siri':
                    project.update({'application': 'Text Generation'})
                    project.update({'expcount': 1})
                    project.update({'owner': 'John W.'})
            fn = path + name + "\\" + datafile

            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                with open(fn) as f:
                    contents = {}
                    objDate = datetime.datetime.strptime(runtimestamp, '%m%d%y-%H%M%S')
                    contents.update({'timestamptext': datetime.datetime.strftime(objDate, '%b %d, %Y %H:%M')})
                    contents.update({'timestamp': runtimestamp})
                    contents.update({'project': projname})
                    contents.update({'experiment': name})
                    contents.update({'owner': 'John W.'})
                    for line in f:
                        linesplits = line.replace("\n", "").split(":")
                        contents.update({linesplits[0]: linesplits[1]})

                exp[name] = contents
                #exp[name].append(dict(name=runtimestamp, contents=contents))
    tree[currentproject] = project
    return tree
