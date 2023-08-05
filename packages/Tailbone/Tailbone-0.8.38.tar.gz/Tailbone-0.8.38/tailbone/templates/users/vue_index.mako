## -*- coding: utf-8; -*-
<%inherit file="/users/index.mako" />

## <%def name="head_tags()">
##   ${parent.head_tags()}
##   ## TODO: this is needed according to Bulma docs?
##   ## https://bulma.io/documentation/overview/start/#code-requirements
##   <meta name="viewport" content="width=device-width, initial-scale=1">
## </%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}

  <!-- vue -->
  ${h.javascript_link('https://cdn.jsdelivr.net/npm/vue')}

  <!-- vuex -->
  ${h.javascript_link('https://unpkg.com/vuex')}

  <!-- vue-tables-2 -->
  ${h.javascript_link('https://cdn.jsdelivr.net/npm/vue-tables-2@1.4.70/dist/vue-tables-2.min.js')}
  ## ${h.javascript_link(request.static_url('tailbone:static/js/lib/vue-tables.js'))}

  <!-- bulma -->
  ${h.stylesheet_link('https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css')}

  <!-- fontawesome -->
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">

  <style type="text/css">
    /* workaround for header logo, needed for Bulma (ugh) */
    ## TODO: this img should be 49px for height, what gives here?
    .home img { height: 59px; }
  </style>

</%def>

<div id="vue-app">

  ## TODO: need to make endpoint a bit more configurable somehow
  <v-server-table name="users" url="/api/users" :columns="columns" :options="options">

    ## TODO: make URLs more flexible / configurable... also perms?
    % if request.has_perm('users.view'):
        <span slot="username" slot-scope="props"><a :href="'/users/'+props.row.uuid">{{ props.row.username }}</a></span>
        <span slot="person_display_name" slot-scope="props"><a :href="'/users/'+props.row.uuid">{{ props.row.person_display_name }}</a></span>
    % endif

    ## TODO: why on earth doesn't it render bool as string by default?
    <span slot="active" slot-scope="props">{{ props.row.active }}</span>

    ## TODO: make URLs more flexible / configurable... also perms?
    <span slot="actions" slot-scope="props">
      % if request.has_perm('users.view'):
          <a :href="'/users/'+props.row.uuid">View</a>
      % endif
      % if request.has_perm('users.edit'):
          | <a :href="'/users/'+props.row.uuid+'/edit'">Edit</a>
      % endif
    </span>

  </v-server-table>
</div>

<script type="text/javascript">

// Vue.use(Vuex);

var store = new Vuex.Store({
  // state: {
  //     appVersion: null,
  //     // TODO: is this really needed or can we just always check appsettings?
  //     production: appsettings.production,
  //     user: null,
  //     pageTitle: null
  // },
  // mutations: {
  //     setAppVersion(state, payload) {
  //         state.appVersion = payload;
  //     },
  //     setPageTitle(state, payload) {
  //         state.pageTitle = payload;
  //     },
  //     setUser(state, payload)  {
  //         state.user = payload;
  //     }
  // },
  // actions: {
  // }
})

Vue.use(VueTables.ServerTable, {
    sortIcon: {
        is: 'fa-sort',
        base: 'fas',
        up: 'fa-sort-up',
        down: 'fa-sort-down'
    }
}, true, 'bulma', 'default');

<%
   columns = [
       'username',
       'person_display_name',
       'active',
   ]
   if request.has_any_perm('users.view', 'users.edit'):
       columns.append('actions')
%>

var app = new Vue({
    el: '#vue-app',
    store: store,
    data: {
        columns: ${json.dumps(columns)|n},
        options: {
            columnsDropdown: true,
            filterable: false,
            headings: {
                person_display_name: "Person"
            },
            sortable: [
                'username',
                'person_display_name',
                'active'
            ],
            orderBy: {
                column: 'username',
                ascending: true
            },
            perPageValues: [10, 25, 50, 100, 200],
            // preserveState: true,
            saveState: true,
            // TODO: why doesn't local storage work?  but alas, table does not
            // properly submit the 'orderBy' param, and results aren't paginated
            storage: 'session'
        }
    }
});

// $.get('/api/users', {sort: 'username|desc', page: 1, per_page: 10}, function(data) {
//     app.users = data.users;
// });

</script>
