package Sample;

use strict;
use warnings;

use Text::Markdown 'markdown';

sub convert {
    my ($text) = @_;
    return markdown($text);
}

1;
