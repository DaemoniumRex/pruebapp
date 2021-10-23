import os

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from markupsafe import escape  # Evitar inyección de código
from werkzeug.security import check_password_hash, generate_password_hash

from formularios import Login, Registro,fbforma
from utils import email_valido, login_valido, pass_valido
from dblala import accion, seleccion

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def ppal():
    return render_template('index2.html')


@app.route('/entrar/', methods=['GET', 'POST'])
def login():

    frm = Login()

    if request.method == 'GET':
        return render_template('Index.html',titulo='GRUPO LALA :: Login')
    else:

        # Será un código con mitigación de riesgo
        #user = escape(frm.usr.data.strip())
        #passw = escape(frm.pwd.data.strip())
        user = escape(request.form['user'].strip())
        passw = escape(request.form['pass'].strip())
    # Preparar la consulta - No paramétrica
        sql = f"SELECT identificacion, nombre, usuario, password,perfil FROM empleados WHERE usuario='{user}' AND estado='A'"
        # Ejecutar la consulta

        res = seleccion(sql)
        # Procesar los resultados
        

        if len(res) == 0:

            flash('ERROR: Usuario o contraseña invalidos')
            return render_template('Index.html', titulo='GRUPO LALA :: Login')
        else:
            # Recupero la clave almacenada en la base de datos - cifrada
            cbd = res[0][3]
            # Comparo contra la clave suminstrada por el usuario
            if check_password_hash(cbd, passw):
                # Se guardarán los datos del usuario en una variable de sesion
                session.clear()
                session['id'] = res[0][0]
                session['nom'] = res[0][1]
                session['usr'] = user
                session['cla'] = passw
                session['ema'] = res[0][2]
                session['perf'] = res[0][4]
                return redirect(url_for('inicio'))
            else:
                flash('ERROR: Usuario o contraseña invalidos')
                return render_template('Index.html', titulo='GRUPO LALA :: Login',session=session)

@app.route('/vperfil/')
def profile():
    sql = f"SELECT * FROM empleados WHERE identificacion='{session['id']}'"
    res=seleccion(sql)
    return render_template('vperfil.html', titulo='GRUPO LALA :: Perfil de Empleado', emple=res)

@app.route('/inicio3/')
def inicio3():
    
    sql = f"SELECT identificacion,nombre,apellidos,tipo_contrato  FROM empleados WHERE estado='A'"
    res=seleccion(sql)
    return render_template('listar.html',emple=res,msg='DATOS ELIMINADOS CON EXITO!')


@app.route('/inicio2/')
def inicio2():
    
    sql = f"SELECT identificacion,nombre,apellidos,tipo_contrato  FROM empleados WHERE estado='A'"
    res=seleccion(sql)
    return render_template('listar.html',emple=res,msg='DATOS EDITADOS CON EXITO!')

@app.route('/inicio/')
def inicio():
    sql = f"SELECT identificacion,nombre,apellidos,tipo_contrato  FROM empleados WHERE estado='A'"
    res=seleccion(sql)
    return render_template('listar.html',emple=res)
    

@app.route('/cargar/<id>')
def get_data(id):
    sql = f"SELECT * FROM empleados WHERE identificacion='{id}'"
    res=seleccion(sql)
    
    return render_template('editar2.html',datos=res)
  
