
const GridFilter = {
    template: '#grid-filter-template',
    props: {
        filter: Object
    },

    methods: {

        changeVerb() {
            // set focus to value input, "as quickly as we can"
            this.$nextTick(function() {
                this.focusValue()
            })
        },

        focusValue: function() {
            this.$refs.valueInput.focus()
            // this.$refs.valueInput.select()
        }
    }
}

Vue.component('grid-filter', GridFilter)
