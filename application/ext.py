
#* En este archivo se instancian las extenciones para que no ocurran errores de referencias circulares *#

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

ma = Marshmallow()
migrate = Migrate()