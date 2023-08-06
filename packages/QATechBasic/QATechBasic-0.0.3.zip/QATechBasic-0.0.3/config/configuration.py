# -*- coding: utf-8 -*-
# author:      hj
# create_time: 2018/12/19 11:10
# update_time: 2018/12/19 11:10
import ConfigParser
import os
import re
import threading


class Configuration:
    """
    cached all of system configuration.
    configuration implement will overwrite application.config properties when option is equal.
    """
    _instance_lock = threading.Lock()
    config = {}     # 暂存所有的配置文件信息

    DEFAULT_CONFIG_FILE_NAME = 'application.config'     # 默认配置文件
    DEFAULT_DEPLOY_RESOURCE_DIR = './resource'  # 默认部署路径

    def __init__(self, config_path):
        """
        :param config_path: D:\qatech\workspace\integration_core_src\resource/application.config
        """
        if not hasattr(Configuration, "_instance"):
            if not os.path.exists(config_path):
                raise RuntimeError('Can not find about application config.')

            config_parser = ConfigParser.RawConfigParser()
            config_parser.read(config_path)

            # 字符串拼接处理
            arr1 = re.split(r"[/\\]", config_path)
            self.config_file_name = arr1[arr1.__len__()-1]
            __file_name_arr = self.config_file_name.split('.')
            self.resources_dir = "/".join(arr1[0:arr1.__len__()-1])
            profiles_active = config_parser.get('root', 'profiles_active')
            if profiles_active:
                profiles_active_config_file_name = __file_name_arr[0]+'-'+profiles_active+'.'+__file_name_arr[1]
                if not os.path.exists(os.path.join(self.resources_dir, profiles_active_config_file_name)):
                    raise RuntimeError('Can not read profiles active config file name:' +
                                       profiles_active_config_file_name)
                config_parser.read(os.path.join(self.resources_dir, profiles_active_config_file_name))

            for option in config_parser.options('root'):
                self.config[option] = config_parser.get('root', option)

    @classmethod
    def instance(cls, config_path):
        if not hasattr(Configuration, "_instance"):
            with Configuration._instance_lock:
                if not hasattr(Configuration, "_instance"):
                    Configuration._instance = Configuration(config_path)
        return Configuration._instance

    def get_str(self, key, default_value=''):
        """
        获取字符串
        :param key:
        :param default_value:
        :return:
        """
        try:
            value = self.config.get(key)
            if not value:
                return default_value
            return str(value)
        except Exception as e:
            print e.message
        return default_value

    def get_boolean(self, key, default_value=False):
        """
        获取布尔值
        :param key: 配置文件
        :param default_value:
        :return:
        """
        try:
            value = self.config.get(key)
            if not value:
                return default_value
            if value:
                if str(value).isdigit():
                    if str(value).strip() == '0':
                        return False
                    else:
                        return True
                else:
                    if str(value).lower().strip() == 'true':
                        return True
                    else:
                        return False
        except Exception as e:
            print e.message
        return default_value

    def get_int(self, key, default_value=0):
        """
        获取数值
        :param key:
        :param default_value:
        :return:
        """
        try:
            value = self.config.get(key)
            if not value:
                return default_value
            if value:
                if str(value).isdigit():
                    return int(value)
                else:
                    return eval(value)
        except Exception as e:
            print e.message
        return default_value

    def get_long(self, key, default_value=0):
        """
        获取数值
        :param key:
        :param default_value:
        :return:
        """
        try:
            value = self.config.get(key)
            if not value:
                return default_value
            if value:
                if str(value).isdigit():
                    return long(value)
                else:
                    return eval(value)
        except Exception as e:
            print e.message
        return default_value

    def get_float(self, key, default_value=0):
        """
        获取数值
        :param key:
        :param default_value:
        :return:
        """
        try:
            value = self.config.get(key)
            if not value:
                return default_value
            if value:
                if str(value).isdigit():
                    return float(value)
                else:
                    return eval(value)
        except Exception as e:
            print e.message
        return default_value

    def get_path(self, key, default_value=''):
        """
        查找目录或文件，主要在于解析classpath
        :param key:
        :param default_value:
        :return:
        """
        try:
            value = self.config.get(key)
            if value:
                if re.findall(r'classpath *:', str(value)):
                    value = re.sub(r'classpath *:', '', str(value))
                    relate_path = value.lstrip().rstrip()
                    if re.findall(r'^/', str(value).rstrip()):
                        relate_path = re.sub(r'^/', '', str(value).rstrip())
                    return os.path.join(self.resources_dir, relate_path)
                else:
                    return str(value)
        except Exception as e:
            print e.message
        return default_value


if __name__ == "__main__":
    # print Configuration.instance().get_float('logger.rotate.file.max.bytes')
    # print Configuration.instance().get_boolean("system.license.enabled")
    # print Configuration.instance().get_path('db.init_data.file.path')
    # print Configuration.instance().get_path("port.scan.mass_scan.installation.directory")
    print Configuration.instance().get_str("ffmpeg.task_kill.command")