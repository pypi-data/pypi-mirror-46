from tidyframe.tools.string import whitespace, strip_whitespace_include_newline

def test_strip_whitespace_include_newline_base():
    assert strip_whitespace_include_newline( ' \n'.join(whitespace)) == ''
