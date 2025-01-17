from enum import Enum


class NotificationType(str, Enum):
    NOT_PULLED_FROM_QUEUE = 'not_pulled_from_queue'
    PULLED_FROM_QUEUE = 'pulled_from_queue'
    ADDED_NEW_GROUP = 'added_new_group'
    ASSIGNED_TO_NEW_GROUP_AS_A_TEACHER = 'assigned_to_new_group_as_teacher'
    TEACHER_HAS_BEEN_CHANGED_ENROLLED = 'teacher_has_been_changed_enrolled'
    TEACHER_HAS_BEEN_CHANGED_QUEUED = 'teacher_has_been_changed_queued'
    NEWS_HAS_BEEN_ADDED = 'news_has_been_added'
    NEWS_HAS_BEEN_ADDED_HIGH_PRIORITY = 'news_has_been_added_high_priority'
    THESIS_VOTING_HAS_BEEN_ACTIVATED = 'thesis_voting_has_been_activated'
    DEFECT_MODIFIED = 'defect_modified'


mapping = {
    NotificationType.NOT_PULLED_FROM_QUEUE:
    'Proces wciągania Cię do grupy przedmiotu "{course_name}", gdzie prowadzący to {teacher}, a '
    'typ grupy {type}, zakończył się niepowodzeniem. Powód: {reason}.',
    NotificationType.PULLED_FROM_QUEUE:
    'Nastąpiło pomyślne zapisanie Cię do grupy przedmiotu "{course_name}", gdzie prowadzący grupy '
    'to {teacher}, a typ grupy to {type}.',
    NotificationType.ADDED_NEW_GROUP:
    'W przedmiocie "{course_name}" została dodana grupa prowadzona przez {teacher}.',
    NotificationType.ASSIGNED_TO_NEW_GROUP_AS_A_TEACHER:
    'Przydzielono Cię do grupy przedmiotu "{course_name}" jako prowadzącego.',
    NotificationType.TEACHER_HAS_BEEN_CHANGED_ENROLLED:
    'Nastąpiła zmiana prowadzacego w grupie przedmiotu "{course_name}", do której jesteś zapisany/a. '
    'Typ grupy to {type}, a nowy prowadzący to {teacher}.',
    NotificationType.TEACHER_HAS_BEEN_CHANGED_QUEUED:
    'Nastąpiła zmiana prowadzacego w grupie przedmiotu "{course_name}", do której jesteś w kolejce. '
    'Typ grupy to {type}, a nowy prowadzący to {teacher}.',
    NotificationType.NEWS_HAS_BEEN_ADDED:
    "Dodano nową wiadomość w aktualnościach:\n# {title}\n\n{contents}",
    NotificationType.NEWS_HAS_BEEN_ADDED_HIGH_PRIORITY:
    "Dodano nową wiadomość w aktualnościach:\n# {title}\n\n{contents}",
    NotificationType.THESIS_VOTING_HAS_BEEN_ACTIVATED:
    'W pracy dyplomowej "{title}" pojawiła się możliwość głosowania.',
    NotificationType.DEFECT_MODIFIED:
    'Zgłoszona przez Ciebie usterka o nazwie "{defect_name}" została zmodyfikowana.',
}

mapping_title = {
    NotificationType.NOT_PULLED_FROM_QUEUE:
    'Proces wciągania Cię do grupy zakończył się niepowodzeniem',
    NotificationType.PULLED_FROM_QUEUE:
    'Nastąpiło pomyślne zapisanie Cię do grupy przedmiotu "{course_name}"',
    NotificationType.ADDED_NEW_GROUP:
    'W przedmiocie "{course_name}" została dodana grupa',
    NotificationType.ASSIGNED_TO_NEW_GROUP_AS_A_TEACHER:
    'Przydzielono Cię do grupy przedmiotu "{course_name}"',
    NotificationType.TEACHER_HAS_BEEN_CHANGED_ENROLLED:
    'Nastąpiła zmiana prowadzacego w grupie przedmiotu "{course_name}"',
    NotificationType.TEACHER_HAS_BEEN_CHANGED_QUEUED:
    'Nastąpiła zmiana prowadzacego w grupie przedmiotu "{course_name}"',
    NotificationType.NEWS_HAS_BEEN_ADDED:
    "{title}",
    NotificationType.NEWS_HAS_BEEN_ADDED_HIGH_PRIORITY:
    "{title}",
    NotificationType.THESIS_VOTING_HAS_BEEN_ACTIVATED:
    'W pracy dyplomowej "{title}" pojawiła się możliwość głosowania.',
}
