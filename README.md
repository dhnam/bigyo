# bigyo

[![Downloads](https://pepy.tech/badge/bigyo)](https://pepy.tech/project/bigyo)
(Badge for me :D)

Bigyo (비교(KR): Comparison) is simple python library for side-by-side diff in terminal.

Use difflib as its engine.

Supports beautiful output with multi-width or zero-width character.

## Install

```
pip install bigyo
```

It just works!

## How to

Replace 
```py
difflib.Differ().compare(a, b)
```
to
```py
bigyo.Bigyo().compare(a, b)
```
and you get your nice side-by-side comparison generator. (Note it is generator)

Also, to get full comparison string at once, there is
```py
bigyo.Bigyo().comparison_string(a, b)
```
method for you to use.

## Bigyo rendering strategy

Default bigyo rendering strategy is `SimpleBigyoRenderer` with default params, which will look like this.
```
- Hello, World |+  Helo, Wold!
?    -     -   |?            +
```

However, you can change separator (defaults to `|`) if you wish, by making `BigyoRenderer` class with parameter,
```py
bigyo_rd = SimpleBigyoRenderer(sep="*")
```
...And give it as parameter of `Bigyo`.
```py
bigyo_cls = bigyo.Bigyo(bigyo_renderer = bigyo_rd)
```

In this case, result will look like this.
```
- Hello, World *+  Helo, Wold!
?    -     -   *?            +
```

Also there exists `OnelineBigyoRenderer` which will render difference like this.
```
He>l<lo, Wo>r<ld|Helo, Wold<!>
```

## History

All the commits can be found in [github page](https://github.com/dhnam/bigyo).

```
0.0.1   2022.12.15 Project init!
0.1.0   2022.12.17 Added comparison_string method, changed name from BigyoStrategy to BigyoRenderer, bugfix
0.1.1   2022.12.17 Separate bigyo_renderer, change directory structure
0.1.2   2022.12.21 Now with sphinx document!
0.1.3   2022.12.21 Requirements.txt had typo.
0.1.4   2022.12.27 Documentation fixs
0.1.4a8 2023.01.05 Tinkering with github action (nothing to do with actual program!)
```
