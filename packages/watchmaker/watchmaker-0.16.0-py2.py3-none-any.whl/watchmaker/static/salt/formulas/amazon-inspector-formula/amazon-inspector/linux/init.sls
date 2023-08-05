# -*- coding: utf-8 -*-
{%- from tpldir ~ '/map.jinja' import data with context %}

install_amazon_inspector:
  cmd.script:
    - name: amazon-inspector-agent-install.sh
    - source: {{ data.install_url }} 
    - cwd: /root
    - shell:  /bin/bash

start_amazon_inspector:
  cmd.run:
    - name: /etc/init.d/awsagent restart

ensure_amazon_inspector_is_running:
  cmd.run:
    - name: /opt/aws/awsagent/bin/awsagent status
