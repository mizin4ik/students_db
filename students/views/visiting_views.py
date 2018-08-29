# -*- coding: utf-8 -*-

from django.shortcuts import render


# Views for Students

def visitor_list(request):
    visitors = (
        {
            'id': 1,
            'student_visitor': {'id': 1, 'name': u'Кіт Вікторія'},
            'days': [
                True, False, True, True, True, True, True,
                True, True, True, True, True, True, True, True,
                True, False, True, True, True, True, True, True,
                True, True, True, True, True, True, False
            ]
        },
        {
            'id': 2,
            'student_visitor': {'id': 2, 'name': u'Нельсон Софія'},
            'days': [
                False, False, False, True, False, True, True, True,
                True, True, True, True, True, True, True, True,
                True, False, True, True, True, True, True, True,
                True, True, True, True, True, True
            ]
        },
        {
            'id': 3,
            'student_visitor': {'id': 3, 'name': u'Іванишин Клава'},
            'days': [
                True, True, False, False, False, True, False, True, True, True,
                True, True, True, True, True, True, True, True,
                True, False, True, True, True, True, True,
                True, True, True, True, True
            ]
        },
    )
    return render(request, 'students/visiting.html', {'visitors': visitors})
