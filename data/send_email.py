# -*- coding: utf-8 -*-

#código base: https://humberto.io/pt-br/blog/enviando-e-recebendo-emails-com-python/

#email_from = {'login':'email@gmail.com','password':'senha_do_email'}
#emails_to = ['email@exemplo.com','email2@exemplo.com']

import smtplib
from email.mime.text import MIMEText

def send_email (assunto,mensagem):
    # conexão com os servidores do google
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    # username ou email para logar no servidor
    username = email_from['login']
    password = email_from['password']
    
    from_addr = email_from['login']
    to_addrs = emails_to
    
    # a biblioteca email possuí vários templates
    # para diferentes formatos de mensagem
    # neste caso usaremos MIMEText para enviar
    # somente texto
    try:
        message = MIMEText(mensagem)
        message['subject'] = assunto
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)
        
        # conectaremos de forma segura usando SSL
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        # para interagir com um servidor externo precisaremos
        # fazer login nele
        server.ehlo()
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()
    except NameError:
        print("""
A funcionalidade de enviar mensagens de erro por e-mail está desativada.
Para ativá-la, siga as instruções no arquivo README.""")
    
    
