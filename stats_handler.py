from label import Label
from utils import def_font

class StatsHandler:
    
    def __create__labels(self):
        games_played = Label("total games played: ", def_font, 30, (50, 200))
        games_completed = Label("total games completed: ", def_font, 30, (50, 250))
        average_time = Label("average time: ", def_font, 30, (50, 300))
        average_hints = Label("average hints given : ", def_font, 30, (50, 350))
        average_mistakes = Label("average mistakes made: ", def_font, 30, (50, 400))
        most_freq_mode = Label("most frequented game mode: ", def_font, 30, (50, 450))
        labels = (games_played, games_completed, average_time, average_hints, average_mistakes, most_freq_mode)
        return labels
    
    def show_stats(self, conn, screen, color):
        labels = self.__create__labels()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM game_data")
        games_played = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(id) FROM game_data WHERE completed = 1")
        games_completed = cursor.fetchall()[0][0]
        cursor.execute("SELECT AVG(time) FROM game_data")
        average_time = round(cursor.fetchall()[0][0],2)
        cursor.execute("SELECT AVG(hints) FROM game_data")
        average_hints = round(cursor.fetchall()[0][0],2)
        cursor.execute("SELECT AVG(mistakes) FROM game_data")
        average_mistakes = round(cursor.fetchall()[0][0],2)
        most_freq_query = """SELECT mode, COUNT(*) as row_count
                            FROM game_data
                            GROUP BY mode
                            ORDER BY row_count DESC
                            LIMIT 1;"""
        cursor.execute(most_freq_query)
        most_freq_mode = cursor.fetchall()[0][0]
        
        stats = (games_played, games_completed, average_time, average_hints, average_mistakes, most_freq_mode)
        for label, stat in zip(labels, stats):
            new_text = label.name_text + str(stat)
            label.set_text(new_text)
            label.change_theme(color)
            label.display_label(screen)
            
        conn.close()
        
        
        
        