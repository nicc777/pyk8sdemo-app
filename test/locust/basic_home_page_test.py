from locust import HttpUser, task, between
import os

HOST1 = os.getenv('HOST1', '127.0.0.1')
HOST2 = os.getenv('HOST2', '127.0.0.1')
HOST3 = os.getenv('HOST3', '127.0.0.1')


class node1(HttpUser):

    host = 'http://{}:8880'.format(HOST1)
    wait_time = between(2, 4)

    @task()
    def node_t1(self):
        self.client.get('/')


class node2(HttpUser):

    host = 'http://{}:8880'.format(HOST2)
    wait_time = between(2, 4)

    @task()
    def node_t1(self):
        self.client.get('/')


class node3(HttpUser):

    host = 'http://{}:8880'.format(HOST3)
    wait_time = between(2, 4)

    @task()
    def node_t1(self):
        self.client.get('/')
        
        
