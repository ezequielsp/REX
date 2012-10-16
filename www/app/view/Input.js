Ext.define('REX.view.Input' ,{
    extend: 'Ext.form.Panel',
    alias: 'widget.rexinput',
    
    region: 'west',
    title: 'REX input',
    
    width: '45%',
    bodyStyle: 'padding-top: 15; padding-left: 5; padding-right: 5; padding-bottom: 5',
    
    items: [
    	{
    		xtype: 'textarea',
    		fieldLabel: 'Regular expression',
    		name: 'regex',
    		height: 100,
    		anchor: '100%'
    	},
    	{
    		xtype: 'fieldset',
            flex: 1,
            title: 'Regular expression flags',
            anchor: '100%',
            layout: 'column', // arrange fieldsets side by side
            
            items: [
           		{
           			xtype: 'fieldset',
           			columnWidth: 0.5,
           			border: false,
           			items: [
           				{
           					xtype: 'checkbox',
           					boxLabel: 'Ignore case',
                			name: 'ignore-case',
                			inputValue: 'ignore-case'
           				},
           				{
           					xtype: 'checkbox',
           					boxLabel: 'Locale',
                			name: 'locale',
                			inputValue: 'locale'
           				},
           				{
           					xtype: 'checkbox',
           					boxLabel: 'Multi line',
                			name: 'multi-line',
                			inputValue: 'multi-line'
           				}
           			]
           		},
           		{
           			xtype: 'fieldset',
           			columnWidth: 0.5,
           			border: false,
           			items: [
           				{
           					xtype: 'checkbox',
           					boxLabel: 'Dot all',
                			name: 'dot-all',
                			inputValue: 'dot-all'
           				},
           				{
           					xtype: 'checkbox',
           					boxLabel: 'Unicode',
                			name: 'unicode',
                			inputValue: 'unicode'
           				},
           				{
           					xtype: 'checkbox',
           					boxLabel: 'Verbose',
                			name: 'verbose',
                			inputValue: 'verbose'
           				}
           			]
           		}
            ]
    	},
    	{
    		xtype: 'textarea',
    		fieldLabel: 'Input text',
    		name: 'input_text',
    		height: 180,
    		anchor: '100%'
    	},
    	{
    		xtype: 'button',
    		text: 'Submit',
    		action: 'submit',
    		width: 70,
    		bodyStyle: 'padding-top: 30px'
    	}
    ]
});