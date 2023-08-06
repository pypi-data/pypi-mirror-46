Ext.define('Ext.m3.MenuItem', {
    extend: 'Ext.menu.Item',
    xtype: 'm3-menuitem',

    bubbleEvents: [
        'gethandler'
    ],

    initComponent: function () {
        this.callParent();

        if (typeof this.handler === 'string') {
            this.fireEvent('gethandler', this, this.handler,
                function (newHandler) {
                    if (newHandler) {
                        this.setHandler(newHandler, this);
                    }
                }.bind(this)
            );
        }
    },

    // setBlocked: function(blocked, exclude) {
    //     if (!includeInArr(exclude, this.itemId)) {
    //         this.setDisabled(blocked);
    //     }
    // }
});