@app.route('/edit/', methods=['POST'])
def editar12():
    
        nom = escape(request.form['nom'])
        ema = escape(request.form['ema'])
        cla = escape(request.form['cla'])
        #verc = escape(request.form['ver'])
        ident = escape(request.form['id'])
        tipo_id = escape(request.form['tipo_id'])
        apellidos = escape(request.form['apellidos'])
        genero = escape(request.form['genero'])
        fecha_naci = escape(request.form['fecha_nac'])
        fecha_ing = escape(request.form['fecha_ingreso'])
        fin_contrato = escape(request.form['fin_contrato'])
        tipo_cont = escape(request.form['tipoContrato'])
        cargo = escape(request.form['cargo'])
        depen = escape(request.form['dependencia'])
        sal = escape(request.form['salario'])
        perfil = escape(request.form['rol'])
        telefono = escape(request.form['tel'])
        dir = escape(request.form['dir'])
        observacion = escape(request.form['observacion'])

         # validar datos
        swerror = False
        if nom == None or len(nom) == 0:
            flash('ERROR: Debe suministrar un nombre de usuario')
            swerror = True
        if apellidos == None or len(apellidos) == 0:
            flash('ERROR: Debe suministrar un apellido de usuario')
            swerror = True
        if ema == None or len(ema) == 0 or not email_valido(ema):
            flash('ERROR: Debe suministrar un email válido')
            swerror = True
        if cla == None or len(cla) == 0 or not pass_valido(cla):
            flash('ERROR: Debe suministrar una clave válida')
            swerror = True
        """if verc ==None or len(verc)==0 or not pass_valido(verc):
                flash('ERROR: Debe suministrar una verificación de clave válida')
                swerror = True
            if cla !=verc:
                flash('ERROR: La clave y la verificación no coinciden')
                swerror = True"""
        if ident == None or len(ident) == 0:
            flash('ERROR: Debe suministrar una identificacion valida')
            swerror = True
        if tipo_id == None or len(tipo_id) == 0:
            flash('Elija una opcion valida')
            swerror = True
        if genero==None or genero == 'Elige una opción...':
            flash('Elija una opcion valida')
            swerror = True
        if fecha_naci == None or len(fecha_naci) == 0:
            flash('Suministre una fecha valida')
            swerror = True
        if fecha_ing == None or len(fecha_ing) == 0:
            flash('Suministre una fecha valida')
            swerror = True
        if fin_contrato == None or len(fin_contrato) == 0:
            flash('Suministre una fecha valida')
            swerror = True
        if tipo_cont == None or len(tipo_cont) == 0:
            flash('Suministre un tipo de Contrato')
            swerror = True
        if cargo == None or len(cargo) == 0:
            flash('ERROR: Debe suministrar su cargo')
            swerror = True
        if depen == None or len(depen) == 0:
            flash('ERROR: Debe suministrar su dependencia')
            swerror = True
        if sal == None or len(sal) == 0:
            flash('ERROR: Debe suministrar su salario')
            swerror = True
        if perfil == None or len(perfil) == 0:
            flash('ERROR: Debe suministrar su perfil')
            swerror = True
        if telefono == None or len(telefono) == 0:
            flash('ERROR: Debe suministrar su telefono/s')
            swerror = True
        if dir == None or len(dir) == 0:
            flash('ERROR: Debe suministrar su direccion')
            swerror = True

        if not swerror:
            sql = f"SELECT identificacion FROM empleados WHERE identificacion='{ident}'"
            
            res = seleccion(sql)
            if len(res)!=0:
                res2=str(res[0]).replace("(","")
                res3=str(res2).replace(")","")
                res4=str(res3).replace(",","")
                res5=str(res4).replace("'","")
            else:
                res5=0
            
            if len(res)==0 or res5==ident :
                sql = f"SELECT  usuario FROM empleados WHERE usuario='{ema}'"
                res = seleccion(sql)

                if len(res) == 0:
                   

                    # Preparar el query -- Paramétrico
                    sql = f"UPDATE empleados SET identificacion=?,tipo_id=?,nombre=?,apellidos=?,genero=?,fecha_nacimiento=?,fecha_ingreso=?,fin_contrato=?,tipo_contrato=?,cargo=?,dependencia=?,salario=?,usuario=?,password=?,perfil=?,telefono=?,direccion=?,observaciones=? WHERE identificacion='{ident}'"
                    # Ejecutar la consulta
                    pwd = generate_password_hash(cla)
                    res = accion(sql, (ident, tipo_id, nom, apellidos, genero, fecha_naci, fecha_ing,
                                 fin_contrato, tipo_cont, cargo, depen, sal, ema, pwd, perfil, telefono, dir, observacion))
                    # Proceso los resultados
                    if res == 0:
                        flash('ERROR: No se pudieron Editar los datos, reintente')
                    else:
                        flash('INFO: Los datos fueron EDITADOS satisfactoriamente')
                        
                else:
                    sql = f"SELECT  usuario FROM empleados WHERE identificacion='{ident}'"
                    res = seleccion(sql)
                    if len(res)!=0:
                        res2=str(res[0]).replace("(","")
                        res3=str(res2).replace(")","")
                        res4=str(res3).replace(",","")
                        res5=str(res4).replace("'","")
                    else:
                        res5=0

                    if ema==res5:
                        sql = f"UPDATE empleados SET identificacion=?,tipo_id=?,nombre=?,apellidos=?,genero=?,fecha_nacimiento=?,fecha_ingreso=?,fin_contrato=?,tipo_contrato=?,cargo=?,dependencia=?,salario=?,usuario=?,password=?,perfil=?,telefono=?,direccion=?,observaciones=? WHERE identificacion='{ident}'"
                        # Ejecutar la consulta
                        pwd = generate_password_hash(cla)
                        res = accion(sql, (ident, tipo_id, nom, apellidos, genero, fecha_naci, fecha_ing,
                                    fin_contrato, tipo_cont, cargo, depen, sal, ema, pwd, perfil, telefono, dir, observacion))
                        # Proceso los resultados
                        if res == 0:
                            flash('ERROR: No se pudieron Editar los datos, reintente')
                        else:
                            flash('INFO: Los datos fueron EDITADOS satisfactoriamente')   
                    else: 
                        flash('INFO: NO PUEDE EDITAR LA DOCUMENTO DE IDENTIDAD Y CORREO DE MANERA SIMULTANEA')
            else:
                flash('ERROR: esta intentando EDITAR un usuario que no existe en la BASE DE DATOS')
          
        return redirect(url_for('inicio2'))
       

