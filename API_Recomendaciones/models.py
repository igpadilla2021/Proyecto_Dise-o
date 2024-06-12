from pymongo import MongoClient, errors

uri = "mongodb+srv://beespinoza2022:eVsJfxayY1I1586t@cluster0.yblbnqi.mongodb.net/?retryWrites=true&w=majority&appName=cluster0"
client = MongoClient(uri)
db = client["proyectoSemestralDis"]
collectionSitios = db["sitios"]

if "sitios" not in db.list_collection_names():
    try:
        db.create_collection("sitios", validator=
                             {
          "$jsonSchema": {
            "bsonType": "object",
            "required": ["nombre", "descripcion", "latitud", "longitud", "categorias", "estado", "fecha_creacion", "usuario_creo"],
            "properties": {
              "nombre": {
                "bsonType": "string",
                "description": "El nombre del sitio debe ser una cadena de texto y es obligatorio"
              },
              "descripcion": {
                "bsonType": "string",
                "description": "La descripción del sitio debe ser una cadena de texto y es obligatoria"
              },
              "latitud": {
                "bsonType": "double",
                "description": "La latitud del sitio debe ser un número de punto flotante y es obligatoria"
              },
              "longitud": {
                "bsonType": "double",
                "description": "La longitud del sitio debe ser un número de punto flotante y es obligatoria"
              },
              "categorias": {
                "bsonType": "array",
                "items": {
                  "bsonType": "string"
                },
                "description": "Las categorías del sitio deben ser un array de cadenas de texto"
              },
              "calificacion_promedio": {
                "bsonType": "double",
                "description": "La calificación promedio del sitio debe ser un número de punto flotante"
              },
              "reseñas": {
                "bsonType": "array",
                "items": {
                  "bsonType": "object",
                  "required": ["usuario", "calificacion", "comentario", "fecha"],
                  "properties": {
                    "usuario": {
                      "bsonType": "string",
                      "description": "El nombre del usuario que hizo la reseña debe ser una cadena de texto y es obligatorio"
                    },
                    "calificacion": {
                      "bsonType": "double",
                      "description": "La calificación de la reseña debe ser un número de punto flotante y es obligatoria"
                    },
                    "comentario": {
                      "bsonType": "string",
                      "description": "El comentario de la reseña debe ser una cadena de texto y es obligatorio"
                    },
                    "fecha": {
                      "bsonType": "date",
                      "description": "La fecha de la reseña debe ser una fecha y es obligatoria"
                    }
                  }
                },
                "description": "Las reseñas del sitio deben ser un array de objetos"
              },
              "estado": {
                "bsonType": "string",
                "enum": ["activo", "inactivo"],
                "description": "El estado del sitio debe ser 'activo' o 'inactivo' y es obligatorio"
              },
              "fecha_creacion": {
                "bsonType": "date",
                "description": "La fecha de creación del sitio debe ser una fecha y es obligatoria"
              },
              "usuario_creo": {
                "bsonType": "string",
                "description": "El usuario que creó el sitio debe ser una cadena de texto y es obligatorio"
              },
              "fecha_modificacion": {
                "bsonType": "date",
                "description": "La fecha de la última modificación del sitio debe ser una fecha"
              },
              "usuario_modifico": {
                "bsonType": "string",
                "description": "El usuario que realizó la última modificación debe ser una cadena de texto"
              },
              "fecha_ultimo_ingreso": {
                "bsonType": "date",
                "description": "La fecha del último ingreso al sitio debe ser una fecha"
              }
            }
          }
        })
    except errors.CollectionInvalid:
        pass

collectionUsuarios = db["usuarios"]

if "usuarios" not in db.list_collection_names():
    try:
        db.create_collection("usuarios", validator=
            {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["nombre", "email", "estado", "usuario_creacion", "es_administrador"],
                "properties": {
                  "nombre": {
                    "bsonType": "string",
                    "description": "El nombre del usuario debe ser una cadena de texto y es obligatorio"
                  },
                  "email": {
                    "bsonType": "string",
                    "description": "El correo electrónico del usuario debe ser una cadena de texto y es obligatorio"
                  },
                  "preferencias": {
                    "bsonType": "array",
                    "items": {
                      "bsonType": "string"
                    },
                    "description": "Las preferencias del usuario deben ser un array de cadenas de texto"
                  },
                  "fecha_nacimiento": {
                    "bsonType": "date",
                    "description": "La fecha de nacimiento del usuario debe ser una fecha"
                  },
                  "estado": {
                    "bsonType": "string",
                    "enum": ["activo", "inactivo"],
                    "description": "El estado del usuario debe ser 'activo' o 'inactivo' y es obligatorio"
                  },
                  "fecha_creacion": {
                    "bsonType": "date",
                    "description": "La fecha de creación del usuario debe ser una fecha y es obligatorio"
                  },
                  "usuario_creacion": {
                    "bsonType": "string",
                    "description": "El usuario que creó el usuario debe ser una cadena de texto y es obligatorio"
                  },
                  "fecha_ultima_modificacion": {
                    "bsonType": "date",
                    "description": "La fecha de la última modificación del usuario debe ser una fecha"
                  },
                  "usuario_modifico": {
                    "bsonType": "string",
                    "description": "El usuario que realizó la última modificación debe ser una cadena de texto"
                  },
                  "fecha_ultimo_ingreso": {
                    "bsonType": "date",
                    "description": "La fecha del último ingreso del usuario debe ser una fecha"
                  },
                  "es_administrador": {
                    "bsonType": "bool",
                    "description": "Indica si el usuario es administrador y es obligatorio"
                  }
                }
              }
            }
        )
    except errors.CollectionInvalid:
        pass

    
class Usuario:
    def __init__(self, user_id, nombre, sitios_visitados):
        self.user_id = user_id
        self.nombre = nombre
        self.sitios_visitados = sitios_visitados
    
    @classmethod
    def from_json(cls, json_data):
        if json_data:
            return cls(
                user_id = json_data.get('_id'),
                nombre = json_data.get('name'),
                sitios_visitados = json_data.get('visited_sites', [])
            )
        return None
    
class Sitio:
    def __init__(self, nombre_sitio, latitud, longitud, descripcion=None, tags=None, categoria=None, popularidad=0, rating=0.0, horario_apertura=None, direccion=None):
        self.nombre_sitio = nombre_sitio
        self.latitud = latitud
        self.longitud = longitud
        self.descripcion = descripcion
        self.tags = tags if tags is not None else []
        self.categoria = categoria
        self.popularidad = popularidad
        self.rating = rating
        self.horario_apertura = horario_apertura
        self.direccion = direccion

    @classmethod
    def from_json(cls, json_data):
        return cls(
            nombre_sitio=json_data.get('nombre_sitio'),
            latitud=json_data.get('latitud'),
            longitud=json_data.get('longitud'),
            descripcion=json_data.get('descripcion'),
            tags=json_data.get('tags', []),
            categoria=json_data.get('categoria'),
            popularidad=json_data.get('popularidad', 0),
            rating=json_data.get('rating', 0.0),
            horario_apertura=json_data.get('horario_apertura'),
            direccion=json_data.get('direccion')
        )

    def to_json(self):
        return {
            'nombre_sitio': self.nombre_sitio,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'descripcion': self.descripcion,
            'tags': self.tags,
            'categoria': self.categoria,
            'popularidad': self.popularidad,
            'rating': self.rating,
            'horario_apertura': self.horario_apertura,
            'direccion': self.direccion
        }
