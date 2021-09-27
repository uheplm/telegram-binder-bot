import enstrings as strings
import telebot
from telebot import types
import cfg
import json
import re
import random
import multitasking
from threading import Thread
# open db.json and loading this
with open("db.json") as data:
    storage = json.loads(data.read())
with open("admins.json") as data:
    admins = json.loads(data.read())

REQUIRES = {
    'pin':'pin',
    'pinl':'pin',
    'kick':'ban',
    'mute_f':'ban',
    'mute_d':'ban',
    'mute_w':'ban',
    'mute_m':'ban',
    'mute_h':'ban',
    'unban':'ban',
    'del':'del',
    'none':'none'
}

def user_keyboard(chat_id, i, page):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(
            text=(strings.user_ignore
                  if not storage[chat_id]['members'][i]['IgnoreUser']
                  else strings.user_unignore),
            callback_data='$$iu_' + chat_id + ':::' + i
        )
    )
    keyboard.row(
        types.InlineKeyboardButton(
            text=(strings.user_disreports
                  if not storage[chat_id]['members'][i]['DisableReports']
                  else strings.user_enreports),
            callback_data='$$dr_' + chat_id + ':::' + i
        )
    )
    keyboard.row(
        types.InlineKeyboardButton(
            text=strings.back,
            callback_data='$$users_' + chat_id + ':::' + page
        )
    )

    return keyboard


def word_keyboard(chat_id, i, page):
    keyboard = types.InlineKeyboardMarkup()
    task = strings.tasks
    if (not i == 'welcome_message' and not storage[chat_id]['keywords'][i]['type'] == 'sticker'):
        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.view,
                callback_data='$$show_' + chat_id + ':::' + i
            ),
            types.InlineKeyboardButton(
                text=strings.word_edit,
                callback_data='$$editt_' + chat_id + ':::' + i
            )
        )

        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.word_type_switch,
                callback_data='$$wts_' + chat_id + ':::' + i
            ),
            types.InlineKeyboardButton(
                text=strings.word_replymode_switch,
                callback_data='$$wrm_' + chat_id + ':::' + i
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.salo
                .format('✅'
                        if storage[chat_id]['keywords'][i]['silent']
                        else '❌'),
                callback_data='$$salo_' + chat_id + ':::' + i
            ),
            types.InlineKeyboardButton(
                text=strings.delafter
                .format('✅'
                        if storage[chat_id]['keywords'][i]['delafter']
                        else '❌'),
                callback_data='$$delaft_' + chat_id + ':::' + i
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.task
                .format(task[storage[chat_id]['keywords'][i]['task']]),
                callback_data='$$task_' + chat_id + ':::' + i
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.tor_card
                .format(strings.tor_self
                        if not storage[chat_id]['keywords'][i]['task_on_reply']
                        else strings.tor_reply),
                callback_data='$$tor_' + chat_id + ':::' + i
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.adminkey
                .format('✅'
                        if storage[chat_id]['keywords'][i]['admin_only']
                        else '❌'),
                callback_data='$$adm_' + chat_id + ':::' + i
            )
        )

        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.disable_key
                if storage[chat_id]['keywords'][i]['enabled']
                else strings.enable_key,
                callback_data='$$dis_' + chat_id + ':::' + i
            ),
            types.InlineKeyboardButton(
                text=strings.delete,
                callback_data='$$del_' + chat_id + ':::' + i
            ),
            types.InlineKeyboardButton(
                text=strings.chance
                .format(storage[chat_id]['keywords'][i]['chance']),
                callback_data='$$cha_' + chat_id + ':::' + i
            ))

        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.back,
                callback_data='$$keys_' + chat_id + ':::' + page
            )
        )
    elif not storage[chat_id]['keywords'][i]['type'] == 'sticker':
        keyboard.row(types.InlineKeyboardButton(
                text = strings.view,
                callback_data = '$$show_'  + chat_id + ':::' + i
            ))
        keyboard.row(types.InlineKeyboardButton(
                text = strings.salo.format('✅' if storage[chat_id]['keywords'][i]['silent'] else '❌'),
                callback_data = '$$salo_'  + chat_id + ':::' + i
            ),
        types.InlineKeyboardButton(
                text = strings.delafter.format('✅' if storage[chat_id]['keywords'][i]['delafter'] else '❌'),
                callback_data = '$$delaft_'  + chat_id + ':::' + i
            ))
        keyboard.row(types.InlineKeyboardButton(
                text = strings.task.format(task[storage[chat_id]['keywords'][i]['task']]),
                callback_data = '$$task_'  + chat_id + ':::' + i
            ))

        keyboard.row(
            types.InlineKeyboardButton(
                text = strings.disable_key if storage[chat_id]['keywords'][i]['enabled'] else strings.enable_key, 
                callback_data = '$$dis_' + chat_id + ':::' + i
            ),
            types.InlineKeyboardButton(
                text = strings.delete, 
                callback_data = '$$del_' + chat_id + ':::' + i
            ))

        keyboard.row(types.InlineKeyboardButton(
                text = strings.back,
                callback_data = '$$keys_'  + chat_id + ':::' + page
            ))
    elif storage[chat_id]['keywords'][i]['type'] == 'sticker':
        keyboard.row(types.InlineKeyboardButton(
                text = strings.delafter.format('✅' if storage[chat_id]['keywords'][i]['delafter'] else '❌'),
                callback_data = '$$delaft_'  + chat_id + ':::' + i
            ))
        keyboard.row(types.InlineKeyboardButton(
                text = strings.task.format(task[storage[chat_id]['keywords'][i]['task']]),
                callback_data = '$$task_'  + chat_id + ':::' + i
            ))
        keyboard.row(types.InlineKeyboardButton(
                text = strings.tor_card.format(strings.tor_self if not storage[chat_id]['keywords'][i]['task_on_reply'] else strings.tor_reply),
                callback_data = '$$tor_'  + chat_id + ':::' + i
            ))
        keyboard.row(types.InlineKeyboardButton(
                text = strings.adminkey.format('✅' if storage[chat_id]['keywords'][i]['admin_only'] else '❌'),
                callback_data = '$$adm_'  + chat_id + ':::' + i
            ))

        keyboard.row(
            types.InlineKeyboardButton(
                text = strings.disable_key if storage[chat_id]['keywords'][i]['enabled'] else strings.enable_key, 
                callback_data = '$$dis_' + chat_id + ':::' + i
            ),
            types.InlineKeyboardButton(
                text = strings.delete, 
                callback_data = '$$del_' + chat_id + ':::' + i
            ))

        keyboard.row(types.InlineKeyboardButton(
                text = strings.back,
                callback_data = '$$keys_'  + chat_id + ':::' + page
            ))
    return keyboard


def chat_keyboard(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    if storage[str(chat_id)]['settings']['ReportFeature']:
        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.user_disreports,
                callback_data = '$$grf_' + chat_id + ':::' + 'off'
                )
            )
    else:
        keyboard.row(
            types.InlineKeyboardButton(
                text=strings.user_enreports,
                callback_data = '$$grf_' + chat_id + ':::' + 'on'
                )
            )
    keyboard.row(types.InlineKeyboardButton(
            text = strings.wm_switch.format('✅' if storage[chat_id]['settings']['welcome_message']['Enable'] else '❌'),
            callback_data = '$$wm_'  + chat_id
        ))
    keyboard.row(types.InlineKeyboardButton(
            text = strings.back,
            callback_data = '$$set_'  + chat_id
        ))
    return keyboard


