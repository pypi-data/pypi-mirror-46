// AJAX CSRF setup. Source: https://docs.djangoproject.com/en/1.10/ref/csrf/#ajax

jQuery.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            var csrfToken = $('#nexus-constants').data('csrfToken');
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});

/* Facebox setup as per instructions at https://github.com/defunkt/facebox */

(function () {

    var nexusMediaPrefix = $('#nexus-constants').data('nexusMediaPrefix'),
        loadingImage = nexusMediaPrefix + '/nexus/img/facebox/loading.gif',
        closeImage = nexusMediaPrefix + '/nexus/img/facebox/closelabel.png';

    $.facebox.settings.closeImage = closeImage;
    $.facebox.settings.loadingImage = loadingImage;

})();
