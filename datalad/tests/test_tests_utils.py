# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

import os

from .utils import eq_, ok_, with_tempfile, with_testrepos, with_tree

#
# Test with_tempfile, especially nested invocations
#
@with_tempfile
@with_tempfile
def test_nested_with_tempfile_basic(f1, f2):
    ok_(f1 != f2)
    ok_(not os.path.exists(f1))
    ok_(not os.path.exists(f2))

# And the most obscure case to test.  Generator for the test is
# used as well to verify that every one of those functions adds new argument
# to the end of incoming arguments.
@with_tempfile(prefix="TEST", suffix='big')
@with_tree((('f1.txt', 'load'),))
@with_tempfile(suffix='.cfg')
@with_tempfile(suffix='.cfg.old')
@with_testrepos(flavors=['local'])
def check_nested_with_tempfile_parametrized_surrounded(param, f0, tree, f1, f2, repo):
    eq_(param, "param1")
    ok_(f0.endswith('big'), msg="got %s" % f0)
    ok_(os.path.basename(f0).startswith('TEST'), msg="got %s" % f0)
    ok_(os.path.exists(os.path.join(tree, 'f1.txt')))
    ok_(f1 != f2)
    ok_(f1.endswith('.cfg'), msg="got %s" % f1)
    ok_(f2.endswith('.cfg.old'), msg="got %s" % f2)
    ok_('testrepos' in repo)

def test_nested_with_tempfile_parametrized_surrounded():
    yield check_nested_with_tempfile_parametrized_surrounded, "param1"