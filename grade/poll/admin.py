# -*- coding: utf-8 -*-
"""
    Django admin panel for polls
"""

from django.contrib           import admin
from fereol.grade.poll.models import Option, \
                                     OpenQuestionOrdering, \
                                     SingleChoiceQuestionOrdering, \
                                     MultipleChoiceQuestionOrdering, \
                                     SectionOrdering, \
                                     OpenQuestion, \
                                     SingleChoiceQuestion, \
                                     MultipleChoiceQuestion, \
                                     Section, \
                                     Poll, \
                                     SavedTicket, \
                                     OpenQuestionAnswer, \
                                     SingleChoiceQuestionAnswer, \
                                     MultipleChoiceQuestionAnswer

admin.site.register( Option )
admin.site.register( OpenQuestionOrdering )
admin.site.register( SingleChoiceQuestionOrdering )
admin.site.register( MultipleChoiceQuestionOrdering )
admin.site.register( SectionOrdering )
admin.site.register( OpenQuestion )
admin.site.register( SingleChoiceQuestion )
admin.site.register( MultipleChoiceQuestion )
admin.site.register( Section )
admin.site.register( Poll )
admin.site.register( SavedTicket )
admin.site.register( OpenQuestionAnswer )
admin.site.register( SingleChoiceQuestionAnswer )
admin.site.register( MultipleChoiceQuestionAnswer )