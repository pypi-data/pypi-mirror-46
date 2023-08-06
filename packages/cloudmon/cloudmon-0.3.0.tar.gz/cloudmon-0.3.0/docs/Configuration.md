# Configuration

## Configuration File
After installation CloudMon will create a default configuration file in `/etc/cloudmon/cloudmon.conf` (or if you're using a virtualenv: `[virtualenv_dir]/etc/cloudmon/cloudmon.conf`)

This file should be edited according to your needs.

Configuration rules:
```
###############################################################################
# CloudMon Configuration File
###############################################################################
#
#   This is an example to show how to edit the configuration file.
#
#   Values should be assigned to one field using the equal operator.
#
#   If a field is omitted, its default value will be assigned unless the field
# is required, then CloudMon won't start.
#
#   Multiple assigned values (lists) should be separated by comma, unless the
# comments state otherwise.
#
#   Values: true, t, yes, y, 1, False, f, no, n, 0 (case insensitive) are
# interpreted as booleans.
#
#   Quotes are usually not needed, unless a value starts or ends with
# whitespace, or contains a quote mark or comma, then it should be surrounded
# by quotes.
#
#   Sections are designated by square brackets before and after the section
# name. The number of square brackets represents the nesting level of the
# sub-section.
#
#   One section ends when another section starts. So, it's recommended
# to not change the order of the fields in this file.
#
#   Comments start with a #, possibly preceded by whitespace.
#
#   Multi-line entries can be done using triple quotes.
#       field = '''
#           This is a multi-line entry
#       '''
#
#   Indentation is not significant, but can be preserved.
#
#   Extra files can be included using: +include name_and_path_of_the_file
# The contents of the included file will be added at the place
# where the directive +include was passed.

```


Configuration file example/explanation:
```
# Section to define verification of SSL certificates for https requests.
[ssl]
    # Verify or not https requests to zabbix.
    # Boolean. True to verify, False to not verify. If omitted, assigns: True
    verify_zabbix = True

    # Verify or not https requests to cloudstack.
    # Boolean. True to verify, False to not verify. If omitted, assigns: True
    verify_cloudstack = True

    # Custom path to a CA_BUNDLE file or directory.
    # If ommited, no extra path will be used.
    ca_bundle = /etc/pki/tls/certs/ca-bundle.crt

# Section to define CloudMon Server parameters
[cloudmon]
    # ipv4 that CloudMon will listen. If omitted, assigns: 127.0.0.1
    listen_address = 127.0.0.1

    # port which CloudMon will listen. Required
    listen_port = 5555

    # Select which operations CloudMon will make through the CloudStack API
    # thread. This selection won't interfere with the CloudStack Event Queue
    # thread, which will do all the operations getting data from the queue
    # This field accepts multiple values separeted by comma
    # Accepted values: create, update, delete
    # If omitted, assigns: create, update, delete
    monitor_operations = create, update, delete

    # Caches data from CloudStack and Zabbix with redis.
    # Requires a Redis Server. If omitted, assigns: False
    use_cache = True

# Section to define Zabbix parameters
[cloudstack]
    # Timeout (seconds) for CloudStack HTTP requests. If omitted, assigns: 300
    timeout = 500

# Section to define Zabbix parameters
[zabbix]
    # Zabbix Server (or proxy) ipv4. If omitted, assigns: 127.0.0.1
    zabbix_server = 127.0.0.1

    # Zabbix Server (or proxy) port. REQUIRED
    zabbix_port = 10051

    # Zabbix FrontEnd URL. REQUIRED
    frontend_url = http://localhost

    # Zabbix User. REQUIRED
    zabbix_user = Admin

    # Zabbix Password. REQUIRED
    zabbix_password = zabbix

    # Zabbix Sender path. If omitted, assigns: /usr/bin/zabbix_sender
    zabbix_sender = /usr/bin/zabbix_sender

    # Hostgroup which hosts deleted in CloudStack will be moved to.
    # If this field is commented, hosts will permanently deleted straight away
    deleted_hosts_group = CloudMon Deleted Hosts

    # Look at section proxies first. Boolean. If omitted, assigns: False
    #   True => Hosts might change proxies in order to always maintain the
    # percentage requested at the section proxies
    #   False => Once a host starts being monitored by a given proxy, it will
    # keep being monitored by it. The percentage requested at the section
    # proxies will only count for new hosts
    update_proxy = False

    # Proxy(ies) that will monitor the Cloud Infrastructure
    # Comment this section if you want the node to be monitored by the server
    [[proxies]]
        # Name of the Proxy
        [[[PROXY_A]]]
            # Percentage (int) of nodes that will be monitored
            # by this proxy. REQUIRED
            weight = 65
            # Proxy address:port pair required for sending Zabbix Senders to
            # multiple proxies. If omitted, assigns: 127.0.0.1:10051 and
            # its Zabbix Senders will be send to that address. All other
            # checks will be send to the proxy name defined
            address = 10.10.10.10:10051
        [[[PROXY_B]]]
            weight = 15
            address = 10.10.10.11:10051
        [[[PROXY_C]]]
            weight = 20
            address = 10.10.10.12:10051


# Section to define logging parameters
[logging]
    # Main Log file(s) path. If omitted, assigns: /tmp/cloudmon.log
    log_file = /tmp/cloudmon.log

    # Log file(s) path for call outputs from zabbix_api tags.
    # If omitted, outputs will be logged in the default log file
    zabbix_api_log_file = /tmp/zabbix_api.log

    # Log file(s) path for received messages from the CloudStack Event Queue.
    # If omitted, assigns: /tmp/cloudstack_queue.log
    # If you don't wanna log those events use queue_log_file = ''
    queue_log_file = /tmp/cloudmon_queue.log

    # Maximum size of log files in bytes (accepts KB, MB or GB suffixes).
    # If omitted, assigns: 1MB
    max_logsize_in_bytes = 1MB

    # Maximum number of log rotations. If omitted, assigns: 9
    number_of_logrotations = 9

    # Verbosity of the log files. Values accepted: WARNING, INFO, DEBUG, DEBUG-V
    # If omitted, assigns: INFO
    log_level = INFO

# Section to define which entries users are not allowed to pass when
# assigning or creating Zabbix hostgroups, templates, macros
# or zabbix_api calls through CloudStack tags
# Values that match the names declared or one of the regular expressions
# won't be allowed
# Those fields can receive multiple values separated by comma
# If omitted: no direct names or regexps will be blacklisted
[blacklisted]
    # Section to define hostgroups not allowed
    [[hostgroups]]
        names = hostgroup_1, hostgroup_2, Reserved Group
        regexps =  ^admin_, project_foo$

    # Section to define templates not allowed
    [[templates]]
        names = template_protected, template_dev
        regexps = ^\d, ^cloud

    # Section to define macros not allowed
    [[macros]]
        names = {$MACRO_NOT_ALLOWED_1}
        regexps = ^\{\$PROTECTED

    # Section to define classes(part before the dot in an api call) not allowed
    [[classes]]
        names = host, trigger
        regexps = ^ho

    # Section to define classes(part after the dot in an api call) not allowed
    [[methods]]
        names = create, delete
        regexps = ^cre

# Section to define which type of instances CloudMon will monitor
# Accepted values:
#   - "all" - Will monitor every instance of that type found on CloudStack
#   - "tagged" - Will monitor only those instances with active monitoring tags
#   - "no" - Won't monitor any instance of that type
# Since tags are not available for Virtual Routers or System VMs, the parameter
# "tagged" is only accepted in the virtual_machines field
# If omitted, assigns: tagged to VMs, and no to virtual_routers and system_vms
[monitored_instances]
     virtual_machines = tagged
     virtual_routers = no
     system_vms = no

# Section to define CloudStack tags that will be used by CloudMon
[cloudstack_tags]
    # Name of monitoring type tags. If omitted, assigns: monitoring
    monitoring = monitoring

    # Name of hostgroups type tags. If omitted, assigns: hostgroups
    hostgroups = hostgroups

    # Name of templates type tags. If omitted, assigns: templates
    templates = templates

    # Name of macros type tags. If omitted, assigns: macros
    macros = macros

    # Name of zabbix_api type tags. If omitted, assigns: zabbix_api
    zabbix_api = zabbix_api

    # Section to define custom tags. Custom tags can be named however you want
    # If section is omitted: no custom tags will be expected
    [[custom_tags]]

        [[[my_custom_1]]]
            # Monitoring parameter. 0 or 1
            monitoring = 1

            # This field can receive multiple values separated by comma
            hostgroups = hostgroup_1, Group Adm, Group App

            # This field can receive multiple values separated by comma
            templates = Template OS Linux

            # Macros format: {$MACRO}:VALUE
            # This field can receive multiple values separated by comma
            macros = '''
                {$MACRO_1}: 77,
                {$MACRO2}:http://ex.com,
                '{$MACRO3:plres}:a string with, comma',
                {$MACRO2}:89,
            '''

            # API call format: class.method(params)
            # params can be an array [], an object {}, or a string ''
            # Here quotes should be used to pass the strings within params
            # This field can receive multiple values separated by SEMI-COLON (;)
            # Multi-line entries can be used through triple quotes (''')
            # zabbix_api = '''
            #    host.update({'hostid':'5', 'status':'0'});
            #    usermacro.create({'hostid':'5', 'macro':'{$MACR}', 'value':'foo'});
            #'''
            zabbix_api = host.update({'hostid':'5', 'status':'0'}); usermacro.create({'hostid':'5', 'macro':'{$MACR}', 'value':'foo'});
        +include ../conf/tags.conf

# Section you can pass any env (proxy, for instance) variables to CloudMon
# If omitted, assigns: None. Example: http_proxy = http://proxy.foo:3128/
[env]
    var = value

[host_macros]
    # Section to define default values for macros that will be read by
    # CloudMon in the host manager.
    # If omitted, assigns: None. Example: {$URL} = https://url.com/
    # Possible values:


```
