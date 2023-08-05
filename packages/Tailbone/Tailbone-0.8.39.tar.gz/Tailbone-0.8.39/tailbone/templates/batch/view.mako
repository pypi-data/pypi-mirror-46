## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.batch.js') + '?ver={}'.format(tailbone.__version__))}
  <script type="text/javascript">

    var has_execution_options = ${'true' if master.has_execution_options(batch) else 'false'};

    $(function() {
        % if master.has_worksheet:
            $('.load-worksheet').click(function() {
                disable_button(this);
                location.href = '${url('{}.worksheet'.format(route_prefix), uuid=batch.uuid)}';
            });
        % endif
        % if master.batch_refreshable(batch) and request.has_perm('{}.refresh'.format(permission_prefix)):
            $('#refresh-data').click(function() {
                $(this)
                    .button('option', 'disabled', true)
                    .button('option', 'label', "Working, please wait...");
                location.href = '${url('{}.refresh'.format(route_prefix), uuid=batch.uuid)}';
            });
        % endif
    });

  </script>
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">

    .grid-wrapper {
        margin-top: 10px;
    }

    .complete form {
        display: inline;
    }
    
  </style>
</%def>

<%def name="buttons()">
    <div class="buttons">
      ${self.leading_buttons()}
      ${refresh_button()}
      ${execute_button()}
    </div>
</%def>

<%def name="leading_buttons()">
  % if master.has_worksheet and master.allow_worksheet(batch) and request.has_perm('{}.worksheet'.format(permission_prefix)):
      <button type="button" class="load-worksheet">Edit as Worksheet</button>
  % endif
</%def>

<%def name="refresh_button()">
  % if master.viewing and master.batch_refreshable(batch) and request.has_perm('{}.refresh'.format(permission_prefix)):
      <button type="button" id="refresh-data">Refresh Data</button>
  % endif
</%def>

<%def name="execute_button()">
  % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
      % if execute_enabled:
          <button type="button" id="execute-batch">${execute_title}</button>
      % elif why_not_execute:
          <button type="button" id="execute-batch" disabled="disabled" title="${why_not_execute}">${execute_title}</button>
      % else:
          <button type="button" id="execute-batch" disabled="disabled">${execute_title}</button>
      % endif
  % endif
</%def>

<%def name="object_helpers()">
  ${self.render_status_breakdown()}
</%def>

<%def name="render_status_breakdown()">
  % if status_breakdown is not Undefined and status_breakdown is not None:
      <div class="object-helper">
        <h3>Row Status Breakdown</h3>
        <div class="object-helper-content">
          % if status_breakdown:
              <div class="grid full">
                <table>
                  % for i, (status, count) in enumerate(status_breakdown):
                      <tr class="${'even' if i % 2 == 0 else 'odd'}">
                        <td>${status}</td>
                        <td>${count}</td>
                      </tr>
                  % endfor
                </table>
              </div>
          % else:
              <p>Nothing to report yet.</p>
          % endif
        </div>
      </div>
  % endif
</%def>

<div style="display: flex; justify-content: space-between;">

  <div class="form-wrapper">
    ${form.render(form_id='batch-form', buttons=capture(buttons))|n}
  </div><!-- form-wrapper -->

  <div style="display: flex; align-items: flex-start;">

    <div class="object-helpers">
      ${self.object_helpers()}
    </div>

    <ul id="context-menu">
      ${self.context_menu_items()}
    </ul>

  </div>

</div>

% if use_buefy:
    <br /><br />
    ## TODO: stop using |n filter
    ${rows_grid.render_buefy(allow_save_defaults=False, tools=rows_grid_tools)|n}
% else:
    ## no buefy, so do the traditional thing
    ${rows_grid|n}
% endif

% if master.handler.executable(batch) and not batch.executed:
    <div id="execution-options-dialog" style="display: none;">
      ${execute_form.render_deform(form_kwargs={'name': 'batch-execution'}, buttons=False)|n}
    </div>
% endif
