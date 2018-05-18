#!/usr/bin/python3
# coding: utf-8

# Python modules
import logging, threading, os, signal, json
from flask import Flask, render_template, Response, request, redirect

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
		# actions...
		return "OK"

def Main():
	serverApp.run("0.0.0.0", 9000, debug=False)

Main()