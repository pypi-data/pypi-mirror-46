## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">New ${model_title_plural if master.creates_multiple else model_title}</%def>

<%def name="context_menu_items()"></%def>

<div style="display: flex; justify-content: space-between;">

  <div class="form-wrapper">
    ${form.render()|n}
  </div><!-- form-wrapper -->

  <ul id="context-menu">
    ${self.context_menu_items()}
  </ul>

</div>
