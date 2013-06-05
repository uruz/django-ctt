#!/usr/bin/env python
#-*- coding: utf-8 -*-
#vim: set ts=4 sw=4 et fdm=marker : */
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TreePathModel(models.Model):
#    ancestor = models.ForeignKey('Node', related_name='tpa')
#    descendant = models.ForeignKey('Node', related_name='tpd')
    path_len = models.IntegerField()

    class Meta:
        unique_together = ('ancestor', 'descendant')
        abstract = True

    def __str__(self):
        return '%s -> %s (%d)' % (self.ancestor, self.descendant, self.path_len)


def register(cls):
    """
    generuje TreePathModel dla podanego modelu
    :param cls:
    :return:
    """
    tpcls = type(str(cls.__name__ + 'TreePath'),
                (TreePathModel,),
                {str('__module__'): cls.__module__})
    ancestor_field = models.ForeignKey(cls, related_name='tpa')
    descendant_field = models.ForeignKey(cls, related_name='tpd')
    ancestor_field.contribute_to_class(tpcls, 'ancestor')
    descendant_field.contribute_to_class(tpcls, 'descendant')
    cls._tpm = tpcls
    cls._cls = cls
    return tpcls
