# -*- coding: utf8 -*-
from sys       import maxint
from django.db import models

from open_question            import OpenQuestionOrdering
from single_choice_question   import SingleChoiceQuestionOrdering
from multiple_choice_question import MultipleChoiceQuestionOrdering
from fereol.grade.poll.utils  import ordering_cmp
                        
class Section( models.Model ):
    title       = models.CharField( max_length = 50,  verbose_name = 'tytuł' )
    description = models.TextField( blank = True, verbose_name = 'opis' ) 
    poll        = models.ManyToManyField( 'Poll', verbose_name = 'ankieta',
                                          through = 'SectionOrdering' )
    
    class Meta:
        verbose_name        = 'sekcja'
        verbose_name_plural = 'sekcje'
        app_label           = 'poll'
        
    def __unicode__( self ):
        return unicode( self.title )
        
    def all_questions( self ):
        open            = OpenQuestionOrdering.objects.filter( sections = self )
        single_choice   = SingleChoiceQuestionOrdering.objects.filter( sections = self )
        multiple_choice = MultipleChoiceQuestionOrdering.objects.filter( sections = self )
        
        orderings = list( open ) + list( single_choice ) + list( multiple_choice )
        orderings.sort( ordering_cmp )
        return map( lambda o: o.question, orderings )
        
class SectionOrdering( models.Model ):
    poll     = models.ForeignKey( 'Poll',      verbose_name = 'ankieta' )
    section  = models.ForeignKey( Section, verbose_name = 'sekcja' )
    position = models.IntegerField( verbose_name = 'pozycja' )

    class Meta:
        verbose_name_plural = 'pozycje sekcji'
        verbose_name        = 'pozycja sekcji'
        ordering            = [ 'poll', 'position' ]
        unique_together     = [ 'poll', 'position' ]
        app_label           = 'poll'
        
    def __unicode__( self ):
        return unicode( self.position ) + u'[' + unicode( self.poll ) + u']' + unicode( self.section )