from flask import  request, jsonify
from app import app
from app import socketio
from app.schemas import *
from datetime import datetime
import socket
import random
import string
import json
import qrcode
import base64
import os
from flask_socketio import join_room, leave_room
import time
import math


#funcion time_passed
def time_passed(fecha):
        mesFecha = ["Ene", "Feb","Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep",
        "Oct", "Nov", "Dic"  ];
        timestamp = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        timestamp = datetime.timestamp(timestamp)
        print("timestamp",timestamp)

        print("fecha normal", datetime.fromtimestamp(timestamp))
        fechaNormal = datetime.fromtimestamp(timestamp)
        year = fechaNormal.strftime("%Y")
        print("año ", year)
        print(int(time.time()))

        diff = int(time.time()) - int(timestamp)
        print(diff)
        if diff == 0: 
             return 'justo ahora'

        if diff > 604800:
                dia = fechaNormal.strftime("%d")
                mes = fechaNormal.strftime("%b")
                #mes = mes[1:2]
                return f"{dia} {mes}"

        if diff < 604800:
                intervals = ['days', 86400]
        if diff < 86400:
                intervals = ['h', 3600]
        if diff < 3600:
                intervals = ['min', 60]
        if diff < 60:
                intervals = ['seg', 1]

        value = math.floor(diff/intervals[1])
        return f"{value} {intervals[0]}"




@app.route('/_guardar_capture' , methods=["POST"])
def guardar_capture():
        tipo = request.form.get('tipo', '', type=int)
        capture = request.form.get('capture', '', type=str)
        captureR = capture.replace('data:image/png;base64,', '')
        codigo = request.form.get('codigo', '', type=str)
        CodigoR = codigo[0:5]
        imgdata = base64.b64decode(captureR)
        if tipo == 1:
                #os.remove('app/static/img/captures/capture_'+CodigoR+'.jpg')
                filename = 'app/static/img/captures/capture_'+CodigoR+'.jpg'  # I assume you have a way of picking unique filenames
        if tipo == 2:
                #os.remove('app/static/img/captures/captureR_'+CodigoR+'.jpg')
                filename = 'app/static/img/captures/captureR_'+CodigoR+'.jpg'  # I assume you have a way of picking unique filenames

        with open(filename, 'wb') as f:
                f.write(imgdata)
        #actualizar encuesta img
        if tipo == 1:
                sql = f"""
                update encuesta set img = 1  where cod = '{CodigoR}'
                """ 
        if tipo == 2:
                print("tipo2")
                sql = f"""
                update encuesta set img2 = 1  where cod = '{CodigoR}'
                """
        
        updateEncuesta = updateData(sql)
        print(sql)

        return jsonify(1) 


@app.route('/_buscar_encuesta_codigo' , methods=["POST"])
def buscar_encuesta_codigo():
        codigo = request.form.get('codigo', '', type=str)
        sql = f"SELECT * FROM encuesta where cod = '{codigo}'  " 
        encuesta = getDataOne(sql)
        if encuesta:
                response = {
                'codigo': codigo,
                'status': 1,
                }
        else:
                response = {
                'status': 0,
                }

        return jsonify(response) 

@app.route('/_get_panel' , methods=["GET"])
def get_panel():
        miUid = request.cookies.get('uPoll')
        sqlV = f"SELECT COUNT(*) FROM `votos_opciones` WHERE id_user = '{miUid}' " 
        cantVotos = getData(sqlV)
        sql = f"SELECT * FROM encuesta where id_user = '{miUid}' order by id desc " 
        #buscar por uid las encuestas q tenga en la db 
        encuesta = getData(sql)
        data = []
        if encuesta:
                for row in encuesta:
                        #buscar cantidad de votos 
                        idEncuesta=row[0]
                        sqlVO = f"SELECT COUNT(*) FROM `votos_opciones` WHERE  id_encuesta = '{idEncuesta}' " 
                        cantVotoO = getData(sqlVO)
                        data.append({
                        'id': row[0],
                        'pregunta': row[1],
                        'codigo': row[3],
                        'fecha':   time_passed(str(row[4])),
                        'cantVoto': cantVotoO[0][0]
                        })

                response = {
                'encuestas': data,
                'cantVotos': cantVotos[0][0],
                'cantEncuestas': len(encuesta),
                'status': 1,
                }

        else:
                response = {
                'status': 0,
                }
        return jsonify(response)

        

