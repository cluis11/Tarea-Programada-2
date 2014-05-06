from flask import Flask, render_template, request, redirect, url_for, abort, session 
app = Flask("Aplicacion Web") 
from pyswip import Prolog
from pyswip import *
prolog= Prolog()

#Funcion que se encarga de la lectura del archivo para poder usar la informacion en la base de conocimientos
def Cargar_Base():
    BaseC = open("BaseC.txt", "a+")
    str = BaseC.readline();
    while str !='':
        prolog.assertz(str)
        str = BaseC.readline()
    BaseC.close()
#Direcciones de la aplicacion Web
#Direccion de la pagina principal
@app.route('/') 
def home(): 
	return render_template('index.html')
#Direcciones para insertar informacion
#Direccion de pagina donde se ingresa un restaurante
@app.route('/Ingresa Restaurante')
def Ingresa_Restaurante():
    return render_template('Restaurante.html')
#Direccion donde se ingresan los platillos
@app.route('/Ingresa Platillo')
def Ingresa_Platillo():
    return render_template('Platillo.html')
#Agregar restaurante, toma los datos del html y los inserta a la base y al txt
@app.route('/InsertaR', methods=['POST'])
def InsertaR():
    Nombre = request.form['restaurante']
    Tipo_Restaurante = request.form['tipo_comida']
    Ubicacion = request.form['ubicacion']
    Telefono= request.form['telefono']
    Horario= request.form['horario']
    Inserta_Restaurante(Nombre,Tipo_Restaurante,Ubicacion,Telefono,Horario)
    return render_template('Agregado.html')
#Funcion que agrega el restaurante a la base de conocimientos y al txt, resive los datos del html
def Inserta_Restaurante(Restaurante,Tipo_restaurante,Ubicacion,Telefono,Horario):
    restaurante="restaurante("+Restaurante+","+Tipo_restaurante+","+Ubicacion+","+Telefono+","+Horario+")"
    prolog.assertz(restaurante)
    BaseC= open("BaseC.txt","a+")
    BaseC.write(agregar_restaurante+"\n")
    BaseC.close()
    
#Agregar PLatillo
#Direccion que se encarga de ingresa los datos para insertar un plantillo y llama la funcion para ingresarlo a la base
@app.route('/InsertaP', methods=['POST'])
def InsertaP():
    restaurante = request.form['restaurante']
    platillo = request.form['platillo']
    sabor= request.form['sabor']
    pais= request.form['pais']
    ingrediente= request.form['ingrediente']
    Ingresa_Platillo(restaurante,platillo,sabor,pais,ingrediente)
    return render_template('AgregadoP.html')
#Funcion que ingresa los platillos a la base de conocimientos y al txt, toma los datos del html
def Ingresa_Platillo(Restaurante,Platillo,Sabor,Pais,Ingredientes):
    Platillo=  "platillo("+Restaurante+","+Platillo+","+Sabor+","+Pais+","+"["+Ingredientes+"]"+")"
    prolog.assertz(Platillo)
    BaseC= open("BaseC.txt","a+")
    BaseC.write(agregar_Platillo+"\n")
    BaseC.close()


@app.route('/Consulta de restaurante')
def Consultas():
    BaseC = open("BaseC.txt", "a+")
    linea = BaseC.readline();
    if linea =='':
        return render_template('Vacia.html')
    else:
        return render_template('lista_consultas.html')
    BaseC.close()


#Consultas
def NoEsta_enLista(Lista,elemento):
    for i in Lista:
        if i == elemento:
            return False
        else:
            return True


@app.route('/Consulta de restaurantes')
def Consulta_de_restaurantes():
    
    ListaRest = []
    for i in prolog.query("restaurante(Restaurante,_,_,_,_)"):
        if ListaRest == []:
            ListaRest.append(i ["Restaurante"])
        elif NoEsta_enLista(ListaRest, i ["Restaurante"]):
            ListaRest.append(i ["Restaurante"])
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
        restaurante = list(ListaRest)
    	return render_template('Consulta.html',restaurante=restaurante)
    
#Consulta del restaurane por nombre
@app.route('/Consulta nombre del restaurante')
def Rest_por_Nombres():
    return render_template('Rest_por_Nombres.html')

