## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<div id="profile-info-app">
  <b-tabs v-model="activeTab" type="is-boxed">

    <b-tab-item label="Personal" icon="check" icon-pack="fas">
      <div style="display: flex; justify-content: space-between;">

        <div>

          <div class="field-wrapper first_name">
            <div class="field-row">
              <label>First Name</label>
              <div class="field">
                ${person.first_name}
              </div>
            </div>
          </div>

          <div class="field-wrapper middle_name">
            <div class="field-row">
              <label>Middle Name</label>
              <div class="field">
                ${person.middle_name}
              </div>
            </div>
          </div>

          <div class="field-wrapper last_name">
            <div class="field-row">
              <label>Last Name</label>
              <div class="field">
                ${person.last_name}
              </div>
            </div>
          </div>

          <div class="field-wrapper street">
            <div class="field-row">
              <label>Street 1</label>
              <div class="field">
                ${person.address.street if person.address else ''}
              </div>
            </div>
          </div>

          <div class="field-wrapper street2">
            <div class="field-row">
              <label>Street 2</label>
              <div class="field">
                ${person.address.street2 if person.address else ''}
              </div>
            </div>
          </div>

          <div class="field-wrapper city">
            <div class="field-row">
              <label>City</label>
              <div class="field">
                ${person.address.city if person.address else ''}
              </div>
            </div>
          </div>

          <div class="field-wrapper state">
            <div class="field-row">
              <label>State</label>
              <div class="field">
                ${person.address.state if person.address else ''}
              </div>
            </div>
          </div>

          <div class="field-wrapper zipcode">
            <div class="field-row">
              <label>Zipcode</label>
              <div class="field">
                ${person.address.zipcode if person.address else ''}
              </div>
            </div>
          </div>

          % if person.phones:
              % for phone in person.phones:
                  <div class="field-wrapper">
                    <div class="field-row">
                      <label>Phone Number</label>
                      <div class="field">
                        ${phone.number} (type: ${phone.type})
                      </div>
                    </div>
                  </div>
              % endfor
          % else:
              <div class="field-wrapper">
                <div class="field-row">
                  <label>Phone Number</label>
                  <div class="field">
                    (none on file)
                  </div>
                </div>
              </div>
          % endif

          % if person.emails:
              % for email in person.emails:
                  <div class="field-wrapper">
                    <div class="field-row">
                      <label>Email Address</label>
                      <div class="field">
                        ${email.address} (type: ${email.type})
                      </div>
                    </div>
                  </div>
              % endfor
          % else:
              <div class="field-wrapper">
                <div class="field-row">
                  <label>Email Address</label>
                  <div class="field">
                    (none on file)
                  </div>
                </div>
              </div>
          % endif

        </div>

        <div>
          % if request.has_perm('people.view'):
              ${h.link_to("View Person", url('people.view', uuid=person.uuid), class_='button')}
          % endif
        </div>

      </div>
    </b-tab-item><!-- Personal -->

    <b-tab-item label="Customer" ${'icon="check" icon-pack="fas"' if person.customers else ''|n}>
      % if person.customers:
          <p>${person} is associated with <strong>${len(person.customers)}</strong> customer account(s)</p>
          <br />
          <div id="customers-accordion">
            % for customer in person.customers:

                <b-collapse class="panel"
                            ## TODO: what's up with aria-id here?
                            ## aria-id="contentIdForA11y2"
                            >

                  <div
                     slot="trigger"
                     class="panel-heading"
                     role="button"
                     ## TODO: what's up with aria-id here?
                     ## aria-controls="contentIdForA11y2"
                     >
                    <strong>${customer.id} - ${customer.name}</strong>
                  </div>

                  <div class="panel-block">

                    <div style="display: flex; justify-content: space-between; width: 100%;">

                      <div>

                        <div class="field-wrapper id">
                          <div class="field-row">
                            <label>ID</label>
                            <div class="field">
                              ${customer.id or ''}
                            </div>
                          </div>
                        </div>

                        <div class="field-wrapper name">
                          <div class="field-row">
                            <label>Name</label>
                            <div class="field">
                              ${customer.name}
                            </div>
                          </div>
                        </div>

                        % if customer.phones:
                            % for phone in customer.phones:
                                <div class="field-wrapper">
                                  <div class="field-row">
                                    <label>Phone Number</label>
                                    <div class="field">
                                      ${phone.number} (type: ${phone.type})
                                    </div>
                                  </div>
                                </div>
                            % endfor
                        % else:
                            <div class="field-wrapper">
                              <div class="field-row">
                                <label>Phone Number</label>
                                <div class="field">
                                  (none on file)
                                </div>
                              </div>
                            </div>
                        % endif

                        % if customer.emails:
                            % for email in customer.emails:
                                <div class="field-wrapper">
                                  <div class="field-row">
                                    <label>Email Address</label>
                                    <div class="field">
                                      ${email.address} (type: ${email.type})
                                    </div>
                                  </div>
                                </div>
                            % endfor
                        % else:
                            <div class="field-wrapper">
                              <div class="field-row">
                                <label>Email Address</label>
                                <div class="field">
                                  (none on file)
                                </div>
                              </div>
                            </div>
                        % endif

                      </div>

                      <div>
                        % if request.has_perm('customers.view'):
                            ${h.link_to("View Customer", url('customers.view', uuid=customer.uuid), class_='button')}
                        % endif
                      </div>

                    </div>

                  </div>
                </b-collapse>
            % endfor
          </div>

      % else:
          <p>${person} has never been a customer.</p>
      % endif
    </b-tab-item><!-- Customer -->

    <b-tab-item label="Employee" ${'icon="check" icon-pack="fas"' if employee else ''|n}>

      % if employee:
          <div style="display: flex; justify-content: space-between;">

            <div>

              <div class="field-wrapper id">
                <div class="field-row">
                  <label>ID</label>
                  <div class="field">
                    ${employee.id or ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper display_name">
                <div class="field-row">
                  <label>Display Name</label>
                  <div class="field">
                    ${employee.display_name or ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper status">
                <div class="field-row">
                  <label>Status</label>
                  <div class="field">
                    ${enum.EMPLOYEE_STATUS.get(employee.status, '')}
                  </div>
                </div>
              </div>

              % if employee.phones:
                  % for phone in employee.phones:
                      <div class="field-wrapper">
                        <div class="field-row">
                          <label>Phone Number</label>
                          <div class="field">
                            ${phone.number} (type: ${phone.type})
                          </div>
                        </div>
                      </div>
                  % endfor
              % else:
                  <div class="field-wrapper">
                    <div class="field-row">
                      <label>Phone Number</label>
                      <div class="field">
                        (none on file)
                      </div>
                    </div>
                  </div>
              % endif

              % if employee.emails:
                  % for email in employee.emails:
                      <div class="field-wrapper">
                        <div class="field-row">
                          <label>Email Address</label>
                          <div class="field">
                            ${email.address} (type: ${email.type})
                          </div>
                        </div>
                      </div>
                  % endfor
              % else:
                  <div class="field-wrapper">
                    <div class="field-row">
                      <label>Email Address</label>
                      <div class="field">
                        (none on file)
                      </div>
                    </div>
                  </div>
              % endif

            </div>

            <div>
              % if request.has_perm('employees.view'):
                  ${h.link_to("View Employee", url('employees.view', uuid=employee.uuid), class_='button')}
              % endif
            </div>

          </div>

      % else:
          <p>${person} has never been an employee.</p>
      % endif
    </b-tab-item><!-- Employee -->

    <b-tab-item label="User" ${'icon="check" icon-pack="fas"' if person.users else ''|n}>
      % if person.users:
          <p>${person} is associated with <strong>${len(person.users)}</strong> user account(s)</p>
          <br />
          <div id="users-accordion">
            % for user in person.users:

                <b-collapse class="panel"
                            ## TODO: what's up with aria-id here?
                            ## aria-id="contentIdForA11y2"
                            >

                  <div
                     slot="trigger"
                     class="panel-heading"
                     role="button"
                     ## TODO: what's up with aria-id here?
                     ## aria-controls="contentIdForA11y2"
                     >
                    <strong>${user.username}</strong>
                  </div>

                  <div class="panel-block">

                    <div style="display: flex; justify-content: space-between; width: 100%;">

                      <div>

                        <div class="field-wrapper id">
                          <div class="field-row">
                            <label>Username</label>
                            <div class="field">
                              ${user.username}
                            </div>
                          </div>
                        </div>

                      </div>

                      <div>
                        % if request.has_perm('users.view'):
                            ${h.link_to("View User", url('users.view', uuid=user.uuid), class_='button')}
                        % endif
                      </div>

                    </div>

                  </div>
                </b-collapse>
            % endfor
          </div>

      % else:
          <p>${person} has never been a user.</p>
      % endif
    </b-tab-item><!-- User -->

  </b-tabs>
</div>

<script type="text/javascript">

  new Vue({
      el: '#profile-info-app',
      data() {
          return {
              activeTab: 0
          }
      }
  })

</script>
