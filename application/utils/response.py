from flask import jsonify
class Response:
    @staticmethod
    def ok(data=None, status=200, mensaje='Petición Exitosa'):        
        return {'data': data, 'mensaje':mensaje}, status
    
    @staticmethod
    def error(mensaje='Error desconocido', error=None, status=500):
        return {'mensaje': mensaje, 'error': error}, status