@app.route('/_guardar_encuesta' , methods=["POST"])
def guardar_encuesta():
    pregunta = request.form.get('pregunta', '', type=str)
    opciones = request.form.get('opciones', '', type=str)
    miCodigo = request.form.get('miCodigo', '', type=str)

    miUid = request.cookies.get('uPoll')
    misOpciones = json.loads(opciones)
    #ahora a guardar los datos 
    sql = f"""
            INSERT INTO encuesta ( pregunta, id_user, cod, fecha) VALUES ( '{pregunta}',
             '{miUid}', '{miCodigo}', '{datetime.now()}'  ) 
                 """ 
    id_encuesta = updateData(sql)
    #crear qr
    data = url_site+miCodigo
    QRCodefile = "app/static/img/qr/QR_"+miCodigo+".png"
    QRimage = qrcode.make(data)
    QRimage.save(QRCodefile)


    for op in misOpciones:
            sql = f"""
            INSERT INTO opcion_encuesta ( opcion, id_encuesta) VALUES ( '{op}',
             '{id_encuesta}' ) 
                 """ 
            actualizar = updateData(sql)

    response = {
        'status': actualizar,
        'codigo': miCodigo,
        }
    return jsonify(response)

@app.route('/_guardar_encuesta_editar' , methods=["POST"])
def guardar_encuesta_editar():
        pregunta = request.form.get('pregunta', '', type=str)
        miCodigo = request.form.get('codigo', '', type=str)
        opciones = request.form.get('opciones', '', type=str)
        opcionesNuevas = request.form.get('opcionesNuevas', '', type=str)
        miUid = request.cookies.get('uPoll')
        misOpciones = json.loads(opciones)
        misOpcionesNuevas = json.loads(opcionesNuevas)
        #buscar si soy el due���o de la encuesta 
        sql = f"SELECT * FROM encuesta where cod = '{miCodigo}' and id_user = '{miUid}' " 
        
        #buscar por uid las encuestas q tenga en la db 
        busEncuesta = getDataOne(sql)
        id_encuesta = busEncuesta[0]
        if busEncuesta:
                #ahora a guardar los datos 
                sql = f"""
                        update encuesta set pregunta = '{pregunta}', fecha = '{datetime.now()}' 
                        where cod = '{miCodigo}'
                                """ 
                updateEncuesta = updateData(sql)
                for op in misOpciones:
                        opcionTexto = op["opcion"]
                        opcionId = op["id"]
                        sql = f"""
                        update opcion_encuesta set opcion = '{opcionTexto}' where id = '{opcionId}' and id_encuesta = '{id_encuesta}' 
                                """ 
                        actualizar = updateData(sql)
                #ahora insertar las nuevas
                for op2 in misOpcionesNuevas:
                        sql = f"""
                        INSERT INTO opcion_encuesta ( opcion, id_encuesta) VALUES ( '{op2}',
                        '{id_encuesta}' ) 
                        """ 
                        actualizar = updateData(sql)


                response = {
                'status': 1,
                }
                
        else:
                response = {
                'status': 0,
                }

        return jsonify(response)
                


@app.route('/_get_encuesta_editar' , methods=["GET"])
def get_encuesta_editar():
        codigo = request.args.get('codigo', '')
        sql = f"SELECT * FROM encuesta where cod = '{codigo}'  " 
        encuesta = getDataOne(sql)
        idEncuesta = encuesta[0]
        sql2 = f"SELECT * FROM opcion_encuesta where id_encuesta = {idEncuesta}  " 
        opciones = getData(sql2)
        data = []
        for row in opciones:
                #debo saber si ya hay votos en esta opción
                opcion = row[0]
                sql4 = f"SELECT * FROM votos_opciones where id_encuesta = {idEncuesta} and id_opcion = '{opcion}'  "
                siVote = 0 
                votos = getData(sql4)
                if votos:
                        siVote = 1
                data.append({
                        "id" : row[0],
                        "opcion": row[1], 
                        "siVote": siVote
                }
                        
                        )
        
        response = {
                'opciones': data,
                'encuesta': encuesta, 
                
                }
        return jsonify(response) 

