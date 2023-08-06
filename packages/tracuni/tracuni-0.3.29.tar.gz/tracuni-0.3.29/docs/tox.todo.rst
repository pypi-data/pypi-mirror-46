====================
How to setup project
====================

 * setup virtual environment tools
   * install pipsi from "https://github.com/mitsuhiko/pipsi"
   * install pyenv from "https://github.com/pyenv/pyenv-installer"
   * put pyenv initialization in .(ba|z)shrc and add it to system path
   * add user python packages executables to system path (~/.local/bin)
   * tell virtualenv to use project directory to create virtual environment files
   * install via pyenv all python versions designated for tesing purposes
   * installing python 3.4 in some distributions requires some hacking with openssl lib path
   * set them as global versions
   * remove python version requirement from Pipfile

   $> curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python
   $> curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
   $> echo 'export PATH="/home/tova/.local/bin:$PATH"\nexport PATH="/home/tova/.pyenv/bin:$PATH"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)"\n\nexport PIPENV_VENV_IN_PROJECT=true' >> ~/.bashrc
   $> echo 'export PATH="/home/tova/.local/bin:$PATH"\nexport PATH="/home/tova/.pyenv/bin:$PATH"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)"\n\nexport PIPENV_VENV_IN_PROJECT=true' >> ~/.zshrc
   $> pyenv install x.x.x
   # ex. python versions (3.7.1 3.6.7 3.5.6 3.4.9)
   $> LDFLAGS="-L/usr/lib/openssl-1.0" \
   CFLAGS="-I/usr/include/openssl-1.0" \
   pyenv install 3.4.9
   $> pyenv global x.x.x y.y.y
   $> pipsi install pipenv

 * prepare template project
   * install cookiecutter (scaffolding package)
   * use "https://github.com/audreyr/cookiecutter-pypackage" template
   * tox.ini - remove unsuitable settings: travis etc.
   * tox.ini - add exact interpretator location for each used versions to make PyCharm find them
   * tox.ini - add settings to main enviroment passenv & whitelist to avoid warnings
   * add .idea & Pipfile.lock to git ignore
   * remove excecive files
   * > make incipient commit and configure origin

   $> pipsi install cookiecutter
   $> cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git
   answer simple questions and cd to project directory
   $> vim tox.ini
   .. code::

     [testenv:py34]
     basepython = /home/tova/.pyenv/versions/3.4.9/bin/python

     [testenv:py35]
     basepython = /home/tova/.pyenv/versions/3.5.6/bin/python

     [testenv:py36]
     basepython = /home/tova/.pyenv/versions/3.6.7/bin/python

     [testenv:py37]
     basepython = /home/tova/.pyenv/versions/3.7.1/bin/python

     [testenv]
     passenv =
       LANG
       PYTHONPATH

     whitelist_externals =
       python

   $> echo '\n# pipenv lock\nPipfile.lock\n\n# idea project settings\n.idea/\n' >> .gitignore
   $> rm -rf ./{.github/,CONTRIBUTING.rst,travis.yaml}
   $> git init && git add . && git commit -m 'chore:\n  - start from template'
 
 * create python virtual environment with pipenv
   * create environment
   * install development dependencies and generate requirements
   * install package dependencies and generate requirements
   * > push dependencies changes
   * make install before run py.test (to install project into itself)
   * tox-pipenv <=1.8.0 plugin is not compatible with tox >=3.7.0, update
   plugin or patch: /_getresolvedeps/get_resolved_dependencies/
    pip install -e .
   $> pipenv install
   $> pipenv shell
   $> pipenv install --dev tox tox-pipenv pytest pytest-mock flake8 twine
   $> pipenv install Click
   $> pipenv lock -r --dev > requirements_dev.txt
   $> pipenv lock -r > requirements.txt

 * check if works in CLI and pycharm
   * run "tox" command inside project directory - it should pass all tests in all versions
   * open project in pycharm - it should have environment set (Settings > Project > Project Interpreter) that we create before
   * run tox via pycharm tooling: run from tox.ini file - tox run configuration should be created and run output should be the same as from CLI
   * make command is used to manage builds, see make help for command list

 * test local pipy deployment
   * add ./.devpi (directory to store local pypi repo) to git ignore
   * add requirements and tox settings file to manifest
   * install local pipy substitute "devpi"
   * configure devpi repositories as described here: "https://stefan.sofa-rockers.org/2017/11/09/getting-started-with-devpi/"

   $> echo '\ninclude requirements_dev.txt\ninclude requirements.txt\ntox.ini\n' >> MANIFEST.in
   $> pipenv install --dev devpi-server devpi-client
   $> devpi-server --serverdir=<absolute path to project dir>/.devpi --init --start
   $> devpi-server --serverdir=<absolute path to project dir>/.devpi --passwd root
   enter password
   $> devpi use http://localhost:3141
   $> devpi login root --password=xx
   $> devpi index -c dev bases=root/pypi
   $> devpi use dev
   $> devpi upload
   package is now in repository
   $> devpi test
   you can run test inside devpi the same way as localy

 * have fun & póg mo thóin

