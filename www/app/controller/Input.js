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
    	var flags = '';
    	
    	/** Build flags string here, thus leading to a cleaner and nicer code on server side **/
    	form.getForm().getValues()['ignore-case'] ? flags = flags.concat('re.IGNORECASE|') : false;
    	form.getForm().getValues()['locale'] ? flags = flags.concat('re.LOCALE|') : false;
    	form.getForm().getValues()['multi-line'] ? flags = flags.concat('re.MULTILINE|') : false;
    	form.getForm().getValues()['dot-all'] ? flags = flags.concat('re.DOTALL|') : false;
    	form.getForm().getValues()['unicode'] ? flags = flags.concat('re.UNICODE|') : false;
    	form.getForm().getValues()['verbose'] ? flags = flags.concat('re.VERBOSE|') : false;
    	
    	Ext.Ajax.request({
		    url: 'getResult',
		    method: 'POST',
		    params: {
		    	regex: form.getForm().getValues()['regex'],
		    	input_text: form.getForm().getValues()['input_text'],
		    	flags: flags
		    },
		    success: function(response, opts) {
		        var obj = Ext.decode(response.responseText);
		        //console.dir(obj);
		        Ext.getCmp('rex-result').update(obj['html']);
		    }
		});
    }
});