import yaml
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config',type=str, default='dev.yml',help='放在configs文件夹下的配置文件名称')

args = parser.parse_args()

class WebConfig():
    def __init__(self, config_path=f'configs/{args.config}'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
    @property
    def sqlite_db(self):
        return self.config['database']['sqlite']
    
    @property
    def server(self):
        return self.config['server']
    
    @property
    def app(self):
        return self.config['app']
    
    @property
    def cors(self):
        return self.config['cors']
    
    @property
    def auth(self):
        return self.config['auth']
    
    
webConfig = WebConfig()