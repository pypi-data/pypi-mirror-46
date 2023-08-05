var __JustEvalJsPattern_reg_pageUUID=new RegExp("<="+window.JUST.JustEvalJsPattern_pageUUID+"(.*?)"+window.JUST.JustEvalJsPattern_pageUUID+"=>","g")
let _insertTpl=function(func)
{return function(tplText){if(!tplText)
{return this;}
if(!this.length)
{return this;}
if(typeof tplText!=="string")
{tplText=""+tplText}
let val=this[0].getAttribute("data-tplText")
let testTplText=tplText.replace(/just-watch-class-[0-9]+/g,"").replace(/justId[0-9]+/g,"").replace(/__JUST_onInsertFunctions\['[^']+']/g,"")
if(val==testTplText)
{return this;}
this[0].setAttribute("data-tplText",testTplText)
var html=tplText.replace(window.__JustEvalJsPattern_reg_pageUUID,"")
this.each(function()
{var oldHtml=$(this).find("[data-onunload]");for(var i=0;i<oldHtml.length;i++)
{eval(oldHtml[i].attr('data-onunload'))}
$(this)[func](html)});var js=tplText.match(window.__JustEvalJsPattern_reg_pageUUID)
for(var i in js)
{if(js[i]&&js[i].length>8);{var code=js[i].substr(2+window.JUST.JustEvalJsPattern_pageUUID.length,js[i].length-(4+window.JUST.JustEvalJsPattern_pageUUID.length*2))
eval(code);}}
return this;}};$.fn.insertTpl=_insertTpl('html')
$.fn.appendTpl=_insertTpl('append')
$.fn.prependTpl=_insertTpl('prepend')
$.fn.replaceWithTpl=_insertTpl('replaceWith')
var justReactive={justStrip:function(html)
{if(typeof html=="number")
{return html;}
if(typeof html!="string"&&(!html||!html.toString))
{return"";}
var tmp=document.createElement("DIV");tmp.innerHTML=html.toString().replace(/</g,'&lt;').replace(/>/g,'&gt;');return tmp.textContent||tmp.innerText||"";},addMethod:function(setter,prop,method)
{Object.defineProperty(this[prop],method,{enumerable:false,configurable:true,writable:true,value:function(){var res=Array.prototype[method].apply(this,arguments);setter.apply(this,["__justReactive_update"]);return res;}});},_just_Id:0,methods:['pop','push','reduce','reduceRight','reverse','shift','slice','some','sort','unshift','unshift'],megreFunc:function(obj,prop,newval,level)
{obj[prop]=newval},applyFunc:function(val,newval)
{for(var i in newval.just_ids)
{if(newval.just_ids[i].type=="watch")
{newval.just_ids[i].callBack(val,newval.just_ids[i].customData)}
else if(newval.just_ids[i].type=='innerTPL')
{var el=document.getElementById("_justReactive"+newval.just_ids[i].id)
if(!el)
{delete newval.just_ids[i]
continue;}
$(el).insertTpl(newval.just_ids[i].callBack(val,newval.just_ids[i].customData))}
else if(newval.just_ids[i].type=='innerHTML')
{var el=document.getElementById("_justReactive"+newval.just_ids[i].id)
if(!el)
{continue;}
el.innerHTML=newval.just_ids[i].callBack(val,newval.just_ids[i].customData)}
else if(newval.just_ids[i].type=='textContent')
{var el=document.getElementById("_justReactive"+newval.just_ids[i].id)
if(!el)
{continue;}
el.textContent=newval.just_ids[i].callBack(val,newval.just_ids[i].customData)}
else if(newval.just_ids[i].type=='class')
{var el=document.getElementsByClassName("just-watch-class-"+newval.just_ids[i].id)
if(!el||!el.length)
{continue;}
var valT=newval.just_ids[i].callBack(val,newval.just_ids[i].customData)
for(var j=0;j<el.length;j++)
{if(!valT)
{el[j].className=el[j].className.replace(new RegExp("^"+newval.just_ids[i].className+"$","g"),"").replace(new RegExp(" +"+newval.just_ids[i].className+" +","g")," ").replace(new RegExp(" +"+newval.just_ids[i].className+"$","g"),"").replace(new RegExp("^"+newval.just_ids[i].className+" +","g")," ")}
else
{el[j].className=el[j].className.replace(new RegExp("^"+newval.just_ids[i].className+"$","g"),"").replace(new RegExp(" +"+newval.just_ids[i].className+" +","g")," ").replace(new RegExp(" "+newval.just_ids[i].className+"$","g"),"").replace(new RegExp("^"+newval.just_ids[i].className+" +","g")," ")
+" "+newval.just_ids[i].className}}}
else if(newval.just_ids[i].type=='notClass')
{var el=document.getElementsByClassName("just-watch-class-"+newval.just_ids[i].id)
if(!el||!el.length)
{continue;}
var valT=newval.just_ids[i].callBack(val,newval.just_ids[i].customData)
for(var j=0;j<el.length;j++)
{if(valT)
{el[j].className=el[j].className.replace(new RegExp("^"+newval.just_ids[i].className+"$","g"),"").replace(new RegExp(" +"+newval.just_ids[i].className+" +","g")," ").replace(new RegExp(" +"+newval.just_ids[i].className+"$","g"),"").replace(new RegExp("^"+newval.just_ids[i].className+" +","g"),"")}
else
{el[j].className=el[j].className.replace(new RegExp("^"+newval.just_ids[i].className+"$","g"),"").replace(new RegExp(" +"+newval.just_ids[i].className+" +","g")," ").replace(new RegExp(" "+newval.just_ids[i].className+"$","g"),"").replace(new RegExp("^"+newval.just_ids[i].className+" +","g")," ")
+" "+newval.just_ids[i].className}}}
else if(newval.just_ids[i].type=='className')
{var el=document.getElementsByClassName("just-watch-class-"+newval.just_ids[i].id)
if(!el||!el.length)
{continue;}
var valT=newval.just_ids[i].callBack(val,newval.just_ids[i].customData)
for(var j=0;j<el.length;j++)
{var oldValuematch=el[j].className.match(/just-old-val-([^ "']*)/)
var newClassValue=el[j].className;if(oldValuematch&&oldValuematch[0])
{newClassValue=newClassValue
.replace(new RegExp("^"+oldValuematch[0]+"$","g"),"").replace(new RegExp(" +"+oldValuematch[0]+" +","g")," ").replace(new RegExp(" "+oldValuematch[0]+"$","g"),"").replace(new RegExp("^"+oldValuematch[0]+" +","g")," ")
.replace(new RegExp("^"+oldValuematch[1]+"$","g"),"").replace(new RegExp(" +"+oldValuematch[1]+" +","g")," ").replace(new RegExp(" "+oldValuematch[1]+"$","g"),"").replace(new RegExp("^"+oldValuematch[1]+" +","g")," ")}
else
{newClassValue=newClassValue.replace(new RegExp("^just-old-val-$","g"),"").replace(new RegExp(" +just-old-val- +","g")," ").replace(new RegExp(" just-old-val-$","g"),"").replace(new RegExp("^just-old-val- +","g")," ")}
el[j].className=newClassValue+" "+valT+" just-old-val-"+valT}}
else if(newval.just_ids[i].type=='attr'||newval.just_ids[i].type=='bindAttr')
{var el=document.querySelectorAll("[data-just-watch-"+newval.just_ids[i].id+"]");if(!el||!el.length)
{continue;}
var attrVal=newval.just_ids[i].callBack(val,newval.just_ids[i].customData)
for(var j=0;j<el.length;j++)
{if(attrVal)
{if(el[j][newval.just_ids[i].attrName])
{el[j][newval.just_ids[i].attrName]=attrVal}
else
{el[j].setAttribute(newval.just_ids[i].attrName,attrVal);}}
else
{if(el[j][newval.just_ids[i].attrName])
{el[j][newval.just_ids[i].attrName]=null}
el[j].removeAttribute(newval.just_ids[i].attrName);}}}}},defaultcallBack:function(val)
{if(val&&val.toString)
{return val.toString();}
return val;},setValue:function(opt)
{justReactive._just_Id++;var id=justReactive._just_Id;if(!opt.callBack)
{opt.callBack=justReactive.defaultcallBack}
var oldValue=this[opt.prop]
this[opt.prop]="__justReactive_test";if(this[opt.prop]==="__justReactive_test")
{this[opt.prop]=oldValue
var newval={val:oldValue,just_ids:[{id:id,callBack:opt.callBack,type:opt.type,className:opt.className,attrName:opt.attrName,customData:opt.customData}],}
if(delete this[opt.prop])
{var setter=function(val)
{if(val==="__justReactive_test")
{return val;}
if(val&&val.__add_justHtml_test==="__justReactive_test")
{newval.just_ids.push({id:val.id,attrName:val.attrName,callBack:val.callBack,className:val.className,customData:val.customData,type:val.type})
return val;}
if(val==="__justReactive_update")
{}
else
{if(typeof val=="object"&&val!==null)
{justReactive.megreFunc(newval,'val',val);}
else
{newval.val=val;}
}
justReactive.applyFunc(val,newval)
return val;}
Object.defineProperty(this,opt.prop,{get:function(){return newval.val;},set:setter,enumerable:true,configurable:true});if(Array.isArray(newval.val))
{var thisObj=this
Object.defineProperty(this[opt.prop],'splice',{enumerable:false,configurable:true,writable:true,value:function(){var keys=Object.keys(newval.val);var tmpRes=Array.prototype['splice'].apply(keys,arguments);var res=[]
for(var i in tmpRes)
{res[i]=newval.val[tmpRes[i]]}
var newObj=[]
for(var i in keys)
{newObj[i]=newval.val[keys[i]]}
justReactive.megreFunc(newval,'val',newObj)
return res;}});for(var i in justReactive.methods)
{justReactive.addMethod.apply(this,[setter,opt.prop,justReactive.methods[i]])}}}}
else
{this[opt.prop]={__add_justHtml_test:"__justReactive_test",id:id,type:opt.type,callBack:opt.callBack,attrName:opt.attrName,className:opt.className,customData:opt.customData}}
if(opt.type=='innerTPL')
{return"<div id='_justReactive"+id+"' class='just-watch just-watch-tpl' style='display: contents;' >"+opt.callBack(this[opt.prop],opt.customData)+"</div>";}
else if(opt.type=='innerHTML')
{return"<div id='_justReactive"+id+"' class='just-watch just-watch-html' style='display: contents;' >"+opt.callBack(this[opt.prop],opt.customData)+"</div>";}
else if(opt.type=='textContent')
{return"<div id='_justReactive"+id+"' style='display: contents;' class='just-watch just-watch-text' >"+justReactive.justStrip(opt.callBack(this[opt.prop],opt.customData))+"</div>";}
else if(opt.type=='class')
{var val=opt.callBack(this[opt.prop],opt.customData)
if(val)
{return" just-watch just-watch-class just-watch-class-"+id+" "+justReactive.justStrip(opt.className)+" ";}
else
{return" just-watch just-watch-class just-watch-class-"+id+" ";}}
else if(opt.type=='notClass')
{var val=opt.callBack(this[opt.prop],opt.customData)
if(!val)
{return" just-watch just-watch-class just-watch-class-"+id+" "+justReactive.justStrip(opt.className)+" ";}
else
{return" just-watch just-watch-class just-watch-class-"+id+" ";}}
else if(opt.type=='className')
{var val=justReactive.justStrip(opt.callBack(this[opt.prop],opt.customData))
return" just-watch just-watch-class just-watch-class-"+id+" just-old-val-"+val+" "+val;}
else if(opt.type=='attr')
{var val=opt.callBack(this[opt.prop],opt.customData)
if(val)
{return" data-just-watch-"+id+" "+opt.attrName+"=\""+justReactive.justStrip(val).replace(/"/g,'&quot;')+"\"";}
else
{return" data-just-watch-"+id+" ";}}
else if(opt.type=='bindAttr')
{var val=opt.callBack(this[opt.prop],opt.customData)
var html=""
if(val)
{html=" data-just-watch-"+id+"=\"true\" "+opt.attrName+"=\""+justReactive.justStrip(val).replace(/"/g,'&quot;')+"\"";}
else
{html=" data-just-watch-"+id+"=\"true\" ";}
var thisObj=this
html=window.JUST.onInsert(html,function()
{var element=document.querySelector("[data-just-watch-"+id+"=true]")
if(opt.attrName=='value')
{element.addEventListener('input',function()
{if(thisObj[opt.prop]!==element.value)
{console.log("input",element.value);thisObj[opt.prop]=element.value;}},false);}
var observer=new MutationObserver(function(mutations)
{mutations.forEach(function(mutation)
{if(mutation.type=="attributes"&&mutation.attributeName==opt.attrName&&thisObj[opt.prop]!==mutation.target.getAttribute(opt.attrName))
{thisObj[opt.prop]=mutation.target.getAttribute(opt.attrName);element.value=mutation.target.getAttribute(opt.attrName)}});});observer.observe(element,{attributes:true,characterData:true});})
return html;}
return opt.callBack(this[opt.prop],opt.customData)}}
Object.defineProperty(Object.prototype,"justHtml",{enumerable:false,configurable:true,writable:false,value:function(prop,callBack,customData){return justReactive.setValue.apply(this,[{type:'innerHTML',prop:prop,callBack:callBack,customData:customData}])}});Object.defineProperty(Object.prototype,"justTpl",{enumerable:false,configurable:true,writable:false,value:function(prop,callBack,customData){return justReactive.setValue.apply(this,[{type:'innerTPL',prop:prop,callBack:callBack,customData:customData}])}});Object.defineProperty(Object.prototype,"justText",{enumerable:false,configurable:true,writable:false,value:function(prop,callBack,customData){return justReactive.setValue.apply(this,[{type:'textContent',prop:prop,callBack:callBack,customData:customData}])}});Object.defineProperty(Object.prototype,"justClass",{enumerable:false,configurable:true,writable:false,value:function(prop,className,callBack,customData)
{return justReactive.setValue.apply(this,[{type:'class',prop:prop,className:className,callBack:callBack,customData:customData}])}});Object.defineProperty(Object.prototype,"justNotClass",{enumerable:false,configurable:true,writable:false,value:function(prop,className,callBack,customData)
{return justReactive.setValue.apply(this,[{type:'notClass',prop:prop,className:className,callBack:callBack,customData:customData}])}});Object.defineProperty(Object.prototype,"justClassName",{enumerable:false,configurable:true,writable:false,value:function(prop,callBack,customData)
{return justReactive.setValue.apply(this,[{type:'className',prop:prop,callBack:callBack,customData:customData}])}});Object.defineProperty(Object.prototype,"justAttr",{enumerable:false,configurable:true,writable:false,value:function(prop,attrName,callBack,customData){return justReactive.setValue.apply(this,[{type:'attr',prop:prop,callBack:callBack,attrName:attrName,customData:customData}])}});Object.defineProperty(Object.prototype,"bindAttr",{enumerable:false,configurable:true,writable:false,value:function(prop,attrName,callBack,customData){return justReactive.setValue.apply(this,[{type:'bindAttr',prop:prop,callBack:callBack,attrName:attrName,customData:customData}])}});Object.defineProperty(Object.prototype,"justWatch",{enumerable:false,configurable:true,writable:false
,value:function(prop,callBack,customData)
{return justReactive.setValue.apply(this,[{type:'watch',prop:prop,deep:false,callBack:callBack,customData:customData}])}});Object.defineProperty(Object.prototype,"justDeepWatch",{enumerable:false,configurable:true,writable:false,value:function(prop)
{var deepWatch=function(obj,prop)
{if(typeof obj[prop]!="object"||obj[prop]===null)
{obj.justWatch(prop);return;}
for(var i in obj[prop])
{if(typeof obj[prop][i]=="object"&&obj[prop][i]!==null)
{deepWatch(obj[prop],i);obj[prop].justWatch(i);}
else
{obj[prop].justWatch(i);}}}
deepWatch(this,prop)
return true;}});if(!Object.prototype.watch){Object.defineProperty(Object.prototype,"watch",{enumerable:false,configurable:true,writable:false,value:function(prop,handler){var
oldval=this[prop],newval=oldval,getter=function(){return newval;},setter=function(val){oldval=newval;return newval=handler.call(this,prop,oldval,val);};if(delete this[prop]){Object.defineProperty(this,prop,{get:getter,set:setter,enumerable:true,configurable:true});}}});}
if(!Object.prototype.unwatch){Object.defineProperty(Object.prototype,"unwatch",{enumerable:false,configurable:true,writable:false,value:function(prop){var val=this[prop];delete this[prop];this[prop]=val;}});}
function isObject(item){return(item&&typeof item==='object'&&!Array.isArray(item));}
function mergeDeep(target,...sources){if(!sources.length)return target;if(target===undefined)
{target=sources.shift();}
const source=sources.shift();if(isObject(target)&&isObject(source)){for(const key in source){if(isObject(source[key])){if(!target[key])Object.assign(target,{[key]:{}});mergeDeep(target[key],source[key]);}else{Object.assign(target,{[key]:source[key]});}}}
return mergeDeep(target,...sources);}