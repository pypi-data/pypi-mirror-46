"""paver config file"""

# from testing python book
from paver.easy import sh
from paver.tasks import task, needs


@task
def nosetests():
    """unit testing"""
    #sh('nosetests --cover-package=bd --cover-tests '
    #   ' --with-doctest --rednose  ./src/')
    pass

@task
def pylint():
    """pyltin"""
    #sh('pylint ./src/')
    pass 

@task
def pypi():
    """Instalation on PyPi"""
    sh('python setup.py sdist')
    sh('twine upload dist/*')

@task
def local():
    """local install"""
    sh("pip uninstall bdmagic")
    sh("python setup.py install")


@task
def sphinx():
    """Document creation using Shinx"""
    #sh('cd docs; make html; cd ..')
    pass

@needs('nosetests', 'pylint', 'sphinx')
@task
def default():
    """default"""
    pass

