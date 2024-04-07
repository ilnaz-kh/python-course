from exceptions import CinemahallError, FileError

class CinemaHall:
    def __init__(self, file):
        self.file = file


    def save_cinemahall(self, hall_name, total_seats):
        try: 
            ## create unique cinemahall_id
            cinemahall_id = self.file.create_id("CinemaHall")
            data_dict = {
                'cinemahall_id': cinemahall_id,
                'name' : hall_name,
                'total_seats': total_seats
            }
            ## save the cinema hall's informations to the associated file
            self.file.save_data('CinemaHall', data_dict)
        except FileError as e:
            raise CinemahallError(e.__str__())
      