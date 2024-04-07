from person import Person
from exceptions import EmailInvalidError, PhoneInvalidError, ReservationError, FeedbackError, FileError
from reservation import Reservation
from feedback import Feedback

class User(Person):
    
    def __init__(self, file):
        self.file = file


    def register_user(self, username, password, name, phone, email=None):
        """
        - username : A unique name for each user
        - password : A password to enter the system
        - user_id : A unique identifier for each user. (made by system)
        - name: The name of the user.
        - phone: The phone number associated with the user.
        - email: The email address associated with the user.
        """
        try:
            super().email_validity(email)
            super().phone_validity(phone)
        except EmailInvalidError as e:
            print(f"Cannot register user: {e.__str__()}")
        except PhoneInvalidError as e:
            print(f"Cannot register user: {e.__str__()}")
        else:
            if self.unique_username_check(username= username):
                try:
                    ## create unique user_id
                    user_id = self.file.create_id('User', )
                    data_dict = {
                        'user_id': user_id,
                        'username': username,
                        'password': password,
                        'name': name,
                        'phone': phone,
                        'email': email
                        }
                    ## save the user's informations to the associated file
                    self.file.save_data('User', data_dict)
                except FileError as e:
                    print(f"Cannot register user: {e.__str__()}")
                else:
                    print("The user's registration has been successfully completed.")


    def unique_username_check(self, username):
        try:
            id_list = self.file.select_data(class_name= "User", coloumns=["user_id"], where={"username": username})
        except FileError as e:
            print("FileError occured while checking username, please try again")
            return False
        if id_list: # username is already taken
            print(f"The requested username `{username}` is already taken.")
            return False
        return True


    def user_login(self, username, password):
        try:
            id_pass_list = self.file.select_data(class_name= "User", coloumns=["user_id", "password"], where={"username": username})
        except FileError as e:
            print(e.__str__())
            return None
        if not id_pass_list: # returned list is empty means the username is not found
            print(f"The provided username `{username}` does not exist.")
            return None
        id_ = id_pass_list[0]["user_id"]
        pass_ = id_pass_list[0]["password"]
        if pass_ != password:
            print(f"The provided password is not correct.")
            return None
        return id_
        

    def make_reservation(self, user_id, show_id, seat_number):
        ## Save reservation
        try:
            Reservation(self.file).save_reservtion(user_id, show_id, seat_number)
        except ReservationError as e:
            print("The reservation cannot be made!")
            print(e)


    def cancel_reservation(self, user_id, reservation_id):
        try:
            Reservation(self.file).cancel_reservation(user_id, reservation_id)
        except ReservationError as e:
            print(f"The reservation cannot be cancelled: {e}")


    def submit_feedback(self, user_id, movie_id, rating=5, comment=""):
        try:
            Feedback(self.file).create_feedback(user_id, movie_id, rating, comment)
        except FeedbackError as e:
            print(f"The feedback cannot be submitted: {e.__str__()}")


    def view_profile(self, user_id):
        self.view_info(user_id)
        self.view_feedbacks(user_id)
        self.view_reservations(user_id)
    

    def view_info(self, user_id):
        try:
            if not self.file.is_id('User', user_id):
                print(f"The provided user ID `{user_id}` does not exist!")
                return
            ## get information from users file
            user_info = self.file.get_attributes("User", user_id, ["name", "phone", "email"])
            print("\nUser Information\n"+ "-"*40)
            print(f"Name: {user_info['name']}, Phone: {user_info['phone']}, Email: {user_info['email']}")
        except FileError as e:
            print(e)


    def view_feedbacks(self, user_id):
        try:
            if not self.file.is_id('User', user_id):
                print(f"The provided user ID `{user_id}` does not exist!")
                return
            ## get required information from feedbacks file using user_id:
            user_feedbacks = self.file.select_data(class_name= 'Feedback', 
                                                   coloumns= ["movie_id", "rating", "comment", "timestamp"], 
                                                   where= {'user_id': user_id})
            if user_feedbacks:
                print("\nUser Feedback(s):\n" + "-"*40)
                ## get movie title from movies file associated with movie_id from feedbacks file:
                for fb in user_feedbacks:
                    result = self.file.get_attributes(class_name= "Movie", id_= fb["movie_id"], attrs=["title"])
                    fb["title"] = result["title"]
                    print(f"MovieTitle: {fb['title']}, Time: {fb['timestamp']}, Rating: {fb['rating']}, Comment: {fb['comment']}")            
        except FileError as e:
            print(e)


    def view_reservations(self, user_id):
        try:
            if not self.file.is_id('User', user_id):
                print(f"The provided user ID `{user_id}` does not exist!")
                return
            ## get required information from reservations file using user_id:
            user_reservations = self.file.select_data(class_name= 'Reservation',
                                                      coloumns= ["reservation_id", "show_id", "seat_number", "status"],
                                                      where= {'user_id': user_id})
            
            if user_reservations: # user made at least one reservation
                print("\nUser Reservation(s):\n" + "-"*40)
                for rsv in user_reservations:
                    ## get show information from `shows` file associated with `show_id` from `reservations` file:
                    result1 = self.file.get_attributes(class_name= "Show", id_= rsv["show_id"], 
                                                      attrs=["movie_id", "cinemahall_id", "show_date", "show_number", "status"])
                    ## get `cinemahall name` from `cinemahalls` file correspond to `cinemahall_id` from `shows` file
                    result2 = self.file.get_attributes(class_name= "CinemaHall", id_= result1["cinemahall_id"], attrs= ["name"])
                    ## get `movie title` from `movies` file correspond to `movie_id` from `shows` file
                    result3 = self.file.get_attributes(class_name= "Movie", id_= result1["movie_id"], attrs= ["title"])
                    ## insert informations into user_reservation:
                    rsv["show_date"] = result1["show_date"]
                    rsv["show_num"] = result1["show_number"]
                    rsv["show_status"] = result1["status"]
                    rsv["hall_name"] = result2["name"]
                    rsv["title"] = result3["title"]
                    ## print joint information of each reservation:
                    print(f"Res. ID: {rsv['reservation_id']}, Res. Status: {rsv['status']}, MovieTitle:{rsv['title']}, "
                          + f"ShowDate: {rsv['show_date']}, ShowNo.: {rsv['show_num']}, ShowStatus: {rsv['show_status']}, "
                            + f"HallName: {rsv['hall_name']}, SeatNo.: {rsv['seat_number']}")
        except FileError as e:
            print(e)


    def view_upcoming_shows(self):
        upcoming_shows = self.file.select_data(class_name= "Show", 
                                               coloumns= ["show_id", "movie_id", "cinemahall_id", "show_date", "show_number"], 
                                               where= {"status": "Upcoming"})
        if upcoming_shows:
            print("\nList of Upcomming Shows:")
            for show in upcoming_shows:
                ## get `cinemahall name` from `cinemahalls` file correspond to `cinemahall_id` from `shows` file
                show["hall_name"] = self.file.get_attributes(class_name= "CinemaHall", id_= show["cinemahall_id"], attrs= ["name"])["name"]
                ## get `movie title` from `movies` file correspond to `movie_id` from `shows` file
                show["title"] = self.file.get_attributes(class_name= "Movie", id_= show["movie_id"], attrs= ["title"])["title"]
                ## print
                print(f"Show ID: {show['show_id']}, Movie: {show['title']}, Date: {show['show_date']}, " + 
                      f"Show Number: {show['show_number']}, Hall Name: {show['hall_name']}")

