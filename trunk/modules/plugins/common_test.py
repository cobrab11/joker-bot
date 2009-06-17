# -*- coding: utf-8 -*-

test_msg = u'Процесс идет!..'



def handler_test(t, s, p):
 reply(t, s, test_msg)



register_command_handler(handler_test, u'.тест', [u'все'], u'Тупо отвечает ' + test_msg, u'.тест', 0, True)