@app.route('/_delete_option_encuesta' , methods=["GET"])
def delete_option_editar():
        cod_encuesta = request.args.get('cod_encuesta', '')
        id_opcion = request.args.get('id_opcion', '')
        miUid = request.cookies.get('uPoll')
        #consultar si la encuesta es del usuario
        sql = f"SELECT * FROM encuesta where cod = '{cod_encuesta}' and id_user = '{miUid}'  " 
        encuesta = getDataOne(sql)
        if encuesta:
                #eliminar la opcion con el id de la encuesta 
                id_encuesta = encuesta[0]
                sql = f"""
                DELETE FROM `opcion_encuesta` WHERE id = '{id_opcion}' and id_encuesta = '{id_encuesta}'
                        """ 
                actualizar = updateData(sql)
                sql = f"""
                DELETE FROM `votos_opciones` WHERE id_opcion = '{id_opcion}' and id_encuesta = '{id_encuesta}'
                        """ 
                actualizar = updateData(sql)
                #buscar las opciones que quedan 
                sql2 = f"SELECT * FROM opcion_encuesta where id_encuesta = {id_encuesta}  " 
                opciones = getData(sql2)
                data = []
                for row in opciones:
                        data.append({
                        "id" : row[0],
                        "opcion": row[1]
                         } )

                response = {
                'status': 1,
                'opciones': data
                }
                return jsonify(response) 
        else:
                response = {
                'status': 0,
                }
                return jsonify(response)


        

#delete encuesta 
@app.route('/_delete_encuesta' , methods=["GET"])
def delete_encuesta():
        id_encuesta =  request.args.get('id', '', type=str)
        miUid = request.cookies.get('uPoll')
        #consultar si la encuesta es del usuario
        sql = f"DELETE FROM `encuesta` WHERE id = '{id_encuesta}' and id_user = '{miUid}' " 
        delete = deleteData(sql)
        if delete:
                #eliminar la opcion con el id de la encuesta 
                sql = f"""
                DELETE FROM `opcion_encuesta` WHERE  id_encuesta = '{id_encuesta}'
                        """ 
                actualizar = deleteData(sql)
                sql = f"""
                DELETE FROM `votos_opciones` WHERE  id_encuesta = '{id_encuesta}'
                        """ 
                actualizar = deleteData(sql)
                #buscar las encuestas que le quedan
                sql = f"SELECT * FROM encuesta where id_user = '{miUid}'  " 
                #buscar por uid las encuestas q tenga en la db 
                encuesta = getData(sql)
                data = []
                for row in encuesta:
                        data.append({
                        'id': row[0],
                        'pregunta': row[1],
                        'codigo': row[3],
                        'fecha':   str(row[4]),
                        })

                response = {
                'encuestas': data,
                'status': 1,
                }

                return jsonify(response) 
        else:
                response = {
                'status': 0,
                }
                return jsonify(response)



