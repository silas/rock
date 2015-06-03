use strict;
use warnings;

use Test::More tests => 1;

use Sample;

is Sample::convert('# Test'), "<h1>Test</h1>\n";
