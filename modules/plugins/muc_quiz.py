# -*- coding: utf-8 -*-

from __future__ import with_statement

import time
import threading

### LANGPACK ###

muc_quiz_start_msg = u'Викторина началась! Во время игры доступны команды:\n подсказка - "%s"\n пропуск вопроса - "%s"\n остановить игру - "%s"'
muc_quiz_victory_msg = u'Правильный ответ! Вы получаете %d %s.'
muc_quiz_stop_msg = u'Викторина остановлена. Результаты игры можно узнать по команде "%s"'
muc_quiz_help_msg = u'Подсказка: '
muc_quiz_righrt_answer = u'Правильный ответ: %s'
muc_quiz_no_right_answer_msg = u'Никто не дал правильный ответ. '
muc_quiz_question_msg = u'Внимание, вопрос!'
muc_quiz_no_more_help_msg = u'Подсазки исчерпаны. '
muc_quiz_bonus_msg = u'\nЗа %d правильных %s подряд вы получаете %d %s!'
muc_quiz_results_msg = u'ВИКТОРИНА:'
muc_quiz_empty_results_msg = u'Результаты игры отсутствуют'
muc_quiz_personal_results_msg = u'\nВаш результат: %d %s'
muc_quiz_result_string_msg = u'\n%d. %s: %d %s'

################

MUC_QUIZ_LIMIT = 10

timer_help_delay = 5
timer_answer_delay = 120

#quiz_score = ((3, u'балла'), (2, u'балла'), (1, u'балл'))
#quiz_score_bonus = (1, u'балл')
quiz_score = (3, 2, 1)
quiz_score_bonus = 1

question_delay = 2

muc_quiz_cmd_help_msg = u'.'
muc_quiz_cmd_next_msg = u'.хз'
muc_quiz_cmd_stop_msg = u'.стоп'
muc_quiz_cmd_results_msg = u'.топ'

quiz_base_file = './data/static/questions.txt'

quiz_clear_key = u'викторина'

################

QUIZ = {}

try: CLEANERS
except NameError: CLEANERS = {}

CLEANERS[quiz_clear_key] = ['quiz']

################



def handler_quiz_start(t, s, p):
 muc = s[1]
 nick = s[2]

 if not muc in QUIZ:				# если не запущена
  QUIZ[muc] = {}
  QUIZ[muc]['lock'] = True
  QUIZ[muc]['last'] = ['', 0]				# ник, количество правильных ответов
  QUIZ[muc]['lock'] = True

  reply('groupchat', (None, muc, None), muc_quiz_start_msg % (muc_quiz_cmd_help_msg, muc_quiz_cmd_next_msg, muc_quiz_cmd_stop_msg))
  quiz_next_question(muc)



def quiz_cmd_stop(muc):			# нужно ли ник?
 print 'GAME OVER'
 del QUIZ[muc]
 reply('groupchat', (None, muc, None), muc_quiz_stop_msg % (muc_quiz_cmd_results_msg,))



def quiz_cmd_next(muc):
 if QUIZ[muc]['help']:
  reply('groupchat', (None, muc, None), muc_quiz_righrt_answer % QUIZ[muc]['answer'])
  quiz_next_question(muc)



def quiz_cmd_help(muc):			# нужно ли ник?
 if QUIZ[muc]['help']:
  print 'HELP'

  answer = QUIZ[muc]['answer']
  tip = QUIZ[muc]['tip']

  if tip.count('*') > 2:		# количество оставшихся звездочек

   while True:
    i = random.randrange(0, len(answer) - 1)

    if tip[i] == '*':
     tip = tip[:i] + answer[i] + tip[i+1:]
     break

   reply('groupchat', (None, muc, None), muc_quiz_help_msg + tip)

   QUIZ[muc]['tip'] = tip
   QUIZ[muc]['help'] = False

   if QUIZ[muc]['score'] < 2:
    QUIZ[muc]['score'] += 1

   threading.Thread(None, process_help_timer, 'quiz_help_' + muc, (muc,)).start()

  else:
   reply('groupchat', (None, muc, None), muc_quiz_no_more_help_msg + muc_quiz_righrt_answer % QUIZ[muc]['answer'])
   quiz_next_question(muc)



def quiz_cmd_results(t, s, p=None):
 muc = s[1]
 nick = s[2]

 QUIZ_SCORE = []

 personal = load_attribute(muc, get_attribute(muc, nick, 'jid'), 'quiz') or 0

 for jid in list_db_nodes(muc):
  score = load_attribute(muc, jid, 'quiz')

  if score:
   nick = load_attribute(muc, jid, 'nicks')[0]
   QUIZ_SCORE.append((score, nick))

 answer = muc_quiz_results_msg

 if not QUIZ_SCORE:
  answer = muc_quiz_empty_results_msg

 else:
  QUIZ_SCORE.sort(reverse=True)

  for i in range(len(QUIZ_SCORE)):
   if i > MUC_QUIZ_LIMIT - 1:
    break

#   ### поправка на правила русского языка ;-)
#
#   num_end = str(QUIZ_SCORE[i][0])
#
#   if num_end.endswith('1'):
#    ending = u'балл'
#
#   elif num_end.endswith('2') or num_end.endswith('3') or num_end.endswith('4'):
#    ending = u' балла'
#
#   else:
#    ending = u'баллов'
#
#   ###

   answer += muc_quiz_result_string_msg % ( i+1, QUIZ_SCORE[i][1], QUIZ_SCORE[i][0], string_rus(QUIZ_SCORE[i][0], (u'баллов', u'балл', u'балла')) )

