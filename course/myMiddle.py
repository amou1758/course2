import datetime

from django.utils.deprecation import MiddlewareMixin

from course.models import Course


class AutoCloseCourse(MiddlewareMixin):
    def process_request(self, request):
        ntime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        courses = Course.objects.filter(course_status=4)
        for course in courses:
            if ntime >= course.course_close_time.strftime("%Y-%m-%d %H:%M:%S"):
                course.course_status = 5
                course.course_online = False
                course.save()
