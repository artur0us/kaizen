#!/usr/bin/python3
# coding: utf-8

from __future__ import print_function
from __future__ import division
from future import standard_library
from ufal.udpipe import Model, Pipeline
import nltk
from nltk.corpus import stopwords
import sys, os, wget, gensim, logging, re, itertools, json
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import threading, signal, base64
from flask import Flask, render_template, Response, request, redirect

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

TEST = True
# Global variables
serverThread = None
serverApp = Flask(__name__, static_folder="web", static_url_path="", template_folder="web")

# Web-site's pages routes
@serverApp.route("/")
def indexPage():
    return render_template("index.html")
# API routes
@serverApp.route("/api/base_data_analyze", methods = ['GET', 'POST'])
def baseDataAnalyze():
    if request.method == 'POST':
        newFile = request.files["data_file"]
        newFile.save(newFile.filename)
        result = allActions(newFile.filename)
        #print(result)
        return result

def allActions(userFile):
    # ANOTHER MAIN ACTIONS
    unique = []
    tagged = []
    vectors = []
    if not TEST:
        standard_library.install_aliases()
        udpipe_model_url = 'http://rusvectores.org/static/models/udpipe_syntagrus.model'
        udpipe_filename = udpipe_model_url.split('/')[-1]
        if not os.path.isfile(udpipe_filename):
            print('UDPipe model not found. Downloading...', file=sys.stderr)
            wget.download(udpipe_model_url)
        print('Loading the model...', file=sys.stderr)
        udpipe_model = Model.load(udpipe_filename)
        process_pipeline = Pipeline(udpipe_model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
        nltk.download('stopwords')
        model = gensim.models.KeyedVectors.load_word2vec_format('ruwikiruscorpora-superbigrams_skipgram_300_2_2018.vec.gz', binary=False)
        model.init_sims(replace=True)
        file = open('data_full.csv', "r")
        content = file.readlines()
        file.close()
        temp = ""
        for item in content:
            temp += item.replace('""', "'").replace("\n", "")
        items = temp.split('""')
        items[0] = items[0].replace('"', '')
        items[-1] = items[-1].replace('"', '')
        unique = []
        unique.append(items[0])
        for item in items:
            if item != unique[-1]:
                unique.append(item)
        asd = 0
        print(len(unique))
        tagged = []
        vectors = []
        pos = True
        for item in unique:
            asd += 1
            print(asd)
            clean = ''
            for word in item.split(' '):
                if word not in stopwords.words('russian'):
                    clean += word + ' '
            processed = process_pipeline.process(clean)
            content = [l for l in processed.split('\n') if not l.startswith('#')]
            tagged_ = [w.split('\t')[2].lower() + '_' + w.split('\t')[3] for w in content if w]
            tagged_propn = []
            propn = []
            for t in tagged_:
                if t.endswith('PROPN'):
                    if propn:
                        propn.append(t)
                    else:
                        propn = [t]
                elif t.endswith('PUNCT'):
                    propn = []
                    continue
                else:
                    if len(propn) > 1:
                        name = '::'.join([x.split('_')[0] for x in propn]) + '_PROPN'
                        tagged_propn.append(name)
                    elif len(propn) == 1:
                        tagged_propn.append(propn[0])
                    tagged_propn.append(t)
                    propn = []
            if not pos:
                tagged_propn = [t.split('_')[0] for t in tagged_propn]
            tagged.append(tagged_propn)

            item_vec = [0] * 300
            for word in tagged_propn:
                if word in model:
                    for i in range(len(model.wv[word])):
                        item_vec[i] += model.wv[word][i]
            vectors.append(item_vec)
        file = open("unique.json", "w")
        file.write(json.dumps(unique, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
        file.close()
        file = open("tagged.json", "w")
        file.write(json.dumps(tagged, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
        file.close()
        file = open("vectors.json", "w")
        file.write(json.dumps(vectors, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
        file.close()
    else:
        with open('unique.json') as file:
            unique = json.load(file)
        with open('tagged.json') as file:
            tagged = json.load(file)
        with open('vectors.json') as file:
            vectors = json.load(file)
    
    # TSNE_PLOT FUNCTION
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    for i in range(len(unique)):
        labels.append(i)
    for vec in vectors:
        tokens.append(vec)
    tsne_model = TSNE(n_components=2) 
    from sklearn.cluster import KMeans  
    X = tsne_model.fit_transform(tokens)
    kmeans = KMeans(n_clusters=20)
    kmeans.fit(X)
    ###########################
    #print(X)

    clusters = kmeans.labels_.tolist()
    prepared = []
    for i in range(len(unique)):
        item = {'item': unique[i], 'cluster': clusters[i]}
        prepared.append(item)
    file = open("prepared.json", "w")
    file.write(json.dumps(prepared, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
    file.close()

    return json.dumps([X.tolist(), kmeans.labels_.tolist(), 20, unique])

    ###########################
    """plt.figure(figsize=(7, 7)) 
    plt.scatter(X[:,0],X[:,1], c=kmeans.labels_, cmap='rainbow')
    x = []
    y = []
    for value in X:
        x.append(value[0])
        y.append(value[1])
    for i in range(len(x)):
        plt.annotate(labels[i], xy=(x[i], y[i]), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')
    plt.show()"""

def main():
    serverApp.run("0.0.0.0", 9000, debug=False)
    #allActions()

main()
