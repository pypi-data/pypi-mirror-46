## -*- coding: utf-8; -*-

<script type="text/x-template" id="grid-filter-template">

  <div class="level filter" v-show="filter.visible">
    <div class="level-left">

      <div class="level-item">

        <b-field>
          <b-checkbox-button v-model="filter.active" native-value="IGNORED">
            <b-icon pack="fas" icon="check" v-show="filter.active"></b-icon>
            <span>{{ filter.label }}</span>
          </b-checkbox-button>
        </b-field>

      </div>

      <b-field grouped v-show="filter.active" custom-class="level-item">

        <b-select v-model="filter.verb"
                  @input="focusValue()">
          <option v-for="verb in filter.verbs"
                  :key="verb"
                  :value="verb">
            {{ filter.verb_labels[verb] }}
          </option>
        </b-select>

        <b-input v-model="filter.value"
                 v-show="! (filter.valueless_verbs && filter.valueless_verbs.includes(filter.verb))"
                 ref="valueInput">
        </b-input>

      </b-field>

    </div><!-- level-left -->
  </div><!-- level -->

</script>


<div id="buefy-grid-app">

  <div style="display: flex; justify-content: space-between; margin-bottom: 0.5em;">

    <div style="display: flex; flex-direction: column; justify-content: space-between;">
      <div></div>
      <div class="filters">
        % if grid.filterable:
            ## TODO: stop using |n filter
            ${grid.render_filters(allow_save_defaults=allow_save_defaults)|n}
        % endif
      </div>
    </div>

    <div style="display: flex; flex-direction: column; justify-content: space-between;">

      <div class="context-menu">
        % if context_menu:
            <ul id="context-menu">
              ## TODO: stop using |n filter
              ${context_menu|n}
            </ul>
        % endif
      </div>

      <div class="grid-tools-wrapper">
        % if tools:
            <div class="grid-tools field is-grouped">
              ## TODO: stop using |n filter
              ${tools|n}
            </div>
        % endif
      </div>

    </div>

  </div>

  <b-table
     :data="data"
     :columns="columns"
     :loading="loading"
     :row-class="getRowClass"

     % if grid.checkboxes:
     checkable
     :checked-rows.sync="checkedRows"
     ## TODO: definitely will be wanting this...
     ## :is-row-checkable=""
     % endif

     :default-sort="[sortField, sortOrder]"
     backend-sorting
     @sort="onSort"

     % if grid.pageable:
     paginated
     :per-page="perPage"
     :current-page="page"
     backend-pagination
     :total="total"
     @page-change="onPageChange"
     % endif

     ## TODO: should let grid (or master view) decide how to set these?
     icon-pack="fas"
     ## note that :striped="true" was interfering with row status (e.g. warning) styles
     :striped="false"
     :hoverable="true"
     :narrowed="true">

    <template slot-scope="props">
      % for column in grid_columns:
          <b-table-column field="${column['field']}" label="${column['label']}" ${'sortable' if column['sortable'] else ''}>
            % if grid.is_linked(column['field']):
                <a :href="props.row._action_url_view" v-html="props.row.${column['field']}"></a>
            % else:
                <span v-html="props.row.${column['field']}"></span>
            % endif
          </b-table-column>
      % endfor

      % if grid.main_actions or grid.more_actions:
          <b-table-column field="actions" label="Actions">
            % for action in grid.main_actions:
                <a :href="props.row._action_url_${action.key}"><i class="fas fa-${action.icon}"></i>
                  ${action.label}
                </a>
            % endfor
          </b-table-column>
      % endif
    </template>

    <template slot="empty">
      <section class="section">
        <div class="content has-text-grey has-text-centered">
          <p>
            <b-icon
               pack="fas"
               icon="fas fa-sad-tear"
               size="is-large">
            </b-icon>
          </p>
          <p>Nothing here.</p>
        </div>
      </section>
    </template>

    % if grid.pageable and grid.pager:
    <template slot="footer">
      <div class="has-text-right">showing {{ firstItem }} - {{ lastItem }} of {{ total }} results</div>
    </template>
    % endif

  </b-table>
</div>

