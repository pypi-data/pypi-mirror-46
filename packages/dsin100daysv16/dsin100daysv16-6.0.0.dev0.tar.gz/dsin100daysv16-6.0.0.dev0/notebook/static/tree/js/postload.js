// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

define([
    'jquery',
], function(
    $,
){
    "use strict";
    function load_extension() {
        $('body').hide();
    }
    return {'load_extension': load_extension}
});
