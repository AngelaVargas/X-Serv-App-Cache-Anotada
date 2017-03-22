
import socket
import urllib.request

class webApp:

	def Analiza(self,Pet):

		lista_datos = Pet.split(' ', 2)

		return (lista_datos)


	def Process(self,cache,metodo,recurso):

		if (metodo == "GET"):
			if (recurso in cache):
				body = cache[recurso]	
			else:
				url = "http:/" + recurso
				print(url)
				f = urllib.request.urlopen(url)
				content = f.read()
				content = content.decode('utf-8')
				content = str(content)
				n = content.find("<body")
				head = content[0:n]
				m = content.find(">", n)
				body = content[n:m+1]
				rest = content[m+1:]
				body = head + body + "<a href=" + url + ">Página original\n</a>" +\
						"<a href=http://localhost:1234/reload" + recurso + ">Reload</a>" + rest
				cache[recurso] = body
	
			return("200 OK", body)


		else:
			return("404 Not Found" , "<html><body><h1>Método no encontrado</h1></body></html>")

	def __init__(self, hostname, port):
		"""Initialize the web application."""

		# Create a TCP objet socket and bind it to a port
		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		mySocket.bind((hostname, port))

		cache = {}

		# Queue a maximum of 5 TCP connection requests
		mySocket.listen(5)

		# Accept connections, read incoming data, and call
		# parse and process methods (in a loop)

		while True:
			print('Waiting for connections')
			(recvSocket, address) = mySocket.accept()
			print('HTTP request received (going to parse and process):')
			request = recvSocket.recv(2048).decode('utf-8')
			print(request)
			lista_datos = self.Analiza(request)
			try:
				method = lista_datos[0]
				resource = lista_datos[1]
				(returnCode, htmlAnswer) = self.Process(cache,method, resource)
				print('Answering back...')
				recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n" + htmlAnswer + "\r\n", 'utf-8'))
				recvSocket.close()
			except:
				recvSocket.send(bytes("<html><body><h1>Introduce un recurso</h1></body></html>" , 'utf-8'))

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234)
