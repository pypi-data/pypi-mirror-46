## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {
        $('#restart-client').click(function() {
            disable_button(this);
            location.href = '${url('tempmon.clients.restart', uuid=instance.uuid)}';
        });
    });
  </script>
</%def>

<%def name="object_helpers()">
  % if instance.enabled and master.restartable_client(instance) and request.has_perm('{}.restart'.format(route_prefix)):
      <div class="object-helper">
        <h3>Client Tools</h3>
        <div class="object-helper-content">
          <button type="button" id="restart-client">Restart tempmon-client daemon</button>
        </div>
      </div>
  % endif
</%def>

${parent.body()}
