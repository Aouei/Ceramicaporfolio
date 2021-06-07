#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from passlib.hash import sha256_crypt

client = MongoClient("mongodb+srv://manolorooter:Iv6u7PQjQjcsjBY7@macramehuetorvega.vuchl.mongodb.net/MacrameHuetorVega?retryWrites=true&w=majority")

db = client.MacrameHuetorVega

def addUser(name, lastname, email, password, is_staff):
	user = [x for x in db.users.find({'email':email})]

	if len(user) > 0:
		return False, u'Ya existe un usuario con el mismo correo'
	elif len(password) >= 8:
		password = sha256_crypt.encrypt(password)
		db.users.insert({'name':name, 'lastname':lastname, 'email':email, 'password':password, 'is_staff':is_staff, 'favs':[]})
		return True, u'El usuario se ha registrado correctamente'
	else:
		return False, u'La contraseña debe tener al menos una longitud de 8 caracteres'

def delUser(email):
	pass

def updUser(name, lastname, email, password, is_staff):
	pass

def loginUser(email, password):
	user = [x for x in db.users.find({'email':email})]

	if len(user) == 0:
		return False, u'No existe ningún usuario con el correo introducido'
	else:
		name = user[0]['name']
		lastname = user[0]['lastname']
		is_staff = user[0]['is_staff']
		
		if sha256_crypt.verify(password, user[0]["password"]):
			return True, u'Bienvenida/o ' + name + " " + lastname , name, lastname, is_staff
		else:
			return False, u'La contraseña no es correcta'

def addProduct(photos, name, price, description, colours, metrics, materials):
	db.productos.insert({'photos':photos, 'name':name, 'price':price, 'description':description, 'colours':colours, 'metrics':metrics, 'materials':materials})

def getHomeProducts():
	nCols = 4

	products = db.productos.find()

	res, aux = [], []

	for idx, i in enumerate(products):
		if idx % nCols != 0:
			aux.append({'name':i['name'],'price':i['price'],'photos':i['photos'][0]})
		else:
			res.append(aux)
			aux = [{'name':i['name'],'price':i['price'],'photos':i['photos'][0]}]
	else:
		if len(aux) != 0:
			res.append(aux)

	res.remove([])

	return res

def getProduct(name):
	product = [i for i in db.productos.find({'name':name})][0]

	return product