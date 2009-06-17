# -*- coding: utf-8 -*-

### LANGPACK ###

muc_info_msg = u'\nУровень доступа: %d'

################


def handler_info(t, s, p):
 muc = s[1]
 nick = s[2]

 p = p.strip()

 if p:
  nick = p

 if is_online(muc, nick):
  answer = muc_info_msg % (AFFILIATIONS[get_attribute(muc, nick, 'afl')],)

 else:
  answer = core_not_in_muc_msg % (p,)

 reply(t, s, answer)



register_command_handler(handler_info, u'.инфо', [u'все'], u'Показывает информацию о пользователе', u'.инфо', 0)
