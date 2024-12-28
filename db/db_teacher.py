import psycopg2
from psycopg2 import sql

import config
import teacher.model

db_config = {
    'dbname': config.DB_NAME,
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'host': config.DB_HOST,
    'port': config.DB_PORT,
}


def db_connection():
    return psycopg2.connect(**db_config)


def check_id(user_id: int) -> (teacher.model.Teacher, int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        # Проверяем наличие пользователя с данным user_id
        check_query = sql.SQL("SELECT EXISTS (SELECT 1 FROM teacher WHERE id = %s)")
        cursor.execute(check_query, (user_id,))
        exists = cursor.fetchone()[0]
        TMP = sql.SQL("SELECT * from teacher WHERE id = %s")
        cursor.execute(TMP, (user_id,))
        if exists:
            # Если пользователь существует, извлекаем информацию
            get_all_query = sql.SQL("SELECT * FROM teacher WHERE id = %s")
            cursor.execute(get_all_query, (user_id,))
            rows = cursor.fetchone()
            user = teacher.model.Teacher(
                id=rows[0],
                name=rows[1],
                grade=rows[2],
                sphere=rows[3],
                description=rows[4],
                show=rows[5],
                nickname=rows[6],
            )
            return user, 1
        else:
            user = teacher.model.Teacher
            user.id = user_id
            return user, 0

    except (Exception, psycopg2.DatabaseError) as error:
        return error, -1,
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_user(usr: teacher.model.Teacher):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        user, i = check_id(usr.id)

        if i == 1:  # Пользователь уже существует
            # Обновляем данные пользователя
            update_query = sql.SQL("""
                UPDATE teacher 
                SET  name = %s, grade = %s, sphere = %s, description = %s, show = %s, nickname = %s
                WHERE id = %s
            """)
            cursor.execute(update_query, (
                usr.name,
                usr.grade,
                usr.sphere,
                usr.description,
                usr.show,
                usr.nickname,
                usr.id,
            ))
            cursor.connection.commit()
        elif i == 0:  # Пользователь новый
            # Добавляем нового пользователя
            insert_query = sql.SQL("""
                INSERT INTO teacher (id, name, grade, sphere, description, show, nickname)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (
                usr.id,
                usr.name,
                usr.grade,
                usr.sphere,
                usr.description,
                usr.show,
                usr.nickname
            ))

        else:  # Произошла ошибка при проверке ID
            return False

        connection.commit()
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()


def change_show(user_id: int, show: bool):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        update_query = sql.SQL("""
                UPDATE teacher 
                SET show = %s
                WHERE id = %s
            """)
        cursor.execute(update_query, (
            show, user_id
        ))
        cursor.connection.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_all_data_all_student(id_teacher: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_student_query = sql.SQL("""SELECT id,  name, grade, sphere, description, nickname
FROM student  
WHERE id != %s and EXISTS  (
    SELECT 1 
    FROM teacher_student 
    WHERE student.id = teacher_student.id_student
    and teacher_student.id_teacher = %s
    AND teacher_student.id_student != teacher_student.id_teacher
)""")
        cursor.execute(get_all_student_query, (id_teacher, id_teacher,))

        rows = cursor.fetchall()
        user_info = [
            {"id": row[0], "name": row[1], "grade": row[2], "sphere": row[3], "bio": row[4], "nickname": row[5]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_all_student(id_teacher: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_student_query = sql.SQL("""SELECT id,  name, grade, sphere, description, nickname
FROM student 
WHERE show = true AND 
id != %s
and NOT EXISTS (
    SELECT 1 
    FROM teacher_student 
    WHERE student.id = teacher_student.id_student
    and teacher_student.id_teacher = %s
    AND teacher_student.id_student != teacher_student.id_teacher
)""")
        cursor.execute(get_all_student_query, (id_teacher, id_teacher,))
        rows = cursor.fetchall()
        user_info = [
            {"id": row[0], "name": row[1], "grade": row[2], "sphere": row[3], "bio": row[4], "nickname": row[5]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()

async def get_one_student(id_student: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_student_query = sql.SQL("""SELECT id,  name, grade, sphere, description, nickname
FROM student 
WHERE id = %s""")
        cursor.execute(get_all_student_query, (id_student,))
        rows = cursor.fetchall()
        user_info = [
            {"id": row[0], "name": row[1], "grade": row[2], "sphere": row[3], "bio": row[4], "nickname": row[5]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()



all_grades = ["No_work", "Intern", "Junior", "Middle", "Senior"]
all_spheres = ["NLP", "CV", "RecSys", "Audio", "Classic_ML", "Any"]


async def get_filter_students(grade, sphere, teacher_id):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        fstudents_query = sql.SQL("""
        SELECT name, grade, sphere, description, id FROM student 
        WHERE 
        grade similar to %s and
        sphere similar to %s and
        show = true AND
        id != %s
        and NOT EXISTS (
    SELECT 1 
    FROM teacher_student 
    WHERE student.id = teacher_student.id_student
    and teacher_student.id_teacher = %s
    AND teacher_student.id_student != teacher_student.id_teacher
)""")
        if not grade and sphere:
            cursor.execute(fstudents_query,
                           ("%(" + "|".join(all_grades) + ")%", "%(" + "|".join(sphere.split(", ")) + ")%",
                            teacher_id, teacher_id,), )
        elif not sphere and grade:
            cursor.execute(fstudents_query,
                           ("%(" + "|".join(grade.split(", ")) + ")%", "%(" + "|".join(all_spheres) + ")%",
                            teacher_id, teacher_id,), )
        elif not grade and not sphere:
            cursor.execute(fstudents_query, ("%(" + "|".join(all_grades) + ")%", "%(" + "|".join(all_spheres) + ")%",
                                             teacher_id, teacher_id,), )
        else:
            cursor.execute(fstudents_query,
                           ("%(" + "|".join(grade.split(", ")) + ")%", "%(" + "|".join(sphere.split(", ")) + ")%",
                            teacher_id, teacher_id,), )
        rows = cursor.fetchmany(size=4)
        user_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3], "id": row[4]}
            for row in rows
        ]
        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error

    finally:
        if connection:
            cursor.close()
            connection.close()
