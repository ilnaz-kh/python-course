from configparser import ConfigParser 
from configparser import Error
from file import File
from user import User
from employee import Employee

def user_interface():
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

    msg1 = """
    \nSelect your role in Cinema Ticket Reservation system (1, 2, 3 or anything else to exit):
    1. User
    2. Employee
    3. Register as a User
    press anything else to Exit
    """
    msg2= """
    \nSelect your option

    User Options:
    ----------------------------------------------------------------------
    1. View User's General Information
    2. View Users's Reservations
    3. View User's Feedbacks
    4. View User's Profile (Info, Reservations and Feedbacks)
    5. View Upcomming Shows
    6. View Movies
    7. Make a Reservation
    8. Cancel a Reservation
    9. Submit a Feedback
    10. Exit

"""
    msg3 = """
    \nSelect your option

    Employee Options:
    ----------------------------------------------------------------------
    1. View All Shows (Upcomming, Finished or Postponed)
    2. View Movies
    3. View Cinema Halls
    4. Schedule a Show
    5. Update the Status of a Show
    6. Add a Movie
    7. Add Cinema Hall
    8. Exit

"""
    while True:
        cmd = input(msg1)

        ## User
        if cmd == "1":
            ## get username and password
            username = input("Username: ")
            password = input("Password: ")
            user_id = user.user_login(username= username, password= password)
            if user_id: # The user is successfully login
                while True:
                    cmd = input(msg2)
                    ## View User's General Information
                    if cmd == "1":
                        user.view_info(user_id=user_id)
                    ## View Users's Reservations
                    elif cmd == "2":
                        user.view_reservations(user_id= user_id)
                    ## View User's Feedbacks
                    elif cmd == "3":
                        user.view_feedbacks(user_id= user_id)
                    ## View User's Profile (Info, Reservations and Feedbacks)
                    elif cmd == "4":
                        user.view_profile(user_id= user_id)
                    ## View Upcomming Shows
                    elif cmd == "5":
                        user.view_upcoming_shows()
                    ## View Movies
                    elif cmd == "6":
                        user.view_movies()
                    ## Make a Reservation
                    elif cmd == "7":
                        show_id = input("Please enter the show ID to reserve: ")
                        try:
                            seat_num = int(input("Please enter a seat number to reserve: "))
                        except Exception as e:
                            print("Please enter a numerical value only for the seat number!")
                        else:
                            user.make_reservation(user_id= user_id, show_id=show_id, seat_number=seat_num)
                    ## Cancel a Reservation
                    elif cmd == "8":
                        res_id = input("Please enter your reservation ID to cancel: ")
                        user.cancel_reservation(user_id=user_id, reservation_id= res_id)
                    ## Submit a Feedback
                    elif cmd == "9":
                        m_id = input("Please enter the movie ID to submit a feedback: ")
                        try:
                            rating = int(input("enter rating [0, 1, 2, 3, 4, 5]: "))
                        except Exception as e:
                            print("You must enter a numerical value as a rating")
                        else:
                            comment = input("Your comment for this movie: ")
                            user.submit_feedback(user_id= user_id, movie_id= m_id, rating= rating, comment= comment)
                    ## Exit
                    elif cmd == "10":
                        break
                    else:
                        print("Please Enter a Valid Option")

        ## Employee
        elif cmd == "2":
            ## get username and password
            username = input("Username: ")
            password = input("Password: ")
            employee_id = employee.employee_login(username= username, password= password)
            if employee_id: # The employee is successfully login
                while True:
                    cmd = input(msg3)
                    ##  View All Shows (Upcomming, Finished or Postponed)
                    if cmd == "1":
                        employee.view_shows()
                    ## View Movies
                    elif cmd == "2":
                        employee.view_movies()
                    ## View Cinema Halls
                    elif cmd == "3":
                        employee.view_cinemahalls()
                    ## Schedule a Show
                    elif cmd == "4":
                        m_id = input("To schedule a show, please provide the movie ID.: ")
                        hall_id = input("Please provide the Cinema Hall ID in order to schedule a show: ")
                        show_d = input("Please enter the date of the show in the format of YYYY-MM-DD : ")
                        try:
                            show_num = int(input("Please select the screening for the show by entering one of the following options: 1, 2, 3, or 4 : "))
                        except Exception as e:
                            print("Please provide a numerical value only")
                        else:
                            employee.schedule_show(movie_id= m_id, cinemahall_id= hall_id, show_date= show_d, show_number= show_num)
                    ## Update the Status of a Show
                    elif cmd == "5":
                        show_id = input("Please enter the show ID for which you would like to change the status: ")
                        new_status = input("Please enter the new status for the show from the available options: `Upcoming`, `Postponed`, or `Finished` :")
                        employee.change_show_status(show_id= show_id, new_status= new_status)
                    ## Add a Movie
                    elif cmd == "6":
                        query = input("Please input either a portion or the complete title of a movie in order to retrieve its information and store it: ")
                        employee.add_movie(query= query)
                    ## Add Cinema Hall
                    elif cmd == "7":
                        name = input("Please enter the name of new cinema hall: ")
                        try:
                            seats_num = int(input(f"Please provide the number of seats available in the cinema hall named `{name}`"))
                        except Exception as e:
                            print("Please provide a numerical value only as number of seats!")
                        else:
                            employee.add_cinemahall(hall_name= name, total_seats= seats_num)
                    ## Exit
                    elif cmd == "8":
                        break
                    else:
                        print("Please Enter a Valid Option")
        ## Register as a User                
        elif cmd == "3":         
            username = input("Username: ")
            if user.unique_username_check(username= username):
                password = input("Password: ")
                name = input("Name: ")
                phone = input("Please input an 11-digit mobile phone number or a land-line phone number consisting of 11 digits (including the area code): ")
                email = input("Please provide an email address or press enter to proceed: ")
                if email == "":
                    email = None 
                user.register_user(username= username, password= password, name= name, phone= phone, email= email)
        ## Not a User Nor an Employee
        else:
            return


if __name__ == "__main__":
    user_interface()