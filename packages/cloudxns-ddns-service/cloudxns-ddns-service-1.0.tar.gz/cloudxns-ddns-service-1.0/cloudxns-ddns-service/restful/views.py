from django.http import HttpResponse
from .api import Api

try:
    import json
except ImportError:
    import simplejson as json


# Create your views here.
# http://username:password@dynupdate.no-ip.com/nic/update?hostname=mytest.testdomain.com&myip=1.2.3.4
def update(request):
    domain = request.GET['domain']
    hostname = request.GET['hostname']
    myip = request.GET['myip']
    print('hostname is :{} , myip is :{}'.format(hostname, myip))
    message = cloudxns(domain, hostname, myip)
    print("-------------" + message + "--------------")
    return HttpResponse(message);


def cloudxns(domain, hostname, ip):
    api_key = '8f598180e8e02104a62559619afae502'
    secret_key = '4ac67a1316e7103b'
    dist_domain = domain
    api = Api(api_key=api_key, secret_key=secret_key)
    result_text = api.domain_list().text
    result = json.loads(result_text)
    if result.get('code') == 1:
        result_datas = result.get('data')
        for result_data in result_datas:
            if result_data.get('domain')[:-1] == dist_domain:
                domain_id = result_data.get('id')
                return cloudxns_host(api, domain_id, hostname, ip)
                break
    return 'can not find domain %s ' % dist_domain


def cloudxns_host(api, domain_id, hostname, ip):
    response = api.host_list(domain_id=domain_id)
    result = json.loads(response.text)
    hosts = result.get('hosts')
    if result.get('code') != 1:
        return 'failed get host list'

    for host in hosts:
        host_id = host.get('id')
        if host.get('host') == hostname:
            record_id = get_record_id(api, domain_id, host_id, hostname, ip)
            if not isinstance(record_id, int):
                return record_id

            rtn = api.record_update(record_id=record_id, domain_id=domain_id, host_name=hostname, value=ip)
            content = json.loads(rtn.content)
            if content.get('code') == 1:
                return 'success update hostname {}  ip = {}'.format(hostname, ip)
            else:
                return 'Update_record action code = {} message = {}'.format(content.get('code'), content.get('message'))
            break

    rtn = api.record_add(domain_id=domain_id, host_name=hostname, value=ip)
    content = json.loads(rtn.content)
    if content.get('code') == 1:
        return 'success add hostname {}  ip = {}'.format(hostname, ip)
    else:
        return 'Add_record action code = {} message = {}'.format(content.get('code'), content.get('message'))

def get_record_id(api,domain_id,host_id, hostname, ip):
    records = json.loads(api.record_list(domain_id, host_id).text).get('data')
    for record in records:
        if record.get('host_id') == host_id:
            if record.get('value') == ip:
                return 'Update_recode is unnecessary update!  hostname = {} ip = {}'.format(hostname, ip)
            return int(record.get('record_id'))
            break
    print('can not find current record_id')
