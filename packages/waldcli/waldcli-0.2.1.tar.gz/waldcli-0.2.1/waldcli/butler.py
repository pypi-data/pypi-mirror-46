#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" butler allows to setup a welance craft3 cms project """

import argparse
import json
import os
import re
import secrets
import subprocess
import sys
import webbrowser
import datetime
import requests
# TODO: do not use 2 different yaml parser in the same project
import yaml
#
from waldcli import prompt

""" name of the out configuration file """


#   ______      ___      ______  ___  ____   ________  _______
#  |_   _ `.  .'   `.  .' ___  ||_  ||_  _| |_   __  ||_   __ \
#    | | `. \/  .-.  \/ .'   \_|  | |_/ /     | |_ \_|  | |__) |
#    | |  | || |   | || |         |  __'.     |  _| _   |  __ /
#   _| |_.' /\  `-'  /\ `.___.'\ _| |  \ \_  _| |__/ | _| |  \ \_
#  |______.'  `.___.'  `.____ .'|____||____||________||____| |___|
#

class DockerCli(object):

    def __init__(self, project_name, verbose=False):
        self.verbose = verbose
        self.project_name = project_name

    def compose(self, params, yaml_path="docker-compose.yml"):
        """ execte docker-compose commmand """
        cmd = f"docker-compose -f {yaml_path} {params}"
        prompt.code(cmd)
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            prompt.err("Error executing docker-compose command", e)

    def compose_stop(self, yaml_path):
        self.compose(f"--project-name {self.project_name} stop ", yaml_path)

    def compose_start(self, yaml_path):
        self.compose(f"--project-name {self.project_name} up -d ", yaml_path)

    def compose_down(self, yaml_path):
        self.compose(f"--project-name {self.project_name} down -v", yaml_path)

    def compose_setup(self, yaml_path):
        # Detached mode: Run containers in the background
        self.compose(f"--project-name {self.project_name} up --no-start ", yaml_path)

    def compose_pull(self, yaml_path):
        self.compose("pull --ignore-pull-failures", yaml_path)

    def exec(self, container_target, command, additional_options=""):
        """ execte docker exec commmand and return the stdout or None when error """
        cmd = """docker exec -i "%s" sh -c '%s' %s""" % (
            container_target, command, additional_options)
        if self.verbose:
            print(cmd)
        try:
            cp = subprocess.run(cmd,
                                shell=True,
                                check=True,
                                stdout=subprocess.PIPE)
            return cp.stdout.decode("utf-8").strip()
        except Exception as e:
            prompt.err(f"Docker exec command failed", e)
            return None

    def cp(self, container_source, container_path, local_path="."):
        """ copy a file from a container to the host """
        # docker cp <containerId>:/file/path/within/container /host/path/target
        cmd = """docker cp %s:%s %s""" % (
            container_source, container_path, local_path)
        print(cmd)
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception:
            pass

    @classmethod
    def list_image_versions(cls, name, max_results=0):
        """retrieve the list of versions and it's size in MB of an image from docker hub"""
        url = f"https://registry.hub.docker.com/v2/repositories/{name}/tags/"
        try:
            images = requests.get(url).json()
        except Exception:
            print("sorry chief, I cannot contact dockerhub right now, try again later")
            exit(0)
        default_version = 0
        versions = []
        for v in images["results"]:
            if v['name'] == 'latest' and images['count'] > 1:
                continue
            versions.append((v['name'], v['full_size'] / 1048576))
        versions = versions[0:max_results] if max_results > 0 else versions
        return default_version, versions


#     ______  ____    ____  ______     ______
#   .' ___  ||_   \  /   _||_   _ `. .' ____ \
#  / .'   \_|  |   \/   |    | | `. \| (___ \_|
#  | |         | |\  /| |    | |  | | _.____`.
#  \ `.___.'\ _| |_\/_| |_  _| |_.' /| \____) |
#   `.____ .'|_____||_____||______.'  \______.'
#


