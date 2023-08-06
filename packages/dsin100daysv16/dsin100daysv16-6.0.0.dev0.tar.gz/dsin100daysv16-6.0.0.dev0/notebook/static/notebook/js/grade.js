// Adds a button to hide the input part of the currently selected cells

define([
  'jquery',
  'base/js/namespace',
  'base/js/events',
], function (
  $,
  Jupyter,
  events,
) {
  "use strict";
  // NOTE: all the functions should be idempotent, i.e on multiple load of same
  // function should have same behaviour
  var add_submit_btn_below = function () {
    var code = '$("#submit_button").text("Submitting");Jupyter.notebook.get_cells().forEach(function(cell) {console.log("cell,", cell.metadata.tags);if (cell.metadata.tags && cell.metadata.tags.includes("grade")) {var i = Jupyter.notebook.find_cell_index(cell);console.log(i, cell);cell.execute();}else{}})'
    Jupyter.notebook.get_cells().forEach(function (cell) {
      if (cell.metadata.tags && cell.metadata.tags.includes("grade")) {
        $(document.getElementById('notebook-container')).after(`<button id="submit_button" style="margin: 15px auto;display: block;padding: 7px 30px;border: none;border-radius: 0;height: 40px;background: #00aeef;text-transform: uppercase;font-weight: 600;font-size: 13px;color: #fff;" onclick='` + code + `' >Submit</button>`);
      }
    });
  };

  var hide_grade_cell_and_create_events = function () {
    Jupyter.notebook.get_cells().forEach(function (cell) {
      if (cell.metadata.tags && cell.metadata.tags.includes('grade')) {
        cell.element.hide();
        events.on("finished_execute.CodeCell", function (e, d) {
          if (d.cell.metadata.tags && d.cell.metadata.tags.includes("grade")) {
            if (d.cell['output_area']['outputs'][0]['output_type'] == 'error') {
              alert(d.cell['output_area']['outputs'][0]['traceback'])

            } else {
              alert(d.cell['output_area']['outputs'][0]['text'])
            }
          }
          setTimeout(function () {
            $("#submit_button").text('submit').css("margin: 15px auto;display: block;padding: 7px 30px;border: none;border-radius: 0;height: 40px;background: #00aeef;text-transform: uppercase;font-weight: 600;font-size: 13px;color: #fff;");
          }, 1000);
        });
      }
    })
  };

  function load_functions() {
    hide_grade_cell_and_create_events();
    add_submit_btn_below();
  }

  var load_extension = function () {
    if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
      load_functions();
    }
    events.on("notebook_loaded.Notebook", load_functions);
  };

  return {
    load_extension: load_extension
  };
});