# Welance Starter (ATM: CraftCMS 3.x + Docker)

The project is the base to fork to create new projects using craft cms.
The repository contains:

- docker configuration for craft container
- docker-compose configuration to run the craft+mysql enviroment
- base schema customization of the craft installation
- apache configuration
- base template for craft frontend
- utility scripts to start/stop the enviroment
- utility scripts to import/export craft schema changes

More info about this project: **[here](build/README.md)**.

# Installation 

To install waldcli run `pip install waldcli`

For preview releases run `pip install --extra-index-url https://test.pypi.org/simple/ waldcli`

## Workflow

The following is the standard workflow to use with the projects using craft/docker for development.

### 0. Setup

⚠️ **note:** Execute point nr. 4, only if the setup has not yet been done
1. Fork the starter project
create a fork of the latest release of the base repo : [https://github.com/welance/welance-craft-starter](https://github.com/welance/welance-craft-starter)
2. Install python/libs and bash completion (make sure to have python3 installed, use [virtualenv](https://virtualenv.pypa.io/en/stable/) if necessary).
3. run:
   - `pip install -r bin/requirements.txt` to install the required libraries and
   - `source bin/butler.bash-completion` to enable commands autocompletion
4. Run `bin/butler.py setup` script. (required: [docker](https://www.docker.com/community-edition)). The script will ask for:

> **!!! ATTENTION !!!**
> customer and project number are used to setup the containers environment,
> they cannot be easily changed once the project is on-going.

5. Commit
commit the chagnes to the repository, in particular the changes reated to:

```
./bin/.butler.json
./docker/docker-compose.yml
./docker/docker-compose-staging.yml
```

### 1. Development

During the development here are the most used commands:

1. **Start!** Start The docker dev environment
`bin/butler.py start --port [PORT_NUMBER]` script starts the docker containers

2. **Work!** The development phase of the project will involve 3 main resources:
- the `templates`folder
- the `config/project.yaml`
- the `plugins` folder

3. **Stop!** Stop the docker dev environment
`bin/butler.py stop` stops the docker conatiners. It doesn't delete the database or cms data.

#### **Import/Export (Project/DB) Schema**
The schema is imported/exported automatically by Craft v3+ into `config/project.yml`, so just make sure tommit it


#### Local **Plugin Development**:
If you would like to develop a local plugin, we need to put it inside the plugins folder such as `/plugins/VENDOR_NAME/PLUGIN_NAME`


##### Import/Export database seed
To import/export the dump of the database that it is used to setup/seed the database

- `bin/butler.py seed-import -f=path/to/file`
- `bin/butler.py seed-export -f=path/to/file`

the seed sql file is imported/exported from `build/dump/base.sql`

**TODO: change this!**

### Accessing the database
Since the database use in the containers is not accessible from outside docker a database web interface is provided to dump/load/edit the database directly. The interface of the database is [Adminer](https://www.adminer.org/) and
is available via http or https.

The urls are:
- [http://HOST/db](http://localhost/db)
- [https://HOST/db](https://localhost/db).

The parameters to log in are:
- System: MySQL or PostgreSQL depending on the driver selected
- Server: database
- Username: craft
- Password: craft
- Database: craft

### Apache configuration and .htaccess
The website apache configuration is stored in `./docker/craft/conf/apache2/conf.d/welance.conf`.
The welance.conf contains all the settings for the installation to work and should be taken as a reference
for production installation. By default .htaccess is _DISABLED_, [because](https://nystudio107.com/blog/stop-using-htaccess-files-no-really).
Changes to the apache configuration require to restart the environment (`bin/butler.py local-stop`, `bin/butler.py local-start`) to be enabled.


### Applying Craftcms updates
_TODO_


### Troubleshooting

**Docker**: the project folder must be located in one of the **Docker File Sharing** paths.
You can add a folder (for example the mamp one) by edit the prefernces of your docker installation

**CraftCMS**: if you log in using HTTPS login with HTTP fails. This has someting to do with sessions
and CSRF protection. To solve the issue clear the browser application data and retry.

**Adminer**: if you log in using HTTPS login with HTTP fails. This has someting to do with sessions
and CSRF protection. To solve the issue clear the browser application data and retry.

### SSL

the certificate shipped with the project has been created using:

```
localhost:/# openssl req -x509 -nodes -days 1825 -newkey rsa:2048 -keyout welance.ssl.key -out welance.ssl.crt
Generating a 2048 bit RSA private key
....................+++
....................................................................+++
writing new private key to 'welance.ssl.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:DE
State or Province Name (full name) []:Berlin
Locality Name (eg, city) []:Berlin
Organization Name (eg, company) []:Welance
Organizational Unit Name (eg, section) []:
Common Name (eg, fully qualified host name) []:
Email Address []:info@welance.de
```


### 2. Deploy on Staging

For staging environment are available the commands:
- `bin/butler.py open-staging`

they are used by the [welance clerk](https://github.com/welance/docker-staging) system


### 3. Create a Release Package
To create an tar.gz archive of the craft installation use the command

- `bin/butler.py release-package`

it will create a file `release.tar.gz` file in the root of the project containing
the craft installation with a **fresh database dump** in the `build/dump/base.sql` location

### Project removal
Once the project is finished to remove the resources associated with the project (containers and data)
the `bin/butler.py teardown`script is provided.

## License

https://commonsclause.com/