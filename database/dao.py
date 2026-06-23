from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def load_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.year as year from team t where t.year >= 1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def load_teams(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.team_code as team_code, t.name as name from team t where year= %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def load_teams_salary(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """with team_salary as (select t.team_code as team_code, SUM(s.salary) as tot 
                    from team t 
                    join salary s on s.team_code= t.team_code 
                    where t.year = %s group by t.team_code)
                                    
                    select distinct ts1.team_code as team1, ts2.team_code as team2, ts1.tot + ts2.tot as total_salary
                    from team_salary ts1, team_salary ts2
                    where ts1.team_code > ts2.team_code
                    group by ts1.team_code, ts2.team_code"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result