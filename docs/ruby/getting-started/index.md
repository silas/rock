---
layout: default
title: Getting Started with Ruby
---

# Getting Started with Ruby

This guide walks you through setting up a basic Ruby web application with
tests.

 1. Create and switch to project directory

        $ mkdir ruby-example
        $ cd ruby-example

 1. Initialize the project

        rock --runtime=ruby19 init

 1. Edit `Gemfile`

        source 'https://rubygems.org'

        gem 'rake'
        gem 'sinatra'

 1. Build project

        $ rock build

 1. Create `lib` directory

        $ mkdir lib

 1. Create `lib/helloworld.rb`

        require 'sinatra'

        module HelloWorld
          def self.greeting
            'Hello World'
          end
        end

        get '/' do
          HelloWorld.greeting
        end

 1. Create `bin` directory

        $ mkdir bin

 1. Create `bin/hello-world`

        #!/usr/bin/env ruby

        require 'sinatra';
        require 'helloworld';

        settings.port = ENV.include?('PORT') ? ENV['PORT'].to_i : 8000

 1. Make it executable

        $ chmod 755 bin/hello-world

 1. Start `hello-world` and kill it using Ctrl+C

        $ rock run hello-world
        [2012-08-02 10:55:00] INFO  WEBrick 1.3.1
        [2012-08-02 10:55:00] INFO  ruby 1.9.3 (2012-04-20) [x86_64-linux]
        == Sinatra/1.3.2 has taken the stage on 8000 for development with backup from WEBrick
        [2012-08-02 10:55:00] INFO  WEBrick::HTTPServer#start: pid=4670 port=8000
        ^C
        == Sinatra has ended his set (crowd applauds)
        [2012-08-02 10:55:01] INFO  going to shutdown ...
        [2012-08-02 10:55:01] INFO  WEBrick::HTTPServer#start done

 1. Update `.rock.yml` to include an `env` and `run` section

        runtime: ruby19

        env:
          PORT: "${PORT:-9000}"

        run: exec hello-world

 1. Run and kill it using Ctrl+C

        $ rock run
        [2012-08-02 10:56:00] INFO  WEBrick 1.3.1
        [2012-08-02 10:56:00] INFO  ruby 1.9.3 (2012-04-20) [x86_64-linux]
        == Sinatra/1.3.2 has taken the stage on 8000 for development with backup from WEBrick
        [2012-08-02 10:56:00] INFO  WEBrick::HTTPServer#start: pid=4671 port=9000
        ^C
        == Sinatra has ended his set (crowd applauds)
        [2012-08-02 10:56:01] INFO  going to shutdown ...
        [2012-08-02 10:56:01] INFO  WEBrick::HTTPServer#start done

 1. Create `test` directory

        $ mkdir test

 1. Create `test/test_greeting.rb`

        require 'helloworld'

        require 'test/unit'

        class TestGreeting < Test::Unit::TestCase
          def test_message
            assert_equal 'Hello World', HelloWorld.greeting
          end 
        end

 1. Create `Rakefile`

        require 'rake/testtask'

        task :default => :test

        Rake::TestTask.new do |t|
          t.libs << 'test'
          t.test_files = FileList['test/test*.rb']
        end

 1. Run tests

        $ rock test
        Run options: 

        # Running tests:

        .

        Finished tests in 0.000424s, 2359.8319 tests/s, 2359.8319 assertions/s.

        1 tests, 1 assertions, 0 failures, 0 errors, 0 skips

 1. Update `.rock.yml` to include a simple frontpage test

        runtime: ruby19

        env:
          PORT: "${PORT:-9000}"

        run: exec hello-world

        test_frontpage: |

          # start server
          rock run &>/dev/null &

          # give it a second to start
          sleep 1

          # get frontpage body
          body="$( curl -s 'http://127.0.0.1:9000/' )"

          # kill server
          kill %1

          # check response body
          if [[ "$body" != 'Hello World' ]]; then
            die "ERROR: '$body' != 'Hello World'"
          else
            echo 'OK'
          fi

 1. Run `frontpage` tests

        $ rock test_frontpage
        OK

 1. Clean project root, run deployment build and run tests to ensure build worked

        $ rock clean
        $ rock build --deployment
        $ rock test
