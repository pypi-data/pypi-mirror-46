if(window.gettext===undefined)
{var gettext=function(text)
{if(window.gettext.data&&window.gettext.data[window.gettext.locale]&&window.gettext.data[window.gettext.locale][text])
{text=window.gettext.data[window.gettext.locale][text];for(var i=1;i<arguments.length;i++)
{text=text.replace("%"+i+"s",arguments[i])}
return text}
for(var i=1;i<arguments.length;i++)
{text=text.replace("%"+i+"s",arguments[i])}
return text;}
window.gettext.data={};window.gettext.locale='en'
if(navigator.language)
{window.gettext.locale=navigator.language}
gettext.setTranslate=function(lang,arr)
{window.gettext.data[lang]=arr}
gettext.setLocale=function(lang)
{window.gettext.locale=lang}
gettext.getLocale=function()
{return window.gettext.locale}}
if(!window.spajs)
{var spajs=function()
{return this;}
spajs.version="2.2";spajs.initSuccess=false;spajs.initProgress=false;spajs.opt={};spajs.opt.holder="body"
spajs.opt.useHistoryApi=true
spajs.opt.useJust=true
spajs.opt.avatar_prefix="";spajs.opt.menu_url="spa"
spajs.opt.addParamsToUrl=true
spajs.opt.menu=[]
spajs.init=function(options)
{if(spajs.initProgress===true)
{return;}
spajs.initProgress=true;for(var i in options)
{if(spajs.opt[i]&&typeof(spajs.opt[i])=="object")
{for(var j in options[i])
{spajs.opt[i][j]=options[i][j]}}
spajs.opt[i]=options[i]}
if(spajs.opt.useJust)
{var root={}
var tplArray=$("script[data-just]")
for(var i=0;i<tplArray.length;i++)
{var val=$(tplArray[i]);root[val.attr("data-just")]=val.html()}
spajs.just=new JUST({root:root});}
$(window).blur(function(){spajs.isActiveTab=false;});$(window).focus(function(){spajs.isActiveTab=true;tabSignal.emitAll("onAnyTabActivated",{})});var lastOnlineStatus=undefined;setInterval(function()
{var status=spajs.isOnline();if(status!==lastOnlineStatus&&lastOnlineStatus!==undefined)
{if(status)
{console.warn("online event");setTimeout(function()
{if(!spajs.isOnline())
{return;}
tabSignal.emitAll("onOnline",{})},5000)}
else
{console.warn("offline event")
tabSignal.emitAll("onOffline",{})}}
lastOnlineStatus=status;},500)
if(spajs.opt.useHistoryApi)
{window.addEventListener('popstate',function(event)
{spajs.openMenuFromUrl(event.state||{url:window.location.href})});}
else
{}}
spajs.openURL=function(url,title)
{if(spajs.findMenu(spajs.getMenuIdFromUrl(url)))
{history.pushState({url:url},title,url);}
var res=spajs.openMenuFromUrl(url,{withoutFailPage:true})
return res}
spajs.getMenuIdFromUrl=function(url)
{let menuId
if(url.indexOf("?")!=-1)
{menuId=window.location.href.slice(window.location.href.indexOf("?")+1)}
else
{menuId=window.location.hash.slice(1)}
if(spajs.opt.menu_url)
{menuId=spajs.getUrlParam(spajs.opt.menu_url)}
return menuId}
spajs.openMenuFromUrl=function(event_state,opt)
{if(!opt)
{opt={}}
if(window.location.href.indexOf("?")!=-1)
{opt.menuId=window.location.href.slice(window.location.href.indexOf("?")+1)}
else
{opt.menuId=window.location.hash.slice(1)}
if(spajs.opt.menu_url)
{opt.menuId=spajs.getUrlParam(spajs.opt.menu_url,event_state)}
opt.addUrlParams={}
opt.notAddToHistory=true
opt.event_state=event_state
return spajs.open(opt)}
spajs.setUrlParam=function(params,title)
{var url=window.location.pathname+"?"+params.toString();if(typeof params==="object")
{var new_url=window.location.href;for(var i in params)
{if(!params.hasOwnProperty(i))
{continue;}
var name=i;var value=params[i];if(value==undefined)
{new_url=new_url.replace(new RegExp(name+"=[^&\/]+"),"");}
else
{if(!new_url.match(new RegExp(name+"=[^&\/]+")))
{if(new_url.indexOf("?")!=-1)
{new_url+="&"+name+"="+value;}
else
{new_url+="?"+name+"="+value;}}
else
{new_url=new_url.replace(new RegExp(name+"=[^&\/]+"),name+"="+value);}}}
url=new_url.replace(/&+/img,"&").replace(/&+$/img,"").replace(/\?+$/img,"").replace(/\?&+/img,"?")}
if(!spajs.opt.addParamsToUrl)
{url=window.location.href;}
if(spajs.opt.useHistoryApi)
{history.pushState({url:new_url},title,url)}
return new_url;}
spajs.getUrlParam=function(name,event_state)
{var url_param=window.location.href.replace(/^.*?[#?](.*)$/,"$1");if(event_state!==undefined&&event_state.url)
{url_param=event_state.url.replace(/^.*?[#?](.*)$/,"$1");}
var param=url_param.match(new RegExp(name+"=[^&\/]+"),"g")
if(!param||!param.length)
{return false;}
return param[0].replace(name+"=","").replace(/#$/,"")}
spajs.getAllUrlParam=function(event_state)
{var url_param=window.location.href.replace(/^.*?[#?](.*)$/,"$1");if(event_state!==undefined&&event_state.url)
{url_param=event_state.url.replace(/^.*?[#?](.*)$/,"$1");}
var param=url_param.split(/[&?]/g)
var res={}
if(param&&param.length)
{for(var i=0;i<param.length;i++)
{param[i]=param[i].split("=")
res[param[i][0]]=param[i][1];}}
return res}
spajs.addMenu=function(menu)
{if(!menu.id)
{menu.id=Math.random()}
if(!menu.type)
{menu.type="custom"}
if(!menu.priority)
{menu.priority=0;}
spajs.opt.menu.push(menu)
spajs.opt.menu=spajs.opt.menu.sort((a,b)=>{return b.priority-a.priority});}
spajs.currentOpenMenu=undefined
spajs.findMenu=function(menuId)
{for(var i in this.opt.menu)
{let val=this.opt.menu[i]
if(val.url_parser!=undefined)
{for(var j in val.url_parser)
{var parsed=val.url_parser[j](menuId)
if(parsed)
{return{menu:val,regExpRes:parsed}}}}
else if(val.urlregexp!=undefined)
{for(var j in val.urlregexp)
{if(val.urlregexp[j].test(menuId))
{return{menu:val,regExpRes:val.urlregexp[j].exec(menuId)}}}}
else if(val.id==menuId)
{return{menu:val,regExpRes:[]}}}
return false}
spajs.open=function(opt)
{console.log("spajs.open",opt)
if(!opt.menuId)
{opt.menuId="";}
if(opt.reopen===undefined)
{opt.reopen=true;}
var def=new $.Deferred();if(!opt.withoutFailPage)
{$.when(def).fail(function(e)
{debugger;if(spajs.errorPage)
{spajs.errorPage(jQuery('#spajs-right-area'),menuInfo,{},e)}})}
if(!spajs.opt.addParamsToUrl&&opt.event_state==undefined)
{opt.event_state={}
opt.event_state.url=window.location.href;}
var regExpRes=[]
let findedMenu=spajs.findMenu(opt.menuId)
var menuInfo=findedMenu.menu
console.log("openMenu",menuInfo)
if(!menuInfo||!menuInfo.onOpen)
{if(!opt.withoutFailPage)
{console.error("URL not registered",opt.menuId,opt)}
def.reject({detail:"Error URL not registered",status:404})
throw{text:"URL not registered "+opt.menuId,code:404};return def.promise();}
if(spajs.currentOpenMenu&&menuInfo.id==spajs.currentOpenMenu.id&&!opt.reopen)
{debugger;console.warn("Re-opening the menu",menuInfo)
def.resolve()
return def.promise();}
if(opt.addUrlParams===undefined)
{opt.addUrlParams={}}
if(spajs.opt.menu_url)
{opt.addUrlParams[spajs.opt.menu_url]=opt.menuId;if(!opt.notAddToHistory)
{var url=spajs.setUrlParam(opt.addUrlParams,menuInfo.title||menuInfo.name)
if(opt.event_state)
{opt.event_state.url=url;}}}
else if(!opt.notAddToHistory)
{var url=spajs.setUrlParam(opt.menuId,menuInfo.title||menuInfo.name)
if(opt.event_state)
{opt.event_state.url=url;}}
if(spajs.currentOpenMenu)
{if(spajs.currentOpenMenu.onClose_promise)
{spajs.currentOpenMenu.onClose_promise.resolve(menuInfo)}
if(spajs.currentOpenMenu.onClose)
{spajs.currentOpenMenu.onClose(menuInfo)}}
if(menuInfo.hideMenu)
{$(spajs.opt.holder).addClass("spajs-spa-show-page");}
if(spajs.currentOpenMenu&&spajs.currentOpenMenu.id)
{$("body").removeClass("spajs-active-"+spajs.currentOpenMenu.id)}
else
{}
$(spajs.opt.holder).addClass("spajs-active-"+menuInfo.id);menuInfo.onClose_promise=new $.Deferred();spajs.urlInfo={menuInfo:menuInfo,data:{url:spajs.getAllUrlParam(opt.event_state),reg:findedMenu.regExpRes}}
tabSignal.emit("spajs.open",spajs.urlInfo)
let res=menuInfo.onOpen(jQuery('#spajs-right-area'),menuInfo,spajs.urlInfo.data,menuInfo.onClose_promise.promise());if(res)
{$("body").addClass("in-loading")
spajs.wait_result(jQuery('#spajs-right-area'),res)}
else
{$("body").removeClass("in-loading")
def.resolve()
res=def}
jQuery("#left_sidebar li").removeClass("active")
jQuery("#spajs-menu-"+menuInfo.id).addClass("active")
spajs.currentOpenMenu=menuInfo;if(opt.callback)
{opt.callback();}
if(typeof res=="string")
{def.resolve()
res=def}
$.when(res).done(()=>{tabSignal.emit("spajs.opened",spajs.urlInfo)})
return res.promise();}
spajs.wait_result=function(block,res)
{if(typeof res=="string")
{$(block).insertTpl(res)
$("body").removeClass("in-loading")
return;}
if(!res)
{$("body").removeClass("in-loading")
return;}
$.when(res).done((html)=>{if(typeof html=="string")
{$(block).insertTpl(html)}
$("body").removeClass("in-loading")}).fail(function(error)
{$(block).insertTpl("error"+JSON.stringify(error))
$("body").removeClass("in-loading")})}
spajs.showLoader=function(promise)
{if(!promise)
{var def=new $.Deferred();def.resolve()
return def.promise();}
$("body").addClass("in-loading")
$.when(promise).then(function()
{$("body").removeClass("in-loading")}).fail(function()
{$("body").removeClass("in-loading")})
return promise}
spajs.openMenu=function(menuId,addUrlParams,notAddToHistory,event_state)
{return spajs.open({menuId:menuId,addUrlParams:addUrlParams,notAddToHistory:notAddToHistory,event_state:event_state})}
spajs.ajax=function(){return this;}
spajs.opt.ajax={}
spajs.ajax.headers={}
spajs.ajax.setHeader=function(header,data)
{spajs.ajax.headers[header]=data}
spajs.ajax.showErrors=function(data)
{if(typeof data==="string")
{guiPopUp.error(data);return;}
if(data&&data.responseJSON)
{return spajs.ajax.showErrors(data.responseJSON)}
if(data&&data.message)
{return spajs.ajax.showErrors(data.message)}
for(var i in data)
{if(i=="error_type"||i=="result")
{continue;}
if(typeof data[i]==="string")
{guiPopUp.error(data[i]);}
else if(typeof data[i]==="object")
{spajs.ajax.showErrors(data[i])}}}
spajs.ajax.ErrorTest=function(data)
{if(data&&(data.status===401 ))
{window.location.reload()
return true;}
if(data&&data.status===500)
{guiPopUp.error("Error 500")
return true;}
if(data&&data.status===422&&data.responseJSON)
{spajs.ajax.showErrors(data.responseJSON)
return true;}
if(data&&data.result===false)
{spajs.ajax.showErrors(data)
return true;}
if(data&&data.error)
{guiPopUp.error(data.error);return true;}
return false;}
spajs.ajax.getPostVars=function()
{var url=[]
for(var i in spajs.opt.ajax.post)
{url.push(i+"="+spajs.opt.ajax.post[i])}
return url.join("&")}
spajs.ajax.gethashCode=function(str)
{var hash=0;if(!str||str.length==0)return hash;for(var i=0;i<str.length;i++)
{hash=((hash<<5)-hash)+str.charCodeAt(i);hash=hash&hash;}
return hash;}
spajs.isOnline=function()
{return navigator.onLine}
spajs.ajax.ajaxCache={}
spajs.ajax.ajaxQueue=[]
spajs.ajax.Abort=function()
{spajs.ajax.ajaxQueue[this.IndexInQueue]=undefined}
spajs.ajax.Call=function(opt)
{try{if(opt.key===undefined)
{opt.key=opt.type+"_"+opt.url+"_"+spajs.ajax.gethashCode(JSON.stringify(opt.data))}
if(!spajs.isOnline()&&spajs.ajax.ajaxCache[opt.key])
{if(opt.error)
{opt.error();}
return{useCache:false,addToQueue:false,ignor:false,abort:function(){}};}
if(!spajs.isOnline()&&opt.reTryInOnline)
{opt.abort=spajs.ajax.Abort;opt.useCache=false;opt.addToQueue=false;opt.ignor=true;spajs.ajax.ajaxQueue.push(opt)
return opt;}
if(!spajs.isOnline())
{if(opt.error)
{opt.error();}
return{useCache:false,addToQueue:false,ignor:true,abort:function(){}};}
var def=new $.Deferred();var defpromise=def.promise()
var successCallBack=opt.success
var errorCallBack=opt.error
opt.success=function(data,status,xhr)
{if(opt.useCache)
{}
if(successCallBack)successCallBack(data,status,xhr)
def.resolve(data,status,xhr)}
opt.error=function(data,status,xhr)
{var headers=data.getAllResponseHeaders()
if(data.status==401||(data.status==403&&headers.indexOf("x-anonymous:")!=-1))
{window.location.reload()}
else if(errorCallBack)
{errorCallBack(data,status,xhr)
def.reject(data,status,xhr)}
else
{def.reject(data,status,xhr)}}
if(!opt.beforeSend)
{opt.beforeSend=function(xhr)
{for(var i in spajs.ajax.headers)
{xhr.setRequestHeader(i,spajs.ajax.headers[i]);}}}
var res=jQuery.ajax(opt);res.useCache=false;res.addToQueue=false;res.ignor=false;defpromise.abort=function()
{res.abort()}
return defpromise}catch(e){debugger;console.error(e)
throw e}}
spajs.ajax.ajaxCallFromQueue=function()
{for(var i in spajs.ajax.ajaxQueue)
{jQuery.ajax(spajs.ajax.ajaxQueue[i]);}
spajs.ajax.ajaxQueue=[]}}