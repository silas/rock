import helper


class RuntimeTestCase(helper.RuntimeTests):

    name = 'ruby22'
    init_files = ['Gemfile', 'Rakefile']
    init_directories = ['test']


if __name__ == '__main__':
    helper.main()
