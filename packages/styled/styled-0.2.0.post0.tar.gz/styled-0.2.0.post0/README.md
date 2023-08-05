.. image:: https://coveralls.io/repos/github/emdb-empiar/styled/badge.svg?branch=master
    :target: https://coveralls.io/github/emdb-empiar/styled?branch=master

.. image:: https://travis-ci.org/emdb-empiar/styled.svg?branch=master
    :target: https://travis-ci.org/emdb-empiar/styled

# Introduction

Welcome to `styled`, a simple Python package that makes a breeze of writing beautiful text to the terminal. 
The main innovation behind `styled` is the dead-simple user interface which does away with the user's need to know 
anything other than the style names. Behind the scenes `styled` handles everything to keep 
your styles consistent and redundant and informing you when you have made formatting errors.

`styled` was borne out of the frustration encountered in using other packages which muddle the boundary between
_user-space_ and _design-space_. The user should be free to be a _user_ and it is the _designer's_ job to hide the 
implementation behind a simple user interface that facilitates the user's task. This is what I've tried to do. If I have 
failed to live up to this please let me know. I'm sure together we can come up with something better.

## Getting Started

To get it from `PyPI` use

```bash
pip install styled
```

It's best to do this in a virtual environment.

```bash
# anaconda/miniconda
conda create -n styled python
source activate styled
pip install styled

# virtualenv
virtualenv /path/to/env/styled -p /path/to/python
source /path/to/envs/styled/bin/activate
pip install styled

```

Using `styled` is easy. Try this out in your Python console.

```python
>>> from styled import Styled
>>> s = Styled("We are [[ 'bold'|bold ]] men!")
>>> print(s)
We are bold men!
```

You can perform string formatting _directly_ in the constructor.

```python
>>> s = Styled("There were up to [[ '{}'|bold:fg-red ]] people who handed over themselves to the \
[[ '{police}'|fg-black:bg-red:bold ]].", 24, police='policia')
>>> print(s)
There were up to 24 people who handed over themselves to the policia.
```

You have to delimit the text you want to style with `[[ ... ]]` then make sure that the following _three (3)_ conditions hold:

* separate the text from the styles with a pipe (`|`),
* quote the text part with either a pair of single (`'...'`) or double (`"..."`) quotes, then 
* separate each style with a colon (`:`)

There are _three (3)_ types of styles:

* _text styling_ such as `bold`, `blink`, `underline` etc.
* *foreground colours*, such as `fg-red`,
* *background colours*, such as `bg-blue`.

If you want to style an extended piece of text you can use a special additional style marker (`no-end`) indicating to 
continue the styling for as long as possible. This can be useful if you want to style a long stretch of text.

```python
>>> s = Styled("There were up to [[ '{}'|bold:fg-red:no-end ]] people who handed over themselves to the \
[[ '{police}'|fg-black:bg-red:bold ]].", 24, police='policia')
>>> print(s)
There were up to 24 people who handed over themselves to the policia.
``` 

The above example will have all the text until the next marker affected by the red foreground styling. You can also 
manually enforce an end marker by using `yes-end` as a style. By default all style markers will terminate on the 
text to be styled. So, for example

```python
>>> # an example of a terminating end marker
>>> s = Styled("There were up to [[ '{}'|bold:fg-red:no-end ]] people who handed over themselves [[ ''|yes-end ]] to the \
[[ '{police}'|fg-black:bg-red:bold ]].", 24, police='policia')
>>> print(s)
There were up to 24 people who handed over themselves to the policia.
``` 

will suspend red foreground at the end of the word 'themselves'.

You can only have one foreground and one background colour. Ignoring this produces a `StyleError`

```python
>>> from styled import Styled
>>> s = Styled("There were up to [[ '{}'|bold:fg-red:fg-blue ]] people who handed over themselves to the [[ '{police}'|fg-black:bg-red:bold ]].", 24, police='policia')
Traceback (most recent call last):
  File "/Users/pkorir/miniconda2/envs/styled/lib/python2.7/site-packages/IPython/core/interactiveshell.py", line 2878, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-3-0993b680f88b>", line 1, in <module>
    s = Styled("There were up to [[ '{}'|bold:fg-red:fg-blue ]] people who handed over themselves to the [[ '{police}'|fg-black:bg-red:bold ]].", 24, police='policia')
  File "/Users/pkorir/PycharmProjects/styled/styled/styled.py", line 55, in __init__
    self._validate(self._tokens)
  File "/Users/pkorir/PycharmProjects/styled/styled/styled.py", line 156, in _validate
    raise StyleError(u"Multiple foreground styles for text '{}': {}".format(text, ', '.join(styles)))
StyleError: Multiple foreground styles for text '24': bold, fg-red, fg-blue
```

Inputing an invalid `style` also raises a `StyleError`