<script type="text/javascript">

  new Vue({
      el: '#buefy-grid-app',
      data() {
          return {
              data: ${json.dumps(grid_data['data'])|n},
              loading: false,
              sortField: '${grid.sortkey}',
              sortOrder: '${grid.sortdir}',
              rowStatusMap: ${json.dumps(grid_data['row_status_map'])|n},
              ## TODO: should be dumping json from server here
              checkedRows: [],

              % if grid.pageable:
              % if static_data:
              total: ${len(grid_data['data'])},
              % else:
              total: ${grid_data['total_items']},
              % endif
              perPage: ${grid.pagesize},
              page: ${grid.page},
              firstItem: ${json.dumps(grid_data['first_item'])|n},
              lastItem: ${json.dumps(grid_data['last_item'])|n},
              % endif

              % if grid.filterable:
              filters: ${json.dumps(filters_data)|n},
              filtersSequence: ${json.dumps(filters_sequence)|n},
              selectedFilter: null,
              % endif
          }
      },
      methods: {

          getRowClass(row, index) {
              return this.rowStatusMap[index]
          },

          loadAsyncData(params) {

              if (params === undefined) {
                  params = [
                      'partial=true',
                      `sortkey=${'$'}{this.sortField}`,
                      `sortdir=${'$'}{this.sortOrder}`,
                      `pagesize=${'$'}{this.perPage}`,
                      `page=${'$'}{this.page}`
                  ].join('&')
              }

              this.loading = true
              this.$http.get(`${request.current_route_url(_query=None)}?${'$'}{params}`).then(({ data }) => {
                  this.data = data.data
                  this.rowStatusMap = data.row_status_map
                  this.total = data.total_items
                  this.firstItem = data.first_item
                  this.lastItem = data.last_item
                  this.loading = false
              })
              .catch((error) => {
                  this.data = []
                  this.total = 0
                  this.loading = false
                  throw error
              })
          },

          onPageChange(page) {
              this.page = page
              this.loadAsyncData()
          },

          onSort(field, order) {
              this.sortField = field
              this.sortOrder = order
              // always reset to first page when changing sort options
              // TODO: i mean..right? would we ever not want that?
              this.page = 1
              this.loadAsyncData()
          },

          resetView() {
              this.loading = true
              location.href = '?reset-to-default-filters=true'
          },

          addFilter(filter_key) {

              // reset dropdown so user again sees "Add Filter" placeholder
              this.$nextTick(function() {
                  this.selectedFilter = null
              })

              // show corresponding grid filter
              this.filters[filter_key].visible = true
              this.filters[filter_key].active = true

              // track down the component
              var gridFilter = null
              for (var gf of this.$refs.gridFilters) {
                  if (gf.filter.key == filter_key) {
                      gridFilter = gf
                      break
                  }
              }

              // tell component to focus the value field, ASAP
              this.$nextTick(function() {
                  gridFilter.focusValue()
              })

          },

          applyFilters(params) {
              if (params === undefined) {
                  params = []
              }

              params.push('partial=true')
              params.push('filter=true')

              for (var key in this.filters) {
                  var filter = this.filters[key]
                  if (filter.active) {
                      params.push(key + '=' + encodeURIComponent(filter.value))
                      params.push(key + '.verb=' + encodeURIComponent(filter.verb))
                  } else {
                      filter.visible = false
                  }
              }

              this.loadAsyncData(params.join('&'))
          },

          clearFilters() {

              // explicitly deactivate all filters
              for (var key in this.filters) {
                  this.filters[key].active = false
              }

              // then just "apply" as normal
              this.applyFilters()
          },

          saveDefaults() {

              // apply current filters as normal, but add special directive
              const params = ['save-current-filters-as-defaults=true']
              this.applyFilters(params)
          },

          deleteResults(event) {

              // submit form if user confirms
              if (confirm("You are about to delete " + this.total + " ${grid.model_title_plural}.\n\nAre you sure?")) {
                  event.target.form.submit()
              }
          },

          checkedRowUUIDs() {
              var uuids = [];
              for (var row of this.$data.checkedRows) {
                  uuids.push(row.uuid)
              }
              return uuids
          }
      }

  });

</script>
