
class NodeCollection(object):

    def __init__(self):
        self._nodes = []

    def append(self, node):
        self._nodes.append(node)

    def __iter__(self):
        for node in self._nodes:
            yield node

    def refresh_all(self):
        for node in self:
            node.refresh()

    def print_all(self):
        for node in self:
            node.print_info()

    def get_all(self):
        lst = []
        for node in self:
            data = {'Node': node.node,
                    'Status': node.status,
                    'Version': node.version,
                    'Git build': node.git_build,
                    'Sync': node.sync_status,
                    'My height': node.my_height,
                    'Leader height': node.leader_height,
                    'Complete height': node.complete_height,
                    'Type': node.node_type,
                    'Chainid': node.chainID
                    }
            lst.append(data)
        return lst





