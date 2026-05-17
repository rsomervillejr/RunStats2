import pathlib


def test_edit_template_includes_duration_validation():
    tpl = pathlib.Path('src/templates/edit.html').read_text(encoding='utf8')
    assert 'duration-mmss' in tpl
    assert 'duration-error' in tpl
    assert 'split_duration.js' in tpl
