import helper


class RuntimeTestCase(helper.RuntimeTests):

    name = 'node010'
    init_files = ['package.json']
    init_directories = ['test']
    create_lock = 'rock run npm shrinkwrap'


if __name__ == '__main__':
    helper.main()
