import os
import asyncio
# import logging
import pydblite
# from singleton_decorator import singleton


class BaseNodeStore(object):

    def expand_group(self, group):
        if group is None:
            return [node['name'] for node in self.get_nodes()]
        elif not group.startswith('@'):
            return [group]
        return [node['node'] for node in self.groups(name=group)
                if node['node'] in self.get_nodes()]

    def select_node(self, node):
        nodes = self.expand_group(node)
        if len(nodes) == 1:
            try:
                node = self.nodes._name[nodes[0]][0]
            except IndexError:
                raise ValueError('node not active')
            if node['freeinits'] == 0:
                raise ValueError('no free inits')
            else:
                return node
        return max([node for node in self.nodes if self.nodes['name'] in nodes
                    and self.nodes['freeinits'] > 0],
                   key=lambda node: node['freeinits'])


class SimpleNodeStore(BaseNodeStore):
    modified = False

    def __init__(self, config):
        self.condition = asyncio.Condition()
        asyncio.get_event_loop().create_task(self.condition.acquire())
        dbgroups_path = os.path.join(config['minor']['data_dir'], 'gnodes.db')
        dbnodes_path = ':memory:'
        self.nodes = pydblite.Base(dbnodes_path)
        self.nodes.create('name', 'status', 'cpu',
                          'totalinits', 'freeinits', 'lastseen')
        self.nodes.create_index('name')
        self.groups = pydblite.Base(dbgroups_path)
        if self.groups.exists():
            self.groups.open()
        else:
            self.groups.create('name', 'node')
            self.groups.create_index('name')

        self.add_node(config['minor']['node_name'], config['minor']['inits'])
        if int(config['minor']['inits']) > 0:
            self.modify_node(config['minor']['node_name'], status='ACT')

    # async def create_lock(self):
    #    await self.condition.acquire()

    # async def send_update(self):
    #    print('SENCINDG NOTIFY ')
    #    self.modified = True
    #    self.condition.notify_all()
    #    await self.condition.acquire()

    def add_node(self, name, inits):
        if (name in self.nodes._name
           and self.nodes._name[name][0]['status'] != 'LST'):
            raise KeyError()
        # if value not in ('UNK', 'LST', 'CLS', 'FUL', 'ACT'):
        #   raise ValueError(f'status {value} not valid for node {self.name}')
        self.nodes.delete(self.nodes._name[name])
        status = 'ACT' if int(inits) > 0 else 'CLS'
        self.nodes.insert(name=name, status=status, cpu=100,
                          totalinits=int(inits), freeinits=int(inits))
        # asyncio.get_event_loop().create_task(self.send_update())

    def modify_node(self, name, **values):
        record = self.nodes._name[name]
        if not record:
            raise IndexError
        self.nodes.update(record, **values)
        # asyncio.get_event_loop().create_task(self.send_update())

    def delete_node(self, name):
        self.nodes.delete(self.nodes(name=name))
        self.modified = True

    def get_node(self, **conditions):
        return self.nodes(**conditions)

    def get_nodes(self):
        return self.nodes

    def get_group(self, group):
        return self.groups(name=group)

    def add_group(self, group):
        pass

    def delete_group(self, group):
        pass

    def delete_node2group(self, group, name):
        pass
        # record = self.groups(group=group, name=name)
        # del self.groups[record]
        # self.groups.commit()
        # self.modified = True

    def add_node2group(self, group, name):
        self.groups.insert(name=group, node=name)
        self.groups.commit()
        # asyncio.get_event_loop().run_until_complete(self.send_update())

    async def clear_nodes(self):
        pass


class RaftNodeStore(BaseNodeStore):

    def __init__(self, config):
        pass
