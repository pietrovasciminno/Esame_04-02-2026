from database.DB_connect import DBConnect
from model.artist import Artist


class DAO:

    @staticmethod
    def get_authorship():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT role
                    FROM authorship"""
        cursor.execute(query)

        for row in cursor:
            result.append(row['role'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_artisti(role):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a1.artist_id as id, a1.name as name, count(a2.object_id ) as num_objects
                    from artists a1, authorship a2, objects o  
                    where a1.artist_id = a2.artist_id 
                    and a2.object_id = o.object_id 
                    and o.curator_approved = 1
                    and a2.role = %s
                    group by a1.artist_id """
        cursor.execute(query, (role,))

        for row in cursor:
            result.append(Artist(row['id'], row['name'], row['num_objects']))

        cursor.close()
        conn.close()
        return result
