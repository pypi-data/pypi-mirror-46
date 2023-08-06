from tidyframe.tools.string import whitespace, strip_whitespace

def test_replace_space_base():
    assert strip_whitespace( ' '.join(whitespace)) == ''

def test_replace_space_without_strip_newline():
    assert strip_whitespace('line_one\n\tline_two') =='line_one\n\tline_two'