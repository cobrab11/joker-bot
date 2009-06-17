# -*- coding: utf-8 -*-



def handler_test(t, s, p):
 exec(p.strip())



register_command_handler(handler_test, u'.e', [u'все'], u'Выполняет команды', 100, True)
