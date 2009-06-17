# -*- coding: utf-8 -*-

### LANGPACK ###

admin_stop_msg = u'Выключение по команде '
admin_restart_msg = u'Перезагрузка по команде '
admin_reason_msg = u'Причина: '
admin_command_msg = u'администратора'

################



def handler_admin_stop(t, s, r=None):
 muc = s[1]
 nick = s[2]

 if is_muc(muc):
  prs = admin_stop_msg + nick

 else:
  prs = admin_stop_msg + admin_command_msg

 if r:
  prs = prs + '\n' + admin_reason_msg + r

 stop(prs)

 if r:
  prs = admin_stop_msg + nick + '\n' + admin_reason_msg + r

 else:
  prs = admin_stop_msg + nick

 stop(prs)



def handler_admin_restart(t, s, r=None):
 muc = s[1]
 nick = s[2]

 if is_muc(muc):
  prs = admin_restart_msg + nick

 else:
  prs = admin_restart_msg + admin_command_msg

 if r:
  prs = prs + '\n' + admin_reason_msg + r

 restart(prs)



register_command_handler(handler_admin_stop, u'.с', [u'все', u'админ'], u'Остановка бота', u'.стоп <причина>', 100, True)
register_command_handler(handler_admin_restart, u'.р', [u'все', u'админ'], u'Перезагрузка бота', u'.рестарт <причина>', 100, True)
