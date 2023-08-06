from nameko.extensions import DependencyProvider

from elasticsearch_dsl.connections import connections

ELASTICSEARCH_SETTINGS_NAME = 'ELASTICSEARCH'


class ElasticSearch(DependencyProvider):
    """ElasticSearch 依赖注入"""
    __es_hosts = None

    def setup(self):
        """初始化设置"""
        # 此时container尚未启动，但是可以从container获取ElasticSearch配置
        try:
            print(self.container.config)
            self.__es_hosts = self.container.config[ELASTICSEARCH_SETTINGS_NAME]['HOSTS']
        except KeyError:
            raise KeyError("ElasticSearch settings name {} or HOSTS settings don't exist in the yaml config file.".format(ELASTICSEARCH_SETTINGS_NAME))

    def get_dependency(self, worker_ctx):
        """实现elastic connection注入service worker的方法"""
        try:
            es = connections.get_connection()
        except KeyError as e:
            es = connections.create_connection(hosts=self.__es_hosts)

        return es
