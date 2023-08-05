## -*- coding: utf-8; -*-

<form action="${form.action_url}" method="GET" v-on:submit.prevent="applyFilters()">

  <grid-filter v-for="key in filtersSequence"
               :key="key"
               :filter="filters[key]"
               ref="gridFilters">
  </grid-filter>

  <b-field grouped>

    <b-button type="is-primary"
              native-type="submit"
              icon-pack="fas"
              icon-left="check"
              class="control">
      Apply Filters
    </b-button>

    <b-select @input="addFilter"
              placeholder="Add Filter"
              v-model="selectedFilter">
      <option v-for="key in filtersSequence"
              :key="key"
              :value="key"
              :disabled="filters[key].visible">
        {{ filters[key].label }}
      </option>
    </b-select>

    <b-button @click="resetView()"
              icon-pack="fas"
              icon-left="home"
              class="control">
      Default View
    </b-button>

    <b-button @click="clearFilters()"
              icon-pack="fas"
              icon-left="trash"
              class="control">
      No Filters
    </b-button>

    % if allow_save_defaults and request.user:
        <b-button @click="saveDefaults()"
                  icon-pack="fas"
                  icon-left="save"
                  class="control">
          Save Defaults
        </b-button>
    % endif

  </b-field>

</form>
