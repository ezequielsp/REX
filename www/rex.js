Ext.application({
    name: 'REX',
    appFolder: 'app',
    requires: ['Ext.container.Viewport'],
    
    controllers: [
    	'Header',
    	'Input',
    	'Result'
    ],

    launch: function() {
        Ext.create('Ext.container.Viewport', {
            layout: 'border',
            items: [
            	{
			        xtype: 'rexheader',
			        id: 'rex-header'
			    },
            	{
                    xtype: 'rexinput',
                    id: 'rex-input'
                },
                {
                    xtype: 'rexresult',
                    id: 'rex-result'
                }
            ]
        });
    }
});