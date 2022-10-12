#!/usr/bin/env python3

import json
from textwrap import dedent
from urllib.request import urlopen

with urlopen('https://pages.github.com/versions.json') as r:
    deps = json.loads(r.read())

ruby_version = deps['ruby']
del deps['ruby']
with open('Gemfile', 'w') as f:
    f.write("source 'https://rubygems.org'\n")
    for name, version in deps.items():
        f.write("gem '%s', '%s'\n" % (name, version))
    f.write("gem 'webrick', '~> 1.7'\n")
    #f.write(dedent('''\
    #    gem 'jekyll-watch'
    #    gem 'jekyll-admin'
    #'''))

with open('Dockerfile', 'w') as f:
    f.write(dedent('''\
        FROM ruby:{version}
        RUN apk update && apk add make gcc g++ libc-dev
        COPY Gemfile* /usr/src/app/
        WORKDIR /usr/src/app/
        ENV RUBYOPT -EUTF-8
        RUN bundle install
        EXPOSE 4000
        CMD jekyll serve
    '''.format(version=ruby_version + '-alpine')))
