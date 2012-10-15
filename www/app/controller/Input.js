Ext.define('REX.controller.Input', {
    extend: 'Ext.app.Controller',
    
    views: [
    	'Input',
    ],
    
    init: function() {
        this.control({
        	'button[action=submit]': {
        		click: this.submitForm
        	}
        });
    },
    
    submitForm: function() {
    	var form = Ext.getCmp('rex-input');
    	Ext.Ajax.request({
		    url: 'getResult',
		    method: 'POST',
		    params: {
		    	regex: form.getForm().getValues()['regex'],
		    	ignore_case: form.getForm().getValues()['ignore-case'] ? 'True' : 'False',
		    	locale: form.getForm().getValues()['locale'] ? 'True' : 'False',
		    	multi_line: form.getForm().getValues()['multi-line'] ? 'True' : 'False',
		    	dot_all: form.getForm().getValues()['dot-all'] ? 'True' : 'False',
		    	unicode: form.getForm().getValues()['unicode'] ? 'True' : 'False',
		    	verbose: form.getForm().getValues()['verbose'] ? 'True' : 'False',
		    	input_text: form.getForm().getValues()['input_text']
		    },
		    success: function(response, opts) {
		        var obj = Ext.decode(response.responseText);
		        //console.dir(obj);
		        Ext.getCmp('rex-result').update(obj['html']);
		    }
		});
    }
});