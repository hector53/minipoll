
from flask import render_template,  request, jsonify,  redirect, url_for, make_response, session
from app import app
from app.schemas import getDataOne, getData
from app.datos import url_site
from app.lang import idioma
import uuid
import datetime
expire_date = datetime.datetime.now()
expire_date = expire_date + datetime.timedelta(days=10000)
from app.request import time_passed
"""
@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)"""

@app.route("/")
def index():
        lang = request.cookies.get('resultAppLang')
        if 'loggedin' in session:
                userR = 1
                if lang:
                        return render_template('index.html', idioma=idioma[int(lang)], linkSite=url_site, index=1, userR=userR)
                else:
                        resp = make_response(render_template('index.html', idioma=idioma[0], linkSite=url_site, index=1, userR=userR))
                        resp.set_cookie('resultAppLang', 0, expires=expire_date)
                        return resp
        else:
                userR = 0
                username = request.cookies.get('uPoll')
                if username:
                        #existe la cookie no la creo 
                        if lang:
                                return render_template('index.html',   idioma=idioma[int(lang)], linkSite=url_site, index=1, userR=userR)
                        else:
                                resp = make_response(render_template('index.html',  idioma=idioma[0], linkSite=url_site, index=1, userR=userR))
                                resp.set_cookie('resultAppLang', '0', expires=expire_date)
                                return resp
                else:
                        #no existe la creo 
                        if lang:
                                resp = make_response(render_template('index.html',  idioma=idioma[int(lang)], linkSite=url_site, index=1, userR=userR))
                                resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                                return resp
                        else:
                                resp = make_response(render_template('index.html',  idioma=idioma[0], linkSite=url_site, index=1, userR=userR))
                                resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                                resp.set_cookie('resultAppLang', 0, expires=expire_date)
                                return resp
                                
@app.route("/crear")
def crear():
        lang = request.cookies.get('resultAppLang')
        if lang:
                print("no la creo")
        else:
                print("la creo")
                crear_cookie_idioma()
                lang = request.cookies.get('resultAppLang')
        
        if 'loggedin' in session:
                userR = 1
                return render_template('encuestaSimple.html', idioma=idioma[int(lang)], linkSite=url_site,  userR=userR)
        else:
                userR = 0
                username = request.cookies.get('uPoll')
                if username:
                        #existe la cookie no la creo 
                        return render_template('encuestaSimple.html', idioma=idioma[int(lang)], linkSite=url_site,  userR=userR)
                else:
                        #no existe la creo 
                        resp = make_response(render_template('encuestaSimple.html', idioma=idioma[int(lang)], linkSite=url_site,  userR=userR))
                        resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                        return resp

@app.route("/sorteos")
def sorteos():
        lang = request.cookies.get('resultAppLang')
        if lang:
                print("no la creo")
        else:
                print("la creo")
                crear_cookie_idioma()
                lang = request.cookies.get('resultAppLang')
        
        if 'loggedin' in session:
                userR = 1
                return render_template('sorteos.html', idioma=idioma[int(lang)], linkSite=url_site, userR=userR)
        else:
                userR = 0
                return render_template('sorteos.html', idioma=idioma[int(lang)],  linkSite=url_site, userR=userR)
         

def crear_cookie_idioma():
        resp = make_response(render_template('setCookie.html'))
        resp.set_cookie('resultAppLang', '0', expires=expire_date)
        return resp


@app.route("/dashboard")
def panel():
        lang = request.cookies.get('resultAppLang')
        if lang:
                print("no la creo")
        else:
                print("la creo")
                crear_cookie_idioma()
                lang = request.cookies.get('resultAppLang')
        
        if 'loggedin' in session:
                userR = 1
                return render_template('panel.html', userR=userR, idioma=idioma[int(lang)])
        else:
                userR = 0
                username = request.cookies.get('uPoll')
                if username:
                        #existe la cookie no la creo 
                        return render_template('panel.html', userR=userR, idioma=idioma[int(lang)] )
                else:
                        #no existe la creo 
                        resp = make_response(render_template('panel.html', userR=userR, idioma=idioma[int(lang)]))
                        resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                        return resp

        

