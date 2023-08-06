
# from basicsums.tests import test; test.run()
import basicsums.basic_sums
import basicsums.multi_indexes
import basicsums.eisenstein
import basicsums.preparation

modules = [('basic_sums', basicsums.basic_sums),
           ('multi_indexes', basicsums.multi_indexes),
           ('eisenstein', basicsums.eisenstein),
	   ('preparation', basicsums.preparation)]

testfiles = ['basic_sums.doctest',
             'conductivity.doctest',
             'weierstrass.doctest']

def run(verbose=False):

    import doctest
    
    for name, m in modules:
        print('Running doctests from:', name)
        result = doctest.testmod(m, verbose=verbose)
        print(result, end='\n\n')

    for tf_name in testfiles:
        print('Running testfile:', tf_name)
        result = doctest.testfile(tf_name, verbose=verbose)
        print(result, end='\n\n')
