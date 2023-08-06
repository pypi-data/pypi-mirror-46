# Terminal Progress Bar
A easy to use python progress bar for your terminal.

![Example Gif](https://media.giphy.com/media/UUnB14M9E9cP906hA6/giphy.gif)

Options:
* label - the text infront of the bar
* bar_length - number of total markers to show
* full_marker - character for progress indicator
* empty_marker - character for remaining progress

## Usage

Check out the included example.py for a working demo of the default usage and a customized version.

```
import progressbar as pb

bar = pb.ProgressBar()

total = 10
for i in range(total):
    bar.progress(i, total)

```

## Credit and Contact

Created by Wyatt Ferguson

For any comments or questions your can reach me on Twitter [@wyattferguson](https://twitter.com/wyattferguson)