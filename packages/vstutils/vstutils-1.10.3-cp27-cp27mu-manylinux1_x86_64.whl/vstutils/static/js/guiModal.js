guiModal={options:{width:'600px',autoOpen:false,overlayColor:'rgba(0, 0, 0, 0.6)',closeOnEscape:true,closeButton:true,fullscreen:true,overlayClose:true,},setModalHTML:function(html,opt)
{let local_options={}
try{this.options['headerColor']=guiCustomizer.skin.value['card_header_bg_color'];}
catch(e){}
for(var i in this.options)
{local_options[i]=this.options[i]}
if(opt!==undefined)
{for(var i in opt)
{local_options[i]=opt[i]}}
if(window.isCordova())
{local_options.fullscreen=true;local_options.overlay=false;local_options.transitionIn=false;local_options.transitionOut=false;local_options.width='100%';local_options.overlayClose=false;}
try
{var modalHolder=jQuery("#guiModal-iziModal");if(!modalHolder.length)
{modalHolder.remove();}
$("body").appendTpl('<div class="iziModal" tabindex="-1" role="dialog" id="guiModal-iziModal" data-izimodal-zindex="20000" data-iziModal-transitionIn="fadeInDown" data-iziModal-transitionOut="fadeOutDown"></div>')
modalHolder=jQuery("#guiModal-iziModal");$(modalHolder).iziModal('destroy');$(modalHolder).iziModal(local_options);if(html)
{$(modalHolder).iziModal('setContent','<div id="modal-content-wrapper-div"></div>');$('#modal-content-wrapper-div').appendTpl(html);}}
catch(exception)
{console.warn("There's something wrong with guiModal");}
return this;},modal:function()
{return jQuery("#guiModal-iziModal");},modalOpen:function()
{var modalHolder=jQuery("#guiModal-iziModal");if(!modalHolder.length)
{return this;}
try
{jQuery(modalHolder).iziModal('open');if(window.isCordova())
{jQuery(modalHolder).iziModal('setFullscreen',true);}}
catch(exception)
{console.warn("There's something wrong with guiModal");}
return this;},modalClose:function()
{var modalHolder=jQuery("#guiModal-iziModal");if(!modalHolder.length)
{return this;}
try
{jQuery(modalHolder).iziModal('close');}
catch(exception)
{console.warn("There's something wrong with guiModal");return this;}}}