@app.route("/p/<string:codigo>")
def vista_encuesta(codigo):
        lang = request.cookies.get('resultAppLang')
        if lang:
                print("no la creo")
        else:
                print("la creo")
                crear_cookie_idioma()
                lang = request.cookies.get('resultAppLang')
        
        if 'loggedin' in session:
                userR = 1
                miUid = session['id_user']
        else:
                userR = 0
                miUid = request.cookies.get('uPoll')
        CodigoR = codigo[0:5]
        print("el codigo es", CodigoR)
        resultado = codigo[-1:]
        print("el resultado es", resultado)
        if resultado == '+':
                resultado = 1
        else:
                resultado = 0
        
        sql = f"SELECT * FROM encuesta where cod = '{CodigoR}'  " 

        #buscar por uid las encuestas q tenga en la db 
        encuesta = getDataOne(sql)
        if encuesta:
                idEncuesta = encuesta[0]
                dataEncuesta = []
                dataEncuesta.append({
                'id': encuesta[0],
                'pregunta': encuesta[1],
                'id_user':   encuesta[2],
                'cod': encuesta[3],
                'fecha': time_passed(str(encuesta[4]))
                })
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
                if userR==1:
                        #existe la cookie no la creo 
                        return render_template("encuesta.html", idioma=idioma[int(lang)], userR=userR, encuesta=dataEncuesta, linkSite=url_site, mio=mio, meta=descripcionMeta, resultado=resultado)
                else:
                        if miUid:
                                return render_template("encuesta.html", idioma=idioma[int(lang)],  userR=userR, encuesta=dataEncuesta, linkSite=url_site, mio=mio, meta=descripcionMeta, resultado=resultado)
                        else:
                                resp = make_response(render_template("encuesta.html", idioma=idioma[int(lang)],  userR=userR, encuesta=dataEncuesta, linkSite=url_site, mio=mio, meta=descripcionMeta, resultado=resultado))
                                resp.set_cookie('uPoll', uuid.uuid4().hex, expires=expire_date)
                                return resp
        else:
                return redirect("/", code=302)


@app.route("/p/<string:codigo>/edit")
def editar_encuesta(codigo):
        lang = request.cookies.get('resultAppLang')
        if lang:
                print("no la creo")
        else:
                print("la creo")
                crear_cookie_idioma()
                lang = request.cookies.get('resultAppLang')
        
        if 'loggedin' in session:
                userR = 1
                username = session['id_user']
        else:
                userR = 0
                username = request.cookies.get('uPoll')
        sql = f"SELECT * FROM encuesta where cod = '{codigo}' and id_user = '{username}'  " 
        #buscar por uid las encuestas q tenga en la db 
        encuesta = getDataOne(sql)
        if encuesta:
                return render_template("edit_encuesta.html", idioma=idioma[int(lang)], userR=userR, encuesta=encuesta)
        else:
                return redirect("/", code=302)


#user
@app.route("/signup")
def signup():
        lang = request.cookies.get('resultAppLang')
        if lang:
                print("no la creo")
        else:
                print("la creo")
                crear_cookie_idioma()
                lang = request.cookies.get('resultAppLang')
        
        if 'loggedin' in session:
                return redirect("/dashboard", code=302)
        else:
                return render_template('user/signup.html', idioma=idioma[int(lang)])

@app.route("/login")
def login():
        lang = request.cookies.get('resultAppLang')
        if 'loggedin' in session:
                return redirect("/dashboard", code=302)
        else:
                
                if lang:
                        return render_template('user/login.html', idioma=idioma[int(lang)])
                else:
                        resp = make_response(render_template('user/login.html',  idioma=idioma[0]))
                        resp.set_cookie('resultAppLang', '0', expires=expire_date)
                        return resp


                

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id_user', None)
   session.pop('username', None)
   return redirect(url_for('login'))

     