import http.server
import socketserver
import cgi
import json

class DataRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>CSV / JSON Metrics</title>
                    <style>
                        table {
                            border-collapse: collapse;
                            width: 100%;
                        }
                        th, td {
                            border: 1px solid black;
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                    <h1>Upload Metrics</h1>
                    <form action="/" method="post" enctype="multipart/form-data">
                        <input type="file" name="file">
                        <input type="submit" value="Upload">
                    </form>
                </body>
                </html>
            ''')

        else:
            super().do_GET()

 

    def do_POST(self):

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        file_item = form['file']

        if file_item.filename:
            file_data = file_item.file.read()
            file_extension = file_item.filename.split('.')[-1]

            if file_extension == 'csv':
                # Handle CSV file
                file_data = file_data.decode('utf-8')
                lines = file_data.split('\n')
                header_row = lines[0]
                data_rows = lines[1:]
 
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(b'''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>CSV / JSON Metrics</title>
                        <style>
                            table {
                                border-collapse: collapse;
                                width: 100%;
                            }

                            th, td {
                                border: 1px solid black;
                                padding: 8px;
                                text-align: left;
                            }

                            th {
                                font-weight: bold;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Upload Metrics</h1>
                        <form action="/" method="post" enctype="multipart/form-data">
                            <input type="file" name="file">
                            <input type="submit" value="Upload">
                        </form>
                        <br>
                        <table>
                ''')

                # Process header row
                header_cells = header_row.strip().split(',')
                header_row_html = '<tr>'
                
                for cell in header_cells:
                    header_row_html += f'<th>{cell}</th>'
                    
                header_row_html += '</tr>'
                self.wfile.write(header_row_html.encode())

                # Process data rows
                for data_row in data_rows:
                    cells = data_row.strip().split(',')
                    row_html = '<tr>'
                    for cell in cells:
                        row_html += f'<td>{cell}</td>'
                    row_html += '</tr>'
                    self.wfile.write(row_html.encode())
                self.wfile.write(b'''
                        </table>
                    </body>
                    </html>
                ''')

            elif file_extension == 'json':

                # Handle JSON file
                try:
                    json_data = json.loads(file_data.decode('utf-8'))

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'''
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>CSV / JSON Metrics</title>
                            <style>
                                table {
                                    border-collapse: collapse;
                                    width: 100%;
                                }

                                th, td {
                                    border: 1px solid black;
                                    padding: 8px;
                                    text-align: left;
                                }

                                th {
                                    font-weight: bold;
                                }

                            </style>
                        </head>
                        <body>
                            <h1>Upload Metrics</h1>
                            <form action="/" method="post" enctype="multipart/form-data">
                                <input type="file" name="file">
                                <input type="submit" value="Upload">
                            </form>
                            <br>
                            <table>
                    ''')

                    # Get the keys from the first item in the JSON data
                    keys = list(json_data[0].keys())
 
                    # Write table header
                    header_row_html = '<tr>'
                    for key in keys:
                        header_row_html += f'<th>{key}</th>'
                        
                    header_row_html += '</tr>'
                    self.wfile.write(header_row_html.encode())

                    # Write table rows
                    for item in json_data:
                        row_html = '<tr>'
                        
                        for key in keys:
                            value = item[key]
                            row_html += f'<td>{value}</td>'

                        row_html += '</tr>'
                        self.wfile.write(row_html.encode())

                    self.wfile.write(b'''
                            </table>
                        </body>
                        </html>
                    ''')

                except ValueError:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'Bad Request: Invalid JSON file')

            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Bad Request: Unsupported file format')

        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Bad Request: No file uploaded')

 

if __name__ == "__main__":

    PORT = 8000
    Handler = DataRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Server running on port", PORT)
        httpd.serve_forever()