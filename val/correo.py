import smtplib #importamos smtplib para el envio de correos electronicos

def mail(msg):
    #Guardamos el mensaje dentro de una variable
    message = msg
    #Guardamos dentro de una variable el mensaje que queremos mostrar como asunto
    subject = "Excepcion encontrada"
    #Dentro de la variable mandamos el formato del mensaje donde
    #Especificamos que 'subject' ira como Asunto
    #y 'message' ira como mensaje 
    message = 'Subject: {}\n\n{}'.format(subject, message)
    #Realizamos la activacion del servicio de Gmail
    #especificando su protocolo y puerto 
    #lo guardamos dentro de una variable
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #Activamos el servicio de Gmail
    server.starttls()
    #Iniciamos sesión con un correo valido y una contraseña
    #NOTA: La contraseña puede o no funcionar
    #en este caso es una contraseña generada especificamente para esto
    server.login('hramonbf@gmail.com', 'clzqmbayjodeslci')
    #Enviamos el correo electronico
    #Especificando el correo que lo envia, a quien va dirigido, y el mensaje
    server.sendmail('hramonbf@gmail.com', 'hbarruetaf97@gmail.com', message)
    #IMPORTANTE. Apagar el servidor 
    server.quit()
