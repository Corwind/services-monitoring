from django.shortcuts import render
from urllib import request as rq
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.template.defaulttags import register

from .models import Machine
import json

# Create your views here.

def index(request):
    results = {}
    passwd_mgr = rq.HTTPPasswordMgrWithDefaultRealm()
    machines = Machine.objects.all()
    for m in machines:
        if m.machine_http_username and m.machine_http_password:
            if not m.machine_address.startswith('http://'):
                url = 'http://' + m.machine_address + ":{}".format(m.machine_port) + '/query'
            else:
                url = m.machine_address + ":{}".format(m.machine_port) + '/query'
            passwd_mgr.add_password(None, url + "/query",
                    m.machine_http_username, m.machine_http_password)
    handler = rq.HTTPBasicAuthHandler(passwd_mgr)
    opener = rq.build_opener(handler)
    for m in machines:
        if not m.machine_address.startswith('http://'):
            url = 'http://' + m.machine_address + ":{}".format(m.machine_port) + '/query'
        else:
            url = m.machine_address + ":{}".format(m.machine_port) + '/query'
        try:
            response = opener.open(url)
            body = response.read().decode('utf-8')
            print(type(body))
            body = json.loads(body)
            print(type(body))
        except Exception as e:
            body = {"Can't connect to {}".format(m.machine_name): ["URL: {}\
            not responding".format(url)]}
        results[m.machine_name] = body
    template = loader.get_template("homepage/index.html")
    return HttpResponse(template.render({'results': results}))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
