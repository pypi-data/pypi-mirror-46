if(!window.guiTestsFiles)
{window.guiTestsFiles=[]}
window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/qUnitTest.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiPaths.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiElements.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiCommon.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiUsers.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiSignals.js');function loadQUnitTests()
{loadAllUnitTests(window.guiTestsFiles)}
function loadAllUnitTests(urls)
{let promises=[]
for(let i in urls)
{let def=new $.Deferred();promises.push(def.promise());var link=document.createElement("script");link.setAttribute("type","text/javascript");link.setAttribute("src",urls[i]+'?r='+Math.random());link.onload=function(def){return function(){def.resolve();}}(def)
document.getElementsByTagName("head")[0].appendChild(link);break;}
$.when.apply($,promises).done(()=>{if(urls.length==1)
{return injectQunit()}
urls.splice(0,1)
loadAllUnitTests(urls)})}
String.prototype.format=function()
{let obj=this.toString();let arg_list;if(typeof arguments[0]=="object")
{arg_list=arguments[0]}
else if(arguments.length>=1)
{arg_list=Array.from(arguments);}
for(let key of this.format_keys())
{if(arg_list[key]!=undefined)
{obj=obj.replace('{'+key+'}',arg_list[key])}
else
{throw"String don't have \'"+key+"\' key";}}
return obj;}
String.prototype.format_keys=function()
{let thisObj=this;let res=thisObj.match(/{([^\}]+)}/g)
if(!res)
{return[]}
return res.map((item)=>{return item.slice(1,item.length-1)})}
function addslashes(string){return string.replace(/\\/g,'\\\\').replace(/\u0008/g,'\\b').replace(/\t/g,'\\t').replace(/\n/g,'\\n').replace(/\f/g,'\\f').replace(/\v/g,'\\v').replace(/'/g,'\\\'').replace(/"/g,'\\"');}
function stripslashes(str){return(str+'').replace(/\\(.?)/g,function(s,n1){switch(n1){case'\\':return'\\'
case'0':return'\u0000'
case't':return"\t"
case'n':return"\n"
case'f':return"\f"
case'v':return"\v"
case'b':return"\b"
case'':return''
default:return n1}})}
function trim(s)
{if(s)return s.replace(/^ */g,"").replace(/ *$/g,"")
return'';}
function inheritance(obj,constructor)
{var object=undefined;var item=function()
{if(constructor)
{return constructor.apply(jQuery.extend(true,item,object),arguments);}
return jQuery.extend(true,item,object);}
object=jQuery.extend(true,item,obj)
return object}
function toIdString(str)
{return str.replace(/[^A-z0-9\-]/img,"_").replace(/[\[\]]/gi,"_");}
function hidemodal()
{var def=new $.Deferred();$(".modal.fade.in").on('hidden.bs.modal',function(e){def.resolve();})
$(".modal.fade.in").modal('hide');return def.promise();}
function capitalizeString(string)
{if(!string)
{return"";}
return string.charAt(0).toUpperCase()+string.slice(1).toLowerCase();}
function sliceLongString(string="",valid_length=100)
{if(typeof string!="string")
{return sliceLongString(""+string,valid_length);}
var str=string.slice(0,valid_length);if(string.length>valid_length)
{str+="...";}
return str;}
function isEmptyObject(obj)
{for(var i in obj){if(obj.hasOwnProperty(i)){return false;}}
return true;}
function readFileAndInsert(event,element)
{for(var i=0;i<event.target.files.length;i++)
{if(event.target.files[i].size>1024*1024*1)
{guiPopUp.error("File is too large")
console.log("File is too large "+event.target.files[i].size)
continue;}
var reader=new FileReader();reader.onload=function(e)
{$(element).val(e.target.result);}
reader.readAsText(event.target.files[i]);}
return false;}
function addCssClassesToElement(element="",title,type)
{element=element.replace(/[\s\/]+/g,'-');let class_list=element+" ";if(title)
{title=title.replace(/[\s\/]+/g,'-');class_list+=element+"_"+title+" ";}
if(title&&type)
{type=type.replace(/[\s\/]+/g,'-');class_list+=element+"_"+type+" ";class_list+=element+"_"+type+"_"+title;}
return class_list.toLowerCase();}
function addStylesAndClassesToListField(guiObj,field,data,opt)
{let output="";if(field.style)
{output+=field.style.apply(guiObj,[data,opt])+" ";}
if(field.class)
{output+=field.class.apply(guiObj,[data,opt])+" ";}
else
{output+="class='"+addCssClassesToElement('td',field.name,guiObj.api.short_name)+"' ";}
return output;}
function turnTableTrIntoLink(event,blank)
{if(!blockTrLink(event.target,'tr','highlight-tr-none'))
{let href;if(event.target.hasAttribute('href'))
{href=event.target.getAttribute('href');}
else if(event.currentTarget)
{href=event.currentTarget.getAttribute('data-href');}
else
{href=event.target.getAttribute('data-href');}
if(blank)
{window.open(href);}
else
{vstGO(href);}}}
function blockTrLink(element,stop_element_name,search_class)
{if(!element)
{return false;}
if(element.classList.contains(search_class))
{return true;}
if(element.parentElement&&element.parentElement.localName!=stop_element_name)
{return blockTrLink(element.parentElement,stop_element_name,search_class);}
return false;}
function hideIdInList(listObj)
{try
{let fields=listObj.value.schema.list.fields;if(fields['id'])
{fields['id'].hidden=true;}}
catch(e)
{console.warn(e);}}
tabSignal.connect("openapi.schema.type.list",function(listObj)
{hideIdInList.apply(this,arguments);})
window.current_window_width=window.innerWidth;window.onresize=function()
{window.current_window_width=window.innerWidth;if(window.innerWidth>991)
{if(guiLocalSettings.get('hideMenu'))
{$("body").addClass('sidebar-collapse');}
if($("body").hasClass('sidebar-open'))
{$("body").removeClass('sidebar-open');}}
else
{if($("body").hasClass('sidebar-collapse')){$("body").removeClass('sidebar-collapse');}}}
function saveHideMenuSettings()
{if(window.innerWidth>991)
{if($('body').hasClass('sidebar-collapse'))
{guiLocalSettings.set('hideMenu',false);}
else
{guiLocalSettings.set('hideMenu',true);}}}
function groupButtonsOrNot(window_width,buttons)
{let buttons_amount=0;if(typeof buttons=="number")
{buttons_amount=buttons;}
else if(typeof buttons=="string")
{buttons_amount=Number(buttons)||0;}
else if(typeof buttons=="object")
{if($.isArray(buttons))
{buttons_amount=buttons.length;}
else
{buttons_amount=Object.keys(buttons).length;}
for(let i in buttons)
{if(buttons[i].hidden)
{buttons_amount--;}}}
if(buttons_amount<2)
{return false;}
else if(buttons_amount>=2&&buttons_amount<5)
{if(window_width>=992)
{return false;}}
else if(buttons_amount>=5&&buttons_amount<8)
{if(window_width>=1200)
{return false;}}
else if(buttons_amount>=8)
{if(window_width>=1620)
{return false;}}
return true;}
var guiLocalSettings={__settings:{},__tmpSettings:{},__beforeAsTmpSettings:{},__removeTmpSettings:function(){for(var item in this.__tmpSettings)
{if(this.__beforeAsTmpSettings[item])
{this.__settings[item]=this.__beforeAsTmpSettings[item];}
else
{delete this.__settings[item];}}},get:function(name){return this.__settings[name];},delete:function(name){this.__removeTmpSettings();delete this.__settings[name];delete this.__tmpSettings[name];delete this.__beforeAsTmpSettings[name];window.localStorage['guiLocalSettings']=JSON.stringify(this.__settings);},set:function(name,value){this.__removeTmpSettings();this.__settings[name]=value;window.localStorage['guiLocalSettings']=JSON.stringify(this.__settings);tabSignal.emit('guiLocalSettings.'+name,{type:'set',name:name,value:value});},setAsTmp:function(name,value){if(this.__settings[name])
{this.__beforeAsTmpSettings[name]=this.__settings[name];}
this.__settings[name]=value;this.__tmpSettings[name]=value;tabSignal.emit('guiLocalSettings.'+name,{type:'set',name:name,value:value});},setIfNotExists:function(name,value){if(this.__settings[name]===undefined)
{this.__settings[name]=value;}}}
if(window.localStorage['guiLocalSettings'])
{try{guiLocalSettings.__settings=window.localStorage['guiLocalSettings'];guiLocalSettings.__settings=JSON.parse(guiLocalSettings.__settings)}catch(e)
{}}
function getNewId(){return("id_"+Math.random()+""+Math.random()+""+Math.random()).replace(/\./g,"")}
window.url_delimiter="#"
function vstMakeLocalUrl(url="",vars={})
{if(Array.isArray(url))
{url=url.join("/")}
if(typeof url=="string")
{let new_url=url.format(vars)
if(new_url.indexOf(window.hostname)!=0&&new_url.indexOf("//")!=0)
{new_url=window.hostname+window.url_delimiter+new_url}
else
{}
url=new_url.replace("#/","#")}
else
{debugger;throw"Error in vstMakeLocalUrl"}
return url.replace("#","#/")}
function vstGO()
{return spajs.openURL(vstMakeLocalUrl.apply(this,arguments))}
function makeUrlForApiKeys(url_string)
{return url_string.replace(/\{([A-z0-9]+)\}/g,"{api_$1}")}
function vstMakeLocalApiUrl(url,vars={})
{if(Array.isArray(url))
{url=url.join("/")}
return vstMakeLocalUrl(makeUrlForApiKeys(url),vars)}
function openHelpModal()
{let info=api.openapi.info;let opt={};if(info.title)
{opt.title=info.title;}
let html=spajs.just.render('help_modal_content',{info:info});guiModal.setModalHTML(html,opt);guiModal.modalOpen();}
function deepEqual(x,y)
{if((typeof x=="object"&&x!=null)&&(typeof y=="object"&&y!=null))
{if(Object.keys(x).length!=Object.keys(y).length)
{return false;}
for(var prop in x)
{if(y.hasOwnProperty(prop))
{if(!deepEqual(x[prop],y[prop]))
{return false;}}
else
{return false;}}
return true;}
else if(x!==y)
{return false;}
else
{return true;}}
function stringToBoolean(string){if(string==null)
{return false;}
switch(string.toLowerCase().trim()){case"true":case"yes":case"1":return true;case"false":case"no":case"0":case null:return false;}}
function searchObjectsInListByJs(filters,data)
{if(!data)
{data=[];}
if(!filters)
{filters={search_query:{}}}
let search_results=[];let search_query_keys=Object.keys(filters.search_query);for(let i in data)
{let item=data[i];let search_key=search_query_keys[0];let search_value=filters.search_query[search_key];if(checkDataValidityForSearchQuery(item[search_key],search_value))
{search_results.push(item);}}
for(let i=1;i<search_query_keys.length;i++)
{let search_key=search_query_keys[i];let search_value=filters.search_query[search_key];for(let j=0;j<search_results.length;j++)
{let item=search_results[j];if(!checkDataValidityForSearchQuery(item[search_key],search_value))
{search_results.splice(j,1);j-=1;}}}
return search_results;}
function checkDataValidityForSearchQuery(data_value,search_value)
{let valid=false;if(typeof data_value=='string')
{if(data_value.match(search_value)!=null)
{valid=true;}}
else
{if(typeof data_value=='boolean'&&typeof search_value=='string')
{search_value=stringToBoolean(search_value);}
if(data_value==search_value)
{valid=true;}}
return valid;}
function oneCharNumberToTwoChar(n){return n>9?""+n:"0"+n;}
function openExternalLink(event)
{if(isCordova())
{let url=event.target.activeElement.href;window.parent.cordova.InAppBrowser.open(url,'_blank','location=yes');event.preventDefault()
return false;}}
window.onbeforeunload=openExternalLink;if(isCordova())
{window.onunload=function(){inAppClose()}}
function allPropertiesIsObjects(obj)
{for(let prop in obj)
{if(typeof obj[prop]!='object')
{return false;}
else
{if($.isArray(obj[prop]))
{return false;}}}
return true;}
function debounce(f,ms){let timer=null;return function(...args){const onComplete=()=>{f.apply(this,args);timer=null;}
if(timer){clearTimeout(timer);}
timer=setTimeout(onComplete,ms);};}
function addTableEntityClass(guiObj)
{let class_name="";if(guiObj&&guiObj.api&&guiObj.api.extension_class_name)
{if(typeof(guiObj.api.extension_class_name)=='string')
{class_name=guiObj.api.extension_class_name;}
else if(Array.isArray(guiObj.api.extension_class_name)&&guiObj.api.extension_class_name.length>0)
{class_name=String(guiObj.api.extension_class_name[0]);}}
return class_name.replace('gui_','');}
function hideSidebar()
{if(window.innerWidth<=991)
{$('body').removeClass('sidebar-open');$('body').addClass('sidebar-collapse');}}
function toggleMenuOpen(el,event)
{event.stopPropagation();let li=el.parentElement.parentElement.parentElement;let ul=$(li).find('ul.nav-treeview');$(li).toggleClass('menu-open');$(ul).slideToggle(300);setTimeout(function()
{if($(li).hasClass('menu-open'))
{$(ul).attr("style","display:block;")}
else
{$(ul).attr("style","display:none;")}},301)}
function setActiveMenuLi()
{let url=window.location.hash.replace("#","")
$(".nav-sidebar li[data-url]").removeClass("active");$(".nav-sidebar a.nav-link").removeClass('active')
$(".nav-sidebar .menu-open").removeClass('menu-open')
$(".nav-sidebar .nav-treeview").hide()
let li=$(".nav-sidebar li[data-url]")
let urllevel=url.split("/").length-1
for(let i=0;i<li.length;i++)
{let val=$(li[i])
let dataurl=val.attr('data-url')
if(dataurl==""&&urllevel>=1)
{continue;}
if(urllevel>1&&url.indexOf(dataurl)!=0)
{continue;}
if(urllevel<=1&&url!=dataurl)
{continue;}
if(val.hasClass('has-treeview'))
{val.addClass("menu-open")
val.children(".nav-treeview").show()}
val.children("a.nav-link").addClass('active')
let parent=val.parent()
let step=0;do{step++;if($(parent).hasClass('has-treeview'))
{$(parent).addClass("menu-open")
parent.children(".nav-treeview").show()}
parent=$(parent).parent()}while(parent.length&&step<10)
break;}}
tabSignal.connect("spajs.open",setActiveMenuLi);tabSignal.connect("loading.completed",setActiveMenuLi)
$(".content-wrapper").hover(function(){$(".hover-li").removeClass("hover-li");})
$(".navbar").hover(function(){$(".hover-li").removeClass("hover-li");})
function hexToRgbA(hex,alpha)
{if(alpha===undefined)
{alpha=1;}
if(typeof(alpha)!="number")
{alpha=Number(alpha);if(isNaN(alpha))
{alpha=1;}}
if(alpha<0||alpha>1)
{alpha=1;}
let c;if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){c=hex.substring(1).split('');if(c.length==3){c=[c[0],c[0],c[1],c[1],c[2],c[2]];}
c='0x'+c.join('');return'rgba('+[(c>>16)&255,(c>>8)&255,c&255].join(',')+','+alpha+')';}
return;}
function getPrefetchText(opt,dataLine,field_name,max_length){if(!max_length){max_length=100;}
if(opt.fields[field_name].prefetch&&dataLine[field_name+'_info']){if(opt.fields['job'].prefetch.field_name&&dataLine[field_name+'_info'][opt.fields['job'].prefetch.field_name]){return sliceLongString(dataLine[field_name+'_info'][opt.fields['job'].prefetch.field_name],max_length);}else if(dataLine[field_name+'_info'].name){return sliceLongString(dataLine[field_name+'_info'].name,max_length)}}
return sliceLongString(dataLine[field_name],max_length);}
function getTimeInUptimeFormat(time){if(isNaN(time))
{return"00:00:00";}
let uptime=moment.duration(Number(time),'seconds')._data;let n=oneCharNumberToTwoChar;if(uptime.years>0)
{return n(uptime.years)+"y "+n(uptime.months)+"m "+n(uptime.days)+"d "+n(uptime.hours)+":"+n(uptime.minutes)+":"+n(uptime.seconds)}else if(uptime.months>0)
{return n(uptime.months)+"m "+n(uptime.days)+"d "+n(uptime.hours)+":"+n(uptime.minutes)+":"+n(uptime.seconds)}
else if(uptime.days>0)
{return n(uptime.days)+"d "+n(uptime.hours)+":"+n(uptime.minutes)+":"+n(uptime.seconds)}
else
{return n(uptime.hours)+":"+n(uptime.minutes)+":"+n(uptime.seconds)}}