@app.route('/Consulta nombre del restaurante', methods=['POST'])
def Consulta_res_por_nombre():
    restaurante =  request.form['restaurante']
    NombreRest = restaurante.lower()
    ListaRest = []
    for i in prolog.query( "restaurante("+NombreRest+",TipoComida,Ubicacion,Telefono,Horario)"):
            ListaRest.append(i["Ubicacion"])
            ListaRest.append(i["TipoComida"])
            ListaRest.append(i["Telefono"])
            ListaRest.append(i["Horario"])
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	nombre = list (ListaRest )
    	return render_template('Consulta_nombre.html',nombre=nombre) 	
   
#####################################################################################
#Consulta del restaurane por tipo de comida
@app.route('/Consulta de tipo de comida')
def Rest_por_Tipo():
    return render_template('Rest_por_Tipo.html')


@app.route('/Consulta nombre del tipo de comida', methods=['POST'])
def Consulta_Rest_por_Tipo():
    tipo_comida = request.form['tipo_comida']
    ListaRest = []
    Comida=tipo_comida.lower()
    for i in prolog.query( "restaurante(Restaurante,"+Comida+",_,_,_)"):
        if ListaRest == []:
            ListaRest.append(i ["Restaurante"])
        elif NoEsta_enLista(ListaRest, i ["Restaurante"]):
            ListaRest.append(i ["Restaurante"])
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	tipo= list(ListaRest)
    	return render_template('Consulta_tipocomida.html',tipo=tipo)
#Consulta de los ingredientes de platillos de un restaurante
@app.route('/Consulta de los ingredientos')
def Platillos_ingredientes():
    return render_template('Platillos_ingredientes.html')

@app.route('/Consulta por ingrediente', methods=['POST'])
def Consulta_Rest_por_ingrediente():
    restaurante = request.form['restaurante']
    ingrediente = request.form['ingrediente']
    
    rest=restaurante.lower()
    ing=ingrediente.lower()
    ListaPlat=[]
    for plato in prolog.query("platillo("+rest+",Platillo,_,_,Ingredientes)"):
        Lista = plato["Ingredientes"]
        for i in Lista:
            if str(i)==ing:
                ListaPlat.append(plato["Platillo"])
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	ingrediente_select = list(ListaPlat)
    	return render_template('Consulta_ingrediente.html',ingrediente_select=ingrediente_select)
##Consulta de los platillos del restaurante
@app.route('/Consulta platillos del restaurante')
def Platillos_qTiene_Rest():
    return render_template('Platillos_qTiene_Rest.html')

@app.route('/Consulta por platillo', methods=['POST'])
def Platillos_Rest():
    restaurante = request.form['restaurante']

    restaurant=restaurante.lower()
    ListaPlat=[]
    RestaurantePlatillo = list(prolog.query("platillo("+restaurant+",Platillo,_,_,_)"))
    for restaurant in prolog.query( "platillo("+restaurant+",Platillo,_,_,_)"):
        ListaPlat.append(restaurant["Platillo"])
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	restaurante_platillo= list (ListaPlat)
    	return render_template('Consulta_por_platillo_en_rest.html',restaurante_platillo=restaurante_platillo)


##Consulta de los restaurantes segun el pais el cual es el platillo
@app.route('/Consulta por platillo de paises')
def Rest_qTiene_PlatilloPais():
    return render_template('Rest_qTiene_PlatilloPais.html')

@app.route('/Consulta por pais', methods=['POST'])
def Rest_Platillo_Pais():
    lugar = request.form['pais']
    pais=lugar.lower()
    ListaRest=[]
    for restaurante in prolog.query( "platillo(Restaurante,_,_,"+pais+",_)"):
        if ListaRest == []:
            ListaRest.append(restaurante["Restaurante"])
        elif NoEsta_enLista(ListaRest, restaurante["Restaurante"]):
            ListaRest.append(restaurante["Restaurante"])
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	pais= list(ListaRest)
    	return render_template('Consulta_pais_ingredientes.html',pais=pais)

#LLamado para cargar la base de conocimientos
Cargar_Base()    
#Inicia la aplicacion web
app.run()
