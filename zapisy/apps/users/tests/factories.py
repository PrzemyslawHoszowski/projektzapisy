# -*- coding: utf-8 -*-

import random

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from ..models import User, Student, UserProfile
import settings

langs = [x[0] for x in settings.LANGUAGES]


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.LazyAttribute(lambda o: o.username)
    is_staff = False
    is_superuser = False


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    matricula = factory.Sequence(lambda n: ('%06d' % n))


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    preferred_language = factory.fuzzy.FuzzyChoice(langs)
    is_employee = random.choice([True, False])
    is_student = factory.LazyAttribute(lambda o: False if o.is_employee else True)
    is_zamawiany = factory.LazyAttribute(
        lambda o: random.choice([True, False]) if o.is_student else False
    )


class StudentProfileFactory(UserProfileFactory):
    is_student = True
    is_employee = False


class EmployeeProfileFactory(UserProfileFactory):
    is_employee = True


class OrderedStudentProfileFactory(UserProfileFactory):
    is_zamawiany = True
    is_employee = False