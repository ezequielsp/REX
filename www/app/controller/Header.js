Ext.define('REX.controller.Header', {
    extend: 'Ext.app.Controller',
    
    views: [
    	'Header',
    ],
    
    init: function() {
        this.control({
            'rexheader': {
                render: this.getHeaderHtml
            }
        });
    },

    getHeaderHtml: function() {
        //console.log('The header panel was rendered');
        Ext.Ajax.request({
		    url: 'getPageHeader',
		    method: 'POST',
		    success: function(response, opts) {
		        var obj = Ext.decode(response.responseText);
		        //console.dir(obj);
		        Ext.getCmp('rex-header').update(obj['html']);
		    }
		});
    }
});