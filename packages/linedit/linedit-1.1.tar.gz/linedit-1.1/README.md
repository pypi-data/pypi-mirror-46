# linedit

- used to quickly bulk edit config files from a python script
- fairly performant
- simple

# install
```
pip install linedit
```

# usage

Single line in a file:
```
import linedit

config_file = '/Users/colathro/Development/config.cfg'
target_line = 35
new_line = 'verbose_trace = FALSE'

linedit.edit(config_file, target_line, new_line)
```


Multiple lines in a file:
```
import linedit

config_file = '/Users/colathro/Development/config.cfg'
target_lines = [(1,'verbose_trace = FALSE'), (23,'database = MYSQL'), (11, 'CASHIER = Wendy'), (55, 'PASSWORD = CarlsJr5for$5')]

linedit.medit(config_file, target_lines)
``` 

# performance

Average Speed for 1000000 line file:
- `MEDIAN 6170.082330703735 ms`
- `MEAN   6260.158348083496 ms`
- `STDEV  149.98134948053402 ms`

Average Speed for 100000 line file:
- `MEDIAN 611.5955114364624 ms`
- `MEAN   643.6208724975586 ms`
- `STDEV  99.59640919899704 ms`

Average Speed for 1000 line file:
- `MEDIAN 8.266568183898926 ms`
- `MEAN   8.282017707824707 ms`
- `STDEV  1.418332126464872 ms`
