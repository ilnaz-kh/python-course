"""
Final Project: Python OOP
Comprehensive Python course for AI
Cinema Reservation System
"""
from configparser import ConfigParser 
from configparser import Error
from file import File
from user import User
from employee import Employee

def test_func():
    ## Read the directory of data from a config file
    try:
        configur = ConfigParser() 
        configur.read('config.ini')
        DIR_ = configur['Directory']['DATA_DIRECTORY']
    except Error as e:
        print(e.__str__())
        return

    file = File(DIR_)
    user = User(file)
    employee = Employee(file)

    # user.register_user(username= "user1", password= "pass", name= "Ali Ahmadi", phone= '09123456789')
    # user.register_user(username= "user1", password= "pass", name= "Aida Rahnama", phone= "09234567898", email= "ai5@fsg.com") # taken username
    # user.register_user(username= "user2", password= "pass", name= "Aida Rahnama", phone= "09234567898", email= "ai5@fsg.com")
    # user.register_user(username= "user3", password= "pass", name= "Rana Saraei", phone= "09123456789")
    # user.register_user(username= "user4", password= "pass", name= "Ali Mousavi", phone= "09123457678")
    # user.register_user(username= "user5", password= "pass", name= "Bahar", phone= "09161287654", email="34ma@yahoo.com")
    # user.register_user(username= "user6", password= "pass", name= "Taha", phone= "06134562345")
    # user.register_user(username= "user7", password= "pass", name= "Iman", phone= "000") # invalid phone
    # user.register_user(username= "user8", password= "pass", name= "Reza", phone= "09123456789", email= "usda@yahoocom") # invalid email

    # employee.register_employee("Ticket Seller", "Mohsen Borna", "03145678901")
    # employee.register_employee(username= "user1", password="pass1", position= "Ticket Seller", name= "Mohsen Borna", phone= "03145678901") 
    # employee.register_employee(username= "user1", password="pass1", position= "Ticket Seller", name= "Mohsen Borna", phone= "03145678901") # taken username
    # employee.register_employee(username= "user2", password="pass2", position= "Ticket Seller", name= "Hamed Akbari", phone= "09361234567") 

    # employee.add_cinemahall(hall_name= "Rose", total_seats=50)
    # employee.add_cinemahall(hall_name= "Tulip", total_seats=25)
    # employee.view_cinemahalls()

    # employee.add_movie(query="Harry Met Sally")
    # employee.add_movie(query="Forrest Gump")
    # employee.add_movie(query="titanic")
    # employee.add_movie(query="Shawshank Redemption")
    # employee.add_movie(query="Roman Holiday")

    ## Schedule Shows:
    # employee.schedule_show(movie_id= "278", cinemahall_id= "C1112", show_date="2024-01-25", show_number= 1)
    # employee.schedule_show(movie_id= "639", cinemahall_id= "C1111", show_date="2024-01-20", show_number= 2)
    # employee.schedule_show(movie_id= "640", cinemahall_id= "C1111", show_date="2024-01-30", show_number= 3) # Error: invalid movie_id

    ## Make Reservations:
    # user.make_reservation(user_id= "U1111", show_id= "S1111", seat_number= 100) # seat `100` is not valid in this cinema hall!
    # user.make_reservation(user_id= "U2111", show_id= "S1112", seat_number= 3)  # Invalid user ID
    # user.make_reservation(user_id= "U1111", show_id= "S1111", seat_number= 2)
    # user.make_reservation(user_id= "U1111", show_id= "S1112", seat_number= 1)
    # user.make_reservation(user_id= "U1111", show_id= "S1112", seat_number= 2)
    # user.make_reservation(user_id= "U1112", show_id= "S2113", seat_number= 3) # show ID S2113 does not exist
    # user.make_reservation(user_id= "U1112", show_id= "S1112", seat_number= 9)
    # user.make_reservation(user_id= "U1112", show_id= "S1112", seat_number= 10)

    ## Cancel Reservations:
    # user.cancel_reservation(user_id= "U1111", reservation_id= "R1112")
    # user.cancel_reservation(user_id= "U1111", reservation_id= "R1112") # reservation is already cancelled
    # user.cancel_reservation(user_id= "U2111", reservation_id= "R1111") # invalid user_id
    # user.cancel_reservation(user_id= "U1111", reservation_id= "R2111") # reservation ID dose not exist!
    # user.cancel_reservation(user_id= "U1113", reservation_id= "R1112") # reservation does not belong to user `U1113`

    ## Submit Feedbacks
    # user.submit_feedback(user_id= "U1112", movie_id= "639", rating= 4, comment= "I recommend this movie")
    # user.submit_feedback(user_id= "U1112", movie_id= "640", rating= 4) # invalid movie id
    # user.submit_feedback(user_id= "U1113", movie_id= "13", rating= 5, comment= "You absolutely must not miss the extraordinary film featuring the legendary Tom Hanks.")
    # user.submit_feedback(user_id= "U1112", movie_id= "278", rating= 5, comment= "masterfully combines hope, friendship, and resilience in the face of adversity.")
    # user.submit_feedback(user_id= "U1114", movie_id= "639", rating= 7) # Invalid rating

    ## View Profile
    # user.view_profile(user_id= "U1112")
    # user.view_feedbacks(user_id= "U1112")
    # user.view_reservations(user_id= "U1112")

    # user.view_upcoming_shows()

    # employee.change_show_status(show_id= "S1112", new_status= "Finished")
    # user.cancel_reservation(user_id= "U1112", reservation_id= "R1115") # reservation for a finished show_id= "S1112"

    employee.view_shows()

    # user.view_movies()
    # employee.view_movies()

if __name__ == "__main__":
    test_func()
