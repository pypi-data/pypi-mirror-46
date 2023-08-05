## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

##############################
## page body
##############################

<div style="display: flex; justify-content: space-between;">

  <div class="form-wrapper">

    <div style="display: flex; flex-direction: column;">

      <div class="panel" id="probe-main">
        <h2>General</h2>
        <div class="panel-body">
          <div>
            ${self.render_main_fields(form)}
          </div>
        </div>
      </div>

      <div style="display: flex;">
        <div class="panel-wrapper">
          ${self.left_column()}
        </div>
        <div class="panel-wrapper" style="margin-left: 1em;"> <!-- right column -->
          ${self.right_column()}
        </div>
      </div>

    </div>
  </div>

  <ul id="context-menu">
    ${self.context_menu_items()}
  </ul>

</div>

% if master.has_rows:
    ${rows_grid|n}
% endif

##############################
## rendering methods
##############################

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  <li>${h.link_to("View Readings as Graph", action_url('graph', instance))}</li>
</%def>

<%def name="render_main_fields(form)">
  ${form.render_field_readonly('client')}
  ${form.render_field_readonly('config_key')}
  ${form.render_field_readonly('appliance')}
  ${form.render_field_readonly('appliance_type')}
  ${form.render_field_readonly('description')}
  ${form.render_field_readonly('location')}
  ${form.render_field_readonly('device_path')}
  ${form.render_field_readonly('notes')}
  ${form.render_field_readonly('enabled')}
  ${form.render_field_readonly('status')}
  ${form.render_field_readonly('therm_status_timeout')}
  ${form.render_field_readonly('status_alert_timeout')}
</%def>

<%def name="left_column()">
  <div class="panel">
    <h2>Temperatures</h2>
    <div class="panel-body">
      ${self.render_temperature_fields(form)}
    </div>
  </div>
</%def>

<%def name="right_column()">
  <div class="panel">
    <h2>Timeouts</h2>
    <div class="panel-body">
      ${self.render_timeout_fields(form)}
    </div>
  </div>
</%def>

<%def name="render_temperature_fields(form)">
  ${form.render_field_readonly('critical_temp_max')}
  ${form.render_field_readonly('good_temp_max')}
  ${form.render_field_readonly('good_temp_min')}
  ${form.render_field_readonly('critical_temp_min')}
</%def>

<%def name="render_timeout_fields(form)">
  ${form.render_field_readonly('critical_max_timeout')}
  ${form.render_field_readonly('good_max_timeout')}
  ${form.render_field_readonly('good_min_timeout')}
  ${form.render_field_readonly('critical_min_timeout')}
  ${form.render_field_readonly('error_timeout')}
</%def>
