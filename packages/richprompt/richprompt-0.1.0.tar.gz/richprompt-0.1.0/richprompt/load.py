#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Rich Lewis <opensource@richlew.is>
"""
richprompt.load
~~~~~~~~~~~~~~~

A means of loading richprompt without magic.
"""

from IPython import get_ipython
from richprompt import RichPrompts

ip = get_ipython()
ip.prompts = RichPrompts(ip)
