from email.utils import formatdate
import socket
import unittest
import http_server
import test_client


class testGatherData(unittest.TestCase):
    def setUp(self):
        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP
            )
        try:
            address = ('127.0.0.1', 50000)
            self.server_socket.bind(address)
            self.server_socket.listen(1)
        finally:
            pass

    def tearDown(self):
        self.conn.close()
        self.server_socket.close()
"""
    def testMessages(self):
        sent_list = ["tiny little thing\r\n\r\n", "really really really really really really long thing\r\n\r\n", "A thirty-two byte message eh\r\n\r\n"]
        received_list = []
        # The above messages must be manually sent via a separate terminal
        # Using the following commands in the Python interpreter:
        # >>>import test_client
        # >>>test_client.run_client("tiny little thing\r\n\r\n")
        # >>>test_client.run_client("really really really really really really long thing\r\n\r\n")
        # >>>test_client.run_client("A thirty-two byte test message\r\n")
        for i in xrange(3):
            self.conn, client_address = self.server_socket.accept()
            received_list.append(http_server.gather_request(self.conn))
            self.conn.shutdown(socket.SHUT_WR)
        self.assertItemsEqual(sent_list, received_list) 
"""

class testSplitFirstLine(unittest.TestCase):
    def setUp(self):
        self.input = "GET /index.html HTTP/1.1\r\nmore data more data more data\r\n\r\n"
        self.first_line = "GET /index.html HTTP/1.1"

    def test_split(self):
        self.assertEqual(http_server.split_off_first_line(self.input), self.first_line)


class testMapURI(unittest.TestCase):
    def setUp(self):
        self.root = "webroot"
        self.missing_URI = "/notfound.html"
        self.missing_type = "text/html"

        self.dir_URI = "/images/"
        self.dir_type = "text/plain"
        self.dir_bytes = "/images\r\n\tJPEG_example.jpg\r\n\tSample_Scene_Balls.jpg\r\n\tsample_1.png"

        self.file_URI = "/a_web_page.html"
        self.file_type = "text/html"
        self.file_bytes = "<!DOCTYPE html>\n<html>\n<body>\n\n<h1>North Carolina</h1>\n\n<p>A fine place to spend a week learning web programming!</p>\n\n</body>\n</html>\n\n"

    def test_map(self):
        self.assertRaises(http_server.NotFoundError, http_server.map_URI, self.root, self.missing_URI)
        self.assertEqual(http_server.map_URI(self.root, self.dir_URI), (self.dir_type, self.dir_bytes))
        self.assertEqual(http_server.map_URI(self.root, self.file_URI), (self.file_type, self.file_bytes))


class testBuildResponse(unittest.TestCase):
    def setUp(self):
        self.found_code = 200
        self.file_type = "text/html"
        self.file_body = "<!DOCTYPE html>\n<html>\n<body>\n\n<h1>North Carolina</h1>\n\n<p>A fine place to spend a week learning web programming!</p>\n\n</body>\n</html>\n\n"
        self.file_response = "HTTP/1.1 200 OK\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/html\r\nContent-Length: 136\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n\n<h1>North Carolina</h1>\n\n<p>A fine place to spend a week learning web programming!</p>\n\n</body>\n</html>\n\n"

        self.dir_type = "text/plain"
        self.dir_body = "/images\r\n\tJPEG_example.jpg\r\n\tSample_Scene_Balls.jpg\r\n\tsample_1.png"
        self.dir_response = "HTTP/1.1 200 OK\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/plain\r\nContent-Length: 66\r\n\r\n/images\r\n\tJPEG_example.jpg\r\n\tSample_Scene_Balls.jpg\r\n\tsample_1.png"

        self.not_found_code = 404
        self.error_type = "text/html"
        self.four04_response = "HTTP/1.1 404 Not found\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/html\r\nContent-Length: 77\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n<h1>404 Error: Not found</h1>\n</body>\n</html>\n\n"

        self.not_allowed_code = 405
        self.four05_response = "HTTP/1.1 405 Method not allowed\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/html\r\nContent-Length: 86\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n<h1>405 Error: Method not allowed</h1>\n</body>\n</html>\n\n"

        self.bad_server_code = 500
        self.five00_response = "HTTP/1.1 500 Some idiot built this server incorrectly\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/html\r\nContent-Length: 108\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n<h1>405 Error: Some idiot built this server incorrectly</h1>\n</body>\n</html>\n\n"

    def test_build(self):
        self.assertEqual(http_server.build_response(self.found_code, self.file_type, self.file_body), self.file_response)
        self.assertEqual(http_server.build_response(self.found_code, self.dir_type, self.dir_body), self.dir_response)
        self.assertEqual(http_server.build_response(self.not_found_code, self.error_type), self.four04_response)
        self.assertEqual(http_server.build_response(self.not_allowed_code, self.error_type), self.four05_response)

if __name__ == '__main__':
    unittest.main()
