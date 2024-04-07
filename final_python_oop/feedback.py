from datetime import datetime
from exceptions import FileError, FeedbackError

class Feedback:
    
    def __init__(self, file):
        self.file = file
        

    def create_feedback(self, user_id, movie_id, rating, comment):
        """
        feedback_id: A unique identifier for each feedback entry.
        user_id: The identifier of the user who submitted the feedback.
        movie_id: The identifier of the movie associated with the feedback.
        rating: A numerical value or rating given by the user for the movie.
        comment: A text field where the user can provide additional comments or feedback.
        timestamp: The date and time when the feedback was submitted.
        """
        try:
            self.feedback_validity(user_id, movie_id, rating)
            feedback_id = self.file.create_id('Feedback')
            data_dict = {
                'feedback_id': feedback_id,
                'user_id': user_id,
                'movie_id': movie_id,
                'rating': rating,
                'comment': comment,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            ## save the user's informations to the associated file
            self.file.save_data('Feedback', data_dict)
        except FileError as e:
            raise FeedbackError(e.__str__())
        except FeedbackError as e:
            raise e
        
        
    def feedback_validity(self, user_id, movie_id, rating):
        try:
            if not self.file.is_id('User', user_id):
                raise FeedbackError(f"The requested user ID `{user_id}` dose not exist!")
            if not self.file.is_id('Movie', movie_id):
                raise FeedbackError(f"The requested movie ID `{movie_id}` dose not exist!")
        except FileError as e:
            raise FeedbackError(e.__str__())
        
        if rating not in [0, 1, 2, 3, 4, 5]:
            raise FeedbackError("The rating you provide must be one of the specific numerical values: 0, 1, 2, 3, 4, or 5!")

        
