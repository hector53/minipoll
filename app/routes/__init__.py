from flask import render_template,  request, jsonify,  redirect, make_response
from app import app
from app.schemas import getDataOne, getData
from app.datos import url_site
import uuid
import datetime
expire_date = datetime.datetime.now()
expire_date = expire_date + datetime.timedelta(days=90)

"""
@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)"""
        
@app.route("/")
def index():
        username = request.cookies.get('uPoll')
        if username:
                #existe la cookie no la creo 
                return render_template('index.html', linkSite=url_site, index=1)
        else:
                #no existe la creo 
                resp = make_response(render_template('index.html', linkSite=url_site, index=1))
                resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                return resp

@app.route("/crear")
def crear():
        username = request.cookies.get('uPoll')
        if username:
                #existe la cookie no la creo 
                return render_template('encuestaSimple.html', linkSite=url_site)
        else:
                #no existe la creo 
                resp = make_response(render_template('encuestaSimple.html', linkSite=url_site))
                resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                return resp

@app.route("/sorteos")
def sorteos():
        return render_template('sorteos.html', linkSite=url_site)
         

@app.route("/dashboard")
def panel():
        username = request.cookies.get('uPoll')
        if username:
                #existe la cookie no la creo 
                return render_template('panel.html')
        else:
                #no existe la creo 
                resp = make_response(render_template('panel.html'))
                resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                return resp

@app.route("/<string:codigo>")
def vista_encuesta(codigo):
        CodigoR = codigo[0:5]
        print("el codigo es", CodigoR)
        resultado = codigo[-1:]
        print("el resultado es", resultado)
        if resultado == '+':
                resultado = 1
        else:
                resultado = 0
        miUid = request.cookies.get('uPoll')
        sql = f"SELECT * FROM encuesta where cod = '{CodigoR}'  " 

        #buscar por uid las encuestas q tenga en la db 
        encuesta = getDataOne(sql)
        if encuesta:
                idEncuesta = encuesta[0]
                if resultado == 1:
                        #buscar votos 
                        sql3 = f"SELECT * FROM votos_opciones where id_encuesta = {idEncuesta}  " 
                        print(sql3)
                        votos = getData(sql3)
                        totalVotos = len(votos)
                #buscar opciones para la descripcion meta
                sql2 = f"SELECT * FROM opcion_encuesta where id_encuesta = {idEncuesta}  " 
                opciones = getData(sql2)
                descripcionMeta = ''
                i = 0
                for row in opciones:
                        if resultado == 1:
                                id_opcion = row[0]
                                sql4 = f"SELECT * FROM votos_opciones where id_encuesta = {idEncuesta} and id_opcion = {id_opcion}  "
                                print(sql4) 
                                voto_opcion = getData(sql4)
                                if voto_opcion:
                                        total_voto_opcion = len(voto_opcion)
                                        porcentaje = (total_voto_opcion * 100) / totalVotos
                                else:
                                        porcentaje = 0
                                if i==0:
                                        descripcionMeta = descripcionMeta + str((i+1))+')'+row[1]+' '+str(porcentaje)+'%'
                                else:
                                        descripcionMeta = descripcionMeta + ', '+str((i+1))+')'+row[1]+' '+str(porcentaje)+'%'
                        else:
                                if i==0:
                                        descripcionMeta = descripcionMeta + str((i+1))+')'+row[1]
                                else:
                                        descripcionMeta = descripcionMeta + ', '+str((i+1))+')'+row[1]
                        i=i+1

                        
                #verificar si la encuesta es del usuario activo 
                sql2 = f"SELECT * FROM encuesta where cod = '{CodigoR}' and id_user = '{miUid}' " 
                #buscar por uid las encuestas q tenga en la db 
                encuestaUser = getDataOne(sql2)
                if encuestaUser:
                        mio = 1
                else:
                        mio = 0
                if miUid:
                        #existe la cookie no la creo 
                        return render_template("encuesta.html", encuesta=encuesta, linkSite=url_site, mio=mio, meta=descripcionMeta, resultado=resultado)
                else:
                        #no existe la creo 
                        resp = make_response(render_template("encuesta.html", encuesta=encuesta, linkSite=url_site, mio=mio, meta=descripcionMeta, resultado=resultado))
                        resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                        return resp
        else:
                return redirect("/", code=302)


@app.route("/<string:codigo>/edit")
def editar_encuesta(codigo):
        username = request.cookies.get('uPoll')
        sql = f"SELECT * FROM encuesta where cod = '{codigo}' and id_user = '{username}'  " 
        #buscar por uid las encuestas q tenga en la db 
        encuesta = getDataOne(sql)
        if encuesta:
                return render_template("edit_encuesta.html", encuesta=encuesta)
        else:
                return redirect("/", code=302)


     