@app.route('/_get_encuesta' , methods=["GET"])
def get_encuesta():
        codigo = request.args.get('codigo', '')
        resultado = codigo[-1:]
        if resultado == '+':
                resultado = 1
        else:
                resultado = 0
        codigo = codigo[0:5]
        
        sql = f"SELECT * FROM encuesta where cod = '{codigo}'  " 
        #buscar por uid las encuestas q tenga en la db 
        encuesta = getDataOne(sql)
        data = []
        if encuesta:
                idEncuesta = encuesta[0]
                sql2 = f"SELECT * FROM opcion_encuesta where id_encuesta = {idEncuesta}  " 
                print(sql2)
                opciones = getData(sql2)
                if opciones:
                        #buscar votos 
                        sql3 = f"SELECT * FROM votos_opciones where id_encuesta = {idEncuesta}  " 
                        print(sql3)
                        votos = getData(sql3)
                        totalVotos = len(votos)
                        descripcionMeta = ''
                        i = 0
                        for row in opciones:
                                #sacar porcentaje 
                                id_opcion = row[0]
                                sql4 = f"SELECT * FROM votos_opciones where id_encuesta = {idEncuesta} and id_opcion = {id_opcion}  "
                                print(sql4) 
                                voto_opcion = getData(sql4)
                                if voto_opcion:
                                        total_voto_opcion = len(voto_opcion)
                                        porcentaje = (total_voto_opcion * 100) / totalVotos
                                        color = i
                                else:
                                        porcentaje = 0
                                        total_voto_opcion = 0
                                        color = 10
                                if i==0:
                                        descripcionMeta = descripcionMeta + str((i+1))+')'+row[1]
                                else:
                                        descripcionMeta = descripcionMeta + ', '+str((i+1))+')'+row[1]
                                
                                data.append({
                                'id': row[0],
                                'valor': row[1],
                                'porcentaje':   "{:.2f}".format(float(porcentaje)),
                                'totalVoto': total_voto_opcion, 
                                'color': color
                                })

                                #buscar por uid si vote en la encuesta
                                miUid = request.cookies.get('uPoll')
                                sql3 = f"SELECT * FROM votos_opciones where id_user = '{miUid}' and id_encuesta = '{idEncuesta}'  " 
                                voto = getDataOne(sql3)
                                
                                if voto:
                                        siVote = 1
                                        miVoto= voto[1]
                                else:
                                        siVote = 0
                                        miVoto= 0
                                
                                i=i+1

                        response = {
                        'totalVotos': totalVotos,
                        'opciones': data,
                        'encuesta': encuesta,
                        'siVote': siVote, 
                        'meta':descripcionMeta, 
                        'resultado': resultado, 
                        'miVoto': miVoto
                        }

                        
                        return jsonify(response) 
        else:
                response =0
                return jsonify(response) 



@app.route('/_votar_' , methods=["GET"])
def votar_encuesta():
        id_opcion = request.args.get('id_opcion', '')
        id_encuesta = request.args.get('id_encuesta', '')
        #buscar si el usuario ya voto en esta encuesta 
        miUid = request.cookies.get('uPoll')
        sql2 = f"SELECT * FROM votos_opciones where id_encuesta = {id_encuesta} and id_user = '{miUid}'    " 
        print(sql2)
        opciones = getData(sql2)
        print(opciones)
        if opciones:
                return jsonify(result = 2) 
        else:
                print("no voto")
                #guardar la votacion nueva 
                sql = f"""
                INSERT INTO votos_opciones ( id_opcion, id_user, id_encuesta, fecha) VALUES ( '{id_opcion}',
                '{miUid}', '{id_encuesta}', '{datetime.now()}'  ) 
                """ 
                actualizar = updateData(sql)
                if actualizar:
                        socketio.emit('respuestaDelVoto', 'votaste')
                        return jsonify(result = 1) 
                else:
                        return jsonify(result = 0) 



@app.route('/_cancelar_voto' , methods=["GET"])
def cancelar_voto():
        id_encuesta = request.args.get('id_encuesta', '')
        miUid = request.cookies.get('uPoll')
        sql = f"""
        DELETE FROM `votos_opciones` WHERE  id_encuesta = '{id_encuesta}' and id_user = '{miUid}'
                """ 
        actualizar = deleteData(sql)
        response = {
        'status': actualizar,
        }
        socketio.emit('respuestaDelVoto', 'votaste')
        return jsonify(response) 


@app.route('/_sortear1' , methods=["GET"])
def sortear1():
        participantes = request.args.get('participantes', '')
        premios = request.args.get('premios', '')
        y = json.loads(participantes)
        #cantidad de participantes 
        cantParticipantes = len(y)
        #lista de ganadores 
        ganadores = []
        while len(ganadores) < int(premios):
                #generamos numero aleatorio
                n = random.randint(1, cantParticipantes)
                if n not in ganadores:
                        #si no existe lo agrego 
                        ganadores.append(y[(n-1)])

        
        response = {
        'status': 1,
        'participantes': y, 
        'ganadores': ganadores
        }
        return jsonify(response) 


#sockets
@socketio.on('conectar')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('realizoVoto')
def realizoVoto(data):
    app.logger.info("{} has votado in the room {}".format(data['username'], data['room']))
    socketio.emit('respuestaDelVoto', data, room=data['room'])