# helpful functions
def database_keeper(bot):
    def Decorator(fn):
        def Wrapper(msg):
            register_chat(msg)
            register_user(msg)
            try:
                fn(msg)
            except telebot.apihelper.ApiException as e:
                bot.reply_to(
                    msg,
                    strings.task_fail
                    .format(json.loads(e.result.text)['description']
                            .split(':')[1]
                            .strip())
                )
            except Exception as e:
                bot.reply_to(msg, strings.exception + ': ' + str(e))
        return Wrapper
    return Decorator


def errors_handler(bot):
    def Decorator(fn):
        def Wrapper(call):
            try:
                fn(call)
            except telebot.apihelper.ApiException as e:
                bot.send_message(
                    call.from_user.id,
                    strings.task_fail
                    .format(json.loads(e.result.text)['description']
                            .split(':')[1]
                            .strip())
                )
            except Exception as e:
                bot.send_message(call.from_user.id, strings.exception + ': ' + str(e))
        return Wrapper
    return Decorator


def admin_command(bot, grouponly=False):
    def Decorator(fn):
        def Wrapper(msg):
            user_id = str(msg.from_user.id)
            if msg.chat.type == 'private' and grouponly:
                bot.reply_to(msg, strings.run_from_chat)
            else:
                if msg.chat.type is 'private' and not grouponly:
                    fn(msg)
                elif (user_id in get_chat_administators(msg.chat.id) and
                      get_chat_administators(msg.chat.id)[user_id]['edit'] or
                      msg.from_user.id is cfg.superadmin):
                    fn(msg)
                else:
                    bot.reply_to(msg, strings.denied)
        return Wrapper
    return Decorator


def register_chat(msg):
    chat_id = str(msg.chat.id)
    wm = 'welcome_message'
    if msg.chat.type is not 'private' and chat_id not in storage:
        storage[chat_id] = {}
        storage[chat_id]['chat_name'] = msg.chat.title
        storage[chat_id]['settings'] = {}
        storage[chat_id]['settings'][wm] = {}
        storage[chat_id]['settings'][wm]['Enable'] = False
        storage[chat_id]['settings'][wm]['Text'] = 'Welcome, $username'
        storage[chat_id]['settings']['ReportFeature'] = True
        storage[chat_id]['keywords'] = {}
        storage[chat_id]['members'] = {}


def register_user(msg):
    chat_id = str(msg.chat.id)
    user_id = str(msg.from_user.id)
    full_name = (msg.from_user.first_name + (
                 msg.from_user.last_name if msg.from_user.last_name else ''
                 ))[:20]
    if (msg.chat.type is not 'private' and
            user_id not in storage[chat_id]['members']):
        storage[chat_id]['members'][user_id] = {}
        storage[chat_id]['members'][user_id]['full_name'] = full_name
        storage[chat_id]['members'][user_id]['IgnoreUser'] = False
        storage[chat_id]['members'][user_id]['DisableReports'] = False
        storage[chat_id]['members'][user_id]['AdminRights'] = False
        storage[chat_id]['members'][user_id]['LastMessageDate'] = msg.date
    elif (msg.chat.type is not 'private' and
          user_id in storage[chat_id]['members'] and
          storage[chat_id]['members'][user_id]['full_name'] is not full_name):
        storage[chat_id]['members'][user_id]['full_name'] = full_name


def register_key(keydata):
    chat_id = keydata['chat_id']
    keyname = keydata['keyname']
    storage[chat_id]['keywords'][keyname] = {}
    storage[chat_id]['keywords'][keyname]['type'] = 'simple'
    storage[chat_id]['keywords'][keyname]['task'] = 'none'
    storage[chat_id]['keywords'][keyname]['silent'] = False
    storage[chat_id]['keywords'][keyname]['task_on_reply'] = False
    storage[chat_id]['keywords'][keyname]['delafter'] = False
    storage[chat_id]['keywords'][keyname]['admin_only'] = False
    storage[chat_id]['keywords'][keyname]['chance'] = 100
    storage[chat_id]['keywords'][keyname]['keyquery'] = keyname.lower().strip()
    storage[chat_id]['keywords'][keyname]['reply_mode'] = 'last'
    storage[chat_id]['keywords'][keyname]['enabled'] = True
    storage[chat_id]['keywords'][keyname]['answer'] = {}
    storage[chat_id]['keywords'][keyname]['answer']['type'] = 'text'
    storage[chat_id]['keywords'][keyname]['answer']['file_id'] = ''
    storage[chat_id]['keywords'][keyname]['answer']['text'] = 'Hello World!'


def register_admin(msg, initial_cid=None):
    user_id = str(msg.from_user.id)
    if user_id not in admins:
        admins[user_id] = []
    elif initial_cid:
        if not str(initial_cid) in admins[user_id]:
            admins[user_id].append(str(initial_cid))


def write_data_to_file():
    wfile = open('db.json', 'w')
    wfile.write(json.dumps(storage, indent=4))
    wfile.close()
    wfile2 = open('admins.json', 'w')
    wfile2.write(json.dumps(admins, indent=4))
    wfile2.close()


def get_chat_administators(chat_id, required=None, required_id=None):
    admins = bot.get_chat_administrators(chat_id)
    result = {}
    for i in admins:
        result[str(i.user.id)] = {}
        result[str(i.user.id)]['ban'] = i.can_restrict_members
        result[str(i.user.id)]['pin'] = i.can_pin_messages
        result[str(i.user.id)]['del'] = i.can_delete_messages
        result[str(i.user.id)]['edit'] = i.can_change_info
    result[str(cfg.superadmin)] = {}
    result[str(cfg.superadmin)]['pin'] = True
    result[str(cfg.superadmin)]['ban'] = True
    result[str(cfg.superadmin)]['del'] = True
    result[str(cfg.superadmin)]['edit'] = True
    if not required and not required_id:
        return result
    else:
        if required is 'none':
            return True
        elif str(required_id) in result:
            return result[str(required_id)][required]
        else:
            return False



def send_media(bot, msg, type, fid, reply_to_message_id='000000'):
    if type == 'photo':
        bot.send_photo(
            msg.chat.id,
            fid,
            reply_to_message_id=reply_to_message_id
        )
    if type == 'sticker':
        bot.send_sticker(
            msg.chat.id,
            fid,
            reply_to_message_id=reply_to_message_id
        )
    if type == 'audio':
        bot.send_audio(
            msg.chat.id,
            fid,
            reply_to_message_id=reply_to_message_id
        )
    if type == 'document':
        bot.send_document(
            msg.chat.id,
            fid,
            reply_to_message_id=reply_to_message_id
        )
    if type == 'video':
        bot.send_video(
            msg.chat.id,
            fid,
            reply_to_message_id=reply_to_message_id
        )
    if type == 'video_note':
        bot.send_video_note(
            msg.chat.id,
            fid,
            reply_to_message_id=reply_to_message_id
        )
    if type == 'voice':
        bot.send_voice(
            msg.chat.id,
            fid,
            reply_to_message_id=reply_to_message_id
        )


