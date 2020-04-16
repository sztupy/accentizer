#\ -p 8080 --host=0.0.0.0
# frozen_string_literal: true

require 'rubygems'
require 'bundler'

Bundler.require

require './server'

run AccentizerServer
