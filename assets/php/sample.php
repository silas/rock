<?php

use dflydev\markdown\MarkdownParser;

function convert($text) {
    $md = new MarkdownParser();
    return $md->transformMarkdown($text);
}
