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

#Direccion donde se accede al menu de consultas
@app.route('/Consulta de restaurante')
def Consultas():
    BaseC = open("BaseC.txt", "a+")
    linea = BaseC.readline();
    if linea =='':
        return render_template('Vacia.html')
    else:
        return render_template('Lista_Consultas.html')
    BaseC.close()

#Direccion de consulta de lista de restaurantes
@app.route('/Consulta de restaurantes')
def Consulta_de_restaurantes():    
    ListaRestaurantes = []
    for r in prolog.query("restaurante(Restaurante,_,_,_,_)"):
		ListaRestaurantes=ListaRestaurante+[r["Restaurante"]]
    if ListaRestaurantes == []:
        return render_template('Vacia.html')
    else:
        restaurante = list(ListaRestaurantes)
    	return render_template('Consulta.html',restaurante=restaurante)
    
#Consulta del restaurane por nombre
@app.route('/Consulta nombre del restaurante')
def Rest_por_Nombres():
    return render_template('Rest_por_Nombres.html')

#Muestra la info del restaurante a buscar
@app.route('/Consulta nombre del restaurante', methods=['POST'])
def Consulta_res_por_nombre():
    restaurante =  request.form['restaurante']
    restaurante = restaurante.lower()
    ListaRestaurante = []
    for i in prolog.query( "restaurante("+NombreRest+",TipoComida,Ubicacion,Telefono,Horario)"):
            ListaRestaurante=ListaRestaurante+[i["Ubicacion"]]
            ListaRestaurante=ListaRestaurante+[i["TipoComida"]]
            ListaRestaurante=ListaRestaurante+[i["Telefono"]]
            ListaRestaurante=ListaRestaurante+[i["Horario"]]
    if ListaRestaurante == []:
        return render_template('Vacia.html')
    else:
    	nombre = list (ListaRestaurante)
    	return render_template('Consulta_nombre.html',nombre=nombre) 	
   
#Consulta del restaurane por tipo de comida
@app.route('/Consulta de tipo de comida')
def Rest_por_Tipo():
    return render_template('Rest_por_Tipo.html')

#Lista de restaurantes por ripo de comida
@app.route('/Consulta nombre del tipo de comida', methods=['POST'])
def Consulta_Rest_por_Tipo():
    tipo = request.form['tipo_comida']
    tipo=tipo.lower()
    ListaRestaurantes = []
    for i in prolog.query( "restaurante(Restaurante,"+Comida+",_,_,_)"):
		ListaRestaurante=Listarestaurante+[i["Restaurante"]]
    if ListaRestaurante == []:
        return render_template('Vacia.html')
    else:
    	tipo= list(ListaRestaurante)
    	return render_template('Consulta_tipocomida.html',tipo=tipo)
    	
#Consulta de los ingredientes de un platillos especifico
@app.route('/Consulta de los ingredientos')
def Platillos_ingredientes():
    return render_template('Platillos_ingredientes.html')

#Lista de ingredientes de un platillos
@app.route('/Consulta por ingrediente', methods=['POST'])
def Consulta_Restaurante_por_ingrediente():
    restaurante = request.form['restaurante']
    ingrediente = request.form['ingrediente']
    restaurante=restaurante.lower()
    ingrediente=ingrediente.lower()
    ListaPlatillos=[]
    for p in prolog.query("platillo("+restaurante+",Platillo,_,_,Ingredientes)"):
        ListaIngredientes = p["Ingredientes"]
        for i in ListaIngredientes:
            if str(i)==ingrediente:
                ListaPlatillos=ListaPlatillos+[p["Platillo"]]
    if ListaRestaurante == []:
        return render_template('Vacia.html')
    else:
    	ingrediente_select = list(ListaPlatillos)
    	return render_template('Consulta_ingrediente.html',ingrediente_select=ingrediente_select)
    	
##Consulta de los platillos del restaurante
@app.route('/Consulta platillos del restaurante')
def Platillos_Tiene_Rest():
    return render_template('Platillos_Tiene_Rest.html')

#Platillos de un restaurantes
@app.route('/Consulta por platillo', methods=['POST'])
def Platillos_Rest():
    restaurante = request.form['restaurante']
    restaurante=restaurante.lower()
    ListaPlatillos=[]
    RestaurantePlatillo = list(prolog.query("platillo("+restaurante+",Platillo,_,_,_)"))
    for r in prolog.query( "platillo("+restaurante+",Platillo,_,_,_)"):
        ListaPlatillos=ListaPlatillos+[r["Platillo"]]
    if ListaPlatillos == []:
        return render_template('Vacia.html')
    else:
    	restaurante_platillo= list (ListaPlatillos)
    	return render_template('Consulta_por_platillo_en_rest.html',restaurante_platillo=restaurante_platillo)


#Consulta de platillos dependiendo de su pais nativo
@app.route('/Consulta por platillo de paises')
def Rest_Tiene_PlatilloPais():
    return render_template('Rest_qTiene_PlatilloPais.html')

#Consulta de restaurantes con un platillo de un pais especifico 
@app.route('/Consulta por pais', methods=['POST'])
def Rest_Platillo_Pais():
    pais=request.form['pais']
    pais=pais.lower()
    ListaRestaurantes=[]
    for r in prolog.query( "platillo(Restaurante,_,_,"+pais+",_)"):
		ListaRestestaurante=ListaRestaurante+[r["Restaurante"]]
    if ListaRestaurantes==[]:
        return render_template('Vacia.html')
    else:
    	pais= list(ListaRestaurantes)
    	return render_template('Consulta_pais_ingredientes.html',pais=pais)

#LLamado para cargar la base de conocimientos
Cargar_Base()    
#Inicia la aplicacion web
app.run()