@app.route('/delete/<ide>')
def delete_emple(ide):
    sql=f"UPDATE empleados SET estado='I' WHERE identificacion=?"
    accion(sql,(ide,))
    
    return redirect(url_for('inicio3'))
        


@app.route('/crear/', methods=['GET', 'POST'])
def create():
    frm = Registro()
    if request.method == 'GET':
        return render_template('crear.html', formCrear=frm, titulo='GRUPO LALA :: Crear Empleado')
    else:
        nom = escape(request.form['nom'])
        ema = escape(request.form['ema'])
        cla = escape(request.form['cla'])
        #verc = escape(request.form['ver'])
        ident = escape(request.form['id'])
        tipo_id = escape(request.form['tipo_id'])
        apellidos = escape(request.form['apellidos'])
        genero = escape(request.form['gen'])
        fecha_naci = escape(request.form['fecha_nac'])
        fecha_ing = escape(request.form['fecha_ingreso'])
        fin_contrato = escape(request.form['fin_contrato'])
        tipo_cont = escape(request.form['tipo_contrato'])
        cargo = escape(request.form['cargo'])
        depen = escape(request.form['dependencia'])
        sal = escape(request.form['salario'])
        perfil = escape(request.form['perfil'])
        telefono = escape(request.form['tel'])
        dir = escape(request.form['dir'])
        observacion = escape(request.form['observacion'])

        # validar datos
        swerror = False
        if nom == None or len(nom) == 0:
            flash('ERROR: Debe suministrar un nombre de usuario')
            swerror = True
        if apellidos == None or len(apellidos) == 0:
            flash('ERROR: Debe suministrar un apellido de usuario')
            swerror = True
        if ema == None or len(ema) == 0 or not email_valido(ema):
            flash('ERROR: Debe suministrar un email válido')
            swerror = True
        if cla == None or len(cla) == 0 or not pass_valido(cla):
            flash('ERROR: Debe suministrar una clave válida')
            swerror = True
        """if verc ==None or len(verc)==0 or not pass_valido(verc):
                flash('ERROR: Debe suministrar una verificación de clave válida')
                swerror = True
            if cla !=verc:
                flash('ERROR: La clave y la verificación no coinciden')
                swerror = True"""
        if ident == None or len(ident) == 0:
            flash('ERROR: Debe suministrar una identificacion valida')
            swerror = True
        if tipo_id == None or len(tipo_id) == 0:
            flash('Elija una opcion valida')
            swerror = True
        if genero == 'Elige una opción...':
            flash('Elija una opcion valida')
            swerror = True
        if fecha_naci == None or len(fecha_naci) == 0:
            flash('Suministre una fecha valida')
            swerror = True
        if fecha_ing == None or len(fecha_ing) == 0:
            flash('Suministre una fecha valida')
            swerror = True
        if fin_contrato == None or len(fin_contrato) == 0:
            flash('Suministre una fecha valida')
            swerror = True
        if tipo_cont == None or len(tipo_cont) == 0:
            flash('Suministre un tipo de Contrato')
            swerror = True
        if cargo == None or len(cargo) == 0:
            flash('ERROR: Debe suministrar su cargo')
            swerror = True
        if depen == None or len(depen) == 0:
            flash('ERROR: Debe suministrar su dependencia')
            swerror = True
        if sal == None or len(sal) == 0:
            flash('ERROR: Debe suministrar su salario')
            swerror = True
        if perfil == None or len(perfil) == 0:
            flash('ERROR: Debe suministrar su perfil')
            swerror = True
        if telefono == None or len(telefono) == 0:
            flash('ERROR: Debe suministrar su telefono/s')
            swerror = True
        if dir == None or len(dir) == 0:
            flash('ERROR: Debe suministrar su direccion')
            swerror = True

        if not swerror:
            sql = f"SELECT identificacion FROM empleados WHERE identificacion='{ident}'"

            res = seleccion(sql)
            if len(res) == 0:
                sql = f"SELECT  usuario FROM empleados WHERE usuario='{ema}'"

                res = seleccion(sql)
                if len(res) == 0:

                    # Preparar el query -- Paramétrico
                    sql = "INSERT INTO empleados(identificacion, tipo_id, nombre, apellidos, genero, fecha_nacimiento, fecha_ingreso, fin_contrato, tipo_contrato, cargo, dependencia, salario, usuario, password, perfil, telefono, direccion, observaciones) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    # Ejecutar la consulta
                    pwd = generate_password_hash(cla)
                    res = accion(sql, (ident, tipo_id, nom, apellidos, genero, fecha_naci, fecha_ing,
                                 fin_contrato, tipo_cont, cargo, depen, sal, ema, pwd, perfil, telefono, dir, observacion))
                    # Proceso los resultados
                    if res == 0:
                        flash('ERROR: No se pudieron almacenar los datos, reintente')
                    else:
                        flash('INFO: Los datos fueron almacenados satisfactoriamente')
                        return redirect(url_for('create'))
                else:
                    flash('ERROR: este usuario(email) ya existe')
            else:
                flash('ERROR: este numero de identificación ya existe')
        return render_template('crear.html', formCrear=frm, titulo='Registro de datos')




