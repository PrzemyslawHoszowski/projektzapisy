# -*- coding: utf8 -*-
from django.db      import models

from base_question  import BaseQuestion
from saved_ticket   import SavedTicket

class OpenQuestion( BaseQuestion ):
    sections = models.ManyToManyField( 'Section',    
                                       verbose_name = 'sekcje', 
                                       through = 'OpenQuestionOrdering' )
    class Meta:
        abstract            = False
        verbose_name        = 'pytanie otwarte'
        verbose_name_plural = 'pytania otwarte'
        app_label           = 'poll'
    
    def get_all_answers_from_poll( self, poll, section ):
        sts = SavedTicket.objects.filter( poll = poll, finished = True )
        result = []
        for st in sts:
            result += st.openquestionanswer_set.filter( section = section )
        return result

class OpenQuestionOrdering( models.Model ):
    question = models.ForeignKey( OpenQuestion, verbose_name = 'pytanie' )
    sections = models.ForeignKey( 'Section', verbose_name = 'sekcja' )
    position = models.IntegerField( verbose_name = 'pozycja' )

    class Meta:
        verbose_name_plural = 'pozycje pytań otwartych'
        verbose_name        = 'pozycja pytań otwartych'
        ordering            = [ 'sections', 'position' ]
        unique_together     = [ 'sections', 'position' ]
        app_label           = 'poll' 
    
    def __unicode__( self ):
        return unicode( self.position ) + u'[' + unicode( self.sections ) + u']' + unicode( self.question )
        