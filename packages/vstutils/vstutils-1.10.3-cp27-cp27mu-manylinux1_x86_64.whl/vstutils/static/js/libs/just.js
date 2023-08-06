/*!
 * JUST JavaScript template engine v0.1.8
 * https://github.com/baryshev/just
 *
 * Copyright 2012, Vadim M. Baryshev <vadimbaryshev@gmail.com>
 * Licensed under the MIT license
 * https://github.com/baryshev/just/LICENSE
 *
 * https://github.com/Levhav/just-template
 * Adding reactive to based on https://github.com/Levhav/justReactive to just template engine
 */
(function(){'use strict';var getUUID=function()
{var s=""
var str="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890";for(var i=0;i<24;i++)
{s+=str[Math.floor(Math.random()*(str.length-1))]}
return s}
var __JUST_onInsertFunctions={}
var onInsert=function(html,func,once=true)
{var key=getUUID()
window.JUST.__JUST_onInsertFunctions[key]={func:func,count:0};var funcCall="";if(once||once===undefined)
{funcCall=" if(window.JUST.__JUST_onInsertFunctions['"+key+"'] !== undefined){"
+" window.JUST.__JUST_onInsertFunctions['"+key+"'].func(window.JUST.__JUST_onInsertFunctions['"+key+"'].count);"
+" window.JUST.__JUST_onInsertFunctions['"+key+"'].count+=1;"
+" delete window.JUST.__JUST_onInsertFunctions['"+key+"'];"
+" } ";}
else
{funcCall="window.JUST.__JUST_onInsertFunctions['"+key+"'].func(window.JUST.__JUST_onInsertFunctions['"+key+"'].count);"
+" window.JUST.__JUST_onInsertFunctions['"+key+"'].count+=1;"}
html+="<="+window.JUST.JustEvalJsPattern_pageUUID+" "+funcCall+" "+window.JUST.JustEvalJsPattern_pageUUID+"=>";return html;}
var JustEvalJsPattern_pageUUID=getUUID("pageUUID");var JustEvalJsPattern=function(text)
{return"<="+window.JUST.JustEvalJsPattern_pageUUID+text.replace(/^<=js|js=>$/g,"")+window.JUST.JustEvalJsPattern_pageUUID+"=>"}
var
JUST=function(newOptions)
{var
options={open:'<%',close:'%>',ext:'',root:''},trimExp=/^\s+|\s+$/g,escapeExp=/([.*+?\^=!:${}()|\[\]\/\\])/g,STATE_RAW=0,STATE_PARTIAL=1,STATE_EXTEND=2,STATE_CONDITION=3,STATE_ELSE=4,STATE_SWITCH=5,STATE_CASE=6,STATE_DEFAULT=7,STATE_LOOP=8,STATE_SUBBLOK=9,STATE_TEXT=10,STATE_JS=11,STATE_HTML=12,cache={},countUid=0,regExpEscape=function(str){return String(str).replace(escapeExp,'\\$1');},reactiveReplace=function(html)
{var status=0
var parts=html.split(/<(?=~)/g)
var startPart={}
var lastStatus=0;for(var i in parts)
{var val=parts[i]
if(val.charAt(0)=='~'&&val.charAt(1)=='>')
{if(status!=0&&status==lastStatus)
{var forCode=startPart[lastStatus].substr(1).split(/>/,1)
if(!forCode||!forCode.length)
{console.error("Invalid sub block definition",forCode)}
var forObject=forCode[0].trim()
if(forObject[forObject.length-1]==']')
{forObject=forObject.match(/^(.*)\[([^\]]+)\]$/)}
else if(forObject.indexOf(".")!=-1)
{forObject=forObject.match(/^(.*)\.([^.]+)$/)
forObject[2]="'"+forObject[2]+"'"}
else
{forObject=[]
forObject[1]='this.data'
forObject[2]=forObject}
var body=startPart[lastStatus].substr(startPart[lastStatus].indexOf(">")+1)
countUid++;var tplName='_superId'+countUid
options.root[tplName]=body
var res=html.replace("<"+startPart[lastStatus]+"<~>","<%= "+forObject[1]+".justTpl("+forObject[2]+", this.partialWatch, ['"+tplName+"', this.data]) %>")
return reactiveReplace(res)}
status--}
else if(val.charAt(0)=='~')
{status++
lastStatus=status
startPart[status]=val}
else
{}}
return html},parseToCode=function(html){html=reactiveReplace(html)
html=html.replace(/<=js(.*?)js=>/g,JustEvalJsPattern)
var
lineNo=1,buffer=["with (this.data) { \nwith (this.customData) { \nthis.buffer.push('"],matches=html.split(new RegExp(regExpEscape(options.open)+'((?:.|[\r\n])+?)(?:'+regExpEscape(options.close)+'|$)')),length,i,text,prefix,postfix,line,tmp,jsFromPos,state;for(i=0,length=matches.length;i<length;i++){text=matches[i];if(i%2===1){line="\nthis.line="+lineNo;jsFromPos=1;state=STATE_RAW;switch(text.charAt(0)){case'@':prefix='\',('+line+', this.partial(';postfix=')),\'';state=STATE_PARTIAL;break;case'!':prefix='\',('+line+', this.extend(';postfix=')),\'';state=STATE_EXTEND;break;case'*':prefix='\',('+line+', this.child(\'';postfix='\')),\'';break;case'[':prefix='\');'+line+';this.blockStart(\'';postfix='\');this.buffer.push(\'';break;case']':prefix='\');'+line+';this.blockEnd(\'';postfix='\');this.buffer.push(\'';break;case'=':prefix='\',('+line+', ';postfix='),\'';state=STATE_HTML;break;case'-':prefix='\',('+line+', ';postfix='),\'';state=STATE_TEXT;break;case'?':prefix='\');'+line+';';postfix='this.buffer.push(\'';state=STATE_CONDITION;break;case':':prefix='\');'+line+';}else';postfix='this.buffer.push(\'';state=STATE_ELSE;break;case'|':prefix='\');'+line+';';postfix='this.buffer.push(\'';state=STATE_LOOP;break;case'~':prefix='\');'+line+';';postfix='this.buffer.push(\'';state=STATE_SUBBLOK;break;default:prefix='\');'+line+';';postfix=';this.buffer.push(\'';jsFromPos=0;}
switch(state){case STATE_RAW:buffer.push(prefix,text.substr(jsFromPos).replace(trimExp,''),postfix);break;case STATE_HTML:buffer.push(prefix,'JustWaitResults('+text.substr(jsFromPos).replace(trimExp,'')+')',postfix);break;case STATE_TEXT:buffer.push(prefix,'JustEscapeHtml('+text.substr(jsFromPos).replace(trimExp,'')+')',postfix);break;case STATE_CONDITION:tmp=text.substr(jsFromPos).replace(trimExp,'');if(!tmp.length){buffer.push(prefix,'}',postfix);}else{buffer.push(prefix,'if(',tmp,'){',postfix);}
tmp=undefined;break;case STATE_ELSE:tmp=text.substr(jsFromPos).replace(trimExp,'');if(!tmp.length){buffer.push(prefix,'{',postfix);}else{buffer.push(prefix,' if(',tmp,'){',postfix);}
tmp=undefined;break;case STATE_PARTIAL:case STATE_EXTEND:tmp=text.substr(jsFromPos).replace(trimExp,'').split(/\s+/);tmp=['\''+tmp[0]+'\'',tmp.splice(1).join(' ')];if(!tmp[1].length){tmp=tmp[0];}else{tmp=tmp.join('');}
buffer.push(prefix,tmp,postfix);tmp=undefined;break;case STATE_LOOP:tmp=text.substr(jsFromPos).replace(trimExp,'').split(/\s+/);if(!tmp[0].length){buffer.push('\');'+line+';}, this);this.buffer.push(\'');}else{buffer.push(prefix,tmp[0],'.forEach(function(',tmp[1],'){this.buffer.push(\'');}
tmp=undefined;break;case STATE_SUBBLOK:buffer.push(prefix,text.substr(jsFromPos).replace(trimExp,''),postfix);break;}}else{buffer.push(text.replace(/[\\']/g,'\\$&').replace(/\r/g,' ').replace(/\n/g,'\\n'));}
lineNo+=text.split(/\n/).length-1;}
buffer.push("'); \n} \n} return this.buffer;");return buffer=buffer.join('');},parse=function(html){return new Function(parseToCode(html));},readSync=function(file){var data=eval('(options.root[\''+file+'\'])');if(Object.prototype.toString.call(data)==='[object String]'){return data;}else{console.error('Failed to load template',file)
throw'Failed to load template '+file}},loadSync=function(file){var data=readSync(file)
var blank=parse(data);return blank;},Template=function(file,data,customData){this.file=file;if(Object.prototype.toString.call(options.root)==='[object String]'){this.file=path.normalize((options.root.length?(options.root+'/'):'')+file+options.ext);}
this.data=data;this.customData=customData||{};this.buffer=[];this.tmpBuffer={};this.tmpBufferNames=[];this.watcher=undefined;this.line=1;this.partials=[];this.childData=[];this.childError=undefined;this.childCallback=undefined;this.callback=undefined;this.blocks={};};Template.prototype.blockStart=function(name){this.tmpBufferNames.push(name)
this.tmpBuffer[name]=this.buffer;if(!this.blocks[name])
{this.blocks[name]=[];}
if(!this.blocks[name].length)
{this.buffer=this.blocks[name];}
else
{this.buffer=[];}};Template.prototype.blockEnd=function(){var name=this.tmpBufferNames.pop(name)
this.buffer=this.tmpBuffer[name];delete(this.tmpBuffer[name]);};Template.prototype.partial=function(template,customData){var page=new Template(template,this.data,customData);return page.renderSync();};Template.prototype.partialWatch=function(v,data){var template=data[0]
var customData=data[1]
var page=new Template(template,customData,undefined);return page.renderSync();};Template.prototype.extend=function(template,customData)
{var page=new Template(template,this.data,customData)
var callback=this.callback;page.blocks=this.blocks;this.callback=function(error,data){if(error){page.childError=error;if(page.childCallback){page.childCallback(error);}}else{page.childData.push(data);if(page.childCallback){page.childCallback();}}};page.partials.push(function(callback){if(page.childError){callback(page.childError);}else if(page.childData.length){callback();}else{page.childCallback=callback;}});return page.renderSync();};Template.prototype.child=function(block){if(block&&block.length){if(!this.blocks[block]){this.blocks[block]=[];}
return this.blocks[block];}
return this.childData;};function arrayRender(arr){let html=''
for(let i in arr)
{html+=(Array.isArray(arr[i]))?arrayRender(arr[i]):arr[i];}
return html}
Template.prototype.renderSync=function(){var that=this;var blank=loadSync(this.file)
var buffer=blank.call(that);for(var i=0;i<that.partials.length;i++)
{that.partials[i].call();}
var html='',length,i;for(i=0,length=buffer.length;i<length;i++)
{html+=(Array.isArray(buffer[i]))?arrayRender(buffer[i]):buffer[i];}
return html;};this.configure=function(newOptions){var option;newOptions=newOptions||{};for(option in options){options[option]=newOptions[option]||options[option];}};this.renderSync=function(template,data,onInsertFunc)
{if(data===undefined)
{data={}}
var tpl=new Template(template,data);var html=tpl.renderSync();if(html==undefined)
{console.error("renderSync error",template,data)}
if(typeof onInsertFunc=='function')
{html=this.onInsert(html,onInsertFunc,false);}
return html;};this.render=this.renderSync
this.isTplExists=function(name){return options.root[name]!==undefined}
this.onInsert=onInsert
this.configure(newOptions);};if(!Array.prototype.filter){Array.prototype.filter=function(fun,thisp){var
len=this.length,res=[],i,val;if(typeof fun!=='function'){throw new TypeError();}
for(i=0;i<len;i++){if(i in this){val=this[i];if(fun.call(thisp,val,i,this)){res.push(val);}}}
return res;};}
if(!Array.prototype.forEach){Array.prototype.forEach=function(fun,thisp){var
len=this.length,i;if(typeof fun!=='function'){throw new TypeError();}
for(i=0;i<len;i++){if(i in this){fun.call(thisp,this[i],i,this);}}};}
if(!Array.isArray){Array.isArray=function(obj){return Object.prototype.toString.call(obj)==='[object Array]';};}
var cbSplit;if(!cbSplit){cbSplit=function(str,separator,limit){if(Object.prototype.toString.call(separator)!=='[object RegExp]'){return cbSplit.nativeSplit.call(str,separator,limit);}
var
output=[],lastLastIndex=0,flags=(separator.ignoreCase?'i':'')+
(separator.multiline?'m':'')+
(separator.sticky?'y':''),separator2,match,lastIndex,lastLength;separator=new RegExp(separator.source,flags+'g');str=str+'';if(!cbSplit.compliantExecNpcg){separator2=new RegExp('^'+separator.source+'$(?!\\s)',flags);}
if(limit===undefined||+limit<0){limit=Infinity;}else{limit=Math.floor(+limit);if(!limit){return[];}}
while(match=separator.exec(str)){lastIndex=match.index+match[0].length;if(lastIndex>lastLastIndex){output.push(str.slice(lastLastIndex,match.index));if(!cbSplit.compliantExecNpcg&&match.length>1){match[0].replace(separator2,function(){var i;for(i=1;i<arguments.length-2;i++){if(arguments[i]===undefined){match[i]=undefined;}}});}
if(match.length>1&&match.index<str.length){Array.prototype.push.apply(output,match.slice(1));}
lastLength=match[0].length;lastLastIndex=lastIndex;if(output.length>=limit){break;}}
if(separator.lastIndex===match.index){separator.lastIndex++;}}
if(lastLastIndex===str.length){if(lastLength||!separator.test('')){output.push('');}}else{output.push(str.slice(lastLastIndex));}
return output.length>limit?output.slice(0,limit):output;};cbSplit.compliantExecNpcg=/()??/.exec('')[1]===undefined;cbSplit.nativeSplit=String.prototype.split;}
String.prototype.split=function(separator,limit){return cbSplit(this,separator,limit);};window.JUST=JUST;window.JUST.onInsert=onInsert;window.JUST.getUUID=getUUID;window.JUST.__JUST_onInsertFunctions=__JUST_onInsertFunctions;window.JUST.JustEvalJsPattern_pageUUID=JustEvalJsPattern_pageUUID;window.JUST.JustEvalJsPattern=JustEvalJsPattern;}());function JustEscapeHtml(text){var map={'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'};if(!text||!text.replace)
{return text;}
return text.replace(/[&<>"']/g,function(m){return map[m];});}
function JustWaitResults(data){if(typeof data=="object")
{if(data.then)
{let id="just-"+Math.random()+""+Math.random()
id=id.replace(/0\./g,"");return JUST.onInsert('<div class="just just-wait-results just-loading" id="'+id+'" ></div>',function()
{data.then((d)=>{$("#"+id).replaceWithTpl(d)},(e)=>{$("#"+id).replaceWithTpl(e)})},true)}}
return data}
justCall_mapArr=[]
function justCall(obj)
{var index=justCall_mapArr.length
justCall_mapArr.push(obj)
return'justCall_mapArr['+index+']'}
function justOn(event,action,id)
{if(!id)
{id="justId"+Math.floor(Math.random()*900000);}
return JUST.onInsert(" id='"+id+"' ",function(){$("#"+id).on(event,action)},true)}
JUST.onInsert("",alert,true)
JUST.onInsert("",alert,true)