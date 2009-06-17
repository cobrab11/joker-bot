# -*- coding: utf-8 -*-

JOKELIST = [
u'/me шмякнул на голову %s вишнёвый торт',
u'/me подсунул в чай %s полпачки слабительного',
u'/me надел на %s балетную пачку',
u'/me спрятал под обшивку стула %s много канцелярских кнопок',
u'/me притащил к %s крутую акустику и включил... TOKYO HOTEL!!!',
u'/me кинул за шиворот %s майского жука',
u'/me намазал %s гуталином и толкнул в толпу скинхедов',
u'/me намазал клавиатуру %s суперклеем',
u'/me заставил ксерокопировать %s Войну и Мир'
]



def handler_nudge(t, s, p):
 muc = s[1]
 nick = s[2]

 p = p.strip()

 if p:
  if is_muc(muc):
   if get_attribute(muc, nick, 'online'):
    target = p

   else:
    reply(t, s, core_not_in_muc_msg)
    return

  else:
   reply(t, s, core_muc_only_msg)
   return

 else:
  target = nick

 answer = JOKELIST[random.randrange(0,len(JOKELIST))] % target

 reply('groupchat', [None, muc, None], answer)



register_command_handler(handler_nudge, u'.тык', [u'конфа',u'все'], u'Приказывает боту поиздеваться над участником', u'.тык [ник]')

