// Global application module.
var Hawat = (function () {

    function _build_param_builder(skeleton, rules) {
        //var _skeleton = Object.assign({}, skeleton);
        var _skeleton = skeleton;
        var _rules = rules;
        return function(value) {
            //var _result = Object.assign({}, _skeleton);
            var _result = _skeleton;
            _rules.forEach(function(r) {
                _result[r[0]] = value;
            });
            return _result;
        }
    }

    var _csag = {
{%- for csag_name in hawat_current_app.csag.keys() | sort %}
        '{{ csag_name }}': [
    {%- for csag in hawat_current_app.csag[csag_name] %}
            {
                'title':    '{{ _(csag.title, name = '{name}') }}',
                'endpoint': '{{ csag.view.get_view_endpoint() }}',
                'icon':     '{{ get_icon(csag.view.get_menu_icon()) }}',
                'params':   _build_param_builder(
                    {{ csag.params.skeleton | tojson | safe }},
                    {{ csag.params.rules | tojson | safe }}
                )
            }{%- if not loop.last %},{%- endif %}
    {%- endfor %}
        ]{%- if not loop.last %},{%- endif %}
{%- endfor %}
    };

    return {
        get_csags: function() {
            return _csag;
        },

        get_csag: function(name) {
            try {
                return _csag[name];
            }
            catch (err) {
                return null
            }
        }
    };
})();
