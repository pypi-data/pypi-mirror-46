## -*- coding: utf-8; -*-
<%inherit file="/principal/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if expose_vuejs_experiments:
      <li>${h.link_to("Vue.js Index", url('{}.vue_index'.format(route_prefix)))}</li>
  % endif
</%def>

${parent.body()}
