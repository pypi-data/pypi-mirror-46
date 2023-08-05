## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="grid_tools()">
  ${parent.grid_tools()}

  % if request.has_perm('datasync.restart'):
      ${h.form(url('datasync.restart'), name='restart-datasync', class_='autodisable control')}
      ${h.csrf_token(request)}
      ${h.submit('submit', "Restart DataSync", data_working_label="Restarting DataSync", class_='button')}
      ${h.end_form()}
  % endif

  % if allow_filemon_restart and request.has_perm('filemon.restart'):
      ${h.form(url('filemon.restart'), name='restart-filemon', class_='autodisable control')}
      ${h.csrf_token(request)}
      ${h.submit('submit', "Restart FileMon", data_working_label="Restarting FileMon", class_='button')}
      ${h.end_form()}
  % endif

</%def>

${parent.body()}