```python
>>> s = Styled("This just can't just [[ 'go'|underline ]] on forever! ")
Traceback (most recent call last):
  File "/Users/pkorir/miniconda2/envs/styled/lib/python2.7/site-packages/IPython/core/interactiveshell.py", line 2878, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-4-528d6d2ac4f4>", line 1, in <module>
    s = Styled("This just can't just [[ 'go'|underline ]] on forever! ")
  File "/Users/pkorir/PycharmProjects/styled/styled/styled.py", line 59, in __init__
    self._styled = self._transform(self._plain, self._cleaned_tokens)
  File "/Users/pkorir/PycharmProjects/styled/styled/styled.py", line 99, in _transform
    styled += plain[i:start] + self.transform(token)
  File "/Users/pkorir/PycharmProjects/styled/styled/styled.py", line 87, in transform
    raise StyleError(u"Unknown style '{}'".format(style_))
StyleError: Unknown style 'underline'
```

(In case you're wondering, it should have been `underlined` not `underline`.)

Which brings us to the tables of styles. (These are borrowed from <https://gitlab.com/dslackw/colored>, by the way.)

| *styles* |
|--------|
| bold|
| dim |
| underlined |
| blink |
| reverse    |
| hidden |
| reset  |
| res_bold   |
| res_dim    |
| res_underlined |
| res_blink  |
| res_reverse    |
| res_hidden |


| *colours* |
|---|
|black |
|red |
|green |
|yellow |
|blue |
|magenta |
|cyan |
|light_gray |
|dark_gray |
|light_red |
|light_green |
|light_yellow |
|light_blue |
|light_magenta |
|light_cyan |
|white |
|grey_0 |
|navy_blue |
|dark_blue |
|blue_3a |
|blue_3b |
|blue_1 |
|dark_green |
|deep_sky_blue_4a |
|deep_sky_blue_4b |
|deep_sky_blue_4c |
|dodger_blue_3 |
|dodger_blue_2 |
|green_4 |
|spring_green_4 |
|turquoise_4 |
|deep_sky_blue_3a |
|deep_sky_blue_3b |
|dodger_blue_1 |
|green_3a |
|spring_green_3a |
|dark_cyan |
|light_sea_green |
|deep_sky_blue_2 |
|deep_sky_blue_1 |
|green_3b |
|spring_green_3b |
|spring_green_2a |
|cyan_3 |
|dark_turquoise |
|turquoise_2 |
|green_1 |
|spring_green_2b |
|spring_green_1 |
|medium_spring_green |
|cyan_2 |
|cyan_1 |
|dark_red_1 |
|deep_pink_4a |
|purple_4a |
|purple_4b |
|purple_3 |
|blue_violet |
|orange_4a |
|grey_37 |
|medium_purple_4 |
|slate_blue_3a |
|slate_blue_3b |
|royal_blue_1 |
|chartreuse_4 |
|dark_sea_green_4a |
|pale_turquoise_4 |
|steel_blue |
|steel_blue_3 |
|cornflower_blue |
|chartreuse_3a |
|dark_sea_green_4b |
|cadet_blue_2 |
|cadet_blue_1 |
|sky_blue_3 |
|steel_blue_1a |
|chartreuse_3b |
|pale_green_3a |
|sea_green_3 |
|aquamarine_3 |
|medium_turquoise |
|steel_blue_1b |
|chartreuse_2a |
|sea_green_2 |
|sea_green_1a |
|sea_green_1b |
|aquamarine_1a |
|dark_slate_gray_2 |
|dark_red_2 |
|deep_pink_4b |
|dark_magenta_1 |
|dark_magenta_2 |
|dark_violet_1a |
|purple_1a |
|orange_4b |
|light_pink_4 |
|plum_4 |
|medium_purple_3a |
|medium_purple_3b |
|slate_blue_1 |
|yellow_4a |
|wheat_4 |
|grey_53 |
|light_slate_grey |
|medium_purple |
|light_slate_blue |
|yellow_4b |
|dark_olive_green_3a |
|dark_green_sea |
|light_sky_blue_3a |
|light_sky_blue_3b |
|sky_blue_2 |
|chartreuse_2b |
|dark_olive_green_3b |
|pale_green_3b |
|dark_sea_green_3a |
|dark_slate_gray_3 |
|sky_blue_1 |
|chartreuse_1 |
|light_green_2 |
|light_green_3 |
|pale_green_1a |
|aquamarine_1b |
|dark_slate_gray_1 |
|red_3a |
|deep_pink_4c |
|medium_violet_red |
|magenta_3a |
|dark_violet_1b |
|purple_1b |
|dark_orange_3a |
|indian_red_1a |
|hot_pink_3a |
|medium_orchid_3 |
|medium_orchid |
|medium_purple_2a |
|dark_goldenrod |
|light_salmon_3a |
|rosy_brown |
|grey_63 |
|medium_purple_2b |
|medium_purple_1 |
|gold_3a |
|dark_khaki |
|navajo_white_3 |
|grey_69 |
|light_steel_blue_3 |
|light_steel_blue |
|yellow_3a |
|dark_olive_green_3 |
|dark_sea_green_3b |
|dark_sea_green_2 |
|light_cyan_3 |
|light_sky_blue_1 |
|green_yellow |
|dark_olive_green_2 |
|pale_green_1b |
|dark_sea_green_5b |
|dark_sea_green_5a |
|pale_turquoise_1 |
|red_3b |
|deep_pink_3a |
|deep_pink_3b |
|magenta_3b |
|magenta_3c |
|magenta_2a |
|dark_orange_3b |
|indian_red_1b |
|hot_pink_3b |
|hot_pink_2 |
|orchid |
|medium_orchid_1a |
|orange_3 |
|light_salmon_3b |
|light_pink_3 |
|pink_3 |
|plum_3 |
|violet |
|gold_3b |
|light_goldenrod_3 |
|tan |
|misty_rose_3 |
|thistle_3 |
|plum_2 |
|yellow_3b |
|khaki_3 |
|light_goldenrod_2a |
|light_yellow_3 |
|grey_84 |
|light_steel_blue_1 |
|yellow_2 |
|dark_olive_green_1a |
|dark_olive_green_1b |
|dark_sea_green_1 |
|honeydew_2 |
|light_cyan_1 |
|red_1 |
|deep_pink_2 |
|deep_pink_1a |
|deep_pink_1b |
|magenta_2b |
|magenta_1 |
|orange_red_1 |
|indian_red_1c |
|indian_red_1d |
|hot_pink_1a |
|hot_pink_1b |
|medium_orchid_1b |
|dark_orange |
|salmon_1 |
|light_coral |
|pale_violet_red_1 |
|orchid_2 |
|orchid_1 |
|orange_1 |
|sandy_brown |
|light_salmon_1 |
|light_pink_1 |
|pink_1 |
|plum_1 |
|gold_1 |
|light_goldenrod_2b |
|light_goldenrod_2c |
|navajo_white_1 |
|misty_rose1 |
|thistle_1 |
|yellow_1 |
|light_goldenrod_1 |
|khaki_1 |
|wheat_1 |
|cornsilk_1 |
|grey_100 |
|grey_3 |
|grey_7 |
|grey_11 |
|grey_15 |
|grey_19 |
|grey_23 |
|grey_27 |
|grey_30 |
|grey_35 |
|grey_39 |
|grey_42 |
|grey_46 |
|grey_50 |
|grey_54 |
|grey_58 |
|grey_62 |
|grey_66 |
|grey_70 |
|grey_74 |
|grey_78 |
|grey_82 |
|grey_85 |
|grey_89 |
|grey_93 |


To view the palette of colours run the following in a Python shell

```python
>>> from styled import Styled, COLOURS
>>> for cn,cv in COLOURS.iteritems():
...     print Styled("Foreground: [[ '{:>30}'|fg-{} ]]\tBackground: [[ '{:>30}'|bg-{} ]]".format(cn, cn, cn, cn))
```

## Concatenation

Concatenating a normal string and a `Styled` string produces a `Styled` string, which is a subclass of string. 
Internally, though, everything is a Unicode string.

```python
>>> s = Styled("This just can't just [[ 'go'|underlined ]] on forever! ")
>>> u = "She shouted back!"
>>> print(type(s + u))
<class 'styled.styled.Styled'>
>>> print(type(u + s))
<class 'styled.styled.Styled'>
>>> s += "Gloria!"
>>> print(type(s))
<class 'styled.styled.Styled'>
```

## Validation

The process of generating the output involves some validation - to check that styles are sane. At present,
only multiple fore- and background colours are checked. This will be expanded as needed.

## Cleaning Styles

In addition to validation, styles are cleaned. Cleaning ensures that the final set of styles is non-redundant.

```python
>>> s = Styled("It takes enormouse [[ 'courage'|bold:bold:bold ]] to admit that you're wrong (Hehehehehehe!)")
>>> s._tokens
[(19, 49, u'courage', [u'bold', u'bold', u'bold'])]
>>> s._cleaned_tokens
[(19, 49, u'courage', [u'bold'])]
```

## Aspirations?

When I grow up I want to have my own Python string declaration like so:

```python
# hey! I'm a styled string
s = s"You have to [[ 'believe'|fg-red ]] it to [[ 'see'|fg-green ]] it!"
```

## Special Thanks

To the following people

* Dimitris Zlatanidis (for the inspiration and resources in his package `colored` available at <https://gitlab.com/dslackw/colored>)
* Cesare Catavitello (for being the _first_ user)