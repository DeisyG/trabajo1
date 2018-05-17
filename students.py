from peewee import *

db=SqliteDatabase('students.db')

class Student(Model):
    username= CharField(max_length=255, unique=True)
    points= IntegerField(default=0)

    class Meta:
        database=db

students=[
    {'username':'Aldo',
    'points':15},
    {'username':'Betty',
    'points':7},
    {'username':'Ariel',
    'points':10},
    {'username':'Jairo',
    'points':0},
    {'username':'Dayana',
    'points':9},
]

#metodo para añadir estudiantes
def add_students():
    for student in students:
        try:
            #crear registro
            Student.create(username=student['username'],points=student['points'])

        except IntegrityError: #cuando ya exista el registro
            student_records=Student.get(username=student['username'])
            student_records.points=student['points']
            student_records.save()#guardar cambios

#metodo que me obtenga el alumno con la calificacion mayor
def top_student():
    topcalif=Student.select().order_by(Student.points.desc()).get()
    return topcalif


if __name__== '__main__':
    db.connect()#permite conectarse a la base de datos
    db.create_tables([Student],safe=True)
    add_students()
    print('El mejor estudiante es {}'.format(top_student().username))