class Commander(object):
    """ main class for command exectution"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        # absolute path to the project root
        self.project_path = os.getcwd()
        # absolute path to the possible config path locaitons
        config_search_paths = [
            os.path.join(self.project_path, config['project_conf_file']),
            os.path.join(self.project_path, "bin", config['project_conf_file']),  # legacy
            os.path.join(self.project_path, "config", config['project_conf_file']),
        ]
        # tells if the project has a configuration file
        self.project_is_configured = False
        self.project_conf = {}
        for p in config_search_paths:
            if os.path.exists(p):
                self.config_path = p
                fp = open(self.config_path, 'r')
                self.project_conf = json.load(fp)
                fp.close()
                self.project_is_configured = True
                self.__register_env()
                break
        # path for staging and local yaml
        self.local_yml = os.path.join(self.project_path, "build", config['docker_compose_local'])
        self.stage_yml = os.path.join(self.project_path, "build", config['docker_compose_stage'])

    def __register_env(self):
        """will register the project coordinates and instantiate the clients"""
        # project code
        c, p = self.project_conf['customer_number'], self.project_conf['project_number']
        self.p_code = f"p{c}-{p}"
        self.db_container = f"{self.p_code}_database"
        self.cms_container = f"{self.p_code}_craft"
        # communicate with th propmt
        self.docker = DockerCli(self.p_code)

    def semver(self):
        """ create a string representation of the versino of the project """
        ma = self.project_conf.get("semver_major", config['semver_major'])
        mi = self.project_conf.get("semver_minor", config['semver_minor'])
        pa = self.project_conf.get("semver_patch", config['semver_patch'])
        self.project_conf["semver_major"] = ma
        self.project_conf["semver_minor"] = mi
        self.project_conf["semver_patch"] = pa
        return f"{ma}.{mi}.{pa}"

    def require_configured(self, with_containers=False):
        """ check if the project is configured or die otherwise """
        if not self.project_is_configured:
            prompt.ln("The project is not yet configured, run the setup command first")
            exit(0)

    def upc(self, key, default_value):
        """set a project_conf value if it is not alredy set"""
        if key not in self.project_conf:
            self.project_conf[key] = default_value

    def write_file(self, filepath, data):
        """ write a file to the filesystem """
        fp = open(filepath, 'w')
        fp.write(data)
        fp.close()

    # delete the last file of the file
    def delete_last_line(self, filepath):

        # delete the EXPOSE port info from the previous project
        try:
            file = open(filepath, "r+", encoding="utf-8")
        except FileNotFoundError as e:
            prompt.err("The file to delete the last line is not found", e)
            return

        # Move the pointer (similar to a cursor in a text editor) to the end of the file.
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()

        file.close()

    def delete_file(self, filepath):
        """ delete a file if exists """
        if os.path.exists(filepath):
            os.unlink(filepath)

    def cmd_setup(self, args=None):

        if args.reset:
            if (not prompt.ask_yesno("Are you sure to delete the project configuration", default_yes=False)):
                prompt.ln("aborted, bye!")
                return
            self.delete_file(os.path.join(self.project_path, "build", "ci", "Dockerfile"))
            self.delete_file(os.path.join(self.project_path, "build", "docker-compose.yml"))
            self.delete_file(os.path.join(self.project_path, "build", "docker-compose.staging.yml"))
            self.delete_file(self.config_path)
            prompt.ln("Project configuration deleted")
            return 0

        """set up the application """
        # shorcut since "self.project_conf" is too long to write
        pc = self.project_conf
        # if the config  already exists prompt what to do
        if pc and not prompt.ask_yesno("The project is already configured, do you want to override the existing configuration?", default_yes=False):
            self.prompt.say('setup_abort')
            return
        # ask for customer number
        pc['customer_number'] = prompt.ask_int("Customer number: ")
        pc['project_number'] = prompt.ask_int("Project number: ")
        pc['site_name'] = prompt.ask_str(f"Site name? {config['default_site_name']}")
        pc['local_url'] = prompt.ask_str(f"Dev URL? {config['default_local_url']}")
        pc['db_driver'] = prompt.ask_str(f"DB driver? {config['default_db_driver']}")

        # retrieve image versions
        dv, vers = DockerCli.list_image_versions(config['dockerhub_cms_image'], 4)
        self.upc("security_key", secrets.token_hex(32))
        for i in range(len(vers)):
            num = "* [%2d]" % i if i == dv else "  [%2d]" % i
            print("%s %10s %dMb" % (num, vers[i][0], vers[i][1]))
        iv = int(prompt.ask_int("Which version do you want to use? [default with *]: ", 0, len(vers) - 1, def_val=dv))
        # select the version name from the version chosen by the user
        pc["craft_image"] = f"{config['dockerhub_cms_image']}:{vers[iv][0]}"
        # build stage domain
        c, p = pc['customer_number'], pc['project_number']
        pc['stage_url'] = f"p{c}-{p}.{config['staging_domain']}"

        #  print summary for the project creation
        print("")

        self.upc("semver_patch", config['semver_patch'])
        self.upc("craft_allow_updates", config['default_craft_allow_updates'])

        self.upc("lang", "C.UTF-8")
        self.upc("environment", "dev")
        self.upc("craft_locale", "en_us")
        self.upc("httpd_options", "")

        print("")

        self.project_conf['local_plugins'] = []

        plugins_path = str(self.project_path) + "/plugins"

        prompt.ln(f"Customer Number: {pc['customer_number']}")
        prompt.ln(f"Project  Number: {pc['project_number']}")
        prompt.ln(f"Site Name      : {pc['site_name']}")
        prompt.ln(f"Local Url      : {pc['local_url']}")
        prompt.ln(f"Staging Host   : {pc['stage_url']}")
        prompt.ln(f"Db Driver      : {pc['db_driver']}")
        prompt.ln(f"Craft version  : {pc['craft_image']}")

        # ask for confirmation
        if (not self.prompt.ask_yesno('Are this information correct', default_yes=True)):
            self.prompt.ln('Setup aborted')
            return
        # register env and instantiate docker cli
        self.__register_env()
        # generate security key
        self.upc("security_key", secrets.token_hex(32))
        # set the other default values
        self.upc("craft_image", config['dockerhub_cms_image'])
        self.upc("db_schema", config['default_db_schema'])
        self.upc("db_server", config['default_db_server'])
        self.upc("db_database", config['default_db_name'])
        self.upc("db_user", config['default_db_user'])
        self.upc("db_password", config['default_db_pass'])
        self.upc("db_table_prefix", config['default_db_table_prefix'])
        self.upc("craft_username", config['default_craft_username'])
        self.upc("craft_email", config['default_craft_email'])
        self.upc("craft_password", config['default_craft_passord'])
        self.upc("semver_major", config['semver_major'])
        self.upc("semver_minor", config['semver_minor'])
        self.upc("semver_patch", config['semver_patch'])
        self.upc("craft_allow_updates", config['default_craft_allow_updates'])

        self.upc("lang", "C.UTF-8")
        self.upc("environment", "dev")
        self.upc("craft_locale", "en_us")
        self.upc("httpd_options", "")

        self.project_conf['composer_require'] = []

        self.project_conf['local_plugins'] = []

        plugins_path = str(self.project_path) + "/plugins"

        if (os.path.isdir(plugins_path)):

            plugins_dir_path = os.listdir(plugins_path)

            # plugin name convention namespace/pluginname
            for namespace in plugins_dir_path:

                if (os.path.isdir(namespace)):
                    pluginname = os.listdir(os.path.join(plugins_path, namespace))
                    if (len(pluginname) != 1):
                        continue
                    namespace_slash_pluginname = namespace + '/' + pluginname[0]

                    (self.project_conf['local_plugins']).append(namespace_slash_pluginname)

        # docker-compose.yml
        docker_compose = {
            "version": "3.1",
            "services": {
                "craft": {
                    "image": pc["craft_image"],
                    "container_name": f"{self.p_code}_craft",
                    # "ports": ["80:80"],
                    "volumes": [
                        # webserver and php mounts
                        "/var/log",
                        "./docker/craft/conf/apache2/craft.conf:/etc/apache2/conf.d/craft.conf",
                        "./docker/craft/conf/php/php.ini:/etc/php7/php.ini",
                        "./docker/craft/logs/apache2:/var/log/apache2",
                        # adminer utility
                        "./docker/craft/adminer:/data/adminer",
                        # craft
                        "../config:/data/craft/config",
                        "../templates:/data/craft/templates",
                        "../web:/data/craft/web",
                        # plugin directory
                        "../plugins:/data/craft/plugins",
                    ],
                    "links": ["database"],
                    "environment": {
                        "LANG": pc["lang"],
                        "DB_DRIVER": pc['db_driver'],
                        "DB_SCHEMA": pc["db_schema"],
                        "DB_SERVER": pc["db_server"],
                        "DB_DATABASE": pc["db_database"],
                        "DB_USER": pc["db_user"],
                        "DB_PASSWORD": pc["db_password"],
                        "DB_TABLE_PREFIX": pc["db_table_prefix"],
                        "SECURITY_KEY": pc['security_key'],
                        "ENVIRONMENT": pc["environment"],
                        "CRAFT_USERNAME": pc["craft_username"],
                        "CRAFT_EMAIL": pc["craft_email"],
                        "CRAFT_PASSWORD": pc["craft_password"],
                        "CRAFT_SITENAME": pc['site_name'],
                        "CRAFT_SITEURL": f"//{pc['local_url']}",
                        "CRAFT_LOCALE": pc["craft_locale"],
                        "CRAFT_ALLOW_UPDATES": pc["craft_allow_updates"],
                        "CRAFT_DEVMODE": 1,  # enable development mode
                        "CRAFT_ENABLE_CACHE": 0,  # disable cache
                        "HTTPD_OPTIONS": pc["httpd_options"],

                    }
                }
            }
        }

        if pc['db_driver'] == 'mysql':
            docker_compose["services"]["database"] = {
                "image":
                    "mysql:5.7",
                "command":
                    "mysqld --character-set-server=utf8  --collation-server=utf8_unicode_ci --init-connect='SET NAMES UTF8;'",
                "container_name": f"{self.p_code}_database",
                "environment": {
                    "MYSQL_ROOT_PASSWORD": self.project_conf["db_password"],
                    "MYSQL_DATABASE": self.project_conf["db_database"],
                    "MYSQL_USER": self.project_conf["db_user"],
                    "MYSQL_PASSWORD": self.project_conf["db_password"]
                },
                "volumes": ["/var/lib/mysql"]
            }
            # set the correct DB_PORT for craft env
            docker_compose["services"]["craft"]["environment"]["DB_PORT"] = "3306"
        elif pc['db_driver'] == 'pgsql':
            docker_compose["services"]["database"] = {
                "image": "postgres:10-alpine",
                "container_name": f"{self.p_code}_database",
                "environment": {
                    "POSTGRES_PASSWORD": pc["db_password"],
                    "POSTGRES_USER": pc["db_user"],
                    "POSTGRES_DB": pc["db_database"]
                },
                "volumes": ["/var/lib/postgresql/data"]
            }
            # set the correct DB_PORT for craft env
            docker_compose["services"]["craft"]["environment"]["DB_PORT"] = "5432"
        else:
            prompt.ln("The value for Db Driver must be mysql or pgsql, aborted.")
            return 1

        # save docker-composer
        self.write_file(self.local_yml, yaml.dump(docker_compose, default_flow_style=False))
        # edit for docker-compose.staging.yaml
        # add the web network
        docker_compose["networks"] = {
            "web": {
                "external": True
            }
        }

        docker_compose["services"]["craft"]["networks"] = ["web"]
        docker_compose["services"]["database"]["networks"] = ["web"]
        # change the image
        docker_compose["services"]["craft"]["image"] = f"registry.welance.com/{self.p_code}:latest"
        # remove volumes
        docker_compose["services"]["craft"].pop("volumes")

        # disable develpment mode and set the website url
        docker_compose["services"]["craft"]["environment"]["CRAFT_SITEURL"] = f"//{pc['stage_url']}"
        docker_compose["services"]["craft"]["environment"]["CRAFT_DEVMODE"] = 0
        docker_compose["services"]["craft"]["environment"]["CRAFT_ENABLE_CACHE"] = 1

        # save docker-composer
        self.write_file(self.stage_yml, yaml.dump(docker_compose, default_flow_style=False))

        # save project conf
        self.write_file(self.config_path, json.dumps(self.project_conf, indent=2))

        # save the dockerfile for ci build
        dockerfile = [
            '# this has to be consistent with the craft version ',
            '# used to develop the website.',
            '# (the one mentioned in the docker-compose.yaml file)',
            '# this is the image that will be used in staging',
            f'FROM {pc["craft_image"]}',
            'LABEL mainteiner="andrea@welance.com"',
            '# override the template',
            'COPY build/docker/craft/scripts /data/scripts',
            'COPY build/docker/craft/conf/apache2/craft.conf /etc/apache2/conf.d/craft.conf',
            'COPY build/docker/craft/conf/php/php.ini /etc/php7/php.ini',
            'COPY build/docker/craft/adminer /data/adminer',
            'COPY config /data/craft/config',
            'COPY templates /data/craft/templates',
            'COPY web /data/craft/web',
            'COPY plugins /data/craft/plugins',
            'COPY translations /data/craft/translations',
            'COPY migrations /data/craft/migrations',
            '# fix permissions',
            'RUN chmod +x /data/scripts/*.sh',
            'RUN chmod +x /data/craft/craft',
            'RUN chown -R apache:apache /data/craft',
            '# everthing is in /data',
            'WORKDIR /data',
            'CMD ["/data/scripts/run-craft.sh"]',
        ]

        # save the docker file
        dockerfile_path = os.path.join(self.project_path, "build", "ci", "Dockerfile")
        self.write_file(dockerfile_path, "\n".join(dockerfile))

        # all done

        prompt.ln("Pulling docker images")
        self.docker.compose_pull(self.local_yml)
        prompt.ln("Creating containers")
        self.docker.compose_setup(self.local_yml)
        prompt.ln("Setup completed")

    def cmd_restore(self, ns=None):
        """restore a project that has been teardown, recreating the configurations """
        self.require_configured()
        # if the config  already exists prompt what to do
        if self.project_conf:
            prompt.ln("Pulling docker images")
            self.docker.compose_pull(self.local_yml)
            prompt.ln("Creating containers")
            self.docker.compose_setup(self.local_yml)
            prompt.ln("Restore completed")

    def cmd_start(self, args=None):
        """start the docker environment"""
        self.require_configured()
        # get the optional port
        local_start_port = str(args.port)
        docker_compose = {}
        # TODO: use docker-compose.override.yaml
        # read the "docker-compose.yml" file
        with open(self.local_yml, 'r') as s:
            try:
                docker_compose = yaml.safe_load(s)
            # we are not able to read the docker-compose.yml file
            except yaml.YAMLError as e:
                # TODO: question doesn't make sense
                prompt.err("The 'docker-compose.yml' can't be read. Do you setup the project correctly?", e)
                return

        docker_compose["services"]["craft"]["ports"] = [local_start_port + ":" + "80"]
        # dump the info to the "docker-compose.yml" file
        self.write_file(self.local_yml, yaml.dump(docker_compose, default_flow_style=False))
        # start the command
        self.docker.compose_start(self.local_yml)
        if (not self.project_conf['local_plugins']):
            prompt.ln("We don't have any local plugins to install")
        else:
            for lp in self.project_conf['local_plugins']:
                cmd = f"cd craft && composer config repositories.repo-name path plugins/" + lp
                self.docker.exec(self.cms_container, cmd)

                cmd = f"cd craft && composer require {lp} --no-interaction"
                self.docker.exec(self.cms_container, cmd)

                # strip the namespace
                p = re.sub(r'^.*?/', '', lp)
                cmd = f"chmod +x craft/craft"  # allow craft to execute
                self.docker.exec(self.cms_container, cmd)
                cmd = f"craft/craft install/plugin {p}"
                self.docker.exec(self.cms_container, cmd)

        # cmd = f"cd craft && composer config repositories.repo-name path plugins/ansport"
        # self.docker.exec(self.cms_container, cmd)
        #
        # cmd = f"cd craft && composer config repositories.repo-name path plugins/zeltinger"
        # self.docker.exec(self.cms_container, cmd)

        # we start the project for the first time
        if (not self.project_conf['composer_require']):

            for p in config['composer_require']:
                self.plugin_install(p)

        # other developers worked in the projects
        # and installed a few plugins already
        else:
            for p in self.project_conf['composer_require']:
                self.plugin_install(p)

        # we will create a initial SQL dump in the host machine (/config). This will
        # be mounted later in the container at the time of start and will be in-sync in
        # the same mapping as long as the container exists.
        self.cmd_seed_export(None, "config", 'backup-{date:%Y-%m-%d_%H:%M:%S}.sql'.format(date=datetime.datetime.now()))
        prompt.ln("The initial database dump is provided in the config directory")

    def cmd_stop(self, args=None):
        """stop the docker environment"""
        self.require_configured()
        target_yaml = self.local_yml
        self.docker.compose_stop(target_yaml)

    def cmd_teardown(self, args=None):
        """destroy the docker environment"""
        self.require_configured()
        target_yaml = self.local_yml
        if prompt.ask_yesno("This action will remove all containers including data, do you want to continue", default_yes=False):
            self.docker.compose_down(target_yaml)

    def cmd_ports_info(self, args=None):

        cmd = "docker ps --format '{{.Ports}}'"

        try:
            cp = subprocess.run(cmd,
                                shell=True,
                                check=True,
                                stdout=subprocess.PIPE)
            cp = cp.stdout.decode("utf-8").strip()

            lines = str(cp).splitlines()
            ports = []

            for line in lines:

                items = line.split(",")

                for item in items:
                    port = re.findall('\d+(?!.*->)', item)
                    ports.extend(port)

            # create a unique list of ports utilized
            ports = list(set(ports))

            # no port is being used for the project
            if (not ports):
                prompt.ln("No port is currently being used")

            # project uses some network ports
            else:
                prompt.ln(f"List of ports utilized till now {ports}\nPlease, use another port to start the project")

        except Exception as e:
            print(f"Docker exec failed command {e}")
            return None

    def cmd_info(self, ns=None):
        """print the current project info and version"""
        self.require_configured()
        pc = self.project_conf

        # provide all the associated info for the respective project
        print("")
        prompt.ln(f"Customer Number : {pc['customer_number']}")
        prompt.ln(f"Project  Number : {pc['project_number']}")
        prompt.ln(f"Site Name       : {pc['site_name']}")
        prompt.ln(f"Staging Url     : https://{pc['stage_url']}")
        prompt.ln(f"Db Driver       : {pc['db_driver']}")
        prompt.ln(f"Project Version : {self.semver()}")
        print("")

    def cmd_package_release(self, ns=None):
        """create a gzip containg the project release"""
        self.require_configured(with_containers=True)
        pc = self.project_conf

        prompt.ln(f"Current version is {self.semver()}")
        val = prompt.ask_int("semver", 0, 2, 0)
        if int(val) == 0:
            pc['semver_major'] += 1
            pc['semver_minor'] = config['semver_minor']
            pc['semver_patch'] = config['semver_patch']
        elif int(val) == 1:
            pc['semver_minor'] += 1
            pc['semver_patch'] = config['semver_patch']
        else:
            pc['semver_patch'] += 1

        # workflow before the package release
        # TODO: are we sure that this should be done here?
        #
        # a. install node and npm in the "/data" folder
        # b. move to craft/templates folder
        # c. run "$ npm install"
        # d. run "$ npm run prod"

        cmd = f"apk add --update nodejs nodejs-npm"
        self.docker.exec(self.cms_container, cmd)

        cmd = f"if cd craft/templates ; then npm install && npm run prod; fi"
        self.docker.exec(self.cms_container, cmd)

        # dump the seed database
        self.cmd_seed_export()

        release_path = f"/data/release_{self.p_code}-{self.semver()}.tar.gz"

        # create archive of the /data/craft directory
        # maybe some directories could be excluded ?
        cmd = "tar -c /data/craft | gzip > %s" % release_path
        self.docker.exec(self.cms_container, cmd)

        # copy the archive locally
        self.docker.cp(self.cms_container, release_path, self.project_path)

        # remove the archive in the container
        cmd = f"rm {release_path}"
        self.docker.exec(self.cms_container, cmd)

        # save project conf
        self.write_file(self.config_path, json.dumps(self.project_conf, indent=2))

    def cmd_composer_update(self, ns=None):
        """run composer install on the target environment (experimental)"""
        self.require_configured(with_containers=True)
        command = """cd craft && composer update"""
        self.docker.exec(self.cms_container, command)

    def cmd_plugin_install(self, args=None):
        """handles the command to install a plugin with composer in craft environment (@see plugin_install)"""
        self.plugin_install(args.name)

    # to install a new plugin, use a similar command like,
    # #$ bin/butler.py plugin-install -n=nystudio107/craft-typogrify:1.1.17
    def plugin_install(self, plugin_name):

        #  ether/seo:3.1.0 / 3.4.3
        """install a plugin with composer in craft environment
        required format to prvide the info vendor/package:version"""

        self.require_configured(with_containers=True)

        # strip the vendor name
        p = re.sub(r'^.*?/', '', plugin_name)
        v = None

        colon = p.find(':')

        if colon >= 0:
            v = p[colon + 1:]
            p = p[:colon]

        command = f"cd craft && composer show --installed | grep {p}"

        result = self.docker.exec(self.cms_container, command)

        # we have the plugin installed, however, we
        # still need to check if it's the same version
        if (result is not None):

            installed_ver = str(result).splitlines()[0].strip().split()[1]

            if (v is not None and v == installed_ver):
                prompt.ln(f"Plugin {p} v{v} already installed.")
                return

        # either we don't have the plugin installed or have a different version
        cmd = f"cd craft && composer require {plugin_name} --no-interaction"
        self.docker.exec(self.cms_container, cmd)

        # run craft install
        if (p == "craft-typogrify"):
            p = "typogrify"

        cmd = f"craft/craft install/plugin {p}"
        self.docker.exec(self.cms_container, cmd)

        prompt.ln(f"Plugin {p} installed")

        # get the list of plugins required for the project in conf
        list_of_plugins = list(self.project_conf.get('composer_require', []))

        # if the previous version of plugin is listed, delete that
        for lp in list_of_plugins:

            if p in lp:
                # delete only if the version mis-match
                d = lp.find(':')

                if (d < 0):
                    continue

                ver = lp[d + 1:]

                if (ver is not None and ver is not v):
                    list_of_plugins.remove(lp)

        if plugin_name not in list_of_plugins:
            list_of_plugins.append(plugin_name)
            self.project_conf['composer_require'] = list_of_plugins

            # save project conf
            self.write_file(self.config_path, json.dumps(self.project_conf, indent=2))

        prompt.ln(f'The plugin name {plugin_name}  is listed in the project config file ".butler.json"')

    def cmd_plugin_remove(self, args=None):
        """handles the command line command to uninstall a plugin with composer in craft environment @see plugin_remove"""
        self.plugin_remove(args.name)

    def plugin_remove(self, plugin_name):
        """uninstall a plugin with composer in craft environment (if installed)"""
        self.require_configured(with_containers=True)

        colon = plugin_name.find(':')

        # get the plugin name excluding the version in the format
        # of  vendor/plugin_name  (from vendor/plugin_name:version)
        if colon >= 0:
            plugin_name = plugin_name[:colon]

        # check if the package is already installed
        cmd = f"cd craft && composer show --name-only | grep {plugin_name} | wc -l"
        res = self.docker.exec(self.cms_container, cmd)

        if int(res) <= 0:
            prompt.ln(f"Plugin {plugin_name} is not installed")

        else:
            # run composer uninstall
            cmd = f"cd craft && composer remove {plugin_name} --no-interaction"
            self.docker.exec(self.cms_container, cmd)

        # get the list of plugins required for the project in conf
        required_plugins = list(self.project_conf.get('composer_require', []))

        for p in required_plugins:

            if plugin_name in p:
                required_plugins.remove(p)
                self.project_conf['composer_require'] = required_plugins
                # save project conf
                self.write_file(self.config_path, json.dumps(self.project_conf, indent=2))

        prompt.ln(f"we have just removed the plugin {plugin_name} for the Craft")

    def cmd_seed_export(self, args=None, dir=None, file=None):
        """Schema export using the CLI and at the time of setup

            export the database with name "database-seed.sql" to the "congig"
            direcotry if no other name is provided with the -f or --file tag

            Args:
                it takes the file and directory name
            Returns:
                it doesn't require any value.
            Raises:
                it doesn raise any exception
            """

        self.require_configured(with_containers=True)

        directory = None
        file_name = None

        # we get the file name from the CLI and will save in the "config" directory
        if (args is not None and args.file is not None):
            directory = "config"
            file_name = args.file

        # we set the initial seed at the time of setup
        elif (dir is not None and file is not None):
            directory = dir
            file_name = file

        else:
            directory = "config"
            file_name = config['database_seed']

        export_file = os.path.join(self.project_path, directory, file_name)

        # run mysql dump
        u, p, d = config['default_db_user'], config['default_db_pass'], config['default_db_name']
        command = f'exec mysqldump -u {u} -p"{p}" --add-drop-table {d}'

        if self.project_conf["db_driver"] == "pgsql":
            command = f'exec pg_dump --clean --if-exists -U {u} -d {d}'

        additional_options = "> %s" % export_file

        # we get the request from the CLI with no alternate file name
        if (args is not None and args.file is None):
            _p = "The export will overwrite the existing database-seed.sql, continue"
            if (not prompt.ask_yesno(_p, default_yes=False)):
                prompt.ln("Export aborted")
                return

        self.docker.exec(self.db_container, command, additional_options)

        prompt.ln(f"Database export complete")

    def cmd_seed_import(self, args=None):
        """Schema import using the CLI

            import the database with name "database-seed.sql" from the "congig"
            direcotry if no other name is provided with the -f or --file tag

            Args:
                it can accept the file name from the CLI
            Returns:
                it doesn't require any value.
            Raises:
                it doesn raise any exception
            """

        self.require_configured(with_containers=True)

        import_file = os.path.join(self.project_path, "config", config['database_seed'])
        # we provided a file name from the CLI
        if args is not None and args.file is not None:
            import_file = args.file

        if not os.path.isfile(import_file):
            prompt.ln(f"Seed file not found: {import_file}")
            return

        _q = f"This operation will restore the database from {import_file}, continue"
        if not prompt.ask_yesno(_q, default_yes=False):
            prompt.ln(f"Seed aborted")

        # add backup dumps before importing (whenever importing, first create
        # a `last-backup-database-seed.sql`, that will be overridden every time
        # after 1st importing of the database
        self.cmd_seed_export(None, "config", "last-backup-database-seed.sql")

        # run mysql dump
        u, p, d = config['default_db_user'], config['default_db_pass'], config['default_db_name']
        command = f'exec mysql -u {u} -p"{p}" {d}'

        if self.project_conf["db_driver"] == "pgsql":
            command = f'exec psql --quiet -U {u} -d "{d}"'

        additional_options = "< %s" % import_file

        self.docker.exec(self.db_container, command, additional_options)
        prompt.ln(f"Seed import complete")

    def cmd_open_staging(self, args=None):
        host = self.project_conf['stage_url']

        # there is a local repository to look for when `composer install` stuff

        if args.all_pages:
            webbrowser.open_new_tab(f"https://{host}/db")
            webbrowser.open_new_tab(f"https://{host}/admin")
        webbrowser.open_new_tab(f"https://--no-dev{host}")

    def cmd_open_dev(self, args=None):
        self.require_configured(with_containers=True)
        host = self.project_conf['local_url']
        if not args.front_only:
            webbrowser.open_new_tab(f"http://{host}/db")
            webbrowser.open_new_tab(f"http://{host}/admin")
        webbrowser.open_new_tab(f"http://{host}")


config = {
    # configuration version
    'version': '0.3.0',
    # name of the project configuration file
    'project_conf_file': ".butler.json",
    'dockerhub_cms_image': "welance/craft",
    'dockerhub_mysql_image': "library/mysql",
    'dockerhub_pgsql_image': "library/posgtre",
    # name of the docker-compose dev file
    'docker_compose_local': "docker-compose.yml",
    # name of the docker-compose staging file
    'docker_compose_stage': "docker-compose.staging.yml",
    # name of the database seed file
    'database_seed': "database-seed.sql",
    # base domain to create the app staging url
    'staging_domain': "staging.welance.com",
    # default values for configuration
    'default_local_url': "localhost",
    'default_site_name': "Welance",
    'default_site_url': "localhost",
    'default_db_driver': "mysql",
    'default_db_server': "database",
    'default_db_user': "craft",
    'default_db_pass': "craft",
    'default_db_name': "craft",
    'default_db_schema': "public",
    'default_db_table_prefix': "craft_",
    # craft defaults
    'default_craft_username': "admin",
    'default_craft_email': "admin@welance.de",
    'default_craft_passord': "welance",
    'default_craft_allow_updates': "false",
    # version management (semver)
    'semver_major': 0,
    'semver_minor': 0,
    'semver_patch': 0,
    # required plugins
    'composer_require': [
        'craftcms/redactor:2.3.3.2',
        'craftcms/aws-s3:1.2.2'
    ]
}


def main():

    # CLI command arguments
    cmds = [

        {
            'name': 'setup',
            'help': 'set up the application',
            'args': [
                {
                    'names': ['--reset'],
                    'help': 'delete the butler configuraiton for the current project',
                    'action': 'store_true',
                    'default': False
                }
            ]
        },
        {
            'name': 'info',
            'help': 'print the current project info and version'
        },
        {
            'name': 'ports-info',
            'help': 'print the current ports utilized for the project'
        },
        {
            'name': 'start',
            'help': 'start the local docker environment',
            'args': [
                {
                    'names': ['--port'],
                    'help': 'provide the port for the current project',
                    'default': 80
                }
            ]
        },
        {
            'name': 'stop',
            'help': 'stop the local docker environment',
            'args': []
        },
        {
            'name': 'teardown',
            'help': 'destroy the local docker environment',
            'args': []
        },
        {
            'name': 'restore',
            'help': 'restore a project that has been teardown, recreating the configurations'
        },
        {
            'name': 'package-release',
            'help': 'create a gzip containg the project release'
        },
        {
            'name': 'plugin-install',
            'help': 'install a plugin into craft',
            'args': [
                {
                    'names': ['-n', '--name'],
                    'help': 'the name of the plugin to install, ex. craftcms/aws-s3',
                }
            ]

        },
        {
            'name': 'plugin-remove',
            'help': 'uninstall a plugin from craft',
            'args': [
                {
                    'names': ['-n', '--name'],
                    'help': 'the name of the plugin to remove, ex. craftcms/aws-s3',
                }
            ]
        },
        {
            'name': 'seed-export',
            'help': 'export the craft schema',
            'args': [
                {
                    'names': ['-f', '--file'],
                    'help': 'path of the schema where to export',
                    # 'default': '/data/craft/config/database-seed.sql'
                }
            ]
        },
        {
            'name': 'seed-import',
            'help': 'import the craft schema',
            'args': [
                {
                    'names': ['-f', '--file'],
                    'help': 'path of the schemat to import',
                    # 'default': '/data/craft/config/database-seed.sql'
                }
            ]
        },
        {
            'name': 'open-staging',
            'help': 'open a browser tabs to staging env (public)',
            'args': [
                {
                    'names': ['-a', '--all-pages'],
                    'help': 'also open admin and adminer',
                    'action': 'store_true'
                }
            ]
        },
        {
            'name': 'open-dev',
            'help': 'open a browser tabs to dev env (public,admin,adminer)',
            'args': [
                {
                    'names': ['-f', '--front-only'],
                    'help': 'open only the public page',
                    'action': 'store_true'
                }
            ]
        },
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='print verbose messages', action='store_true', default=False)
    subparsers = parser.add_subparsers(title="commands")
    subparsers.required = True
    subparsers.dest = 'command'

    # register all the commands
    for c in cmds:

        subp = subparsers.add_parser(c['name'], help=c['help'])
        # add the sub arguments
        for sa in c.get('args', []):
            subp.add_argument(*sa['names'],
                              help=sa['help'],
                              action=sa.get('action'),
                              default=sa.get('default'))

    args = parser.parse_args()

    c = Commander(args.verbose)
    # call the command with our args
    ret = getattr(c, 'cmd_{0}'.format(args.command.replace('-', '_')))(args)
    sys.exit(ret)


if __name__ == '__main__':
    main()
