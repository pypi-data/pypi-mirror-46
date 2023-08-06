"""DNS class file."""

import re
import sys
import urllib
import yaml


class DNS(object):
    """DNS class."""

    def __init__(
            self,
            mhl=None,
            config='http://storage.googleapis.com/broad-hosts/configs/dns.yaml',
            verbose=False):
        """Initialize the object."""
        self.mhl = mhl
        self.settings = self.get_settings(config)
        self.verbose = verbose

        self.default_ttl = 21600

    def get_resource_records(self):
        """Return a list of all resource records from master.host.listing."""
        records = self.get_host_records()
        records += self.get_cname_records()
        records += self.get_mx_records()
        records += self.get_ns_records()
        records += self.get_additional_records()
        return records

    def get_additional_records(self):
        """Get additional resource records."""
        domain = 'broadinstitute.org-external'
        settings = self.settings[domain]

        records = []
        for key in settings:
            record = self.settings['defaults'][key]
            ttl = record.get('ttl', '')
            record['ttl'] = self.get_ttl(ttl=ttl)
            if 'signatureRrdatas' not in record:
                record['signatureRrdatas'] = []
            records.append(record)
        return records

    def get_cname_records(self):
        """Get cname resource records."""
        records = []
        if not self.mhl:
            return
        cnames = self.mhl.mhlfile.cnames
        for hostname in cnames:
            cname = cnames[hostname]
            hostname = '%s.broadinstitute.org.' % (hostname)
            ttl = self.get_ttl(cname)

            target = cname.target
            if re.search(r'\.', target):
                target = '%s.' % (target)

            record = {
                'kind': 'dns#resourceRecordSet',
                'name': hostname,
                'rrdatas': [target],
                'signatureRrdatas': [],
                'ttl': ttl,
                'type': 'CNAME',
            }
            records.append(record)
        return records

    def get_host_records(self):
        """Get host resource records."""
        records = []
        round_robins = {}
        if not self.mhl:
            return
        hosts = self.mhl.mhlfile.hosts
        for hostname in hosts:
            host = hosts[hostname]

            # skip dnsskip hosts
            if 'dnsskip' in host.tags:
                continue

            # skip netapps
            if host.hosttype in ['netapp']:
                continue

            # skip hosts with internal IPs
            if re.match(r'^(192\.168\.|10\.|172\.)', host.ip):
                continue

            hostname = '%s.broadinstitute.org.' % (hostname)
            ttl = self.get_ttl(host)

            # add the host A record
            record = {
                'kind': 'dns#resourceRecordSet',
                'name': hostname,
                'rrdatas': [host.ip],
                'signatureRrdatas': [],
                'ttl': ttl,
                'type': 'A',
            }
            records.append(record)

            # handle round robin records
            if host.round_robin:
                if host.round_robin in round_robins:
                    round_robins[host.round_robin]['rrdatas'].append(host.ip)
                else:
                    round_robin = '%s.broadinstitute.org.' % (host.round_robin)
                    record = {
                        'kind': 'dns#resourceRecordSet',
                        'name': round_robin,
                        'rrdatas': [host.ip],
                        'signatureRrdatas': [],
                        'ttl': ttl,
                        'type': 'A',
                    }
                    round_robins[host.round_robin] = record

            # add cname records
            for cname in host.cnames:
                # skip ldap
                if cname in ['ldap']:
                    continue
                cname = '%s.broadinstitute.org.' % (cname)
                record = {
                    'kind': 'dns#resourceRecordSet',
                    'name': cname,
                    'rrdatas': [hostname],
                    'signatureRrdatas': [],
                    'ttl': ttl,
                    'type': 'CNAME',
                }
                records.append(record)

        # add in the round robin records
        for name in round_robins:
            record = round_robins[name]
            record['rrdatas'] = sorted(record['rrdatas'])
            records.append(record)

        return records

    def get_mx_records(self):
        """Get mx resource records."""
        records = []
        if not self.mhl:
            return
        mxs = self.mhl.mhlfile.mxs
        for hostname in mxs:
            # skip broadinstitute.org. and broad.mit.edu.
            if hostname in ['broad.mit.edu.', 'broadinstitute.org.']:
                continue
            mx = mxs[hostname]
            hostname = '%s.broadinstitute.org.' % (hostname)
            ttl = self.get_ttl(mx)

            targets = []
            for target in mx.targets:
                if not re.search(r'\.', target):
                    target = '%s.broadinstitute.org.' % (target)
                else:
                    target = '%s.' % (target)
                targets.append(target)

            record = {
                'kind': 'dns#resourceRecordSet',
                'name': hostname,
                'rrdatas': targets,
                'signatureRrdatas': [],
                'ttl': ttl,
                'type': 'MX',
            }
            records.append(record)
        return records

    def get_ns_records(self):
        """Get ns resource records."""
        records = []
        if not self.mhl:
            return
        nss = self.mhl.mhlfile.nss
        for hostname in nss:
            ns = nss[hostname]
            hostname = '%s.broadinstitute.org.' % (hostname)
            ttl = self.get_ttl(ns)

            targets = []
            for target in ns.targets:
                if not re.search(r'\.', target):
                    target = '%s.broadinstitute.org.' % (target)
                else:
                    target = '%s.' % (target)
                targets.append(target)
            # targets = ns.targets

            record = {
                'kind': 'dns#resourceRecordSet',
                'name': hostname,
                'rrdatas': targets,
                'signatureRrdatas': [],
                'ttl': ttl,
                'type': 'NS',
            }
            records.append(record)
        return records

    def get_settings(self, url):
        """Get DNS settings from YAML file."""
        # get config from url
        try:
            f = urllib.urlopen(url)
        except Exception as e:
            print('ERROR: Failed to get settings: %s' % (url))
            print(e)
            sys.exit(1)
        # parse config
        try:
            settings = yaml.load(f, Loader=yaml.Loader)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)
        return settings

    def get_ttl(self, entry=None, ttl=''):
        """Return the ttl in seconds."""
        if entry:
            # get ttl from entry
            ttl = entry.ttl
        else:
            ttl = str(ttl)

        ttl = ttl.lower().replace('-', '')

        # if not set, use default
        if not ttl:
            ttl = self.default_ttl

        # if it's just numbers, then return as an int
        elif not re.search('[^0-9]', ttl):
            ttl = int(ttl)

        # seconds * 1
        elif re.search('s$', ttl):
            ttl = int(ttl.replace('s', ''))

        # minutes * 60
        elif re.search('m$', ttl):
            ttl = int(ttl.replace('m', '')) * 60

        # hours * 3600
        elif re.search('h$', ttl):
            ttl = int(ttl.replace('h', '')) * 3600

        # days * 86400
        elif re.search('d$', ttl):
            ttl = int(ttl.replace('h', '')) * 86400

        # weeks * 604800
        elif re.search('w$', ttl):
            ttl = int(ttl.replace('h', '')) * 604800

        # error
        else:
            print('ERROR: Invalid TTL: %s' % (ttl))

        return ttl
