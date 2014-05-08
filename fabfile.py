from fabric.operations import local


def rst_generate():
    local('pandoc --from=markdown --to=rst README.md -o README.rst')


def publish():
    # local('rm -f README.rst')
    # rst_generate()
    local('python setup.py sdist upload')
