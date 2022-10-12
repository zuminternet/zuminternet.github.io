FROM ruby:2.7.4-alpine
RUN apk update && apk add make gcc g++ libc-dev
COPY Gemfile* /usr/src/app/
WORKDIR /usr/src/app/
ENV RUBYOPT -EUTF-8
RUN bundle update
RUN bundle install
EXPOSE 4000
CMD jekyll serve
