

class User(object):
    SCHEMA = {'name': str,
              }

    def test_plugin():
        return User(None)

    def __init__(self, config):
        pass

    def resolve_dependency(self, jobid, dep):
        if dep == 'dep1':
            return True
        else:
            return ('NDF', 'yellow')
