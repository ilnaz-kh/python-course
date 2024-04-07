from person import Person
from exceptions import EmailInvalidError, PhoneInvalidError, ShowError, CinemahallError, FileError, MovieError
from movie import Movie
from show import Show
from cinema_hall import CinemaHall

class Employee(Person):
    
    def __init__(self, file):
        self.file = file


    def register_employee(self, username, password, position, name, phone, email=None):
        try:
            super().email_validity(email)
            super().phone_validity(phone)
        except EmailInvalidError as e:
            print(e.__str__())
        except PhoneInvalidError as e:
            print(e.__str__())
        else:
            if self.unique_username_check(username= username):
                try:
                    ## create unique employee_id
                    employee_id = self.file.create_id('Employee', )
                    data_dict = {
                        'employee_id': employee_id,
                        'username': username,
                        'password': password,
                        'name': name,
                        'phone': phone,
                        'email': email,
                        'position': position
                        }
                    ## save the employee's informations to the associated file
                    self.file.save_data('Employee', data_dict)
                except FileError as e:
                    print(f"Cannot register the employee: {e.__str__()}")
                else:
                    print("The employee's registration has been successfully completed.")


    def unique_username_check(self, username):
        try:
            id_list = self.file.select_data(class_name= "Employee", coloumns=["employee_id"], where={"username": username})
        except FileError as e:
            print("FileError occured while checking username, please try again")
            return False
        if id_list: # username is already taken
            print(f"The requested username `{username}` is already taken.")
            return False
        return True


    def employee_login(self, username, password):
        try:
            id_pass_list = self.file.select_data(class_name= "Employee", coloumns=["employee_id", "password"], where={"username": username})
        except FileError as e:
            print(e.__str__())
            return None
        if not id_pass_list: # returned list is empty means the username is not found
            print(f"The provided username `{username}` does not exist.")
            return None
        id_ = id_pass_list[0]["employee_id"]
        pass_ = id_pass_list[0]["password"]
        if pass_ != password:
            print(f"The provided password is not correct.")
            return None
        return id_
        

    def add_movie(self, query):
        try:
            Movie(self.file).fetch_save_movie(query)
        except MovieError as e:
            print(f"Cannot add movie: {e.__str__()}")

        
    def schedule_show(self, movie_id, cinemahall_id, show_date, show_number):
        try:
            Show(self.file).save_show(movie_id, cinemahall_id, show_date, show_number)
        except ShowError as e:
            print("The requested showtime cannot be scheduled!")
            print(e)


    def add_cinemahall(self, hall_name, total_seats):
        try:
            CinemaHall(self.file).save_cinemahall(hall_name, total_seats)
        except CinemahallError as e:
            print("Cannot add cinema hall!")
            print(e.__str__())


    def change_show_status(self, show_id, new_status):
        try:
            Show(self.file).update_show(show_id, new_status)
        except ShowError as e:
            print(e.__str__())


    def view_shows(self):
        try: 
            shows = self.file.select_data(class_name= "Show", 
                                                coloumns= ["show_id", "movie_id", "cinemahall_id", "show_date", "show_number", "status"], 
                                                where= {})
            if shows:
                print("\nList of all Shows:")
                for show in shows:
                    ## get `cinemahall name` from `cinemahalls` file correspond to `cinemahall_id` from `shows` file
                    show["hall_name"] = self.file.get_attributes(class_name= "CinemaHall", id_= show["cinemahall_id"], attrs= ["name"])["name"]
                    ## get `movie title` from `movies` file correspond to `movie_id` from `shows` file
                    show["title"] = self.file.get_attributes(class_name= "Movie", id_= show["movie_id"], attrs= ["title"])["title"]
                    ## print
                    print(f"Show ID: {show['show_id']}, Movie: {show['title']}, Date: {show['show_date']}, " + 
                        f"Show Number: {show['show_number']}, Show Status: {show['status']}, Hall Name: {show['hall_name']}")
        except FileError as e:
            print(e.__str__())
                
    def view_cinemahalls(self):
        try:
            halls = self.file.select_data(class_name= "CinemaHall", 
                                                coloumns= ["cinemahall_id", "name", "total_seats"], 
                                                where= {})
            if halls:
                print("\nCinema Halls' Informaion:\n" + "-"*40)
                for hall in halls:
                    print(f"Cinema Hall ID: {hall['cinemahall_id']}, Hall Name: {hall['name']}, Number of Seats: {hall['total_seats']}")
        except FileError as e:
            print(e.__str__())

