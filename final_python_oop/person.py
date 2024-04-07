from abc import ABC
from exceptions import EmailInvalidError, PhoneInvalidError, FileError
import re

class Person(ABC):

    @staticmethod
    def email_validity(email):
        """
        A valid email address has four parts:
            * Email prefix
            * @ symbol
            * Domain name
            * Top-level domain

        The email prefix may be 3 up to 64 characters long and consist of:
            * Uppercase and lowercase letters in English (A-Z, a-z)
            * Digits from 0 to 9
            * Special characters such as . ! # $ % & ' * + - / = ? ^ _ ` { | }

        The domain name may 3 up to 20 characters and consist of:
            * Uppercase and lowercase letters in English (A-Z, a-z)
            * Digits from 0 to 9 
            * A hyphen (-)
            * A period (.)  (used to identify a sub-domain; for example,  email.domainsample)

        Top-level domains are the highest level of the domain name system for the Internet and is placed after the domain name in an email address.
        Common top-level domains are:
            .com
            .net
            .org
        """
        pattern = "[A-Za-z0-9.!#$%&'*+/=?^_`{|}-]{3,64}@[A-Za-z0-9.-]{3,20}\.[A-Z|a-z]{2,7}"
        if email and not re.fullmatch(pattern=pattern, string=email):
            raise EmailInvalidError("The specified email is not valid!")

    
    @staticmethod
    def phone_validity(phone):
        """
        The phone number pattern follows a specific rule, which requires it to consist of 11 digits and begin with the digit 0.
        the second digit cannot be zero.
        """
        pattern = "0[1-9]{1}[0-9]{9}"
        if not re.fullmatch(pattern=pattern, string=phone):
            raise PhoneInvalidError("The specified phone number is not valid!")
        
    def view_movies(self):
        try:
            movies = self.file.select_data(class_name= "Movie", 
                                                coloumns= ["movie_id", "title", "original_language", "genres", "runtime", "vote_average", "vote_count", "release_date"], 
                                                where= {})
            if movies:
                print("\nMovies' Informaion:\n" + "-"*40)
                for movie in movies:
                    print(f"Movie ID: {movie['movie_id']}, Title: {movie['title']}, Language: {movie['original_language']}, Genre: {movie['genres']}, " + 
                          f"RunTime: {movie['runtime']}, VoteAVG: {movie['vote_average']}, VoteCount: {movie['vote_count']}, ReleaseDate: {movie['release_date']}")
        except FileError as e:
            print(e.__str__())
    

if __name__ == "__main__":
    try:
        Person.email_validity("f.26A@yahoo.com")
        Person.email_validity("fA@yahoo.com") # print Error
    except:
        print("Invalid Email")

    try:
        Person.phone_validity("09123456570") # True
        Person.phone_validity("03134565765") # True
        Person.phone_validity("+9123456570") # print Error
    except:
        print("Invalid Phone")

    try:
        Person.phone_validity("9123456570") # print Error
    except:
        print("Invalid Phone")

    try:
        Person.phone_validity("0912345657") # print Error
    except:
        print("Invalid Phone")

    try:
        Person.phone_validity("091234565702") # print Error
    except:
        print("Invalid Phone")

    try:
        Person.phone_validity("00134565765") # print Error
    except:
        print("Invalid Phone")
    