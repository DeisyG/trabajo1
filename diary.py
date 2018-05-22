from collections import OrderedDict
import datetime
import sys
import os
from peewee import *

db= SqliteDatabase('diary.db')

class Entry(Model):

    content=TextField()
    timestamp=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def add_entry():
    """Agrega un registro"""
    print("Introduce tu registro, Presione Ctrl+Z+Enter cuando termines ")

    data = sys.stdin.read().strip()
    if data:
        if input('Guardar entrada? [Y/N]: ').lower() != 'n': #si presiona cualquier tecla diferente a n guarda
            Entry.create(content=data)
            print("GUARDADA EXITOSAMENTE")


def view_entries(search_query=None):
    """Ver nuestras entras"""
    entries= Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries= entries.where(Entry.content.contains(search_query))

    for entry in entries:

        timestamp= entry.timestamp.strftime('%A %B %d, %Y %I:%M%p') #formato que deseen
        clear()
        print(timestamp)
        print('+'*len(timestamp))
        #print de esta entrada
        print(entry.id," | ", entry.content)
        print('\n\n\n'+'+'*len(timestamp)+'\n')
        print("n-->siguiente entrada")
        print("q-->salir del menu")

        next_action=input('Accion a realizar [n/q/]: ').lower().strip()
        if next_action == 'q':
            break

def search_entries():
    """Busca una entrada con cierto texto"""

    view_entries(input('Texto a buscar: '))

def delete_entry():
    """Eliminar un registro"""
    entries= Entry.select().order_by(Entry.timestamp.desc())
    for entry in entries:
        timestamp= entry.timestamp.strftime('%A %B %d, %Y %I:%M%p') #formato que deseen
        print(timestamp)
        print('+'*len(timestamp))
        #print de esta entrada
        print(entry.id," | ", entry.content)

    i=input("Ingrese ID: ")
    response=input("Estas seguro? [Y/N]: ").lower()
    if response == 'y':
        f=Entry.get(Entry.id==i)
        f.delete_instance()
        print("ELIMINADO EXITOSAMENTE")

def update_entry():
    """Modificar un registro"""
    entries= Entry.select().order_by(Entry.timestamp.desc())
    for entry in entries:
        timestamp= entry.timestamp.strftime('%A %B %d, %Y %I:%M%p') #formato que deseen
        print(timestamp)
        print('+'*len(timestamp))
        #print de esta entrada
        print(entry.id," | ", entry.content)

    i=input("Ingrese ID: ")
    c=input("ingrese nuevo contenido: ")
    response=input("Estas seguro? [Y/N]: ").lower()
    if response == 'y':
        f=Entry.id
        n=entry.update(content=c).where(f==i)
        n.execute()
        print("MODIFICADO EXITOSAMENTE")

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
    ('m', update_entry),
    ('d', delete_entry),
])

def menu_loop():
    """Muestra el menu con las opciones"""

    choice= None

    while choice != 'q':
        print("")
        print("Presiona 'q' para salir")

        for key, value in menu.items():
            print('{}| {}'.format(key, value.__doc__))
        choice= input('Eleccion: ').lower().strip()
        if choice in menu:
            clear()
            menu[choice]()

def initialize():
    db.connect()
    db.create_tables([Entry],safe=True)

def clear():
    os.system('cls' if os.name== 'nt' else 'clear')


if __name__ == '__main__':
    initialize()
    menu_loop()
