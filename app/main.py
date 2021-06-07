#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask import render_template, url_for, redirect, flash, request
from flask_mail import Mail, Message
from os import listdir
from math import ceil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from .email import email_data

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": email_data['user'],
    "MAIL_PASSWORD": email_data['pass']
}

app.config.update(mail_settings)
mail = Mail(app)

def dividirEnColumnas(datos, columnas):
	resultado, indices = [], list(enumerate(datos))

	for fila in range( len(indices)//columnas + 1 ):
		aux = []

		for columna in range(columnas):
			indice = columna + columnas*fila

			if indice >= len(indices):
				break

			aux.append(datos[indices[indice][1]])

		resultado.append(aux)
		aux = []
	else:
		if len(aux) != 0:
			resultado.append(aux)

	return resultado

def getPiezas(columnas):

	piezas = {}

	for pieza in listdir("./app/static/piezas"):
		aux = pieza.replace('b','').replace('.png','').replace('.jpg','')

		piezas[aux] = piezas.get(aux, {0:url_for('static', filename = 'piezas/' + pieza), 1:url_for('static', filename = 'piezas/' + pieza)})

		if 'b' in pieza:
			piezas[aux][1] = url_for('static', filename = 'piezas/' + pieza)
		else:
			piezas[aux][0] = url_for('static', filename = 'piezas/' + pieza)

	return(dividirEnColumnas(piezas, columnas))

def get_current_section(active_section):
	secciones = {'Piezas':{'url':url_for('home'), 'active':0}, 
				 'Proyectos':{'url':url_for('proyectos'), 'active':0}, 
				 'Hola':{'url':url_for('hola'), 'active':0}, 
				 'Contacto':{'url':url_for('sendmail'), 'active':0}}
	secciones[active_section]['active'] = 1
	return secciones

@app.route('/')
def home():
	return render_template('piezas.html', piezas = getPiezas(columnas = 3), secciones = get_current_section('Piezas'))

@app.route('/proyectos')
def proyectos():
	return render_template('proyectos.html', secciones = get_current_section('Proyectos'))

@app.route('/hola')
def hola():
	return render_template('hola.html', secciones = get_current_section('Hola'))

@app.route('/contacto', methods=['GET', 'POST'])
def sendmail():
	if request.method == "POST":
		try:
			message = request.form.get("message")
			email = request.form.get("email")
			name = request.form.get("name")
			subject = request.form.get("subject")
			message = 'Name: ' + name + '\nEmail: ' + email + '\n' + message

			msg = Message(subject=subject,
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["sergio.heredia.pottery@gmail.com"], # replace with your email for testing
                      body=message)

			mail.send(msg)

			flash(u'Mensaje enviado correctamente', 'success')
		except:
			flash(u'Lo sentimos, por motivos desconocidos no se ha podido enviar el mensaje. Inténtalo manualmente con sergio.heredia.pottery@gmail.com', 'error')

	return render_template('contacto.html', secciones = get_current_section('Contacto'))

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('home'))