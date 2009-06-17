# -*- coding: utf-8 -*-

### LANGPACK ###

muc_roulette_fire_msg = u'ЩЁЛК!'

################


def handler_roulette_one(t, s, p):
 muc = s[1]
 nick = s[2]
 answer = u'Ы'

# if not get_access_level(s) >= 15:
 if is_muc(muc):
  random.seed(int(time.time()))

  if random.randrange(0,4) == 0:
   answer = u'ПТЫДЫЩЬ!!!'
   reply(t, s, answer)
#   do_kick(muc, nick, u'ПТЫДЫЩЬ!!!')
#   msg(muc, u'/me выстрелил в ' + nick)

  else:
   answer = muc_roulette_fire_msg

 else:
  answer = core_muc_only_msg




# else:
#  answer = u'Не поднимается рука в модера стрелять :('

 reply(t, s, answer)


	
#def handler_roulette_many(type, source, parameters):
	
	

register_command_handler(handler_roulette_one, u'.рулетка', [u'конфа',u'все'], u'Старая добрая русская рулетка.', u'.рулетка')