Библиотека предназначена для сохранения информации о вызовах выбранных точек: функций и методов. Выбранная точка оборачивается декоратором, который и запускает процесс извлечения данных и отправку их на запись сервису трассировки. В информацию входит когда, в каком порядке и в каком контексте данных происходил вызов. Для данной цели точки рассматриваются как относящиеся к двум видам-направлениям: входящие и исходящие. Входящие - когда сторонний модуль обращается к текущему и наоборот. Помимо направления каждая точка относится к одному из заранее определенных типов по программному интерфейсу. Вместе с направлением тип интерфейса задаёт вариант точки. Это сделано потому, что разные направления и интерфейсы требуют разной обработки. Вариант точки задается параметрами декоратора.
К каждому варианту прилагается стандартная схема извлечения данных: набор однородных правил откуда брать данные в контексте точки и каким образом их обрабатывать. Таким образом, схема это список правил настроек произвольной длины, каждое из которых состоит из описания источника, описания назначения, списка функций-обработчиков - конвеера, через который последовательно проходят данные до отправки на трассер. Помимо стандартных для любой из точек можно задать пользовательскую схему, которая будет работать вместе со стандартной или вместо её.
Каждое из правил схем работает на определенной стадии прохождения точки. Всего их три: инициализация контекста точки, до вызова точки, после вызова точки.
Для работы по схемам создан процессор схем. Он инцилизируется вместе с декоратором. Для каждого используемого варианта создаётся один экземпляр процессора не зависим от того, сколько точек использует этот вариант. Если ни одна из точек этот вариант не использует, то процессор не создаётся. Если точка использует пользовательскую схему, то всегда создаётся отдельный экземпляр процессора. Поскольку схема может быть привязана не только к конкретному варианту, но и к множеству вариантов (например, все входящие), а также разные правила схем работают на разных стадиях вызова точки, то процессор предварительно разбирает схем по этапам и вариантам при своей инициализации, чтобы не делать это при каждом вызове.

Для сборки библиотеки необходимо создать среду исполнения. Как вариант для этого можно использовать pipenv:
1. установить под пользователем, под которым происходит сборка pyenv: "https://github.com/pyenv/pyenv-installer"
2. установить требуемые для тестирвания версии python, например: "pyenv install 3.6.8 && pyenv install 3.7.2 && pyenv global system 3.6.8 3.7.2"
3. установить под пользователем, под которым происходит сборка pipenv: "pip install --user pipenv"
4. сделать так, чтобы pyenv и pipenv находились по системным путям
5. создать виртуальную среду: "pipenv --python 3.6 && pipenv shell && pipenv install --dev && pipenv install"
6. запустить сборку "make build"
7. или использовать другие команды включенного в проект make файла, в них влючено: создание пакета для локального (devpi) или удаленного репозитория, тестирование, в том числе под разными версиями интерпретатора, линтинг, проверка типов, генерация документации, обновлении версии
