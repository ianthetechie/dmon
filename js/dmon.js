var dmon = (function() {
    var timeframes = [];
    var services = [];
    
    function updatePing(data) {
        for (var i = 0; i < timeframes.length; ++i) {
            var timeframe = timeframes[i];
            var $timeframe_div = $('#' + timeframe + '-div');
            var $timeframe_span = $('#' + timeframe + '-span');

            $timeframe_span.text(timeframe + ' - ' + data[timeframe].rtt.toFixed(2) + ' ms (' + data[timeframe].loss.toFixed(2) + '% loss)');
            $timeframe_span.width(Math.min(parseInt(data[timeframe].rtt / 10), 100) + '%');
            
            var color_class = '';
            if (data[timeframe].rtt < 100 && data[timeframe].loss < 10) {
                color_class = 'success';
            } else if (data[timeframe].rtt > 300 || data[timeframe].loss >= 10) {
                color_class = 'alert';
            }
            
            $timeframe_div.attr('class', 'progress large-12 thick ' + color_class);
        }
    };
    
    function updateServices(data) {
        for (var i = 0; i < services.length; ++i) {
            var service = services[i];
            var $service_span = $('#' + service + '-span');
            
            var color_class = '';
            if (data[service]) {
                color_class = 'success';
            } else {
                color_class = 'alert';
            }
            
            $service_span.attr('class', 'label thick ' + color_class);
        }
    };
    
    $(document).ready(function() {
        setInterval(function() {
            $.getJSON('/ping', updatePing);
            $.getJSON('/server_status', updateServices);
        }, 30000);
    });

    return {
        'setTimeframes': function(timeframe_list) {
            timeframes = timeframe_list;
        },
        'setServices': function(service_list) {
            services = service_list;
        },
        'updatePing': updatePing,
        'updateServices': updateServices
    }
})();
