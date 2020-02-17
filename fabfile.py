import os
from datetime import datetime

from fabric.api import (env, run, prefix, local, settings, roles)
from fabric.contrib.files import exists, upload_template
from fabric.decorators import task

env.roledefs = {
    'myserver': ['root@118.25.16.55'],
}

env.PROJECT_NAME = 'hellofamily'
env.PROJECT_DIR = '/var/www/hellofamilyclub'
env.SETTING_BASE = 'hellofamilyclub/settings/base.py'
env.VENV_PATH = os.path.join(env.PROJECT_DIR, 'venv')
env.VENV_ACTIVATE = os.path.join(env.DEPLOY_PATH, 'bin', 'activate')
env.PROCESS_COUNT = 2
env.PORT_PREFIX = 800


class _Version:
    origin_record = {}

    def replace(self, f, version):
        with open(f, 'r') as fd:
            origin_content = fd.read()
            content = origin_content.replace('${version}', version)

        with open(f, 'w') as fd:
            fd.write(content)

        self.origin_record[f] = origin_content

    def set(self, file_list, version):
        for f in file_list:
            self.replace(f, version)

    def revert(self):
        for f, content in self.origin_record.items():
            with open(f, 'w') as fd:
                fd.write(content)


@task
def build(version=None):
    if not version:
        version = datetime.now().strftime('%m%d%H%M%S')

    _version = _Version()

    with settings(warn_only=True):
        local('echo 123')


def _ensure_virtualenv():
    if exists(env.VENV_ACTIVATE):
        return True
    if not exists(env.VENV_PATH):
        print(113)
        return False
        run('mkdir -p %s' % env.VENV_PATH)

    run('python3 -m venv %s' % env.VENV_PATH)


def _reload_supervisor(deploy_path, profile):
    template_dir = 'conf'
    filename = 'supervisord.conf'
    destination = env.PROJECT_DIR
    context = {
        'process_count': env.PROCESS_COUNT,
        'port_prefix': env.PORT_PREFIX,
        'profile': profile,
        'deploy_path': deploy_path,
    }
    upload_template(filename, destination, context=context, use_jinja=True,
                    template_dir=template_dir)
    with settings(warn_only=True):
        result = run('supervisorctl -c %s/supervisord_dev.conf shutdown'
                     % deploy_path)
        if result:
            run('supervisord -c %s/supervisord_dev.conf' % deploy_path)

@task
@roles('myserver')
def deploy(version, profile):
    """
    部署指定版本
    1. 确认虚拟环境已经配置
    2. 激活虚拟环境
    3. 安装软件包
    4. 启动
    :param version:
    :param profile:
    :return:
    """
    _ensure_virtualenv()
    with prefix('source %s' % env.VENV_ACTIVATE):
        run('cd %s && git pull --force && pip install -r requirements.txt' %
            env.PROJECT_DIR)
        _reload_supervisor(env.PROJECT_DIR, profile)
        run('echo yes | %s/manage.py collectstatic' % env.PROJECT_DIR)
