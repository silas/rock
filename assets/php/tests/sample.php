<?php

require './sample.php';

class Test extends PHPUnit_Framework_TestCase {
    public function testSample() {
        $this->assertEquals("<h1>Test</h1>\n", convert('# Test'));
    }
}
