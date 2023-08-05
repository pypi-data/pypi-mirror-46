## -*- coding: utf-8; -*-

<%def name="feedback_dialog()">
  <div id="feedback-template" style="display: none;">
    ${h.form(url('feedback'))}
    ${h.csrf_token(request)}
    ${h.hidden('user', value=request.user.uuid if request.user else None)}
    <div class="modal-card feedback-dialog">

      <header class="modal-card-head">
        <p class="modal-card-title">User Feedback</p>
      </header>

      <section class="modal-card-body">
        <p>
          Questions, suggestions, comments, complaints, etc.
          <span class="red">regarding this website</span> are
          welcome and may be submitted below.
        </p>

        <b-field label="User Name">
          % if request.user:
              <b-input
                 value="${six.text_type(request.user)}"
                 disabled="true">
              </b-input>
          % else:
              <b-input
                 name="user_name">
              </b-input>
          % endif
        </b-field>
        % if request.user:
            <b-input
               name="user_name"
               type="hidden"
               value="${six.text_type(request.user)}">
            </b-input>
        % endif

        <b-field label="Referring URL">
          <b-input
             :value="referrer"
             disabled="true">
          </b-input>
        </b-field>
        <b-input
           name="referrer"
           type="hidden"
           :value="referrer">
        </b-input>

        <b-field label="Message">
          <b-input
             name="message"
             type="textarea">
          </b-input>
        </b-field>

      </section>

      <footer class="modal-card-foot">
        <button type="button" class="button" @click="$parent.close()">Cancel</button>
        <button type="button" class="button is-primary" @click="sendFeedback()">Send</button>
      </footer>
    </div>
    ${h.end_form()}
  </div>
</%def>