def exec_task(bot, message, bind):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    task = storage[chat_id]['keywords'][bind]['task']
    full = {
        user_id:{
            'pin':True,
            'ban':True,
            'del':True,
            'edit':False
        }
    }
    rights = get_chat_administators(message.chat.id) if storage[chat_id]['keywords'][bind]['admin_only'] else full
    reply = (storage[chat_id]['keywords'][bind]['task_on_reply'] and
             message.reply_to_message is not None)
    try:
        if user_id in rights:
            if task == "pin" and rights[user_id]['pin']:
                bot.pin_chat_message(
                    message.chat.id,
                    message.reply_to_message.message_id if reply else
                    message.message_id,
                    disable_notification=True)
            elif task == "pinl" and rights[user_id]['pin']:
                bot.pin_chat_message(
                    message.chat.id,
                    message.reply_to_message.message_id if reply else
                    message.message_id,
                    disable_notification=False)
            elif task == "kick" and rights[user_id]['ban']:
                bot.kick_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id if reply else
                    user_id)
            elif task == "mute_f" and rights[user_id]['ban']:
                bot.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id if reply else
                    user_id,
                    can_send_messages=False)
            elif task == "mute_d" and rights[user_id]['ban']:
                bot.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id if reply else
                    user_id,
                    can_send_messages=False,
                    until_date=message.date + 86400)
            elif task == "mute_w" and rights[user_id]['ban']:
                bot.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id if reply else
                    user_id,
                    can_send_messages=False,
                    until_date=message.date + 604800)
            elif task == "mute_m" and rights[user_id]['ban']:
                bot.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id if reply else
                    user_id,
                    can_send_messages=False,
                    until_date=message.date + 2592000)
            elif task == "mute_h" and rights[user_id]['ban']:
                bot.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id if reply else
                    user_id,
                    can_send_messages=False,
                    until_date=message.date + 3600)
            elif task == "unban" and rights[user_id]['ban']:
                bot.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id if reply else
                    user_id,
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                    )
            elif task == "del" and rights[user_id]['del']:
                bot.delete_message(
                    message.chat.id,
                    message.reply_to_message.message_id if reply else
                    message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.reply_to(
            message,
            strings.task_fail
            .format(json.loads(e.result.text)['description']
                    .split(':')[1]
                    .strip()
                    .replace('CHAT_NOT_MODIFIED',strings.chat_nm)
                    .replace('CHAT_ADMIN_REQUIRED',strings.admrq))
        )


# creating bot object
bot = telebot.TeleBot(cfg.token)


user_queue = {}  # List of users that pressed "Editkey button"


@bot.message_handler(content_types = ['new_chat_members'])
def addMem(msg):
    if str(msg.chat.id) in storage:
        if not msg.from_user.is_bot and not str(msg.from_user.id) in storage[str(msg.chat.id)]['members']:
            register_user(msg)
        if storage[str(msg.chat.id)]['settings']['welcome_message']['Enable']:
            if 'welcome_message' in storage[str(msg.chat.id)]['keywords']:
                exec_task(bot,msg,'welcome_message')
                if not storage[str(msg.chat.id)]['keywords']['welcome_message']['silent']:
                    if storage[str(msg.chat.id)]['keywords']['welcome_message']['enabled']:
                        if storage[str(msg.chat.id)]['keywords']['welcome_message']['answer']['type'] == 'text':
                            bot.send_message(
                                msg.chat.id, 
                                storage[str(msg.chat.id)]['keywords']['welcome_message']['answer']['text']
                                .replace('$name',(msg.from_user.first_name + ' ' +msg.from_user.last_name) if msg.from_user.last_name else msg.from_user.first_name)
                                .replace('$username',msg.from_user.username if msg.from_user.username else '<a href=\"tg://user?id={}\">{}</a>'.format(msg.from_user.id,msg.from_user.first_name))
                                .replace('$random',str(random.randint(0,100)))
                                .replace('$randuser', list(storage[str(msg.chat.id)]['members'].values())[random.randint(0,len(storage[str(msg.chat.id)]['members'])-1)]['full_name'] if not len(storage[str(msg.chat.id)]['members']) == 0 else 'Никто'),
                                reply_to_message_id = msg.message_id
                                )                
                        else:
                            try:
                                fid = storage[str(msg.chat.id)]['keywords']['welcome_message']['answer']['file_id']
                                if not storage[str(msg.chat.id)]['keywords'][i]['silent']:
                                    if not storage[str(msg.chat.id)]['keywords'][i]['admin_only']:
                                        send_media(bot,msg,storage[str(msg.chat.id)]['keywords'][i]['answer']['type'],fid,reply_to_message_id = msg.message_id)
                                    elif str(msg.from_user.id) in get_chat_administators(int(msg.chat.id)):
                                        send_media(bot,msg,storage[str(msg.chat.id)]['keywords'][i]['answer']['type'],fid,reply_to_message_id = msg.message_id)
                            except:
                                bot.reply_to(msg,strings.corrupted_media)
                    
            else:
                bot.reply_to(msg,'Welcome, '+msg.from_user.first_name)
    else:
        register_chat(msg)

@bot.message_handler(content_types = ['left_chat_member'])
def delMem(msg):
    if str(msg.chat.id) in storage:
        if not msg.from_user.is_bot and str(msg.from_user.id) in storage[str(msg.chat.id)]['members']:
            del storage[str(msg.chat.id)]['members'][str(msg.from_user.id)]
    else:
        register_chat(msg)    

#keys command
@bot.message_handler(commands = ['keys'])
@database_keeper(bot)
def keys(msg):
    if not msg.chat.type == 'private':
        result = strings.keys_header
        counter = 0
        for i in storage[str(msg.chat.id)]['keywords']:
            counter += 1
            result += str(counter) + '. ' + i + ': ' + storage[str(msg.chat.id)]['keywords'][i]['keyquery'] +'\n'
        if counter > 0:
            bot.reply_to(msg,result)
        else:
            bot.reply_to(msg,strings.keys_empty)
    else:
        bot.reply_to(msg,strings.keys_error)


#help and stsrt command
@bot.message_handler(commands = ['help','start'])
@database_keeper(bot)
def help(msg):
    if msg.text == '/help' or msg.text == '/help@trgr3bot' or msg.text == '/start' or msg.text == '/start@trgr3bot':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
                types.InlineKeyboardButton(text = strings.help_button, url = strings.help_url)
            )
        bot.reply_to(msg,strings.help_card, reply_markup = keyboard)


@bot.message_handler(commands = ['admin'])
@database_keeper(bot)
@admin_command(bot,grouponly = True)
def adminre(msg):
    register_admin(msg, initial_cid = msg.chat.id)
    bot.reply_to(msg, strings.chat_admin_reg)


