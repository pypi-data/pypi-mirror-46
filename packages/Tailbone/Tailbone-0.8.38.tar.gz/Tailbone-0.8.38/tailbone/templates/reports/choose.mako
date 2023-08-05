## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">${index_title}</%def>

<%def name="content_title()"></%def>

<%def name="extra_javascript()">
  <script type="text/javascript">

    var report_descriptions = ${json.dumps(report_descriptions)|n};

    function show_description(key) {
        var desc = report_descriptions[key];
        $('#report-description').text(desc);
    }

    $(function() {

        var report_type = $('select[name="report_type"]');

        report_type.change(function(event) {
            show_description(report_type.val());
        });

    });

  </script>
</%def>

<%def name="extra_styles()">
  <style type="text/css">

    #report-description {
      margin-top: 2em;
      margin-left: 2em;
    }

  </style>
</%def>

<%def name="context_menu_items()">
  % if request.has_perm('report_output.list'):
      ${h.link_to("View Generated Reports", url('report_output'))}
  % endif
</%def>


<div style="display: flex; justify-content: space-between;">

  <div class="form-wrapper">
    <p>Please select the type of report you wish to generate.</p>

    <div style="display: flex;">
      ${form.render()|n}
      <div id="report-description"></div>
    </div>

  </div><!-- form-wrapper -->

  <ul id="context-menu">
    ${self.context_menu_items()}
  </ul>

</div>
