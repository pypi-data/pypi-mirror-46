from walt.common.tcp import Requests
from walt.server.tools import DockerClient

def node_exists(db, mac):
    return db.select_unique("nodes", mac=mac) != None

def register_node(  images, topology, db, dhcpd, \
                    mac, ip, node_type, \
                    image_fullname, current_requests):
    # insert in table devices if missing
    if not db.select_unique("devices", mac=mac):
        topology.add_device(type=node_type, mac=mac, ip=ip)
    # insert in table nodes
    db.insert('nodes', mac=mac, image=image_fullname)
    # refresh local cache of node images, mount needed images
    # refresh the dhcpd conf
    db.commit()
    images.refresh()
    images.update_image_mounts()
    dhcpd.update()
    # we are all done
    current_requests.remove(mac)

class RegisterNodeTask(object):
    def __init__(self, image_fullname, **kwargs):
        self.image_fullname = image_fullname
        self.kwargs = kwargs
    def perform(self):
        # this is a lengthy operation
        DockerClient().pull(self.image_fullname)
        return
    def handle_result(self, res):
        register_node(  image_fullname = self.image_fullname,
                        **self.kwargs)

def handle_registration_request( \
                    blocking, images, db, mac, node_type, \
                    current_requests, **kwargs):
    if mac in current_requests or node_exists(db, mac):
        # this is a duplicate request, we already have registered
        # this node or it is being registered
        return
    current_requests.add(mac)
    image_fullname = images.get_default_image(node_type)
    full_kwargs = dict(
        images = images,
        db = db,
        image_fullname = image_fullname,
        mac = mac,
        node_type = node_type,
        current_requests = current_requests,
        **kwargs
    )
    if image_fullname in images:
        # it will not be long, we can do it synchronously
        register_node(**full_kwargs)
    else:
        # we will have to pull an image, that will be long,
        # let's do it asynchronously
        blocking.do(RegisterNodeTask(**full_kwargs))

class NodeRegistrationHandler(object):
    def __init__(self, blocking, sock, sock_file, **kwargs):
        self.sock_file = sock_file
        self.blocking = blocking
        self.mac = None
        self.ip = None
        self.node_type = None
        self.kwargs = kwargs

    # let the event loop know what we are reading on
    def fileno(self):
        return self.sock_file.fileno()
    # the node register itself in its early bootup phase,
    # thus the protocol is simple: based on text lines
    def readline(self):
        return self.sock_file.readline().strip()
    # when the event loop detects an event for us, we
    # know a log line should be read. 
    def handle_event(self, ts):
        if self.mac == None:
            self.mac = self.readline()
        elif self.ip == None:
            self.ip = self.readline()
        elif self.node_type == None:
            self.node_type = self.readline()
            handle_registration_request(
                blocking = self.blocking,
                mac = self.mac,
                ip = self.ip,
                node_type = self.node_type,
                **self.kwargs
            )
            # tell the event_loop that we can be removed
            return False
    def close(self):
        self.sock_file.close()

class NodesManager(object):
    def __init__(self, tcp_server, **kwargs):
        self.kwargs = kwargs
        self.current_requests = set()
        tcp_server.register_listener_class(
                    req_id = Requests.REQ_REGISTER_NODE,
                    cls = NodeRegistrationHandler,
                    current_requests = self.current_requests,
                    **self.kwargs)

