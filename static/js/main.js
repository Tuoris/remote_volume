var app = new Vue({
    el: '#app',
    created() {
        this.getLevel()
    },
    data: {
        level: 0,
        muted: false
    },
    methods: {
        getLevel: function () {
            self = this;
            axios({
                method: 'get',
                url: '/info',
            }).then(function (response) {
                self.level = response.data.level;
                self.muted = response.data.muted
            });
        },
        changeLevel: function () {
            axios({
                method: 'post',
                url: '/change_level',
                data: {
                    level: this.level
                }
            });
        },
        toggleMute: function () {
            this.muted = !this.muted;
            axios({
                method: 'post',
                url: '/mute',
                data: {
                    mute: this.muted
                }
            });
        }
    }
})