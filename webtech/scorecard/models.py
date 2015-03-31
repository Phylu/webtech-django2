from django.db import models


class Lecturer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        """
        Convert the Lecturer Name to a human readable string
        :return: Returns the full name of the lecturer
        """
        return "%s %s" % (self.first_name, self.last_name)


class Course(models.Model):
    """
    This class stores the information about one course
    course_title    is the field which stores the title of a course
    vote            is the number of votes a course got
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
        return self.votes > 100;