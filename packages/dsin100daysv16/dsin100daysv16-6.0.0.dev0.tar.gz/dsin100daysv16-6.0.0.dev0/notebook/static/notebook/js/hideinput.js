// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events'
], function(
    $,
    Jupyter,
    events
) {
    "use strict";

    var update_input_visibility = function () {
        Jupyter.notebook.get_cells().forEach(function(cell) {
            if (cell.metadata.hide_input && cell.cell_type === 'markdown') {
                var code = 'var index = $(this).parent().parent().index(); var cell = Jupyter.notebook.get_cell(index); cell.element.find("div.inner_cell").children("div").toggle("slow"); cell.metadata.hide_input = ! cell.metadata.hide_input;'
                cell.element.find("div.inner_cell")
                    .prepend(`<button onclick='`+code+`' style="width: 100%">Show/Hide Answer</button>`);
                cell.element.find("div.inner_cell").find("div").hide();
            }
        })
    };

    var load_ipython_extension = function() {
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
            // notebook already loaded. Update directly
            update_input_visibility();
        }
        events.on("notebook_loaded.Notebook", update_input_visibility);
    };

    return {
        load_ipython_extension : load_ipython_extension
    };
});
