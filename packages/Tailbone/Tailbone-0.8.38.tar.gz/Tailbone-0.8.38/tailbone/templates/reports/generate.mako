## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">${index_title} &raquo; ${report.name}</%def>

<%def name="content_title()">${report.name}</%def>

<%def name="context_menu_items()">
  % if request.has_perm('report_output.list'):
      ${h.link_to("View Generated Reports", url('report_output'))}
  % endif
</%def>


<div style="display: flex; justify-content: space-between;">

  <div class="form-wrapper">
    <p style="padding: 1em;">${report.__doc__}</p>
    ${form.render()|n}
  </div><!-- form-wrapper -->

  <ul id="context-menu">
    ${self.context_menu_items()}
  </ul>

</div>
