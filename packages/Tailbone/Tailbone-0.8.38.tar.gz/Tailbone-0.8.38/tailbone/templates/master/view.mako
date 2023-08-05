## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">${index_title} &raquo; ${instance_title}</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if master.has_rows:
      % if use_buefy:
          ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.gridfilters.js') + '?ver={}'.format(tailbone.__version__))}
      % else:
      <script type="text/javascript">
        $(function() {
            $('.grid-wrapper').gridwrapper();
        });
      </script>
      % endif
  % endif
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  % if master.has_rows and not use_buefy:
      <style type="text/css">
        .grid-wrapper {
            margin-top: 10px;
        }
      </style>
  % endif
</%def>

<%def name="content_title()">
  ${instance_title}
</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Permalink for this {}".format(model_title), action_url('view', instance))}</li>
  % if master.has_versions and request.rattail_config.versioning_enabled() and request.has_perm('{}.versions'.format(permission_prefix)):
      <li>${h.link_to("Version History", action_url('versions', instance))}</li>
  % endif
  % if master.editable and instance_editable and request.has_perm('{}.edit'.format(permission_prefix)):
      <li>${h.link_to("Edit this {}".format(model_title), action_url('edit', instance))}</li>
  % endif
  % if master.deletable and instance_deletable and request.has_perm('{}.delete'.format(permission_prefix)):
      <li>${h.link_to("Delete this {}".format(model_title), action_url('delete', instance), class_='delete-instance')}</li>
  % endif
  % if master.creatable and master.show_create_link and request.has_perm('{}.create'.format(permission_prefix)):
      % if master.creates_multiple:
          <li>${h.link_to("Create new {}".format(model_title_plural), url('{}.create'.format(route_prefix)))}</li>
      % else:
          <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
      % endif
  % endif
  % if master.cloneable and request.has_perm('{}.clone'.format(permission_prefix)):
      <li>${h.link_to("Clone this as new {}".format(model_title), url('{}.clone'.format(route_prefix), uuid=instance.uuid))}</li>
  % endif
  % if master.touchable and request.has_perm('{}.touch'.format(permission_prefix)):
      <li>${h.link_to("\"Touch\" this {}".format(model_title), url('{}.touch'.format(route_prefix), uuid=instance.uuid))}</li>
  % endif
  % if master.has_rows and master.rows_downloadable_csv and request.has_perm('{}.row_results_csv'.format(permission_prefix)):
      <li>${h.link_to("Download row results as CSV", url('{}.row_results_csv'.format(route_prefix), uuid=instance.uuid))}</li>
  % endif
  % if master.has_rows and master.rows_downloadable_xlsx and request.has_perm('{}.row_results_xlsx'.format(permission_prefix)):
      <li>${h.link_to("Download row results as XLSX", url('{}.row_results_xlsx'.format(route_prefix), uuid=instance.uuid))}</li>
  % endif
</%def>

<%def name="object_helpers()"></%def>


<div style="display: flex; justify-content: space-between;">

  <div class="form-wrapper">
    ${form.render()|n}
  </div><!-- form-wrapper -->

  <div style="display: flex;">
    <div class="object-helpers">
      ${self.object_helpers()}
    </div>

    <ul id="context-menu">
      ${self.context_menu_items()}
    </ul>
  </div>

</div>

% if master.has_rows:
    % if use_buefy:
        <br /><br />
        ## TODO: stop using |n filter
        ${rows_grid.render_buefy(allow_save_defaults=False, tools=rows_grid_tools)|n}
    % else:
        ## no buefy, so do the traditional thing
        ${rows_grid|n}
    % endif
% endif
