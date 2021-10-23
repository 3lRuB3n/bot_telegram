#Este es un bot para controlar un equipo de musica
#Mas info en https://github.com/3lRuB3n/bot_telegram/

import telebot
from telebot import types
import time
import os

TOKEN = '1950473547:AAEsbgLLkeNCm4ZxuMcH2d5HQDE_WAcF2eg'

knownUsers = [681682244] # todo: save these in a file,
userStep = {} # so they won't reset every time the bot restarts

commands = { # command description used in the "help" command
            'ayuda': 'Da informacion sobre los comandos disponibles'
            ,'exec': 'Ejecuta un comando'
            ,'temp': 'Comprueba la temperatura de la raspberry'
            ,'reinicia': 'Reinicia el equipo'
            ,'apaga': 'Apaga el equipo'
            ,'actualizar_equipo': 'Descarga, instala y elimina los paquetes de software'
#            ,'actualizar_bot': 'Descarga la última versión del bot en el repositorio de github: https://github.com/3lRuB3n/bot_telegram'
}



hideBoard = types.ReplyKeyboardRemove() # if sent as reply_markup, will hide the keyboard

# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
# had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print "New user detected, who hasn't used \"/start\" yet"
        return 0

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener) # register listener

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        command_help(m) # show the new user the help page

# help page
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Estos son los comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)

@bot.message_handler(func=lambda message: message.text == "Ponme sonidos de ambiente")
def command_text_hi(m):
    bot.send_message(m.chat.id, "¿Alguno en concreto?")
    mensaje = "Estos son los disponibles:"
    for sfx in os.listdir("/home/pi/sfx"):
        mensaje = mensaje + "\n\t" + sfx
    bot.send_message(m.chat.id, mensaje)

# Reinicia servidor
@bot.message_handler(commands=['reinicia'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Voy a reiniciar el equipo...")
    bot.send_chat_action(cid, 'typing')
    time.sleep(3)
    bot.send_message(cid, ".")
    os.system("sudo shutdown -r now")

#Apaga el servidor
@bot.message_handler(commands=['apaga'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Voy a apagar el equipo...")
    bot.send_chat_action(cid, 'typing')
    time.sleep(3)
    bot.send_message(cid, ".")
    os.system("sudo shutdown now")
    
#Actualiza el equipo
@bot.message_handler(commands=['actualizar_equipo'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Descargando paquetes...")
    bot.send_chat_action(cid, 'typing')
    os.system("sudo apt-get update -y")   #update
    result = f.read()
    bot.send_message(cid, ""+result)
    
    bot.send_message(cid, "Instalando paquetes...")
    bot.send_chat_action(cid, 'typing')
    os.system("sudo apt-get upgrade -y")   #upgrade
    result = f.read()
    bot.send_message(cid, ""+result)
    
    bot.send_message(cid, "Eliminando paquetes...")
    bot.send_chat_action(cid, 'typing')
    os.system("sudo apt-get autoremove -y")   #eliminar dependencias
    result = f.read()
    bot.send_message(cid, ""+result)
    os.system("sudo apt-get autoclean -y")    #elimina paquetes antiguos
    result = f.read()
    bot.send_message(cid, ""+result)

"""# Descarga telegram_bot.py
@bot.message_handler(commands=['actualizar_bot'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Este comando va a eliminar el script actual y lo sustituira por el de GitHub")
    bot.send_message(cid, "¿Estas seguro de que quieres hacerlo, el equipo tendrá que reiniciarse?")
    
    @bot.message_handler(func=lambda message: message.text == "Si")
    if message.text == "Si":
        def command_text_hi(m):
        bot.send_message(m.chat.id, "Ahora mismo")
        
        os.system("./actualizar_bot.sh")
        result = f.read()
        bot.send_message(cid, ""+result)
"""

# Mira temperaturas
@bot.message_handler(commands=['temp'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Vamos a comprobar si has puesto caliente a tu equipo...")
    bot.send_chat_action(cid, 'typing') # show the bot "typing" (max. 5 secs)
    time.sleep(2)
    f = os.popen("temperatura")
    result = f.read()
    bot.send_message(cid, ""+result)

# Ejecuta un comando
@bot.message_handler(commands=['exec'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Ejecutando: "+m.text[len("/exec"):])
    bot.send_chat_action(cid, 'typing') # show the bot "typing" (max. 5 secs)
    time.sleep(2)
    f = os.popen(m.text[len("/exec"):])
    result = f.read()
    bot.send_message(cid, "Resultado: "+result)


#@bot.message_handler(func=lambda message: message.text == "Texto_entrada")
#def command_text_hi(m):
#    bot.send_message(m.chat.id, "Texto_salida")

#Esto responde a mensajes especificos


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No te entiendo, prueba con /ayuda")

bot.polling()