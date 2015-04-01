from django.db import models


class Lecturer(models.Model):
    """
    This class stores the information about one lecturer
    first_name  is the field which stores the first name
    last_name   is the field which stores the last name
    pk          is created automatically as the primary key
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        """
        Convert the Lecturer Name to a human readable string
        :return: Returns the full name of the lecturer
        """
        return "{0} {1}".format(self.first_name, self.last_name)


class Course(models.Model):
    """
    This class stores the information about one course
    course_title    is the field which stores the title of a course
    vote            is the number of votes a course got
    lecturer        refers to the Lecturer model and identifies the lecturer responsible for the course
    pk              is created automatically as the primary key
    """
    course_title = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    lecturer = models.ForeignKey(Lecturer)

    def __str__(self):
        """
        Convert a Course Model to a human readable string
        :return: Returns the title of the course
        """
        return self.course_title

    def is_great_course(self):
        """
        Figures out if a course is great or not.
        Great courses have more than 100 positive votes
        :return: True if votes > 100, Fales otherwise
        """
        return self.votes > 100