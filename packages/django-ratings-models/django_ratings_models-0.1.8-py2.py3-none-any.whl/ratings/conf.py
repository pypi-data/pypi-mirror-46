# -*- coding: utf-8 -*-
"""
License boilerplate should be used here.
"""
# python 3 imports
from __future__ import absolute_import, unicode_literals

# python imports
import logging

# 3rd. libraries imports
from appconf import AppConf

# django imports
from django.conf import settings  # noqa

logger = logging.getLogger(__name__)


class RatingsConfig(AppConf):
    TICKET_MANAGEMENT_ADVISOR = 'ticket-management-advisor'
    TICKET_MANAGEMENT_USER = 'ticket-management-user'
    TICKET_ADVISOR = 'ticket-advisor'
    ANSWER_ADVISOR = 'answer-advisor'
    STEP_FEEDBACK = 'step-feedback'

    CATEGORIES = (
        (TICKET_MANAGEMENT_ADVISOR, 'Ticket Management - Advisor'),
        (TICKET_MANAGEMENT_USER, 'Ticket Management - User'),
        (TICKET_ADVISOR, 'Advisor in ticket'),
        (ANSWER_ADVISOR, 'Advisor in questions'),
        (STEP_FEEDBACK, 'Step Feedback'),
    )

    CH_STATUS_RATING = 'R'
    CH_STATUS_PENDING = 'P'
    CH_STATUS_NOT_RATING = 'N'
    CH_STATUS_SKIPPED = 'S'
