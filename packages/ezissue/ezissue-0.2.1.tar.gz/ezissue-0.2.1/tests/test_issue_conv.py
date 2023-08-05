import ezissue.ezissue as ezissue


def test_md_table_row_to_array():
    md = '| get to the choppa | asdf | jkl |'
    array = ezissue.md_table_row_to_array(md)

    if not array == ['get to the choppa', 'asdf', 'jkl']:
        raise AssertionError()


def test_add_md_checkbox():
    arg = "asdf;asdf;adsf;asdf"
    resp = ezissue.add_md_checkbox(arg)
    if not (resp == '- [ ] asdf\n- [ ] asdf\n- [ ] adsf\n- [ ] asdf\n'):
        raise AssertionError()


def test_format_description():
    desc = "lorem ipsum dolor sit amet"
    a = ezissue.format_description(desc)
    print(repr(a))
    if not (a == '**Issue description:**\nlorem ipsum dolor sit amet\n'):
        raise AssertionError()


def test_add_prefix_to_title():
    titles = ["make america great again", "make stuff work"]
    formattedUS = []
    formattedTS = []

    for idx, title in enumerate(titles):
        formattedUS.append(
            ezissue.add_prefix_to_title(title, idx+1, 'US', '', True)
        )
        formattedTS.append(
            ezissue.add_prefix_to_title(title, idx+1, 'TS', '', True)
        )
    for idx, title in enumerate(titles):
        formattedUS.append(
            ezissue.add_prefix_to_title(title, idx+1, 'US', 'M', False)
        )
        formattedTS.append(
            ezissue.add_prefix_to_title(title, idx+1, 'TS', 'M', False)
        )
    for idx, title in enumerate(titles):
        formattedUS.append(
            ezissue.add_prefix_to_title(title, idx+1, '', '', False)
        )
        formattedTS.append(
            ezissue.add_prefix_to_title(title, idx+1, '', '', False)
        )

    if not (formattedUS[0] == 'US1 Make america great again' and formattedTS[0] == 'TS1 Make america great again'):
        raise AssertionError()
    if not (formattedUS[1] == 'US2 Make stuff work' and formattedTS[1] == 'TS2 Make stuff work'):
        raise AssertionError()

    if not (formattedUS[2] == 'USM Make america great again' and formattedTS[2] == 'TSM Make america great again'):
        raise AssertionError()
    if not (formattedUS[3] == 'USM Make stuff work' and formattedTS[3] == 'TSM Make stuff work'):
        raise AssertionError()

    if not (formattedUS[4] == ' Make america great again' and formattedTS[4] == ' Make america great again'):
        raise AssertionError()
    if not (formattedUS[5] == ' Make stuff work' and formattedTS[5] == ' Make stuff work'):
        raise AssertionError()


def test_create_github_url():
    url = ezissue.create_github_url('commit-helper', 'andre-filho')
    expected = "https://api.github.com/repos/andre-filho/commit-helper/issues"
    if not url == expected:
        raise AssertionError()


def test_create_gitlab_url():
    url = ezissue.create_gitlab_url(1234)
    expected = "https://gitlab.com/api/v4/projects/1234/issues"
    if not url == expected:
        raise AssertionError()