@app.route('/vretro/<id>',methods=['GET'])
@app.route('/vretro/',methods=['POST'])
def vretro(id=None):
    frm = fbforma()
    if request.method == 'GET':
        
      return render_template('retro.html', fbcrear=frm,valor=id, titulo='crear retroalimentacion')
    else:
        # Recuperar los datos del formulario
        # Esta forma permite validar las entradas

        id = escape(request.form['id'])
        fecha = escape(request.form['fecha'])
        cp = escape(request.form['cp'])
        mt = escape(request.form['mt'])
        tw = escape(request.form['tw'])
        act = escape(request.form['act'])
        cul = escape(request.form['cul'])
        emp = escape(request.form['emp'])
        obs = escape(request.form['obs'])
        #pun = escape(request.form['pun'])
        

       
        # Validar los datos
        swerror = False
       
        if fecha==None :
            flash('ERROR: Debe indicar un asunto')
            swerror = True
        if cp==None :
            flash('ERROR: Debe indicar un asunto')
            swerror = True
        if mt==None :
            flash('ERROR: Debe indicar un asunto')
            swerror = True    
        if tw==None :
            flash('ERROR: Debe indicar un asunto')
            swerror = True   
        if act==None :
            flash('ERROR: Debe indicar un asunto')
            swerror = True
        if cul==None :
            flash('ERROR: Debe indicar un asunto')
            swerror = True
        if emp==None :
            flash('ERROR: Debe indicar un asunto')
            swerror = True


        respun = ((int(cp) + int(mt) + int(tw) + int(act) + int(cul) + int(emp) )/6)

        if not swerror:
            sql = "INSERT INTO feedback(fecha, cuid_per, man_time, team_work, actitud, cultura, empatia, observaciones, puntaje, identificacion) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            res = accion(sql, (fecha, cp, mt, tw, act, cul, emp, obs, respun, id))
        if res==0:
                flash('ERROR: No se pudo enviar el mensaje, reintente')
        else:
                flash('INFO: Su mensaje fue enviado satisfactoriamente')
        return render_template('retro.html', fbcrear=frm, titulo='crear retroalimentacion')
        


@app.route('/buscar/', methods=['GET', 'POST'])
def buscar():
    if request.method == 'GET':
        print("prueba entro al GET")
        return render_template('buscar.html',  titulo='GRUPO LALA :: Buscar')

    else:
        busc=escape(request.form['buscarTxt'])
        print("prueba",busc)
        # Preparar la consulta
        sql = f"SELECT identificacion,nombre,apellidos,tipo_contrato FROM empleados WHERE identificacion like '%{busc}%' or nombre like '%{busc}%'  "

        # Ejecutar la consulta
        res = seleccion(sql)
        # Proceso los resultados
        if len(res)==0:
            tit = f"No se encontraron empleados "
            res = 0
        else:
            tit = f"Se muestran los empleados "
        return render_template('buscar.html', titulo=tit, res=res, buscar=busc)   




"""@app.route('/buscar/', methods=['GET'])
def search():
    if 'usuario' in session:
        usuario = session['usuario']
    return render_template('buscar.html', titulo='GRUPO LALA :: Buscar Empleado', usuario=usuario)"""


@app.route('/salir/')
def salir():
    
    session.pop('usr', None)
    session.clear()
    return render_template('Index.html', titulo='GRUPO LALA :: Login')





if __name__ == '__main__':
    app.run(debug=True, port=8080)
