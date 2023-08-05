## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Temperature Graph</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.bundle.min.js"></script>
  <script type="text/javascript">

    var ctx = null;
    var chart = null;

    function fetchReadings(timeRange) {
        if (timeRange === undefined) {
            timeRange = $('#time-range').val();
        }

        var timeUnit;
        if (timeRange == 'last hour') {
            timeUnit = 'minute';
        } else if (['last 6 hours', 'last day'].includes(timeRange)) {
            timeUnit = 'hour';
        } else {
            timeUnit = 'day';
        }

        $('.form-wrapper').mask("Fetching data");
        if (chart) {
            chart.destroy();
        }

        $.get('${url('{}.graph_readings'.format(route_prefix), uuid=probe.uuid)}', {'time-range': timeRange}, function(data) {

            chart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: "${probe.description}",
                        data: data
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            time: {unit: timeUnit},
                            position: 'bottom'
                        }]
                    }
                }
            });

            $('.form-wrapper').unmask();
        });
    }

    $(function() {

        ctx = $('#tempchart');

        $('#time-range').selectmenu({
            change: function(event, ui) {
                fetchReadings(ui.item.value);
            }
        });

        fetchReadings();
    });

  </script>
</%def>

<div class="form-wrapper">

  <div class="field-wrapper">
    <label>Appliance</label>
    <div class="field">
      % if probe.appliance:
          <a href="${url('tempmon.appliances.view', uuid=probe.appliance.uuid)}">${probe.appliance}</a>
      % endif
    </div>
  </div>

  <div class="field-wrapper">
    <label>Probe Location</label>
    <div class="field">${probe.location}</div>
  </div>

  <div class="field-wrapper">
    <label>Showing</label>
    <div class="field">
      ${time_range}
    </div>
  </div>

</div>

<canvas id="tempchart" width="400" height="150"></canvas>