#settings command    
@bot.message_handler(commands = ['settings'])
@database_keeper(bot)
@admin_command(bot,grouponly = False)
def settings(msg):
    if not msg.chat.type == 'private':
        register_admin(msg, initial_cid = msg.chat.id)
        bot.reply_to(msg, strings.chat_admin_reg)
    
    keyboard = types.InlineKeyboardMarkup()
    page = 0
    if str(msg.from_user.id) in admins:
        for i in admins[str(msg.from_user.id)][int(page)*5:int(page)*5+5]:
            try:
                if str(msg.from_user.id) in get_chat_administators(int(i)):
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text = storage[str(i)]['chat_name'],
                            callback_data = '$$set_' + str(i)
                            )
                        )
            except:
                continue
        if not len(admins[str(msg.from_user.id)]) <= 5:
            keyboard.row(
                    types.InlineKeyboardButton(
                        text = '1/'+str(len(admins[str(msg.from_user.id)])//5+1),
                        callback_data = 'empty'
                        ),
                    types.InlineKeyboardButton(
                        text = '>>>',
                        callback_data = '$$cl_1'
                        )
                    )
        bot.send_message(
            msg.from_user.id,
            strings.chat_list_card,
            reply_markup = keyboard,
            parse_mode = 'HTML'
            )
    else:
        bot.reply_to(msg,strings.chat_list_noone)


#add command
@bot.message_handler(commands = ['add'])
@admin_command(bot,grouponly = True)
@database_keeper(bot)
def addkey(msg):
    key = msg.text.split('/add')[1].strip().replace('(','').replace(')','').replace('^','').replace('$','').replace('[','').replace(']','').replace('{','').replace('}','').replace('*','').replace('.','').replace('+','').replace('\\','')
    if key == 'welcome_message':
        storage[str(msg.chat.id)]['settings']['welcome_message']['enabled'] = True
    fid = ''
    filetype = ''
    if (not msg.reply_to_message == None) and (not key == '') and len(key.split(' ')) == 1:
        if msg.reply_to_message.photo:
            fid = msg.reply_to_message.photo[0].file_id
            filetype = 'photo'
        elif msg.reply_to_message.voice:
            fid = msg.reply_to_message.voice.file_id
            filetype = 'voice'
        elif msg.reply_to_message.audio:
            fid = msg.reply_to_message.audio.file_id
            filetype = 'audio'
        elif msg.reply_to_message.sticker:
            fid = msg.reply_to_message.sticker.file_id
            filetype = 'sticker'
        elif msg.reply_to_message.video:
            fid = msg.reply_to_message.video.file_id
            filetype = 'video'
        elif msg.reply_to_message.video_note:
            fid = msg.reply_to_message.video_note.file_id
            filetype = 'video_note'
        elif msg.reply_to_message.document:
            fid = msg.reply_to_message.document.file_id
            filetype = 'document'
        elif msg.reply_to_message.text:
                register_key({'chat_id':str(msg.chat.id), 'keyname':key})
                storage[str(msg.chat.id)]['keywords'][key]['answer']['type'] = 'text'
                storage[str(msg.chat.id)]['keywords'][key]['answer']['text'] = msg.reply_to_message.text
                if key == 'welcome_message':
                    bot.reply_to(msg,strings.wm_success)
                else:
                    bot.reply_to(msg,strings.add_success)
        else:
            bot.reply_to(msg,strings.add_fail)    

        if fid and filetype:
            register_key({'chat_id':str(msg.chat.id), 'keyname':key})
            storage[str(msg.chat.id)]['keywords'][key]['answer']['type'] = filetype
            storage[str(msg.chat.id)]['keywords'][key]['answer']['file_id'] = fid
            storage[str(msg.chat.id)]['keywords'][key]['answer']['text'] = ''
            if key == 'welcome_message':
                bot.reply_to(msg,strings.wm_success)
            else:
                bot.reply_to(msg,strings.add_success)
        
    else:
        bot.reply_to(msg,strings.add_fail)    


@bot.message_handler(commands = ['addsticker'])
@admin_command(bot,grouponly = True)
@database_keeper(bot)
def addsticker(msg):
    key = msg.text.split('/addsticker')[1].strip().replace('(','').replace(')','').replace('^','').replace('$','').replace('[','').replace(']','').replace('{','').replace('}','').replace('*','').replace('.','').replace('+','').replace('\\','')
    if len(key.split(' ')) == 1 and not key == '':
        if msg.reply_to_message:
            if msg.reply_to_message.sticker:
                register_key({'chat_id':str(msg.chat.id), 'keyname':key})
                storage[str(msg.chat.id)]['keywords'][key]['type'] = 'sticker'
                storage[str(msg.chat.id)]['keywords'][key]['answer']['type'] = 'none'
                storage[str(msg.chat.id)]['keywords'][key]['keyquery'] = msg.reply_to_message.sticker.file_id
                bot.reply_to(msg,strings.succ_sticker)
            else:
                bot.reply_to(msg,strings.not_sticker)
        else:
            bot.reply_to(msg,strings.not_sticker)
    else:
        bot.reply_to(msg,strings.inv_name)
        print(key)


#inline call handler
@bot.callback_query_handler(func=lambda call: True)
@errors_handler(bot)
def callback_inline(call):
        if call.message:
            bot.answer_callback_query(call.id,strings.loading,show_alert = False)

            if call.data.startswith('$$set_'):
                chat_id = call.data.replace('$$set_','')
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.row(types.InlineKeyboardButton(text = strings.keywords, callback_data = '$$keys_' + chat_id + ':::' + '0'))
                    keyboard.row(types.InlineKeyboardButton(text = strings.users, callback_data = '$$users_' + chat_id + ':::' + '0'))
                    keyboard.row(types.InlineKeyboardButton(text = strings.chat_settings, callback_data = '$$cset_' + chat_id))
                    keyboard.row(types.InlineKeyboardButton(text = strings.back, callback_data = '$$cl_0'))        
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.control_panel_main.format(storage[chat_id]['chat_name'],str(len(storage[chat_id]['keywords'])),str(len(storage[chat_id]['members'])) + ' (' + str(round(len(storage[chat_id]['members'])/bot.get_chat_members_count(chat_id)*100,1)) + strings.indexed),
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Opens main settings screen of current chat. Made for Back button

            if call.data.startswith('$$keys_'):
                chat_id = call.data.replace('$$keys_','').split(':::')[0]
                page = call.data.replace('$$keys_','').split(':::')[1]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    keyboard = types.InlineKeyboardMarkup()
                    for i in list(storage[chat_id]['keywords'].keys())[int(page)*5:int(page)*5+5]:
                        keytype = storage[chat_id]['keywords'][i]['answer']['type']
                        icon = {'photo':'🖼 ','voice':'🎙 ','audio':'🎧 ','sticker':'🔖 ','video':'📹 ','video_note':'🎥 ','document':'📄 ','text':'📝 ','none':'⚙️ '}
                        keyboard.row(
                            types.InlineKeyboardButton(text = icon[keytype] + '| ' + i if not i == 'welcome_message' else strings.welcome, callback_data = '$$keyob_' + chat_id + ':::' + i + ':::' + page)
                        )
                    if not len(storage[chat_id]['keywords']) <= 5:
                        if page == '0':
                            keyboard.row(
                                types.InlineKeyboardButton(text = '1/'+str(len(storage[chat_id]['keywords'])//5+1),callback_data = 'empty'),
                                types.InlineKeyboardButton(text = '>>>',callback_data = '$$keys_'+chat_id+':::1')
                                )
                        elif int(page) == len(storage[chat_id]['keywords'])//5:
                            keyboard.row(
                                types.InlineKeyboardButton(text = '<<<',callback_data = '$$keys_'+chat_id+':::'+str(int(page)-1)),
                                types.InlineKeyboardButton(text = str(int(page)+1) +'/'+str(len(storage[chat_id]['keywords'])//5+1),callback_data = 'empty')
                                )
                        elif int(page) > 0:
                            keyboard.row(
                                types.InlineKeyboardButton(text = '<<<',callback_data = '$$keys_'+chat_id+':::'+str(int(page)-1)),
                                types.InlineKeyboardButton(text = str(int(page)+1) + "/" +str(len(storage[chat_id]['keywords'])//5+1),callback_data = 'empty'),
                                types.InlineKeyboardButton(text = '>>>',callback_data = '$$keys_'+chat_id+':::'+str(int(page)+1))
                                )
                    keyboard.row(
                        types.InlineKeyboardButton(text = strings.back,callback_data = '$$set_' + chat_id),
                        # types.InlineKeyboardButton(text = strings.update,callback_data = '$$keys_' + chat_id + ':::' + page)
                        )
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keywords_list.format(storage[chat_id]['chat_name']) if not len(storage[chat_id]['keywords'])==0 else strings.keys_empty,
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Opens list of keys, that created in cc (current chat)

            if call.data.startswith('$$keyob_'):
                keydata = call.data.replace('$$keyob_','').split(':::')
                chat_id = keydata[0]
                i = keydata[1]
                page = keydata[2]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    if i in storage[chat_id]['keywords']:
                        bot.edit_message_text(
                                chat_id = call.from_user.id,
                                message_id = call.message.message_id,
                                text = strings.keyword_card.format(
                                        i,
                                        strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                        strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                        storage[chat_id]['keywords'][i]['keyquery']
                                    ),
                                reply_markup = word_keyboard(chat_id,i,page),
                                parse_mode = 'HTML'
                            )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Opens detailed info and settings for keyword

            if call.data.startswith('$$del_'):
                keydata = call.data.replace('$$del_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    del storage[chat_id]['keywords'][i]
                    
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text = strings.back, callback_data = '$$keys_' + chat_id + ':::0'))
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.key_deleted,
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Deletes keyword

            if call.data.startswith('$$dis_'):
                keydata = call.data.replace('$$dis_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    storage[chat_id]['keywords'][i]['enabled'] = not storage[chat_id]['keywords'][i]['enabled']
                    
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                        i,
                                        strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                        strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                        storage[chat_id]['keywords'][i]['keyquery']
                                    ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Disables keyword...
            if call.data.startswith('$$users_'):
                chat_id = call.data.replace('$$users_','').split(':::')[0]
                page = call.data.replace('$$users_','').split(':::')[1]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    keyboard = types.InlineKeyboardMarkup()
                    for i in list(storage[chat_id]['members'].keys())[int(page)*5:int(page)*5+5]:
                        keyboard.add(types.InlineKeyboardButton(
                                text = storage[chat_id]['members'][i]['full_name'],
                                callback_data = '$$user_' + chat_id + ':::' + i + ':::' + page)
                            )
                    if not len(storage[chat_id]['members']) <= 5:
                        if page == '0':
                            keyboard.row(
                                types.InlineKeyboardButton(text = '1/'+str(len(storage[chat_id]['members'])//5+1),callback_data = 'empty'),
                                types.InlineKeyboardButton(text = '>>>',callback_data = '$$users_'+chat_id+':::1')
                                )
                        elif int(page) == len(storage[chat_id]['members'])//5:
                            keyboard.row(
                                types.InlineKeyboardButton(text = '<<<',callback_data = '$$users_'+chat_id+':::'+str(int(page)-1)),
                                types.InlineKeyboardButton(text = str(int(page)+1) +'/'+str(len(storage[chat_id]['members'])//5+1),callback_data = 'empty')
                                )
                        elif int(page) > 0:
                            keyboard.row(
                                types.InlineKeyboardButton(text = '<<<',callback_data = '$$users_'+chat_id+':::'+str(int(page)-1)),
                                types.InlineKeyboardButton(text = str(int(page)+1) + "/" +str(len(storage[chat_id]['members'])//5+1),callback_data = 'empty'),
                                types.InlineKeyboardButton(text = '>>>',callback_data = '$$users_'+chat_id+':::'+str(int(page)+1))
                                )
                    keyboard.add(types.InlineKeyboardButton(
                                text = strings.back,
                                callback_data = '$$set_' + chat_id)
                            )
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.users_list.format(storage[chat_id]['chat_name']),
                        reply_markup = keyboard,
                        parse_mode = 'HTML'
                    )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Opens list of all users in group, that leaves at least one message when bot was in group
            if call.data.startswith('$$user_'):
                keydata = call.data.replace('$$user_','').split(':::')
                chat_id = keydata[0]
                page = keydata[2]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.user_card.format(
                                storage[chat_id]['members'][i]['full_name'],
                                storage[chat_id]['chat_name'],
                                '✅' if storage[chat_id]['members'][i]['IgnoreUser'] else '❌',
                                '✅' if storage[chat_id]['members'][i]['DisableReports'] else '❌',
                                '✅' if storage[chat_id]['members'][i]['AdminRights'] else '❌'
                            ),
                        reply_markup = user_keyboard(chat_id,i,page),
                        parse_mode = 'HTML'
                    )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Detailed info and settings about user
            if call.data.startswith('$$iu_'):
                keydata = call.data.replace('$$iu_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    storage[chat_id]['members'][i]['IgnoreUser'] = not storage[chat_id]['members'][i]['IgnoreUser']
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.user_card.format(
                                storage[chat_id]['members'][i]['full_name'],
                                storage[chat_id]['chat_name'],
                                '✅' if storage[chat_id]['members'][i]['IgnoreUser'] else '❌',
                                '✅' if storage[chat_id]['members'][i]['DisableReports'] else '❌',
                                '✅' if storage[chat_id]['members'][i]['AdminRights'] else '❌'
                            ),
                        reply_markup = user_keyboard(chat_id,i,'0'),
                        parse_mode = 'HTML'
                    )        
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Ignore/Unignore users
            if call.data.startswith('$$dr_'):
                keydata = call.data.replace('$$dr_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    storage[chat_id]['members'][i]['DisableReports'] = not storage[chat_id]['members'][i]['DisableReports']
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.user_card.format(
                                storage[chat_id]['members'][i]['full_name'],
                                storage[chat_id]['chat_name'],
                                '✅' if storage[chat_id]['members'][i]['IgnoreUser'] else '❌',
                                '✅' if storage[chat_id]['members'][i]['DisableReports'] else '❌',
                                '✅' if storage[chat_id]['members'][i]['AdminRights'] else '❌'
                            ),
                        reply_markup = user_keyboard(chat_id,i,'0'),
                        parse_mode = 'HTML'
                    )    
             
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Disable reports/Enable reports
            if call.data.startswith('$$wts_'):
                keydata = call.data.replace('$$wts_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.simp,
                            callback_data = '$$settype_' + chat_id + ':::' + i + ':::' + 'simple'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = 'RegExp',
                            callback_data = '$$settype_' + chat_id + ':::' + i + ':::' + 'regexp'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.back,
                            callback_data = '$$keyob_' + chat_id + ':::' + i + ':::0'
                        ))
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.word_type_card.format(i),
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Keyword type-select screen
            if call.data.startswith('$$wrm_'):
                keydata = call.data.replace('$$wrm_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.default,
                            callback_data = '$$setrm_' + chat_id + ':::' + i + ':::' + 'last'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.onreply,
                            callback_data = '$$setrm_' + chat_id + ':::' + i + ':::' + 'deep'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.disa,
                            callback_data = '$$setrm_' + chat_id + ':::' + i + ':::' + 'off'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.back,
                            callback_data = '$$keyob_' + chat_id + ':::' + i + ':::0'
                        ))
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.word_replymode_card.format(i),
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Keyword reply-type screen
            if call.data.startswith('$$settype_'):
                keydata = call.data.replace('$$settype_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    wtype = keydata[2]
                    storage[chat_id]['keywords'][i]['type'] = wtype
                    
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                    i,
                                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                    storage[chat_id]['keywords'][i]['keyquery']
                                ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Sets type of kw
            if call.data.startswith('$$setrm_'):
                keydata = call.data.replace('$$setrm_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    wtype = keydata[2]
                    storage[chat_id]['keywords'][i]['reply_mode'] = wtype
                    
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                    i,
                                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                    storage[chat_id]['keywords'][i]['keyquery']
                                ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Sets replymode of kw 
            if call.data.startswith('$$editt'):
                keydata = call.data.replace('$$editt_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.cancel,
                            callback_data = '$$cancel_' + chat_id + ':::' + i + ':::' + str(call.from_user.id)
                        ))
                    user_queue[str(call.from_user.id)] = {}
                    user_queue[str(call.from_user.id)]['chat_id'] = chat_id
                    user_queue[str(call.from_user.id)]['keyword'] = i
                    user_queue[str(call.from_user.id)]['message_id'] = call.message.message_id
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.word_trigger.format(i),
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Wait for user editing trigger
            if call.data.startswith('$$cancel_'):
                keydata = call.data.replace('$$cancel_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    user = keydata[2]
                    if user in user_queue:
                        del user_queue[user]
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.keyword_card.format(
                                        i,
                                        strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                        strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                        storage[chat_id]['keywords'][i]['keyquery']
                                    ),
                        reply_markup = word_keyboard(chat_id,i,'0'),
                        parse_mode = 'HTML'
                    )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Cancel trigger edit 
            if call.data.startswith('$$cset_'):
                chat_id = call.data.replace('$$cset_','')
                bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.chat_settings_card.format(
                                storage[chat_id]['chat_name'],
                                '✅' if storage[chat_id]['settings']['ReportFeature'] else '❌',
                                '✅' if storage[chat_id]['settings']['welcome_message']['Enable'] else '❌'
                            ),
                        reply_markup = chat_keyboard(chat_id),
                        parse_mode = 'HTML'
                    )#Chat settings (oh no its retarded)
            if call.data.startswith('$$grf_'):
                chat_id = call.data.replace('$$grf_','').split(':::')[0]
                mode = call.data.replace('$$grf_','').split(':::')[1]
                if mode == 'on':
                    storage[chat_id]['settings']['ReportFeature'] = True
                else:
                    storage[chat_id]['settings']['ReportFeature'] = False
                
                bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.chat_settings_card.format(
                                storage[chat_id]['chat_name'],
                                '✅' if storage[chat_id]['settings']['ReportFeature'] else '❌'
                            ),
                        reply_markup = chat_keyboard(chat_id),
                        parse_mode = 'HTML'
                    )
            if call.data.startswith('$$adm_'):
                keydata = call.data.replace('$$adm_','').split(':::')
                chat_id = keydata[0]
                i = keydata[1]
                if storage[keydata[0]]['keywords'][keydata[1]]['admin_only']:
                    storage[keydata[0]]['keywords'][keydata[1]]['admin_only'] = False
                else:
                    storage[keydata[0]]['keywords'][keydata[1]]['admin_only'] = True
                
                bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                    i,
                                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                    storage[chat_id]['keywords'][i]['keyquery']
                                ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
            if call.data.startswith('$$cl_'):
                keyboard = types.InlineKeyboardMarkup()
                page = call.data.replace('$$cl_','')
                if str(call.from_user.id) in admins:
                    if len(admins[str(call.from_user.id)]) > 0:
                        keyboard = types.InlineKeyboardMarkup()
                        if str(call.from_user.id) in admins:
                            keyboard = types.InlineKeyboardMarkup()
                            for i in admins[str(call.from_user.id)][int(page)*5:int(page)*5+5]:
                                try:
                                    if str(call.from_user.id) in get_chat_administators(int(i)):
                                        keyboard.add(types.InlineKeyboardButton(
                                                text = storage[str(i)]['chat_name'],
                                                callback_data = '$$set_' + str(i))
                                            )
                                except:
                                    continue
                            if not len(admins[str(call.from_user.id)]) <= 5:
                                if page == '0':
                                    keyboard.row(
                                        types.InlineKeyboardButton(text = '1/'+str(len(admins[str(call.from_user.id)])//5+1),callback_data = 'empty'),
                                        types.InlineKeyboardButton(text = '>>>',callback_data = '$$cl_1')
                                        )
                                elif int(page) == len(admins[str(call.from_user.id)])//5:
                                    keyboard.row(
                                        types.InlineKeyboardButton(text = '<<<',callback_data = '$$cl_'+str(int(page)-1)),
                                        types.InlineKeyboardButton(text = str(int(page)+1) +'/'+str(len(admins[str(call.from_user.id)])//5+1),callback_data = 'empty')
                                        )
                                elif int(page) > 0:
                                    keyboard.row(
                                        types.InlineKeyboardButton(text = '<<<',callback_data = '$$cl_'+str(int(page)-1)),
                                        types.InlineKeyboardButton(text = str(int(page)+1) + "/" +str(len(admins[str(call.from_user.id)])//5+1),callback_data = 'empty'),
                                        types.InlineKeyboardButton(text = '>>>',callback_data = '$$cl_'+str(int(page)+1))
                                        )
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.chat_list_card,
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.answer_callback_query(call.id,strings.chat_list_noone,show_alert = False)

            if call.data.startswith('$$show_'):
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text = strings.hide, callback_data = '$$shwd_'))
                chat_id = call.data.replace('$$show_','').split(':::')[0]
                i = call.data.replace('$$show_','').split(':::')[1]
                wtype = storage[chat_id]['keywords'][i]['answer']['type']
                content = storage[chat_id]['keywords'][i]['answer']['file_id'] if not wtype == 'text' else strings.view_text.format(i) + storage[chat_id]['keywords'][i]['answer']['text']
                send = {'text':bot.send_message,'photo':bot.send_photo,'sticker':bot.send_sticker,'audio':bot.send_audio,'document':bot.send_document,'video':bot.send_video,'video_note':bot.send_video_note,'voice':bot.send_voice}
                try:
                    send[wtype](call.from_user.id,content,reply_markup = keyboard)
                except:
                    bot.reply_to(call.message, strings.corrupted_media)

            if call.data.startswith('$$shwd_'):
                bot.delete_message(call.from_user.id,call.message.message_id)

            if call.data.startswith('$$cha_'):
                keydata = call.data.replace('$$cha_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.row(types.InlineKeyboardButton(
                            text = '100%',
                            callback_data = '$$setcha_' + chat_id + ':::' + i + ':::' + '100'
                        ),
                    types.InlineKeyboardButton(
                            text = '75%',
                            callback_data = '$$setcha_' + chat_id + ':::' + i + ':::' + '75'
                        ),
                    types.InlineKeyboardButton(
                            text = '50%',
                            callback_data = '$$setcha_' + chat_id + ':::' + i + ':::' + '50'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = '25%',
                            callback_data = '$$setcha_' + chat_id + ':::' + i + ':::' + '25'
                        ),
                    types.InlineKeyboardButton(
                            text = '5%',
                            callback_data = '$$setcha_' + chat_id + ':::' + i + ':::' + '5'
                        ),
                    types.InlineKeyboardButton(
                            text = '1%',
                            callback_data = '$$setcha_' + chat_id + ':::' + i + ':::' + '1'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.back,
                            callback_data = '$$keyob_' + chat_id + ':::' + i + ':::0'
                        ))
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.chance_card,
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Keyword type-select screen

            if call.data.startswith('$$setcha_'):
                keydata = call.data.replace('$$setcha_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    wtype = keydata[2]
                    storage[chat_id]['keywords'][i]['chance'] = int(wtype)
                    
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                    i,
                                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                    storage[chat_id]['keywords'][i]['keyquery']
                                ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )
            if call.data.startswith('$$task_'):
                keydata = call.data.replace('$$task_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.ban,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'kick'
                        ),
                    types.InlineKeyboardButton(
                            text = strings.unban,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'unban'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.pin,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'pin'
                        ),
                    types.InlineKeyboardButton(
                            text = strings.pin_n,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'pinl'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.mute_for,
                            callback_data = 'Empty'
                        ))
                    keyboard.row(
                        types.InlineKeyboardButton(
                            text = strings.hour,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'mute_h'
                        ),types.InlineKeyboardButton(
                            text = strings.day,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'mute_d'
                        ),types.InlineKeyboardButton(
                            text = strings.week,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'mute_w'
                        ),types.InlineKeyboardButton(
                            text = strings.month,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'mute_m'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.forever,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'mute_f'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.delm,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'del'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.none,
                            callback_data = '$$settask_' + chat_id + ':::' + i + ':::' + 'none'
                        ))
                    keyboard.row(types.InlineKeyboardButton(
                            text = strings.back,
                            callback_data = '$$keyob_' + chat_id + ':::' + i + ':::0'
                        ))
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.task_card,
                            reply_markup = keyboard,
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )#Keyword type-select screen

            if call.data.startswith('$$settask_'):
                keydata = call.data.replace('$$settask_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    wtype = keydata[2]
                    storage[chat_id]['keywords'][i]['task'] = wtype
                    
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                    i,
                                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                    storage[chat_id]['keywords'][i]['keyquery']
                                ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )
            if call.data.startswith('$$tor_'):
                keydata = call.data.replace('$$tor_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    storage[chat_id]['keywords'][i]['task_on_reply'] = not storage[chat_id]['keywords'][i]['task_on_reply']
                    storage[chat_id]['keywords'][i]['admin_only'] = storage[chat_id]['keywords'][i]['task_on_reply']
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                    i,
                                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                    storage[chat_id]['keywords'][i]['keyquery']
                                ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )
            if call.data.startswith('$$salo_'):
                keydata = call.data.replace('$$salo_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    storage[chat_id]['keywords'][i]['silent'] = not storage[chat_id]['keywords'][i]['silent']
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                    i,
                                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                    storage[chat_id]['keywords'][i]['keyquery']
                                ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )
            if call.data.startswith('$$delaft_'):
                keydata = call.data.replace('$$delaft_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    i = keydata[1]
                    storage[chat_id]['keywords'][i]['delafter'] = not storage[chat_id]['keywords'][i]['delafter']
                    bot.edit_message_text(
                            chat_id = call.from_user.id,
                            message_id = call.message.message_id,
                            text = strings.keyword_card.format(
                                    i,
                                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                                    storage[chat_id]['keywords'][i]['keyquery']
                                ),
                            reply_markup = word_keyboard(chat_id,i,'0'),
                            parse_mode = 'HTML'
                        )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )
            if call.data.startswith('$$wm_'):
                keydata = call.data.replace('$$wm_','').split(':::')
                chat_id = keydata[0]
                if str(call.from_user.id) in get_chat_administators(int(chat_id)) and get_chat_administators(int(chat_id))[str(call.from_user.id)]['edit']:
                    storage[chat_id]['settings']['welcome_message']['Enable'] = not storage[chat_id]['settings']['welcome_message']['Enable']
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.chat_settings_card.format(
                                storage[chat_id]['chat_name'],
                                '✅' if storage[chat_id]['settings']['ReportFeature'] else '❌',
                                '✅' if storage[chat_id]['settings']['welcome_message']['Enable'] else '❌'
                            ),
                        reply_markup = chat_keyboard(chat_id),
                        parse_mode = 'HTML'
                    )
                else:
                    bot.edit_message_text(
                        chat_id = call.from_user.id,
                        message_id = call.message.message_id,
                        text = strings.permission_fail,
                        parse_mode = 'HTML'
                    )
@bot.message_handler(commands = ['report'])
@database_keeper(bot)
def report(msg):
    success = 0
    if (not msg.reply_to_message == None):
        if str(msg.from_user.id) in storage[str(msg.chat.id)]['members']:
            if not storage[str(msg.chat.id)]['members'][str(msg.from_user.id)]['DisableReports'] and storage[str(msg.chat.id)]['settings']['ReportFeature']:
                for i in get_chat_administators(int(msg.chat.id)):
                    try:
                        bot.send_message(i,strings.report_message.format(msg.from_user.first_name,('@'+ msg.from_user.username if not msg.from_user.username == None else '-')))
                        bot.forward_message(i,msg.chat.id,msg.reply_to_message.message_id)
                        success += 1
                    except:
                        continue
                bot.reply_to(msg,strings.reported.format(str(success)))

#text handler
@bot.message_handler(content_types = ['text'])
@database_keeper(bot)
def thread_process(msg):
    bindsearch = Thread(target=texthandler, args=(msg, ))
    bindsearch.daemon = True
    bindsearch.start()
def texthandler(msg):
    if not msg.chat.type == 'private':
        if not storage[str(msg.chat.id)]['members'][str(msg.from_user.id)]['IgnoreUser']:
            for i in storage[str(msg.chat.id)]['keywords']:    
                #regexp forming
                if storage[str(msg.chat.id)]['keywords'][i]['type'] == 'regexp':
                    p = re.compile(storage[str(msg.chat.id)]['keywords'][i]['keyquery'].lower())
                elif storage[str(msg.chat.id)]['keywords'][i]['type'] == 'simple':
                    p = re.compile('\\b{}[^ ]*\\b'.format(storage[str(msg.chat.id)]['keywords'][i]['keyquery'].lower().strip().replace('(','\\(').replace(')','\\)').replace('^','\\^').replace('$','\\$').replace('[','\\[').replace(']','\\]').replace('{','\\{').replace('}','\\}').replace('*','\\*').replace('.','\\.').replace('+','\\+').replace('\\','')))

                if not p.search(msg.text.lower()) == None:
                    if random.randint(1,100) <= storage[str(msg.chat.id)]['keywords'][i]['chance'] and storage[str(msg.chat.id)]['keywords'][i]['enabled']:
                        #Reply mode 
                        
                        if storage[str(msg.chat.id)]['keywords'][i]['reply_mode'] == 'off':
                            replyentry = None
                        elif storage[str(msg.chat.id)]['keywords'][i]['reply_mode'] == 'last': 
                            replyentry = msg.message_id
                        elif storage[str(msg.chat.id)]['keywords'][i]['reply_mode'] == 'deep':
                            replyentry = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id

                        if storage[str(msg.chat.id)]['keywords'][i]['answer']['type'] == 'text':
                            req = REQUIRES[storage[str(msg.chat.id)]['keywords'][i]['task']]
                            if (get_chat_administators(msg.chat.id, required=req, required_id=msg.from_user.id)) if storage[str(msg.chat.id)]['keywords'][i]['admin_only'] else True:
                                if not storage[str(msg.chat.id)]['keywords'][i]['silent']:
                                    bot.send_message(
                                        msg.chat.id, 
                                        storage[str(msg.chat.id)]['keywords'][i]['answer']['text']
                                        .replace('$name',(msg.from_user.first_name + ' ' +msg.from_user.last_name) if msg.from_user.last_name else msg.from_user.first_name)
                                        .replace('$username',msg.from_user.username if msg.from_user.username else '<a href=\"tg://user?id={}\">{}</a>'.format(msg.from_user.id,msg.from_user.first_name))
                                        .replace('$random',str(random.randint(0,100)))
                                        .replace('$randuser', list(storage[str(msg.chat.id)]['members'].values())[random.randint(0,len(storage[str(msg.chat.id)]['members'])-1)]['full_name'] if not len(storage[str(msg.chat.id)]['members']) == 0 else 'Никто'),
                                        reply_to_message_id = replyentry
                                        )
                                exec_task(bot,msg,i)
                        else:
                            if (get_chat_administators(msg.chat.id, required=req, required_id=msg.from_user.id)) if storage[str(msg.chat.id)]['keywords'][i]['admin_only'] else True:
                                fid = storage[str(msg.chat.id)]['keywords'][i]['answer']['file_id']
                                try:
                                    if not storage[str(msg.chat.id)]['keywords'][i]['silent']:
                                        if not storage[str(msg.chat.id)]['keywords'][i]['admin_only']:
                                            send_media(bot,msg,storage[str(msg.chat.id)]['keywords'][i]['answer']['type'],fid,reply_to_message_id = replyentry)
                                        elif str(msg.from_user.id) in get_chat_administators(int(msg.chat.id)):
                                            send_media(bot,msg,storage[str(msg.chat.id)]['keywords'][i]['answer']['type'],fid,reply_to_message_id = replyentry)
                                except:
                                    bot.reply_to(msg,strings.corrupted_media)
                                exec_task(bot,msg,i)
                        if storage[str(msg.chat.id)]['keywords'][i]['delafter']:
                            bot.delete_message(msg.chat.id,msg.message_id)    
                        break
                        
                else:
                    continue    
                    
    elif str(msg.from_user.id) in user_queue:
        chat_id = user_queue[str(msg.from_user.id)]['chat_id']
        message_id = user_queue[str(msg.from_user.id)]['message_id']
        i = user_queue[str(msg.from_user.id)]['keyword']
        if len(msg.text.split(' ')) == 1 and storage[chat_id]['keywords'][i]['type'] == "simple":
            storage[chat_id]['keywords'][i]['keyquery'] = msg.text
            bot.edit_message_text(
                chat_id = msg.from_user.id,
                message_id = message_id,
                text = strings.keyword_card.format(
                    i,
                    strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                    strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                    storage[chat_id]['keywords'][i]['keyquery']
                ),
                reply_markup = word_keyboard(chat_id,i,'0'),
                parse_mode = 'HTML'
            )
            del user_queue[str(msg.from_user.id)]
        elif storage[chat_id]['keywords'][i]['type'] == "regexp":
            valid = True
            err = ''
            try:
                re.match(msg.text,'Lorem ipsum dolor set amet string for test RegExp 😐😐😡😡😉😊😭')
            except Exception as e:
                valid = False
                err = str(e)
            if valid:
                storage[chat_id]['keywords'][i]['keyquery'] = msg.text
                bot.edit_message_text(
                    chat_id = msg.from_user.id,
                    message_id = message_id,
                    text = strings.keyword_card.format(
                        i,
                        strings.simp if storage[chat_id]['keywords'][i]['type'] == 'simple' else 'RegExp',
                        strings.disa if storage[chat_id]['keywords'][i]['reply_mode'] == 'off' else (strings.default if storage[chat_id]['keywords'][i]['reply_mode'] == 'last' else strings.onreply),
                        storage[chat_id]['keywords'][i]['keyquery']
                    ),
                    reply_markup = word_keyboard(chat_id,i,'0'),
                    parse_mode = 'HTML'
                )
                del user_queue[str(msg.from_user.id)]
            else:
                bot.reply_to(msg, strings.re_error.format(err))

        else:
            bot.reply_to(msg,strings.word_ifsimple)
        
@bot.message_handler(content_types = ['sticker'])
@database_keeper(bot)
def stickerhandler(msg):
    for i in storage[str(msg.chat.id)]['keywords']:
        if storage[str(msg.chat.id)]['keywords'][i]['type'] == 'sticker' and storage[str(msg.chat.id)]['keywords'][i]['keyquery'] == msg.sticker.file_id:
            if storage[str(msg.chat.id)]['keywords'][i]['enabled']:
                exec_task(bot,msg,i)
                if storage[str(msg.chat.id)]['keywords'][i]['delafter']:
                    bot.delete_message(msg.chat.id,msg.message_id)    
                break

def EventHandler(bot,db):
    write_data_to_file()
multitasking.RepeatedTimer(60,EventHandler,bot,storage).start()
#Endless polling
def Poll():
    try:
        bot.polling(none_stop = True,timeout=60)
    except Exception as e:
        bot.send_message(cfg.superadmin,'Ошибка: ' + str(e))
        bot.stop_polling()
        time.sleep(2)
        Poll()
        
Poll()

bot.polling(none_stop = True,timeout=60)

