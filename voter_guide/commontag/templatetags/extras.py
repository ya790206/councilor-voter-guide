# -*- coding: utf-8 -*-
import re
import json
from django.core.serializers.json import DjangoJSONEncoder
from django import template
from django.utils.safestring import mark_safe
from councilors.models import CouncilorsDetail
from bills.models import Bills


register = template.Library()

@register.filter(name='each_county_remark')
def each_county_remark(value):
    maps = {
        u'桃園市': [
            u'找不到議案的資料來源，歡迎一起幫忙找，<a href="http://www.tycc.gov.tw/">議會官網</a>',
            u'出缺席紀錄處理中',
        ],
        u'新北市': [
            u'新北市議會出缺席為2012-09-05到現在的紀錄，2012-09-05之前的會議紀錄找不到記名的出缺席名單，<a href="http://www.ntp.gov.tw/content/information/information04.aspx">詳見議會官網</a>',
        ],
        u'臺中市': [
            u'臺中市議會除了第一次會議，其餘紀錄找不到記名的出缺席名單，<a href="http://www.tccc.gov.tw/govknowledge/know_docview.asp?id={A3251160-17E2-4B5B-9F99-1A985453159A}&wfid=23&info=1837">詳見議會官網</a>',
        ],
    }
    return '<br>'.join(maps.get(value, ''))

@register.filter(name='suggestions_offical_link')
def suggestions_offical_link(value):
    maps = {
        u'臺北市': 'http://www.dbas.taipei.gov.tw/ct.asp?xItem=69201832&ctNode=31636&mp=120001',
        u'高雄市': 'http://dbaskmg.kcg.gov.tw/business3.php?type=128',
        u'新竹市': 'http://dep-auditing.hccg.gov.tw/web/SG?pageID=27404&FP=42985',
    }
    return maps.get(value, '')

@register.filter(name='distinct_district')
def distinct_district(value, arg):
    return CouncilorsDetail.objects.filter(county=value, election_year=arg).exclude(district='').values_list('district', flat=True).distinct()

@register.filter(name='vote_result')
def vote_result(value, arg):
    attribute = {
        'Passed': {
            'td_bgcolor': u'CCFF99',
            'cht': u'通過'
        },
        'Not Passed': {
            'td_bgcolor': u'FF99CC',
            'cht': u'不通過'
        }
    }
    if attribute.get(value):
        return attribute.get(value).get(arg)

@register.filter(name='election_year_range')
def election_year_range(value):
    election_years = ['1969', '1973', '1977', '1981', '1985', '1989', '1994', '1998', '2002', '2006', '2010', '2014', '2018']
    for i in range(0, len(election_years)):
        if election_years[i] == value:
            return '%s~%s' % (value, election_years[i+1])
    election_years = ['2009', '2014', '2018']
    for i in range(0, len(election_years)):
        if election_years[i] == value:
            return '%s~%s' % (value, election_years[i+1])

@register.filter(name='mod')
def mod(value, arg):
    return value % arg

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='multiply')
def subtract(value, arg):
    return value * arg

@register.filter(name='percentage')
def percentage(value, arg):
    if arg:
        try:
            return "{0:.1f}".format(value * 100.0 / arg)
        except Exception, e:
            print e
    else:
        return 0

@register.filter(name='divide')
def divide(value, arg):
    if arg:
        try:
            return "{0:.2f}".format(value / arg)
        except Exception, e:
            print e
    else:
        return 0

@register.filter(name='as_json')
def as_json(data):
    return mark_safe(json.dumps(data, cls=DjangoJSONEncoder))

@register.filter(name='replace')
def replace(value, arg):
    if arg:
        for word in arg.split():
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            value = pattern.sub('<font style="background-color: #FFFF66;">'+word+'</font>', value)
        return value
    else:
        return value
