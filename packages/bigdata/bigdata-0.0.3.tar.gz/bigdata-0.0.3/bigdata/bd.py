from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
import pexpect

@magics_class
class bdMagic(Magics):

    def __init__(self, shell):
        super(bdMagic, self).__init__(shell)
        self.CLI_start = {
            'hive': 'hive  ',
            'pig': 'pig '
        }
        self.CLI_prompt = {
            'hive': 'hive> ',
            'pig': 'grunt>'
        }
        self.CLI_cont = {
            'hive': '    > ',
            'pig': '>> '
        }
        self.CLI_quit = {
            'hive': 'quit;',
            'pig': 'quit'
        }
        self.app = {
            'hive': None,
            'pig': None
        }
        self.timeout = 30
        
    @line_magic
    def timeout(self, line):
        self.timeout = int(line)

    @line_magic
    def pig_start(self, line):
        return self.start('pig', line)
    
    @line_magic
    def hive_start(self, line):
        return self.start('hive', line)
    
    def start(self, appname, line):
        if self.app[appname] is not None:
            self.app[appname].close()
        self.app[appname] = pexpect.spawn(self.CLI_start[appname] + ' ' + line, timeout=self.timeout)
        self.app[appname].expect(self.CLI_prompt[appname], timeout=self.timeout)
        return None
        
    @cell_magic
    def pig(self, line, cell):
        return self.run('pig', line, cell)

    @cell_magic
    def hive(self, line, cell):
        return self.run('hive', line, cell)

    def run(self, appname, line, cell):
        if self.app[appname] is None:
            self.start(appname, line)
        x = cell.split('\n')
        for row in x:
            if row.strip() != '':
                self.app[appname].sendline(row)
                self.app[appname].expect(['\r\n'+self.CLI_cont[appname], 
                                          '\r\n'+self.CLI_prompt[appname]], 
                                         timeout=self.timeout)
                print(self.app[appname].before.decode())
        return None        

    @line_magic
    def hive_quit(self, line):
        self.quit('hive', line)
        return None
    
    @line_magic
    def pig_quit(self, line):
        self.quit('pig', line)
        return None

    def quit(self, appname, line):
        #self.app[appname].expect(self.CLI_quit[appname] + ' ' + line, timeout=self.timeout)
        self.app[appname].close()
        self.app[appname] = None
        return None        

    
def load_ipython_extension(ip):
    bdmagic = bdMagic(ip)
    ip.register_magics(bdmagic)


## esta linea se requiere para depuracion directa 
## en jupyter (commentar para el paquete)
## load_ipython_extension(ip=get_ipython())