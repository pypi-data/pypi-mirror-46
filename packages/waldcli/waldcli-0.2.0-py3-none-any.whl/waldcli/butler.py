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
from pathlib import Path
import datetime
import requests
from termcolor import colored, cprint
# TODO: do not use 2 different yaml parser in the same project
import yaml
import ruamel.yaml

""" name of the out configuration file """


#   _______  _______      ___   _______  ____    ____  _______   _________
#  |_   __ \|_   __ \   .'   `.|_   __ \|_   \  /   _||_   __ \ |  _   _  |
#    | |__) | | |__) | /  .-.  \ | |__) | |   \/   |    | |__) ||_/ | | \_|
#    |  ___/  |  __ /  | |   | | |  ___/  | |\  /| |    |  ___/     | |
#   _| |_    _| |  \ \_\  `-'  /_| |_    _| |_\/_| |_  _| |_       _| |_
#  |_____|  |____| |___|`.___.'|_____|  |_____||_____||_____|     |_____|
#

class Prompter(object):

    def __init__(self):
        self.print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')

    def p(self, prompt_key):
        """ retrieve the message of a prompt  """
        # dictionary with the messages to print in th prompt
        prompts = {
            "project_ovverride": colored(
                "The project is already configured, do you want to overwrite "
                "the configuration? (yes/no)? [no]: ", 'red', attrs=['reverse']),
            "setup_abort": colored("alright, aborted, bye!", 'red', attrs=['reverse']),
            "export_abort": colored("alright, aborted the export, bye!", 'red', attrs=['reverse']),
            "import_abort": colored("alright, aborted the import, bye!", 'red', attrs=['reverse']),
            "customer_number": colored("Please enter the customer number: ", 'green', attrs=['reverse']),
            "project_number": colored("Now enter the project number: ", 'green', attrs=['reverse']),
            "site_name": colored("And the site name? [%s]: " % config['default_site_name'], 'green', attrs=['reverse']),
            "local_url": colored("Url for development [%s]: " % config['default_local_url'], 'green', attrs=['reverse']),
            "db_driver": colored("Which database will you use pgsql/mysql? [%s]: " % config['default_db_driver'], 'green', attrs=['reverse']),
            "setup_confirm": colored("are this info correct? (yes/no)? [no]: ", 'red', attrs=['reverse']),
            "export_confirm": colored(
                "Are you sure you want to export? This will override your "
                "database-seed.sql if no other name is gonna be given? (yes/no)? [no]: ",
                'red', attrs=['reverse']),
            "import_confirm": colored(
                "are you sure you want to IMPORT? This will override your import "
                "database-seed.sql into your APPLICATION_NAME Application. Tip: You "
                "can use import -f to import a file different from database-seed.sql. "
                "(yes/no)? [no]: ", 'red', attrs=['reverse']),
            "setup_reset_confirm": colored(
                "This will remove all the devops related configurations, there is no "
                "coming back. Proceed? (yes/no)? [no]: ", 'red', attrs=['reverse',
                                                                        ]),
            "setup_reset_done": colored("Reset completed", 'green', attrs=['reverse',
                                                                           ]),
            "project_teardown": colored(
                "This action will remove all containers including data, do you want "
                "to continue (yes/no)? [no]: ", 'red', attrs=['reverse']),
            "image_version": colored("Which version do you want to use? "
                                     "[default with *]: ", 'green', attrs=['reverse',
                                                                           ]),
            "semver": colored("options are\n  [0] major\n  [1] minor\n* [2] patch"
                              "\nwhich one do you want? [patch]: ",
                              'green', attrs=['reverse'])
        }

        return prompts.get(prompt_key)

    def say(self, prompt_key):
        """say something"""
        print(self.p(prompt_key))

    def ask_yesno(self, prompt_key):
        """ prompt the user for a yes/no question, when yes return true, false otherwise"""
        val = input(self.p(prompt_key))
        if val.strip().lower() == 'yes':
            return True
        return False

    def ask_int(self, prompt_key, min_val=0, max_val=None, def_val=None):
        """ prompt user for a int value, keep asking until a correct value is entered"""
        val = ""
        while True:
            try:
                val = input(self.p(prompt_key))
                # if there is a default value use it
                if not val and def_val is not None:
                    val = def_val
                    break
                # else check the boundaries
                if int(val) < min_val or (max_val is not None and int(val) > max_val):
                    raise ValueError("")
                break
            except ValueError:
                if max_val is not None:
                    print("sorry boss, choose something between %d and %d" %
                          (min_val, max_val))
                else:
                    print("sorry boss, chose a number greater than %d" %
                          (min_val))
        return val

    def ask_str(self, prompt_key, default_val=""):
        """ read a string from a command line, apply default_val if the input is empty"""
        val = input(self.p(prompt_key)).strip()
        if not val:
            val = default_val
        return val


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
        print(cmd)
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception:
            pass

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
            print(f"Docker exec failed command {e}")
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
        # init command line cli
        self.prompt = Prompter()

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
            print(colored("the project is not yet configured, run the setup command first",
                          'red', attrs=['reverse']))
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
            print(colored("The file to delete the last line is not found",
                          'yellow', attrs=['reverse']))
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

        # port = args.port

        if args.reset:
            if (not self.prompt.ask_yesno('setup_reset_confirm')):
                self.prompt.say('setup_abort')
                return
            self.delete_file(os.path.join(self.project_path, "build", "ci", "Dockerfile"))
            self.delete_file(os.path.join(self.project_path, "build", "docker-compose.yml"))
            self.delete_file(os.path.join(self.project_path, "build", "docker-compose.staging.yml"))
            self.delete_file(self.config_path)
            self.prompt.say('setup_reset_done')
            sys.exit(0)

        """set up the application """
        # shorcut since "self.project_conf" is too long to write
        pc = self.project_conf
        # if the config  already exists prompt what to do
        if pc and not self.prompt.ask_yesno('project_ovverride'):
            self.prompt.say('setup_abort')
            return
        # ask for customer number
        pc['customer_number'] = self.prompt.ask_int('customer_number')
        pc['project_number'] = self.prompt.ask_int('project_number')
        pc['site_name'] = self.prompt.ask_str('site_name', config['default_site_name'])
        pc['local_url'] = self.prompt.ask_str('local_url', config['default_local_url'])
        pc['db_driver'] = self.prompt.ask_str('db_driver', config['default_db_driver'])

        # retriewve image versions
        dv, vers = DockerCli.list_image_versions(config['dockerhub_cms_image'], 4)
        print(colored("Here there are the available craft versions:", 'yellow', attrs=['reverse']))
        for i in range(len(vers)):
            num = "* [%2d]" % i if i == dv else "  [%2d]" % i
            print("%s %10s %dMb" % (num, vers[i][0], vers[i][1]))
        iv = int(self.prompt.ask_int('image_version', 0, len(vers) - 1, def_val=dv))
        # select the version name from the version chosen by the user
        pc["craft_image"] = f"{config['dockerhub_cms_image']}:{vers[iv][0]}"
        # build stage domain
        c, p = pc['customer_number'], pc['project_number']
        pc['stage_url'] = f"p{c}-{p}.{config['staging_domain']}"

        #  print summary for the project creation
        print("")

        colored(f"Customer Number: {pc['customer_number']}", 'blue', attrs=['reverse'])
        colored(f"Project  Number: {pc['project_number']}", 'blue', attrs=['reverse'])
        colored(f"Site Name      : {pc['site_name']}", 'blue', attrs=['reverse'])
        colored(f"Local Url      : {pc['local_url']}", 'blue', attrs=['reverse'])
        colored(f"Staging Host   : {pc['stage_url']}", 'blue', attrs=['reverse'])
        colored(f"Db Driver      : {pc['db_driver']}", 'blue', attrs=['reverse'])
        colored(f"Craft version  : {pc['craft_image']}", 'blue', attrs=['reverse'])

        print("")

        print(colored("Please, check if these informations below are correct", 'yellow', attrs=['reverse']))

        cmd = "bin/butler.py info"
        os.system(cmd)

        # ask for confirmation
        if (not self.prompt.ask_yesno('setup_confirm')):
            self.prompt.say('setup_abort')
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
            print("the value for Db Driver must be mysql or pgsql")
            self.prompt.say('setup_abort')
            return

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

        print(colored("pull doker images images", 'yellow', attrs=['reverse']))
        self.docker.compose_pull(self.local_yml)
        print(colored("create containers", 'yellow', attrs=['reverse']))
        self.docker.compose_setup(self.local_yml)

        print(colored("setup completed", 'green', attrs=['reverse']))

    def cmd_restore(self, ns=None):
        """restore a project that has been teardown, recreating the configurations """
        self.require_configured()
        # if the config  already exists prompt what to do
        if self.project_conf:
            print(colored("pull doker images images", 'yellow', attrs=['reverse']))
            self.docker.compose_pull(self.local_yml)
            print(colored("create containers", 'yellow', attrs=['reverse']))
            self.docker.compose_setup(self.local_yml)
            print(colored("setup completed", 'green', attrs=['reverse']))
            return
        print(colored("there is nothing to restore, perhaps you want to setup?", 'red', attrs=['reverse']))

    def cmd_start(self, args=None):
        """start the docker environment"""

        local_start_port = str(args.port)

        self.require_configured()

        docker_compose = {}

        # read the "docker-compose.yml" file
        with open(self.local_yml, 'r') as s:

            try:
                docker_compose = yaml.safe_load(s)

            # we are not able to read the docker-compose.yml file
            except yaml.YAMLError as e:
                print(colored("The 'docker-compose.yml' can't be "
                              "read. Do you setup the project correctly?",
                              'red', attrs=['reverse']))

                return

        docker_compose["services"]["craft"]["ports"] = [local_start_port + ":" + "80"]

        # dump the info to the "docker-compose.yml" file
        self.write_file(self.local_yml, yaml.dump(docker_compose, default_flow_style=False))

        docker_compose_staging = {}

        # open the docmer-compose.staging.yml file
        with open(self.stage_yml, 'r') as s:
            try:
                docker_compose_staging = yaml.safe_load(s)

            # we are not able to read the docker-compose.staging.yml file
            except yaml.YAMLError as e:
                print(colored("The 'docker-compose.staging.yml' can't be "
                              "read. Do you setup the project correctly?",
                              'red', attrs=['reverse']))
                return

        # expose the port
        docker_compose_staging["services"]["craft"]["expose"] = "80"

        docker_compose_staging["services"]["craft"]["labels"] = [
            "traefik.enable=true",
            "traefik.docker.network=web",
            "traefik.port=80",
            f"traefik.frontend.rule=Host:{self.p_code}.staging.welance.com",
            "traefik.frontend.auth.basic=staging:$$apr1$$2jJI/GYz$$1hZdD66lDNKCq7lmAkb1T1",
        ]

        # dump the info to the "docker-compose.staging.yml" file
        self.write_file(self.stage_yml, yaml.dump(docker_compose_staging, default_flow_style=False))

        # provide the port info to the Dockerfile
        read_docker_file = []

        dockerfile_path = os.path.join(self.project_path, "build", "ci", "Dockerfile")

        try:
            with open(dockerfile_path, 'r') as f:
                read_docker_file = f.readlines()

        except FileNotFoundError as e:
            print(colored("The Dockerfile is not found in the path. Do you setup "
                          "the project properly?", 'red', attrs=['reverse']))
            return

        n = len(read_docker_file)

        # the Dockerfile is empty
        if (n == 0):
            print(colored("The Dockerfile is empty. Do you setup "
                          "the project properly?", 'red', attrs=['reverse']))
            return

        # we had a project started previously and had a PORT exposed. We need
        # to delete the info and provide a new PORT for the current project
        if ("EXPOSE" in read_docker_file[n - 1]):
            self.delete_last_line(dockerfile_path)

        # append the new PORT info at the end of the file
        try:
            with open(dockerfile_path, 'a') as f:
                f.writelines("\nEXPOSE " + "80")
            f.close()

        except FileNotFoundError as e:
            print(colored("The Dockerfile is not found. Do you setup "
                          "the project properly?", 'red', attrs=['reverse']))
            return

        self.docker.compose_start(self.local_yml)

        if (not self.project_conf['local_plugins']):
            print("We don't have any local plugins to install")

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
        print(colored("The initial database dump is provided in the config directory", 'green',
                      attrs=['reverse']))

        # configure the CI/ CD files
        jinja_template = "build/ci/gitlab-ci.yml.j2"
        butlet_json = "bin/.butler.json"
        ci_file = "build/ci/.gitlab-ci.yml"

        if(not os.path.exists(jinja_template) or not os.path.exists(butlet_json) or not os.path.exists(ci_file)):
            # we need to aboart the system
            pass

        # we have tackled inside the jinja2 template if
        # the plugins are specified in the ".butler.json"
        cmd = f"jinja2 {jinja_template} {butlet_json} > {ci_file}"

        # generate a ".gitlab-ci.yml" file with the
        # plugins information in the `build/ci/.gitlab-ci.yml` location
        # the gitlab find a file with the same name `.gitlab-ci.yml` in
        # the root of the project and this file maps to the main CI/CD
        # file located in the `build/ci/.gitlab-ci.yml` location
        os.system(cmd)

        project_id = f"p{self.project_conf['customer_number']}-{self.project_conf['project_number']}"

        file_name = Path(ci_file)

        # update the project ID in the "build/ci/.gitlab-ci.yml" file
        update_project_id(file_name, project_id)

    def cmd_stop(self, args=None):
        """stop the docker environment"""
        self.require_configured()
        target_yaml = self.local_yml
        self.docker.compose_stop(target_yaml)

    def cmd_teardown(self, args=None):
        """destroy the docker environment"""
        self.require_configured()
        target_yaml = self.local_yml
        if self.prompt.ask_yesno('project_teardown'):
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
                print(colored("No port is currently being used", 'green', attrs=['reverse']))

            # project uses some network ports
            else:
                print(
                    colored(
                        f"List of ports utilized till now {ports}\n" + "Please, use another port to start the project",
                        'green',
                        attrs=['reverse']))

        except Exception as e:
            print(f"Docker exec failed command {e}")
            return None

    def cmd_info(self, ns=None):
        """print the current project info and version"""
        self.require_configured()
        pc = self.project_conf

        # provide all the associated info for the respective project
        print("")
        print(colored(f"Customer Number : {pc['customer_number']}", 'green', attrs=['reverse']))
        print(colored(f"Project  Number : {pc['project_number']}", 'green', attrs=['reverse']))
        print(colored(f"Site Name       : {pc['site_name']}", 'green', attrs=['reverse']))
        print(colored(f"Staging Url     : https://{pc['stage_url']}", 'green', attrs=['reverse']))
        print(colored(f"Db Driver       : {pc['db_driver']}", 'green', attrs=['reverse']))
        print(colored(f"Project Version : {self.semver()}", 'green', attrs=['reverse']))
        print("")

    def cmd_package_release(self, ns=None):
        """create a gzip containg the project release"""
        self.require_configured(with_containers=True)
        pc = self.project_conf

        print("Current version is %s" % self.semver())
        val = self.prompt.ask_int("semver", 0, 2, 0)
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

        # check if the docker deamon is running and if not run it
        if (os.path.exists("bin/docker.sh") and os.name == "posix"):
            subprocess.call("bin/docker.sh", shell=True)

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
                print(colored("we already have the plugin with same version installed.", 'green',
                              attrs=['reverse']))
                return

        # either we don't have the plugin installed or have a different version
        cmd = f"cd craft && composer require {plugin_name} --no-interaction"
        self.docker.exec(self.cms_container, cmd)

        # run craft install
        if (p == "craft-typogrify"):
            p = "typogrify"

        cmd = f"craft/craft install/plugin {p}"
        self.docker.exec(self.cms_container, cmd)

        print(colored(f"we have just installed the plugin {plugin_name} for the Craft", 'green',
                      attrs=['reverse']))

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

        print(colored(f'The plugin name {plugin_name}  is listed in the project config file ".butler.json"', 'green',
                      attrs=['reverse']))

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
            print("plugin %s is not installed" % plugin_name)

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

        print(colored(f"we have just removed the plugin {plugin_name} for the Craft", 'green',
                      attrs=['reverse']))

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

            if (not self.prompt.ask_yesno('export_confirm')):
                self.prompt.say('export_abort')
                return

        self.docker.exec(self.db_container, command, additional_options)

        # if we would like to import a database, we will first create a dump
        # of the current database in a file named "last-backup-database-seed.sql"
        # in the "config" directory
        if (file_name == "last-backup-database-seed.sql"):
            print(colored(
                "a backup dump named last-backup-database-seed.sql exported "
                "in the config directory before we imported the database",
                'green', attrs=['reverse']))
            return

        print(colored(f"schema export complete", 'green',
                      attrs=['reverse']))

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

        file = None

        # we provided a file name from the CLI
        if (args is not None and args.file is not None):
            file = args.file

        else:
            file = config['database_seed']

        import_file = os.path.join(self.project_path, "config", file)

        if (not os.path.isfile(import_file)):
            print(colored(f'We are not able to import the database from the provided. '
                          f'No file with name {file} exist in the config directory', 'red', attrs=['reverse']))
            return

        # we get the request from the CLI with no alternate file name
        if (args is not None and args.file is None):

            if (not self.prompt.ask_yesno('import_confirm')):
                self.prompt.say('import_abort')
                return

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
        print(colored(f"schema import complete", 'green', attrs=['reverse']))

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


# provide the project ID is the CI/CD
# file at the end of the setup process
def update_project_id(path, pid):
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)  # non-standard indent of 4 for sequences
    yaml.preserve_quotes = True
    data = yaml.load(path)

    data['before_script'][0] = 'export WE_PROJECT_ID="' + pid + '"'
    yaml.dump(data, path)


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
