import helper


class RuntimeTestCase(helper.RuntimeTests):

    name = 'perl520'
    init_files = ['cpanfile']
    init_directories = ['t']


if __name__ == '__main__':
    helper.main()
