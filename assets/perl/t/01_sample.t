use strict;
use warnings;

use Test::More tests => 1;

use Sample 'convert';

is convert('# Test'), "<h1>Test</h1>\n";
