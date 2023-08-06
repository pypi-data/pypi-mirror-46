from unicon.eal.dialogs import Statement


def login_handler(spawn, patterns):
    spawn.sendline(patterns.login_username)
    spawn.expect('Password: ')
    spawn.sendline(patterns.login_password)
    spawn.expect('Cisco Firepower')
    spawn.sendline()


class KpStatements:
    def __init__(self, patterns):
        self.login_password = Statement(pattern=patterns.prompt.prelogin_prompt,
                                        action=login_handler,
                                        args={'patterns': patterns},
                                        loop_continue=True,
                                        continue_timer=True)

        self.login_incorrect = Statement(pattern='Login incorrect',
                                         action=None,
                                         args=None,
                                         loop_continue=False,
                                         continue_timer=False)
