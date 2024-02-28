import yaml
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config',type=str, default='dev.yml',help='放在configs文件夹下的配置文件名称')

args = parser.parse_args()

class WebConfig():
    def __init__(self, config_path=f'configs/{args.config}'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
            # 密钥，cmd输入获取：openssl rand -hex 32
            self.sk = 'beaa7dbf68bdf1a46298e5258629cdec898a16df57aeb133c63bdcd2b0476a80'
            if sk := self.config.get('SECRET_KEY'):
                if len(sk) > 0:
                    self.sk = sk
                
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
    
webConfig = WebConfig()