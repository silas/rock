import helper


class RuntimeTestCase(helper.RuntimeTests):

    name = 'php54'
    init_files = ['composer.json']
    init_directories = ['tests']


if __name__ == '__main__':
    helper.main()
