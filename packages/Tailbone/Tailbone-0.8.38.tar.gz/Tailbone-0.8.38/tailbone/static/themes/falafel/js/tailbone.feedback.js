
const FeedbackForm = {
    props: ['user_name', 'referrer'],
    template: '#feedback-template',
    methods: {
        sendFeedback() {

            var textarea = $('.feedback-dialog textarea');
            var msg = $.trim(textarea.val());
            if (! msg) {
                alert("Please enter a message.");
                textarea.select();
                textarea.focus();
                return;
            }

            // disable_button(dialog_button(event));

            var form = $('.feedback-dialog').parents('form');
            // TODO: this was copied from default template, but surely we could
            // just serialize() the form instead?
            var data = {
                _csrf: form.find('input[name="_csrf"]').val(),
                referrer: location.href,
                user: form.find('input[name="user"]').val(),
                user_name: form.find('input[name="user_name"]').val(),
                message: msg
            };

            var that = this;
            $.ajax(form.attr('action'), {
                method: 'POST',
                data: data,
                success: function(data) {
                    that.$emit('close');
                    alert("Message successfully sent.\n\nThank you for your feedback.");
                }
            });

        }
    }
}

new Vue({
    el: '#feedback-app',
    methods: {
        showFeedback() {
            this.$modal.open({
                parent: this,
                canCancel: ['escape', 'x'],
                component: FeedbackForm,
                hasModalCard: true,
                props: {
                    referrer: location.href
                }
            });
        }
    }
});
