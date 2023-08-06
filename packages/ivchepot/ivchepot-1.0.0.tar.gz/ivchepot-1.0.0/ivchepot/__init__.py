import logging
import socket
import threading


class HoneyPot(object):
	
	def __init__(self, bind_ip, ports, log_filepath):
		if len(ports) < 1:
			raise Exception("No ports provided.")

		self.bind_ip = bind_ip
		self.ports = ports
		self.log_filepath = log_filepath
		self.listener_threads = {}
		self.logger = self.prepare_logger()

		self.logger.info("Honeypot initializing...")
		self.logger.info("Ports %s:" % self.ports)
		self.logger.info("Log Filepath %s:" % self.log_filepath)


	def prepare_logger(self):
		logging.basicConfig(
				level=logging.DEBUG,
				format="%(asctime)s %(levelname)-8s %(message)s",
				datefmt="%Y-%m-%d %H:%M:%S",
				filename=self.log_filepath,
				filemode='w')
		logger = logging.getLogger(__name__)

		#Adding Console handler
		console_handler = logging.StreamHandler()
		console_handler.setLevel(logging.DEBUG)
		logger.addHandler(console_handler)
		return logger



	def handle_connection(self,  client_socket, port, ip, remote_port):
		self.logger.info("Connection recieved:%s: %s:%d " % (port, ip, remote_port))
		client_socket.settimeout(5)
		try:
			data = client_socket.recv(64)
			self.logger.info("Data recieved: %s: %s:%d: %s" % (port, ip, remote_port, data))
		except socket.timeout as e:
			pass
		client_socket.send("Access denied.\n".encode('utf-8'))
		client_socket.close()


	def start_new_listener_thread(self, port):
		listener = socket.socket() #By default (socket.AF_INET, socket.SOCK_STREAM)
		listener.bind((self.bind_ip, int(port)))
		listener.listen(5)
		while True:
			client, addr = listener.accept()
			client_handler = threading.Thread(target=self.handle_connection, args=(client, port, addr[0], addr[1]))
			client_handler.start()


	def start_listening(self):
		for port in self.ports:
			self.listener_threads[port] = threading.Thread(target=self.start_new_listener_thread, args=(port,))
			self.listener_threads[port].start()


	def run(self):
		self.start_listening()
			
			