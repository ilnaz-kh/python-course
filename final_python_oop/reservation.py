from datetime import datetime
from exceptions import FileError, ReservationError, ShowError
from show import Show

class Reservation:
    def __init__(self, file):
        self.file = file
        

    def save_reservtion(self, user_id, show_id, seat_number):
        """
        - reservation_id: A unique identifier for each reservation.
        - user_id: The ID of the user who made the reservation.
        - show_id: The ID of the show for which the reservation is made.
        - reservation_date: The date and time when the reservation was made.
        - cancel_date: The date and time when the reservation was cancelled.
        - seat_number: The seat number or seat identifier for the reservation.
        - status: The status of the reservation (e.g., confirmed, cancelled).
        """
        try:
            self.reservation_validity(user_id, show_id, seat_number)
            ## Update occupied seats in shows:
            Show(self.file).set_occupied_seats(show_id, seat_number)
        except ReservationError as e:
            raise e
        except ShowError as e:
            raise ReservationError(e.__str__())
        else:
            ## create unique reservation_id
            reservation_id = self.file.create_id("Reservation")
            data_dict = {
                'reservation_id': reservation_id,
                'user_id': user_id,
                'show_id': show_id,
                'seat_number': seat_number,
                'reservation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'cancel_date' : None,
                'status': "confirmed" # options: "confirmed", "cancelled"
            }
            ## save the reservation's informations to the associated file
            self.file.save_data('Reservation', data_dict)


    def reservation_validity(self, user_id, show_id, seat_number):
        ## Check validity of user_id and show_id
        try:
            if not self.file.is_id('User', user_id):
                raise ReservationError(f"The requested user ID `{user_id}` dose not exist!")
            if not self.file.is_id('Show', show_id):
                raise ReservationError(f"The requested show ID `{show_id}` dose not exist!")
        except FileError as e:
            raise ReservationError(e.__str__())
        
        ## Check validity of seat_number
        try:
            results = self.file.get_attributes('Show', show_id, ["cinemahall_id", "occupied_seats"])
            hall_id = results["cinemahall_id"]
            occupied_seats = results["occupied_seats"] 
            total_seats = self.file.get_attributes('CinemaHall', hall_id, ["total_seats"])["total_seats"]
        except FileError as e:
            raise ReservationError(e.__str__())
        
        if seat_number in occupied_seats:
            raise ReservationError(f"The requested seat `{seat_number}` is taken!")           
        if seat_number < 1 or seat_number > total_seats:
            raise ReservationError(f"The requested seat `{seat_number}` is not valid in this cinema hall!")
        

    ## cancel the reservation.
    def cancel_reservation(self, user_id, reserervation_id):
        ## Check validity of user_id and reservation_id
        try:
            if not self.file.is_id('User', user_id):
                raise ReservationError(f"The requested user ID `{user_id}` dose not exist!")
            if not self.file.is_id('Reservation', reserervation_id):
                raise ReservationError(f"The requested reservation ID `{reserervation_id}` dose not exist!")
        except FileError as e:
            raise ReservationError(e.__str__())

        try:
            results = self.file.get_attributes('Reservation', reserervation_id, ["user_id", "status", "seat_number", "show_id"])
        except FileError as e:
            raise ReservationError(e.__str__())
        
        id_ = results["user_id"]
        status = results["status"]
        seat_num = results["seat_number"]
        show_id = results["show_id"]
        if id_ != user_id:
            raise ReservationError(f"This reservation `{reserervation_id}` does not belong to user `{user_id}`!")
        if status == "cancelled":
            raise ReservationError(f"This reservation is already cancelled!")
        
        try:
            show_status = self.file.get_attributes("Show", show_id, ["status"])["status"]
        except FileError as e:
            raise ReservationError(e.__str__())
        if show_status == "Finished" or show_status == "Postponed":
            raise ReservationError(f"A {show_status} show cannot be cancelled!")
        
        try:
            ## Update Reservation.status and Reservation.cancel_date
            c_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.file.set_attributes('Reservation', reserervation_id, {"status": "cancelled", "cancel_date": c_date})
            ## Update Show.occupied_seats
            result = self.file.get_attributes("Show", show_id, ["occupied_seats"])
            occupied_seats = result["occupied_seats"]
            occupied_seats.remove(seat_num)
            self.file.set_attributes("Show", show_id, {"occupied_seats": occupied_seats})
        except FileError as e:
            raise ReservationError(e.__str__())
        