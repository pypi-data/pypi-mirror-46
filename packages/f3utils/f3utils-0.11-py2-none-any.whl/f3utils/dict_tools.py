# -*- encoding: utf-8 -*-
# Copyright P. Christeas <xrg@pefnos.com> 2008-2019
# Copyright 2010 OpenERP SA. http://www.openerp.com
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###############################################################################

#.apidoc title: dict_tools - Helpers for dict() manipulations

from __future__ import absolute_import
from copy import deepcopy


def dict_merge(*dicts):
    """ Return a dict with all values of dicts
    """
    res = {}
    for d in dicts:
        res.update(d)
    return res

def dict_merge2(*dicts):
    """ Return a dict with all values of dicts.
        If some key appears twice and contains iterable objects, the values
        are merged (instead of overwritten).
    """
    res = {}
    for d in dicts:
        for k in d.keys():
            if k in res and isinstance(res[k], (list, tuple)):
                res[k] = res[k] + d[k]
            elif k in res and isinstance(res[k], dict):
                res[k].update(d[k])
            else:
                res[k] = d[k]
    return res

def dict_filter(srcdic, keys, res=None):
    ''' Return a copy of srcdic that has only keys set.
    If any of keys are missing from srcdic, the result won't have them, 
    either.
    @param res If given, result will be updated there, instead of a new dict.
    '''
    if res is None:
        res = {}
    for k in keys:
        if k in srcdic:
            res[k] = srcdic[k]
    return res


def merge_dict(d1, d2, copy=True):
    """Full (deep) merge of two dicts
    
        A newer implementation over `dict_merge2()` , ensuring that any
        updated sub-containers are properly copied.
    """
    if copy:
        d1 = deepcopy(d1)
    
    for k, v in d2.items():
        if k in d1:
            if v is None:
                del d1[k]
            elif isinstance(v, dict) and isinstance(d1[k], dict):
                merge_dict(d1[k], v, copy=False)
            elif isinstance(v, (list, tuple)):
                if isinstance(d1[k], list):
                    d1[k].extend(deepcopy(v))
                elif isinstance(d1[k], tuple):
                    d1[k] = d1[k] + tuple(deepcopy(v))
                else:
                    raise TypeError("Cannot merge list to %s" % type(d1[k]))
            else:
                d1[k] = deepcopy(v)
        else:
            d1[k] = deepcopy(v)

    return d1

#eof
