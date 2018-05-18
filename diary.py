import sys
from collections import OrderedDict
import datetime
from peewee import *


db=SqliteDatabase('diary.db')

class Entry(Model):
    content=TextField()
    timestamp=DateTimeField(default=datetime.datetime.now)#coger la fecha y hora
    class Meta:
        database=db
def add_entry():
    """Agregar un registro"""
    print("Introduzca un registro, Presiones Ctrl+z+Enter para terminar")
    data=sys.stdin.read().strip()
    if data:
        if input("Desea guardar este registro [Y/N]: ").lower() !='y':
            Entry.create(content=data)
            print("Se ha guardado exitosamente")

def view_entries():
    """Ver un registro"""

    entries= Entry.select().order_by(Entry.timestamp.desc())
    for entry in entries:
        timestamp= entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print("*******************")
        print(entry.content)
        print("n---> Ver el siguiente registro")
        print("q---> Salir del menu")

        next_entry=input("Desea ver la siguiente entrada [n/q]: ").lower().strip()
        if next_entry == 'q':
            break
def delete_entries():
    """Eliminar un registro"""

menu=OrderedDict([
    ('a',add_entry),
    ('v',view_entries),

])

def menu_loop():
    """Mostrar opciones"""
    choice=None
    while choice != 'x':
        print("Presiona 'x' para salir")

        for key, value in menu.items():#nos permite corre cada uno de lo elementos que tenemos en los corchetes
            print('{}--->{}'.format(key, value.__doc__))
        choice=input("Escoja opcion: ").lower().strip()#strip permite eliminar espacio o caracteres
        if choice in menu:
            menu[choice]()

def init():
    db.connect()
    db.create_tables([Entry],safe=True)

if __name__ == '__main__':
    init()
    menu_loop()
