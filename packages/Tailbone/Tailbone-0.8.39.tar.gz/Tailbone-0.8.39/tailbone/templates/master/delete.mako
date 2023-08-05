## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Delete ${model_title}: ${instance_title}</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to {}".format(model_title_plural), url(route_prefix))}</li>
  % if master.viewable and request.has_perm('{}.view'.format(permission_prefix)):
      <li>${h.link_to("View this {}".format(model_title), action_url('view', instance))}</li>
  % endif
  % if master.editable and request.has_perm('{}.edit'.format(permission_prefix)):
      <li>${h.link_to("Edit this {}".format(model_title), action_url('edit', instance))}</li>
  % endif
  % if master.creatable and master.show_create_link and request.has_perm('{}.create'.format(permission_prefix)):
      <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
  % endif
</%def>

<%def name="confirmation()">
  <br />
  <p>Are you sure about this?</p>
  <br />

  ${h.form(request.current_route_url(), class_='autodisable')}
  ${h.csrf_token(request)}
    <div class="buttons">
      <a class="button" href="${form.cancel_url}">Whoops, nevermind...</a>
      ${h.submit('submit', "Yes, please DELETE this data forever!", class_='button is-primary')}
    </div>
  ${h.end_form()}
</%def>

<div style="display: flex; justify-content: space-between;">

  <div>
    <br />
    <p>You are about to delete the following ${model_title} and all associated data:</p>

    <div class="form-wrapper">
      ${form.render()|n}
    </div><!-- form-wrapper -->

    ${self.confirmation()}
  </div>

  <ul id="context-menu">
    ${self.context_menu_items()}
  </ul>

</div>
