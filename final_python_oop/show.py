from datetime import datetime, date, timedelta
from exceptions import ShowError, FileError

class Show:

    def __init__(self, file):
        self.file = file
        
    
    def save_show(self, movie_id, cinemahall_id, show_date, show_number):
        try:
            self.show_validity(movie_id, cinemahall_id, show_date, show_number)
        except ShowError as e:
            raise e
        try:
            ## create unique show_id
            show_id = self.file.create_id('Show')
            data_dict = {
                'show_id': show_id,
                'movie_id': movie_id,
                'cinemahall_id': cinemahall_id,
                'show_date': show_date,
                'show_number': show_number,
                'status': 'Upcoming',
                'occupied_seats': [],
            }   
            ## save the show's informations to the associated file
            self.file.save_data('Show', data_dict)
        except FileError as e:
            raise ShowError(e.__str__())


    def show_validity(self, movie_id, cinemahall_id, show_date, show_number):
        ## Check validity of movie_id and cinemahall_id
        try: 
            if not self.file.is_id('Movie', movie_id):
                raise ShowError(f"The requested movie ID `{movie_id}` does not exist!")
            if not self.file.is_id('CinemaHall', cinemahall_id):
                raise ShowError(f"The requested cinema hall ID `{cinemahall_id}` does not exist!")
        except FileError as e:
            raise ShowError(e.__str__())
        ## Check validity of date and showing number
        try:
            show_date_obj = datetime.strptime(show_date, "%Y-%m-%d").date()
        except ValueError as e: # time data does not match format '%Y-%m-%d'
            raise ShowError(e.__str__())
        if show_date_obj < date.today():
            raise ShowError("The requested day for the show has already passed!")
        if show_date_obj > date.today() + timedelta(days=10):
            raise ShowError("You have the option to arrange a show within the upcoming ten days!")
        if show_number not in [1, 2, 3, 4]:
            raise ShowError("You are required to select one of the valid screenings: 1 2 3 4") # available

        ## Verify the validity of the show date, number, and cinema hall ID together
        ## load data of shows:
        shows_data = self.file.load_data('Show')
        for show in shows_data.values():
            if show["show_date"] == show_date and show["show_number"] == show_number:
                result = self.file.get_attributes('Movie', show["movie_id"], ["title"])
                title = result["title"]
                raise ShowError(f"The requested date for the screening has already been scheduled for the movie `{title}`.")
            

    def set_occupied_seats(self, show_id, seat_number):
        try:
            occupied_seats = self.file.get_attributes("Show", show_id, ["occupied_seats"])["occupied_seats"]
            occupied_seats.append(seat_number)
            self.file.set_attributes("Show", show_id, {"occupied_seats": occupied_seats})
        except FileError as e:
            raise ShowError(e.__str__())
        
        
    def update_show(self, show_id, new_status):
        valid_statuses = ["Upcoming", "Finished", "Postponed"]
        try:
            if not self.file.is_id('Show', show_id):
                raise ShowError(f"The requested show ID `{show_id}` dose not exist!")
            if new_status not in valid_statuses:
                raise ShowError(f"You should select one of the following options for status: 'Upcoming', 'Finished' or 'Postponed'")
            self.file.set_attributes("Show", show_id, {"status": new_status})
        except FileError as e:
            raise ShowError(e.__str__())
