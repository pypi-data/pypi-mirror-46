## -*- coding: utf-8; -*-

<script type="text/x-template" id="buefy-form-template">
  % if not readonly:
  ${h.form(form.action_url, id=dform.formid, method='post', enctype='multipart/form-data', **form_kwargs)}
  ${h.csrf_token(request)}
  % endif

  <section>
    % for field in form.fields:
        <% field = dform[field] %>

        <b-field label="${form.get_label(field.name)}"
                 % if field.error:
                 type="is-danger"
                 :message='${form.messages_json(field.error.messages())|n}'
                 % endif
                 >
          ${field.serialize(use_buefy=True)|n}
        </b-field>

    % endfor
  </section>

  % if buttons:
      <br />
      ${buttons|n}
  % elif not readonly and (buttons is Undefined or (buttons is not None and buttons is not False)):
      <br />
      <div class="buttons">
        ${h.submit('save', getattr(form, 'submit_label', getattr(form, 'save_label', "Submit")), class_='button is-primary')}
        % if getattr(form, 'show_reset', False):
            <input type="reset" value="Reset" class="button" />
        % endif
        % if getattr(form, 'show_cancel', True):
            % if form.mobile:
                ${h.link_to("Cancel", form.cancel_url, class_='ui-btn ui-corner-all')}
            % else:
                ${h.link_to("Cancel", form.cancel_url, class_='cancel button{}'.format(' autodisable' if form.auto_disable_cancel else ''))}
            % endif
        % endif
      </div>
  % endif

  % if not readonly:
  ${h.end_form()}
  % endif
</script>


<div id="buefy-form-app">
  <buefy-form></buefy-form>
</div>


<script type="text/javascript">

  const BuefyForm = {
      template: '#buefy-form-template',
      methods: {

          formatDate(date) {
              // just need to convert to simple ISO date format here, seems
              // like there should be a more obvious way to do that?
              var year = date.getFullYear()
              var month = date.getMonth() + 1
              var day = date.getDate()
              month = month < 10 ? '0' + month : month
              day = day < 10 ? '0' + day : day
              return year + '-' + month + '-' + day
          },

          parseDate(date) {
              // note, this assumes classic YYYY-MM-DD (i.e. ISO?) format
              var parts = date.split('-')
              return new Date(parts[0], parseInt(parts[1]) - 1, parts[2])
          }
      }
  }

  Vue.component('buefy-form', BuefyForm)

  new Vue({
      el: '#buefy-form-app'
  })

</script>
