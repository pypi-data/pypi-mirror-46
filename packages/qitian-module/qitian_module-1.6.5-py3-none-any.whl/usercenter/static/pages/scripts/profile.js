let Profile = function () {

    let dashboardMainChart = null;

    return {
        //main function
        init: function () {
            Profile.initMiniCharts();
            $('#passwd_form').validate({
                rules: {
                    old_password: {
                        required: true,
                        remote: {
                            url: '/uc/check_password/',
                            type: 'post',
                            dataType: 'json',
                            data: {
                                password: $('#old_password').val(),
                            },
                        },
                    },
                    password: {
                        required: true,
                    },
                    re_password: {
                        required: true,
                        equalTo: '#password',
                    },

                },
                messages: {
                    old_password: {
                        required: '请验证旧密码',
                        remote: '原密码不正确。',
                    },
                    password: {
                        required: '请输入密码',
                    },
                    re_password: {
                        required: '请确认密码',
                        equalTo: '二次密码输入不一致，请检查更正。'
                    },

                }
            });
        },

        initMiniCharts: function () {

            // IE8 Fix: function.bind polyfill
            if (App.isIE8() && !Function.prototype.bind) {
                Function.prototype.bind = function (oThis) {
                    if (typeof this !== "function") {
                        // closest thing possible to the ECMAScript 5 internal IsCallable function
                        throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
                    }

                    var aArgs = Array.prototype.slice.call(arguments, 1),
                        fToBind = this,
                        fNOP = function () {
                        },
                        fBound = function () {
                            return fToBind.apply(this instanceof fNOP && oThis ? this : oThis,
                                aArgs.concat(Array.prototype.slice.call(arguments)));
                        };

                    fNOP.prototype = this.prototype;
                    fBound.prototype = new fNOP();

                    return fBound;
                };
            }

            $("#sparkline_bar").sparkline([8, 9, 10, 11, 10, 10, 12, 10, 10, 11, 9, 12, 11], {
                type: 'bar',
                width: '100',
                barWidth: 6,
                height: '45',
                barColor: '#F36A5B',
                negBarColor: '#e02222'
            });

            $("#sparkline_bar2").sparkline([9, 11, 12, 13, 12, 13, 10, 14, 13, 11, 11, 12, 11], {
                type: 'bar',
                width: '100',
                barWidth: 6,
                height: '45',
                barColor: '#5C9BD1',
                negBarColor: '#e02222'
            });
        }

    };

}();

if (App.isAngularJsApp() === false) {
    jQuery(document).ready(function () {
        Profile.init();
    });
}

function reset_from(form_name) {
    document[form_name].reset();
}

function check_passwd() {
    if ($('#password').val() != $('#re_password').val()) {

    }
}