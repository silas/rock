import helper


class RuntimeTestCase(helper.RuntimeTests):

    name = 'python27'
    init_files = ['requirements.txt']
    init_directories = ['tests']


if __name__ == '__main__':
    helper.main()