# ### личный зачет ###
#
#  ### поправка на правила русского языка ;-)
#
#  num_end = str(personal)
#
#  if num_end.endswith('1'):
#   ending = u'балл'
#
#  elif num_end.endswith('2') or num_end.endswith('3') or num_end.endswith('4'):
#   ending = u'балла'
#
#  else:
#   ending = u'баллов'
#
#  ###

  answer += muc_quiz_personal_results_msg % ( personal, string_rus(personal, (u'баллов', u'балл', u'балла')) )

 reply(t, s, answer)



def handler_message_quiz(t, s, b):
 muc = s[1]
 nick = s[2]
 jid = s[0]

 b = b.strip().lower()

 if b == muc_quiz_cmd_results_msg:				# итоги можно проверять в любое время
  quiz_cmd_results(t, s)

 if muc in QUIZ:						# проверяем, запущена ли викторина в данной конфе
  if b == muc_quiz_cmd_stop_msg:				# завершить игру
   quiz_cmd_stop(muc)
   return

  if t == 'groupchat':
   if not QUIZ[muc]['lock']:					# если разрешено отвечать
    if b == QUIZ[muc]['answer'].lower().strip():
     QUIZ[muc]['lock'] = True

     bonus = 0

     if nick == QUIZ[muc]['last'][0]:
      QUIZ[muc]['last'][1] += 1

      if QUIZ[muc]['last'][1] > 2:				# за три правильных ответа подряд
       bonus = quiz_score_bonus

     else:
      QUIZ[muc]['last'] = [nick, 1]

     answer = muc_quiz_victory_msg % ( quiz_score[QUIZ[muc]['score']], string_rus(quiz_score[QUIZ[muc]['score']], (u'баллов', u'балл', u'балла')) )

     if bonus:
      answer += muc_quiz_bonus_msg % ( QUIZ[muc]['last'][1], string_rus(QUIZ[muc]['last'][1], (u'ответов', u'ответ', u'ответа')), bonus, string_rus(bonus, (u'баллов', u'балл', u'балла')) )

     save_attribute(( (muc, jid, 'quiz', (load_attribute(muc, jid, 'quiz') or 0) + quiz_score[QUIZ[muc]['score']]), ))
     reply(t, s, answer)
     quiz_next_question(muc)

    elif b == muc_quiz_cmd_help_msg:
     quiz_cmd_help(muc)

    elif b == muc_quiz_cmd_next_msg:
     quiz_cmd_next(muc)



def process_answer_timer(muc):
 id = random.randrange(0, 9999)		# генерация идентификатора процесса
 print 'ta_id', id
 QUIZ[muc]['timer_answer'] = id			# запись актуального идентификатора

 time.sleep(timer_answer_delay)

 if muc in QUIZ:			# если викторина еще запущена
  if id == QUIZ[muc]['timer_answer']:		# проверка на актуальность данного процесса
   QUIZ[muc]['lock'] = True
   reply('groupchat', (None, muc, None), muc_quiz_no_right_answer_msg + muc_quiz_righrt_answer % QUIZ[muc]['answer'])
   quiz_next_question(muc)



def process_help_timer(muc):
 id = random.randrange(0, 9999)		# генерация идентификатора процесса
 print 'th_id', id
 QUIZ[muc]['timer_help'] = id			# запись актуального идентификатора
 time.sleep(timer_help_delay)

 if muc in QUIZ:			# если викторина еще запущена
  if id == QUIZ[muc]['timer_help']:		# проверка на актуальность данного процесса
   QUIZ[muc]['help'] = True
   print 'quiz help allowed'

 exit(0)


def quiz_next_question(muc):
# QUIZ[muc]['lock'] = True
 QUIZ[muc]['help'] = False

 reply('groupchat', (None, muc, None), muc_quiz_question_msg)

 time.sleep(question_delay)

### чтение рандомного вопроса (взято из O`Relly: Python Cookbook)

 f = open(quiz_base_file, 'r')

 i = 0
 line = ''

 while True:
  random_line = f.readline()
  if not random_line:
   break

  i += 1

  # How likely is it that this is the last line of the file?

  if random.uniform(0,i) < 1:				# как работает???
   line = unicode(random_line, 'windows-1251')

 f.close()

###

# line = u'вопрос|ответ'
 line = line.split('|')

 if muc in QUIZ:
  QUIZ[muc]['question'] = line[0].strip()
  QUIZ[muc]['answer'] = line[1].strip()
  QUIZ[muc]['tip'] = '*'*len(QUIZ[muc]['answer'])
  QUIZ[muc]['lock'] = False

  QUIZ[muc]['score'] = 0
 
  reply('groupchat', (None, muc, None), u'%s [%d %s]' % (QUIZ[muc]['question'], len(QUIZ[muc]['answer']), string_rus(len(QUIZ[muc]['answer']), (u'букв', u'буква', u'буквы'))))

  with threading.BoundedSemaphore(value = 100):
   threading.Thread(None, process_answer_timer, 'quiz_time_' + muc, (muc,)).start()

  with threading.BoundedSemaphore(value = 100):
   threading.Thread(None, process_help_timer, 'quiz_help_' + muc, (muc,)).start()



register_command_handler(handler_quiz_start, u'.викторина', [u'конфа', u'все'], u'Запуск викторины. Для очистки результатов виторины используйте команду ".очистить %s"' % quiz_clear_key, u'.викторина', 15)
register_message_handler(handler_message_quiz)
