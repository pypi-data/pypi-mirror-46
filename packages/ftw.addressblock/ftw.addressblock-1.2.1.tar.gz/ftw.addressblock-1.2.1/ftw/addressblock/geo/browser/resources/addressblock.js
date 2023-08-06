// XXX: NEEDS TO BE REMOVED, SINCE IT HAS NO EFFECT
// The addressblock needs the mapblock.js in order to work

(function() {

    "use strict";

    $(function() {

        $(document).on("onLoad", ".overlay", function() {
            if ($.fn.collectivegeo) {

                var maps = $('.widget-cgmap').filter(':hidden');
                if (maps.length > 0) {
                    var tabs = $('select.formTabs, ul.formTabs');
                    tabs.on("onClick", function(e, index) {
                        var curpanel = $(this).data('tabs').getCurrentPane();
                        curpanel.find('.widget-cgmap').collectivegeo(); // refresh
                        curpanel.find('.map-widget .widget-cgmap').collectivegeo('add_edit_layer');
                        curpanel.find('.map-widget .widget-cgmap').collectivegeo('add_geocoder');
                    });
                }

            }
        });
    });
})();
