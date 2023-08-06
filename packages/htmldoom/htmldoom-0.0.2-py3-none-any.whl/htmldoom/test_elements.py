import htmldoom.elements as e


def test_double_quote():
    assert e.double_quote('abc"xyz') == '"abc\\"xyz"'


def test_style():
    txt = e.style(
        **{"color": "red", "text-align": "center", "font-family": ("Segoe UI", "Arial")}
    )
    assert txt == "color:'red';text-align:'center';font-family:'Segoe UI','Arial';"


def test_css():
    txt = e.css(**{"p": {"color": "red"}, ".center": {"text-align": "center"}})
    assert txt == "p{color:'red';}.center{text-align:'center';}"


def test__RawText():
    assert repr(e._RawText("<div>&nbsp;</div>")) == "<div>&nbsp;</div>"


def test__Text():
    assert repr(e._Text("foo &nbsp;<p>")) == "foo &amp;nbsp;&lt;p&gt;"


def test__Comment():
    assert repr(e._Comment("Commenting -->")) == "<!-- Commenting --&gt; -->"
    assert isinstance(e._Comment("foo"), e._Declaration)


def test_DocType():
    assert repr(e.DocType("html")) == "<!DOCTYPE html>"
    assert (
        repr(
            e.DocType(
                "HTML",
                "PUBLIC",
                "-//W3C//DTD HTML 4.01//EN",
                "http://www.w3.org/TR/html4/strict.dtd",
            )
        )
        == '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
    )
    assert isinstance(e.DocType("html"), e._Declaration)


def test_Br():
    assert repr(e.Br()) == "<br />"


def test_A():
    assert repr(e.A(href="#")) == '<a href="#"></a>'
    assert repr(e.A(href="#")("foo")) == '<a href="#">foo</a>'


def test_Abbr():
    assert repr(e.Abbr(title="foo")("bar")) == '<abbr title="foo">bar</abbr>'


def test_Address():
    assert (
        repr(e.Address()(e._RawText(f"foo{e.Br()}"))) == "<address>foo<br /></address>"
    )


def test_audio():
    assert repr(e.Audio("controls")("foo")) == "<audio controls>foo</audio>"


def test_script():
    assert (
        repr(e.Script()('var x = "<p>&nbsp;</p>";'))
        == '<script>var x = "<p>&nbsp;</p>";</script>'
    )
