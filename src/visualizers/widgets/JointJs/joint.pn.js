define([], function () {
    'use strict';

    function addPetriNetDefinitions(joint) {
        joint.shapes.basic.Generic.define('pn.Place', {
            size: {width: 50, height: 50},
            attrs: {
                '.root': {
                    r: 25,
                    fill: '#888888',
                    stroke: '#000000',
                    'stroke-width': 3,
                    transform: 'translate(25, 25)'
                },
                '.label': {
                    'text-anchor': 'middle',
                    'ref-x': .5,
                    'ref-y': -20,
                    ref: '.root',
                    fill: '#000000',
                    'font-size': 12
                },
                '.tokens': {
                    fill: '#FFFFFF'
                },
                '.tokens > text': {
                    'font-size': 12
                },
                '.tokens .red': {
                    transform: 'translate(25, 3)',
                    'text-anchor': 'middle',
                    fill: '#FF0000'
                },
                '.tokens .blue': {
                    transform: 'translate(25, 18)',
                    'text-anchor': 'middle',
                    fill: '#0000FF'
                },
                '.tokens .yellow': {
                    transform: 'translate(25, 32)',
                    'text-anchor': 'middle',
                    fill: '#FFFF00'
                }
            }
        }, {
            markup: '<g class="rotatable"><g class="scalable"><circle class="root"/><g class="tokens" /></g><text class="label"/></g>',
        });

        joint.shapes.pn.PlaceView = joint.dia.ElementView.extend({

            initialize: function () {

                joint.dia.ElementView.prototype.initialize.apply(this, arguments);

                this.model.on('change:tokens', function () {

                    this.renderTokens();
                    this.update();

                }, this);
            },

            render: function () {

                joint.dia.ElementView.prototype.render.apply(this, arguments);

                this.renderTokens();
                this.update();
            },

            renderTokens: function () {
                var tokens = this.model.get('tokens'),
                    $tokens = this.$('.tokens').empty(),
                    $token;

                $tokens[0].className.baseVal = 'tokens';
                $token = joint.V('<text/>').text(tokens.red + '').node;
                $token.className.baseVal = 'red';
                $tokens[0].append($token);

                $token = joint.V('<text/>').text(tokens.blue + '').node;
                $token.className.baseVal = 'blue';
                $tokens[0].append($token);

                $token = joint.V('<text/>').text(tokens.yellow + '').node;
                $token.className.baseVal = 'yellow';
                $tokens[0].append($token);
            }
        });

        joint.shapes.basic.Generic.define('pn.Transition', {
            size: {width: 12, height: 50},
            attrs: {
                '.root': {
                    'fill': '#000000',
                    'stroke': '#000000'
                },
                'rect': {
                    width: 12,
                    height: 50,
                },
                '.label': {
                    'text-anchor': 'middle',
                    'ref-x': .5,
                    'ref-y': -20,
                    ref: 'rect',
                    fill: '#000000',
                    'font-size': 12
                }
            }
        }, {
            markup: '<g class="rotatable"><g class="scalable"><rect class="root"/></g></g><text class="label"/>',
        });

        joint.dia.Link.define('pn.Link', {
            attrs: {
                '.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'},
                '.connection': {
                    'fill': 'none',
                    'stroke-linejoin': 'round',
                    'stroke-width': '2',
                    'stroke': '#000000'
                }
            }
        });

    }

    return addPetriNetDefinitions;
});
