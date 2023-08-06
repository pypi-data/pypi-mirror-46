if(!window.guiTestsFiles){window.guiTestsFiles=[];}
window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/qUnitTest.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiCommon.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiFields.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiSignals.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiTests.js');window.guiTestsFiles.push(hostname+window.guiStaticPath+'js/tests/guiUsers.js');function loadQUnitTests(){loadAllUnitTests(window.guiTestsFiles);}
function loadAllUnitTests(urls){let promises=[];for(let index in urls){let promise_callbacks={resolve:undefined,reject:undefined,};promises.push(new Promise((resolve,reject)=>{promise_callbacks.resolve=resolve;promise_callbacks.reject=reject;}));let link=document.createElement("script");link.setAttribute("type","text/javascript");link.setAttribute("src",urls[index]+'?r='+Math.random());link.onload=function(promise_callbacks){return function(){promise_callbacks.resolve();}}(promise_callbacks);document.getElementsByTagName("head")[0].appendChild(link);break;}
Promise.all(promises).then(()=>{if(urls.length==1){return injectQunit();}
urls.splice(0,1);loadAllUnitTests(urls);});}
String.prototype.format=function(){let obj=this.toString();let arg_list;if(typeof arguments[0]=="object"){arg_list=arguments[0];}else if(arguments.length>=1){arg_list=Array.from(arguments);}
for(let key of this.format_keys()){if(arg_list[key]!=undefined){obj=obj.replace('{'+key+'}',arg_list[key]);}else{throw"String don't have \'"+key+"\' key";}}
return obj;};String.prototype.format_keys=function(){let thisObj=this;let res=thisObj.match(/{([^\}]+)}/g);if(!res){return[];}
return res.map((item)=>{return item.slice(1,item.length-1)});};function trim(s){if(s)return s.replace(/^ */g,"").replace(/ *$/g,"");return'';}
function capitalizeString(string){if(!string){return"";}
return string.charAt(0).toUpperCase()+string.slice(1).toLowerCase();}
function sliceLongString(string="",valid_length=100){if(typeof string!="string"){return sliceLongString(""+string,valid_length);}
let str=string.slice(0,valid_length);if(string.length>valid_length){str+="...";}
return str;}
function isEmptyObject(obj){for(let key in obj){if(obj.hasOwnProperty(key)){return false;}}
return true;}
function addCssClassesToElement(element="",title,type){element=element.replace(/[\s\/]+/g,'_');let class_list=element+" ";if(title){title=title.replace(/[\s\/]+/g,'_');class_list+=element+"-"+title+" ";}
if(title&&type){type=type.replace(/[\s\/]+/g,'_');class_list+=element+"-"+type+" ";class_list+=element+"-"+type+"-"+title;}
return class_list.toLowerCase();}
window.onresize=function(){if(window.innerWidth>991){if(guiLocalSettings.get('hideMenu')){$("body").addClass('sidebar-collapse');}
if($("body").hasClass('sidebar-open')){$("body").removeClass('sidebar-open');}}else{if($("body").hasClass('sidebar-collapse')){$("body").removeClass('sidebar-collapse');}}};function saveHideMenuSettings(){if(window.innerWidth>991){if($('body').hasClass('sidebar-collapse')){guiLocalSettings.set('hideMenu',false);}else{guiLocalSettings.set('hideMenu',true);}}}
class LocalSettings{constructor(name){this.name=name;this.__settings={};this.__tmpSettings={};this.__beforeAsTmpSettings={};this.sync();}
sync(){if(window.localStorage[this.name]){try{this.__settings=JSON.parse(window.localStorage[this.name]);}catch(e){}}}
get(name){return this.__settings[name];}
set(name,value){this.__removeTmpSettings();this.__settings[name]=value;window.localStorage[this.name]=JSON.stringify(this.__settings);tabSignal.emit(this.name+'.'+name,{type:'set',name:name,value:value});}
delete(name){this.__removeTmpSettings();delete this.__settings[name];delete this.__tmpSettings[name];delete this.__beforeAsTmpSettings[name];window.localStorage[this.name]=JSON.stringify(this.__settings);}
setIfNotExists(name,value){if(this.__settings[name]===undefined){this.__settings[name]=value;}}
setAsTmp(name,value){if(this.__settings[name]){this.__beforeAsTmpSettings[name]=this.__settings[name];}
this.__settings[name]=value;this.__tmpSettings[name]=value;tabSignal.emit(this.name+'.'+name,{type:'set',name:name,value:value});}
__removeTmpSettings(){for(let key in this.__tmpSettings){if(this.__beforeAsTmpSettings[key]){this.__settings[key]=this.__beforeAsTmpSettings[key];}else{delete this.__settings[key];}}}}
var guiLocalSettings=new LocalSettings('guiLocalSettings');function deepEqual(x,y){if((typeof x=="object"&&x!=null)&&(typeof y=="object"&&y!=null)){if(Object.keys(x).length!=Object.keys(y).length){return false;}
for(let prop in x){if(y.hasOwnProperty(prop)){if(!deepEqual(x[prop],y[prop])){return false;}}else{return false;}}
return true;}else if(x!==y){return false;}else{return true;}}
function stringToBoolean(string){if(string==null){return false;}
switch(string.toLowerCase().trim()){case"true":case"yes":case"1":return true;case"false":case"no":case"0":case null:return false;}}
function oneCharNumberToTwoChar(n){return n>9?""+n:"0"+n;}
function allPropertiesIsObjects(obj){for(let prop in obj){if(typeof obj[prop]!='object'){return false;}else{if($.isArray(obj[prop])){return false;}}}
return true;}
$(".content-wrapper").hover(function(){$(".hover-li").removeClass("hover-li");});$(".navbar").hover(function(){$(".hover-li").removeClass("hover-li");});function hexToRgbA(hex,alpha){if(alpha===undefined){alpha=1;}
if(typeof(alpha)!="number"){alpha=Number(alpha);if(isNaN(alpha)){alpha=1;}}
if(alpha<0||alpha>1){alpha=1;}
let c;if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){c=hex.substring(1).split('');if(c.length==3){c=[c[0],c[0],c[1],c[1],c[2],c[2]];}
c='0x'+c.join('');return'rgba('+[(c>>16)&255,(c>>8)&255,c&255].join(',')+','+alpha+')';}
return;}
function getTimeInUptimeFormat(time){if(isNaN(time)){return"00:00:00";}
let uptime=moment.duration(Number(time),'seconds')._data;let n=oneCharNumberToTwoChar;if(uptime.years>0){return n(uptime.years)+"y "+n(uptime.months)+"m "+n(uptime.days)+"d "+n(uptime.hours)+":"+
n(uptime.minutes)+":"+n(uptime.seconds);}else if(uptime.months>0){return n(uptime.months)+"m "+n(uptime.days)+"d "+n(uptime.hours)+":"+n(uptime.minutes)+":"+
n(uptime.seconds);}else if(uptime.days>0){return n(uptime.days)+"d "+n(uptime.hours)+":"+n(uptime.minutes)+":"+n(uptime.seconds);}else{return n(uptime.hours)+":"+n(uptime.minutes)+":"+n(uptime.seconds);}}
Object.defineProperty(Array.prototype,'last',{get:function(){return this[this.length-1];}});class ObjectPropertyRetriever{constructor(){this.ob_proto_attrs=this.constructor.getObjectConstructorProperties;this.obj_proto_methods=this.constructor.getObjectConstructorMethods;}
static get getObjectConstructorMethods(){return Object.getOwnPropertyNames({}.constructor.prototype);}
static get getObjectConstructorProperties(){return Object.keys({}.constructor.prototype);}
_enumerable(obj,prop){return obj.propertyIsEnumerable(prop);}
_notEnumerable(obj,prop){return!obj.propertyIsEnumerable(prop);}
_enumerableAndNotEnumerable(obj,prop){return true;}
_getPropertyNames(obj,iterateSelfBool,iteratePrototypeBool,includePropCb){let props=[];do{if(iterateSelfBool){Object.getOwnPropertyNames(obj).forEach(function(prop){if(props.indexOf(prop)===-1&&includePropCb(obj,prop)){props.push(prop);}});}
if(!iteratePrototypeBool){break;}
iterateSelfBool=true;}while(obj=Object.getPrototypeOf(obj));return props;}
getOwnEnumerables(obj){return this._getPropertyNames(obj,true,false,this._enumerable);}
getOwnNonenumerables(obj){return this._getPropertyNames(obj,true,false,this._notEnumerable);}
getOwnEnumerablesAndNonenumerables(obj){return this._getPropertyNames(obj,true,false,this._enumerableAndNotEnumerable);}
getPrototypeEnumerables(obj,obj_proto=true){let props=this._getPropertyNames(obj,false,true,this._enumerable);if(!obj_proto){return props.filter(item=>!this.ob_proto_attrs.includes(item));}
return props;}
getPrototypeNonenumerables(obj,obj_proto=true){let props=this._getPropertyNames(obj,false,true,this._notEnumerable);if(!obj_proto){return props.filter(item=>!this.obj_proto_methods.includes(item));}
return props;}
getPrototypeEnumerablesAndNonenumerables(obj,obj_proto=true){let props=this._getPropertyNames(obj,false,true,this._enumerableAndNotEnumerable);if(!obj_proto){return props.filter(item=>!(this.obj_proto_methods.includes(item)||this.ob_proto_attrs.includes(item)));}
return props;}
getOwnAndPrototypeEnumerables(obj,obj_proto=true){let props=this._getPropertyNames(obj,true,true,this._enumerable);if(!obj_proto){return props.filter(item=>!this.ob_proto_attrs.includes(item));}
return props;}
getOwnAndPrototypeNonenumerables(obj,obj_proto=true){let props=this._getPropertyNames(obj,true,true,this._notEnumerable);if(!obj_proto){return props.filter(item=>!this.obj_proto_methods.includes(item));}
return props;}
getOwnAndPrototypeEnumerablesAndNonenumerables(obj){let props=this._getPropertyNames(obj,true,true,this._enumerableAndNotEnumerable);if(!obj_proto){return props.filter(item=>!(this.obj_proto_methods.includes(item)||this.ob_proto_attrs.includes(item)));}
return props;}}
var obj_prop_retriever=new ObjectPropertyRetriever();class BaseEntityConstructor{constructor(openapi_dictionary){this.dictionary=openapi_dictionary;}
getModelRefsProps(){return this.dictionary.models.ref_names;}
getFieldFormat(field){if(guiFields[field.format]){return field.format;}
if(field.enum&&guiFields['choices']){return"choices";}
let props=Object.keys(field);let refs=this.getModelRefsProps();for(let key in props){if(refs.includes(props[key])){return'api_object';}}
if(guiFields[field.type]){return field.type;}
return'string';}}
function findClosestPath(paths,current_path){let c_p_parts=current_path.replace(/^\/|\/$/g,"").split("/");let matches=[];for(let index in paths){let path=paths[index];let path_paths=path.replace(/^\/|\/$/g,"").split("/");matches.push({path:path,match:0,});for(let num in c_p_parts){let item=c_p_parts[num];if(item==path_paths[num]){matches.last.match++;}else{break;}}}
matches=matches.sort((a,b)=>{return a.match-b.match;});if(matches.last&&matches.last.path&&matches.last.match>0){return matches.last.path;}}
class CurrentView{constructor(){this.loading=null;this.success=null;this.error=null;this.promise=null;this.promise_status="";this.promise_callbacks={};}
initLoading(){this.error=this.response=null;this.loading=true;this._initLoadingPromise();}
setLoadingSuccessful(){this.loading=false;this.success=true;this.error=null;return setTimeout(()=>{this.promise_callbacks.resolve();this.promise_status='resolved';},10);}
setLoadingError(error){this.loading=false;this.success=null;this.error=error;return setTimeout(()=>{this.promise_callbacks.reject();this.promise_status='rejected';},10);}
_initLoadingPromise(){if(!(this.promise&&(this.promise_status==""||this.promise_status=="pending"))){this.promise_callbacks={resolve:undefined,reject:undefined,};this.promise=new Promise((resolve,reject)=>{this.promise_callbacks.resolve=resolve;this.promise_callbacks.reject=reject;});this.promise_status='pending';}}}
var current_view=new CurrentView();var path_pk_key='pk';