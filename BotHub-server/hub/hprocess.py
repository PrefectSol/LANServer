import time
import re
from multiprocessing import Process

from hub.game import Game
from utils.status import StatusCode


class HProcess(Process):
    def __init__(self, child_conn, game_config: dict, source_code: str, settings: dict):
        super(HProcess, self).__init__()
        self._child_conn = child_conn
        self._game_config = game_config
        self._source_code = source_code
        self._settings = settings
        self._log_data = {'msg': '', 'status': StatusCode.Unknown}
            
        
    def run(self):       
        time.sleep(100) 
        # if not self.__add_class(self._game_config, self._source_code, self._settings):
        #     self._log_data['msg'] = 'Failed to create custom class.'
        #     self._log_data['status'] = StatusCode.FailedCreateUserClass
        #     self._child_conn.send(self._log_data)
        #     return 

        # self.__await_bots()
        
        # self._game.set_state()
        # self.__log()
        
        # epoch = 0
        # while self._game.is_playing and epoch < self._game_config['iterations']: 
        #     self._game.step()
        #     self.__log(epoch=epoch)      
        #     epoch += 1
        #     time.sleep(self._game_config['delay'])
            
    
    def __await_bots(self):
        pass        
    
            
    def __add_class(self, game_config: dict, source_code: str, settings: dict) -> bool:
        match = re.search('class (\\w+)', source_code)
        if not match:
            return False
        
        class_name = match.group(1)
        if class_name != game_config['name']:
            return False
        
        try:    
            exec(source_code)
            self._game_class = eval(class_name)
            self._game = self._game_class(settings)
        except:
            return False
        
        return True
    
    
    def __log(self, epoch=None):
        result = self._game.get_log()
        
        if not (epoch is None):
            self._log_data['msg'] = f'ITERATION: {epoch + 1}\n' + result['msg']
        else:
            self._log_data['msg'] = result['msg']
            
        self._log_data['status'] = StatusCode.Success if result['status'] == 0 else StatusCode.InternalGameError
        self._child_conn.send(self._log_data)