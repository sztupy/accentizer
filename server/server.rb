# frozen_string_literal: true

require 'sinatra'
require "sinatra/json"
require 'json'
require 'rest-client'
require 'base64'
require "sinatra/streaming"

class AccentizerServer < Sinatra::Base
  configure :production, :development do
    enable :logging
  end

  helpers Sinatra::Streaming

  set :environment, :production

  post '/accentize' do
    out_file = nil
    unless params[:file] &&
      (tmpfile = params[:file][:tempfile])
      halt 400
    end

    options = +""
    options << " --ffont" if params[:ffont]
    options << " --faccent" if params[:faccent]
    if params[:trans] && params[:trans].to_i > 0 && params[:trans].to_i < 400
      options << " --trans=#{params[:trans].to_i}"
    end

    tmpfile_name = tmpfile.path
    tmpfile_no_extension = tmpfile_name.chomp(File.extname(tmpfile_name))

    halt 400 if File.size(tmpfile_name) > 1_048_576

    system("fontforge /usr/src/app/accentizer.py #{options} '#{tmpfile_name}' 2>&1")

    out_file = tmpfile_no_extension + "out.ttf"
    halt 422 unless File.exist?(out_file)

    attachment("accentized.ttf")

    File.read(out_file, mode: "rb")
  ensure
    File.unlink(out_file) if out_file
  end
end
